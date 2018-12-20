from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'net_delib_20181221C'
    players_per_group = 2
    num_rounds = 1
    chat_time = 5000 #10 * 60 * 1000

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
