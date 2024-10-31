import re

from django.core.exceptions import ValidationError

__all__ = []


class ValidateMustContain:
    def __init__(self, *required_words):
        self.required_words = required_words

    def __call__(self, value):
        for word in self.required_words:
            pattern = rf"(?<!\w){word}(?!\w)"
            if re.search(pattern, value, re.IGNORECASE):
                return
        raise ValidationError(
            "Текст должен содержать одно из следующих слов: "
            f"{', '.join(self.required_words)}.",
        )

    def deconstruct(self):
        return (
            "catalog.validators.ValidateMustContain",
            self.required_words,
            {},
        )
