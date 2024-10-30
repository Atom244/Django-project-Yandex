__all__ = ["PositiveNumConverter"]


class PositiveNumConverter:
    regex = r"[1-9][0-9]*"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return "%s" % value
