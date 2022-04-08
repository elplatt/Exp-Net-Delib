from matplotlib import pyplot as plt
import scipy.stats as spstats

from loomio import *
from socialchoice import *
from timeseries import *

class NetDelib(object):
    
    def __init__(self):
        self.plot_mean = False
    
    def plot_errorbar(self, data, data_labels, ylabel, title):
        for i, d in enumerate(data):
            if self.plot_mean:
                y = d.mean()
            else:
                y = d.y()
            plt.errorbar(range(4), y, yerr=d.yerr95(), label=data_labels[i], capsize=6)
        plt.xticks(range(4))
        plt.xlabel('Stage')
        plt.ylabel(ylabel)
        plt.grid()
        plt.legend()
        plt.title(title)
    
    def plot(self, data, data_labels, ylabel, title):
        for i, d in enumerate(data):
            if self.plot_mean:
                y = d.mean()
            else:
                y = d.y()
            plt.plot(range(4), y, label=data_labels[i])
        plt.xticks(range(4))
        plt.xlabel('Stage')
        plt.ylabel(ylabel)
        plt.grid()
        plt.legend()
        plt.title(title)
    
    def plot_kendall(self):
        self.plot_errorbar(
            [self.kendall_control, self.kendall_random],
            ['Control', 'Random-Pod'],
            'Kendall Correlation',
            self.title + ' (Kendall)')
        
    def plot_spearman(self):
        self.plot_errorbar(
            [self.spearman_control, self.spearman_random],
            ['Control', 'Random-Pod'],
            'Spearman Correlation',
            self.title + ' (Spearman)')
            
    def plot_ballot(self):
        self.plot_errorbar(
            [self.ballot_control, self.ballot_random],
            ['Control', 'Random-Pod'],
            'Ballot Correlation',
            self.title + ' (Ballot)')
    
    def plot_crossing(self):
        self.plot_errorbar(
            [self.crossing_control, self.crossing_random],
            ['Control', 'Random-Pod'],
            'Crossing Correlation',
            self.title + ' (Crossing)')
    
    def plot_tideman(self):
        self.plot(
            [self.tideman_control, self.tideman_random],
            ['Control', 'Random-Pod'],
            'Tideman Fraction',
            self.title + ' (Tideman)')
        
        
class NetDelibAgreement(NetDelib):

    def __init__(self, df_score):
        
        super().__init__()

        self.title = 'Agreement'
        self.bootstrap_runs = 10
        
        self.control_profiles = [
            Profile.from_score(df_score[(df_score.stage == stage) & (df_score.treatment == 1)])
            for stage in sorted(set(df_score.stage))]

        self.random_profiles = [
            Profile.from_score(df_score[(df_score.stage == stage) & (df_score.treatment == 2)])
            for stage in sorted(set(df_score.stage))]


        self.kendall_control = TimeSeriesResult()
        self.spearman_control = TimeSeriesResult()
        self.tideman_control = TimeSeriesResult()
        self.ballot_control = TimeSeriesResult()
        self.crossing_control = TimeSeriesResult()
        
        print('Single Group')
        print('stage\tkendall\tspearman\ttideman\tballot\tcrossing')
        for stage, profile in enumerate(self.control_profiles):

            self.kendall_control.add_y(profile.agreement_kendall())
            self.spearman_control.add_y(profile.agreement_spearman())
            self.tideman_control.add_y(Tideman(profile).agreement_tideman())
            self.ballot_control.add_y(profile.agreement_ballot())
            self.crossing_control.add_y(profile.agreement_crossing())

            for run in range(self.bootstrap_runs):
                p = profile.sample_bootstrap()
                self.kendall_control.add_sample(stage, p.agreement_kendall())
                self.spearman_control.add_sample(stage, p.agreement_spearman())
                self.tideman_control.add_sample(stage, Tideman(p).agreement_tideman())
                self.ballot_control.add_sample(stage, p.agreement_ballot())
                self.crossing_control.add_sample(stage, p.agreement_crossing())

            print("{}\t{}\t{}\t{}\t{}\t{}".format(
                stage,
                self.kendall_control.y()[stage],
                self.spearman_control.y()[stage],
                self.tideman_control.y()[stage],
                self.ballot_control.y()[stage],
                self.crossing_control.y()[stage]))
    
        self.kendall_random = TimeSeriesResult()
        self.spearman_random = TimeSeriesResult()
        self.tideman_random = TimeSeriesResult()
        self.ballot_random = TimeSeriesResult()
        self.crossing_random = TimeSeriesResult()
        print('\nRandom Pod')
        print('stage\tkendall\tspearman\ttideman\tballot\tcrossing')
        for stage, profile in enumerate(self.random_profiles):

            self.kendall_random.add_y(profile.agreement_kendall())
            self.spearman_random.add_y(profile.agreement_spearman())
            self.tideman_random.add_y(Tideman(profile).agreement_tideman())
            self.ballot_random.add_y(profile.agreement_ballot())
            self.crossing_random.add_y(profile.agreement_crossing())

            for run in range(self.bootstrap_runs):
                p = profile.sample_bootstrap()
                self.kendall_random.add_sample(stage, p.agreement_kendall())
                self.spearman_random.add_sample(stage, p.agreement_spearman())
                self.tideman_random.add_sample(stage, Tideman(p).agreement_tideman())
                self.ballot_random.add_sample(stage, p.agreement_ballot())
                self.crossing_random.add_sample(stage, p.agreement_crossing())

            print("{}\t{}\t{}\t{}\t{}\t{}".format(
                stage,
                self.kendall_random.y()[stage],
                self.spearman_random.y()[stage],
                self.tideman_random.y()[stage],
                self.ballot_random.y()[stage],
                self.crossing_random.y()[stage]))

            
class NetDelibInitEvolution(NetDelib):

    def __init__(self, df_score):

        super().__init__()
        
        self.title = 'Agreement w/ Initial'
        self.bootstrap_runs = 10
        self.plot_mean = True
        
        df_control = df_score[df_score.treatment == 1]
        df_random = df_score[df_score.treatment == 2]
        self.control_collection = make_preference_sequence_collection(df_control)
        self.random_collection = make_preference_sequence_collection(df_random)

        participant_ids = self.control_collection.participant_ids()
        self.kendall_control = TimeSeriesResult()
        self.spearman_control = TimeSeriesResult()
        self.ballot_control = TimeSeriesResult()
        self.crossover_control = TimeSeriesResult()
        for stage in range(0, 4):
            for participant_id in participant_ids:
                initial_preference = self.control_collection[participant_id][0]
                try:
                    stage_preference = self.control_collection[participant_id][stage]
                    r, p = spstats.kendalltau(initial_preference.ranks(), stage_preference.ranks())
                    self.kendall_control.add_sample(stage, r)
                    r, p = spstats.spearmanr(initial_preference.ranks(), stage_preference.ranks())
                    self.spearman_control.add_sample(stage, r)
                    r = 1 - 2 * initial_preference.ballot_dissimilarity(stage_preference)
                    self.ballot_control.add_sample(stage, r)
                    r = 1 - 2 * initial_preference.crossover_dissimilarity(stage_preference)
                    self.crossover_control.add_sample(stage, r)
                except:
                    continue

        participant_ids = self.random_collection.participant_ids()
        self.kendall_random = TimeSeriesResult()
        self.spearman_random = TimeSeriesResult()
        self.ballot_random = TimeSeriesResult()
        self.crossover_random = TimeSeriesResult()
        for stage in range(0, 4):
            for participant_id in participant_ids:
                initial_preference = self.random_collection[participant_id][0]
                try:
                    stage_preference = self.random_collection[participant_id][stage]
                    r, p = spstats.kendalltau(initial_preference.ranks(), stage_preference.ranks())
                    self.kendall_random.add_sample(stage, r)
                    r, p = spstats.spearmanr(initial_preference.ranks(), stage_preference.ranks())
                    self.spearman_random.add_sample(stage, r)
                    r = 1 - 2 * initial_preference.ballot_dissimilarity(stage_preference)
                    self.ballot_random.add_sample(stage, r)
                    r = 1 - 2 * initial_preference.crossover_dissimilarity(stage_preference)
                except:
                    continue