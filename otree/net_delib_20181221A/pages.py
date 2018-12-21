from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class StartPage(Page):
    pass

class ChatPageA(Page):
    pass

class SurveyPage(Page):
    def vars_for_template(self):
        return {'survey_url': Constants.survey_url[self.round_number - 1]}

class ChatWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

page_sequence = [
    SurveyPage,
    ChatWaitPage,
    ChatPageA
]
