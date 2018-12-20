from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class StartPage(Page):
    pass

class ChatPageA(Page):
    pass

class ChatWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

page_sequence = [
    StartPage,
    ChatWaitPage,
    ChatPageA
]
