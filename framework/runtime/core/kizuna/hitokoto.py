class Hitokoto:

    def __init__(self, moment: str, sender: str, words: str, when: str, fromWaifu: bool):
        self.moment = moment
        self.who = sender
        self.words = words
        self.when = when
        self.fromWaifu = fromWaifu

    @property
    def json(self):
        return {
            "moment": self.moment,
            "who": self.who,
            "words": self.words,
            "when": self.when,
            "fromWaifu": self.fromWaifu,
        }

    @classmethod
    def create(cls, d: dict):
        obj = cls(
            d["moment"],
            d["who"],
            d["words"],
            d["when"],
            d["fromWaifu"]
        )
        return obj
