from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ChatPageC(Page):
    pass

class EndPage(Page):
    pass

class ChatWaitPage(WaitPage):
    pass

page_sequence = [
#    ChatWaitPage,
    ChatPageC,
    EndPage
]
