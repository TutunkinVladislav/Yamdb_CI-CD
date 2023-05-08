from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > datetime.now().year or value < 0:
        raise ValidationError("Год публикации должен быть не больше текущего"
                              "и не может быть отрицательным числом!")


def validate_score(value):
    if value < 1 or value > 10:
        raise ValidationError("Оценка публикации должна быть "
                              "в диапазоне от 1 до 10!")
