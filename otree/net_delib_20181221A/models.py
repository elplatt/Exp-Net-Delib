from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'net_delib_20181221A'
    players_per_group = 5
    num_rounds = 3
    chat_time = 10 * 60 * 1000
    survey_url = [
        'https://umich.qualtrics.com/jfe/form/SV_5om2ZedQGMW3pXf',
        'https://umich.qualtrics.com/jfe/form/SV_1ByTxFhMWhdUfWd',
        'https://umich.qualtrics.com/jfe/form/SV_b3C58zqJKt0M8El'
    ]

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
