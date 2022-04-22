from dataclasses import dataclass


@dataclass()
class TelegramBotUserDetails:
    def __init__(self):
        self.first_name = None
        self.last_name = None
