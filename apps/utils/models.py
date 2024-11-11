# models.py or utils.py
class ChoicesQuerySet:
    def __init__(self, choices):
        self.choices = [self._wrap_choice(choice) for choice in choices]

    def _wrap_choice(self, choice):
        # This function wraps each choice tuple (value, label) in a named tuple for easy access
        from collections import namedtuple

        Choice = namedtuple("Choice", ["value", "label"])
        return Choice(value=choice[0], label=choice[1])

    def all(self):
        return self.choices

    def __iter__(self):
        return iter(self.choices)

    def filter(self, **kwargs):
        # Optionally implement filters based on kwargs if needed
        return [
            choice
            for choice in self.choices
            if all(getattr(choice, k) == v for k, v in kwargs.items())
        ]
