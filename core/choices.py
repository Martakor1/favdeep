from django.db import models


class PlaceType(models.TextChoices):
    FIELD = "Земельный участок"
    ROOM = "Помещение"


class InvestingFieldType(models.TextChoices):
    GREENFIELD = "Гринфилд"
    BROWNFIELD = "Браунфилд"


class OwnreshipType(models.TextChoices):
    PRIVATE = "Частная"
    GOV = "Государственная до разграничения"
    CITY = "Муниципальная"
    REGION = "Региональная"

class TradeType(models.TextChoices):
    AUCTION_SALE = "Продажа через аукцион"
    AUCTION_RENT = "Аренда через аукцион"
    SALE = "Продажа"
    RENT = "Аренда"


class Possibility_buying_premises(models.TextChoices):
    YES = "да",
    NO = "нет"

class Availability_of_a_free_customs_zone(models.TextChoices):
    YES = "да",
    NO = "нет"  # Ответ да / нет однако есть в верхнем регистре