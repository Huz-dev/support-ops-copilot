from app.models.schemas import (
    Classification,
    Extraction,
    Email,
)


class Validator:

    @staticmethod
    def classification(data):
        return Classification(**data)

    @staticmethod
    def extraction(data):
        return Extraction(**data)

    @staticmethod
    def email(data):
        return Email(**data)