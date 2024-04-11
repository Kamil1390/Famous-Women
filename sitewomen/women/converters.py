class FourDigitYearConverter:
    regex = r'\d{4}'

    @staticmethod
    def to_python(value):
        return int(value)

    @staticmethod
    def to_url(value):
        return str(value)
