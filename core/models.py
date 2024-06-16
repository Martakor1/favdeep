from abc import ABC

from django.db import models
from django.db.models import Q
from django_filters import FilterSet
from django_filters import filters
from core.choices import PlaceType, InvestingFieldType, OwnreshipType, TradeType, Possibility_buying_premises, \
    Availability_of_a_free_customs_zone
from core.filters import InvestPlaceFilter, SpecialEconomicsFilter, RegionalSupportsMeasuresFilter


class InvestPlace(models.Model):
    name = models.CharField(max_length=255)
    preferential_treatment = models.CharField(null=True, max_length=255)
    preferential_treatment_id = models.PositiveIntegerField(null=True)  # as boolean field  check is_null ..
    preferential_treatment_name = models.CharField(null=True, max_length=255)
    support_object_type = models.CharField(null=True, max_length=255)
    support_object_id = models.PositiveIntegerField(null=True)
    support_object_name = models.CharField(null=True, max_length=255)
    region = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    nearest_city = models.CharField(max_length=255)

    place_type = models.CharField(choices=PlaceType, max_length=255)

    novelty_type = models.CharField(choices=InvestingFieldType, max_length=255)

    ownership = models.CharField(choices=OwnreshipType, max_length=255)

    trade_type = models.CharField(choices=TradeType, max_length=255)
    price = models.FloatField(null=True)  # трындец, даже в этом не уверены
    year_price_ga = models.FloatField(null=True)
    year_price_m2 = models.FloatField(null=True)
    rent_time_constraits = models.CharField(null=True, max_length=255)
    price_setting_rule = models.CharField(null=True, max_length=255)
    danger_class = models.CharField(null=True, max_length=255)
    capital_constructions_description = models.TextField(null=True, max_length=1023)
    free_land_ga = models.FloatField(null=True)
    cadastral_number_land = models.CharField(null=True, max_length=255)
    allowed_buisnesses = models.TextField(null=True, max_length=1023)
    surveying = models.BooleanField(null=True, verbose_name="Межевание ЗУ")  # межевание
    land_category = models.CharField(null=True, max_length=255)
    free_room_m2 = models.FloatField(null=True)
    cadastral_number_room = models.CharField(null=True, max_length=255)
    tech_building_characteristics = models.TextField(null=True)
    owner_name = models.CharField(max_length=255)
    owner_inn = models.CharField(max_length=12, null=True)
    owner_url = models.URLField(null=True)
    note = models.TextField(null=True)

    class SupplyLinesAvailability(models.TextChoices):
        YES = "Да",
        NO = "Нет",
        ABILITY = "Возможно создание"

    water_supply = models.CharField(choices=SupplyLinesAvailability, max_length=255)
    water_cost = models.CharField(null=True)  # тоже char пока
    water_cost_transportation = models.CharField(null=True)
    water_facilities_max_power = models.FloatField(null=True)
    water_facilities_free_power = models.FloatField(null=True)
    water_facilities_note = models.TextField(null=True)
    water_throughput = models.FloatField(null=True)
    sewage_supply = models.CharField(choices=SupplyLinesAvailability, max_length=255)
    sewage_cost = models.CharField(null=True)  # float
    sewage_cost_transportation = models.CharField(null=True)
    sewage_facilities_max_power = models.FloatField(null=True)
    sewage_facilities_free_power = models.FloatField(null=True)
    sewage_facilities_note = models.TextField(null=True)
    sewage_throughput = models.FloatField(null=True)
    gas_supply = models.CharField(choices=SupplyLinesAvailability, max_length=255)
    gas_cost = models.CharField(null=True, max_length=255)  # у них указано "от .. до", поэтому char field
    gas_cost_transportation = models.CharField(null=True, max_length=255)
    gas_facilities_max_power = models.FloatField(null=True)
    gas_facilities_free_power = models.FloatField(null=True)
    gas_facilities_note = models.TextField(null=True)
    gas_throughput = models.FloatField(null=True)
    electricity_supply = models.CharField(choices=SupplyLinesAvailability, max_length=255)
    electricity_cost = models.CharField(null=True, max_length=255)  # у них указано "от .. до", поэтому char field
    electricity_cost_transportation = models.CharField(null=True, max_length=255)
    electricity_facilities_max_power = models.FloatField(null=True)
    electricity_facilities_free_power = models.FloatField(null=True)
    electricity_facilities_note = models.TextField(null=True)
    electricity_throughput = models.FloatField(null=True)
    heat_supply = models.CharField(choices=SupplyLinesAvailability, max_length=255)
    heat_cost = models.CharField(null=True, max_length=255)  # у них указано "от .. до", поэтому char field
    heat_cost_transportation = models.CharField(null=True, max_length=255)
    heat_facilities_max_power = models.FloatField(null=True)
    heat_facilities_free_power = models.FloatField(null=True)
    heat_facilities_note = models.TextField(null=True)
    heat_throughput = models.FloatField(null=True)
    tko_availability = models.BooleanField(null=True)
    tko_cost_ton = models.FloatField(null=True)
    tko_cost_m3 = models.FloatField(null=True)
    access_roads_availability = models.BooleanField(null=True)
    raild_roads_availability = models.BooleanField(null=True)
    cargo_parking_availability = models.BooleanField(null=True)
    other_characteristics = models.TextField(null=True)
    application_process_description = models.TextField(null=True)
    application_documents = models.TextField(null=True)
    application_url = models.URLField()
    possible_businesses = models.TextField(null=True)

    urban_planning_characteristics_and_limitations = models.TextField(null=True)
    territorial_planining_documents = models.CharField(null=True, max_length=255)  # нет ни одного экземпляра
    other_information = models.TextField(null=True)
    photos_object_url = models.TextField(max_length=1000, null=True)

    class AvailabilityMaip(models.TextChoices):
        YES = "Да",
        NO = "Нет"

    availability_maip = models.CharField(choices=AvailabilityMaip, max_length=255)
    description_benefit = models.TextField(null=True)
    coordinates = models.CharField(null=True,
                                   max_length=255)  # нужно проверить, задаётся через django.contib.gis.geos.Point()

    # требует gdal который не устанавливается и всё это в django.contrib, поэтому заменил на charfield

    def __str__(self):
        return self.name or ''

    filter_class = InvestPlaceFilter


class SpecialEconomicsZonesAndTechn(models.Model):
    object_category = models.CharField(max_length=200)
    sez = models.CharField(max_length=200, null=True)
    top = models.CharField(max_length=50, null=True)  # нет ни одного экземпляра
    name = models.CharField(max_length=500, null=True)
    region = models.CharField(max_length=50, null=True)
    municipal_formation = models.CharField(max_length=300, null=True)
    nearest_city = models.CharField(max_length=70, null=True)
    number_residents = models.PositiveIntegerField()
    photos_object_url = models.URLField(max_length=1000, null=True)
    documents_object_url = models.URLField(max_length=1000, null=True)
    year_object_formation = models.IntegerField(null=True)  # мб есть какой-то тип с годом, чтобы не весь int пихать
    validation_period_object = models.CharField(max_length=255,
                                                null=True)  # принимает только 2 значения 10 и 31.12.2054
    total_area = models.FloatField(null=True)
    minimal_rental_price = models.FloatField(null=True)

    possibility_buying_premises = models.CharField(choices=Possibility_buying_premises, max_length=255)
    list_industries = models.TextField(null=True)
    restrictions_on_types_activities = models.TextField(null=True)
    infrastructure_and_services = models.TextField(null=True)
    additional_services_management_company = models.TextField(null=True)  # нет ни одного экхемпляра
    name_admin_object = models.CharField(max_length=500, null=True)
    address_admin_object = models.CharField(max_length=500, null=True)
    link_site = models.URLField(max_length=100, null=True)
    working_hours = models.CharField(
        null=True,
        max_length=255)  # вроде оно, но тут может не быть именно промежутка времени, а только конкретное время
    income_tax = models.CharField(max_length=100)  # Короче там процент % поэтому чар
    property_tax = models.CharField(max_length=100, null=True)  # Процент в экселе !!!
    land_tax = models.CharField(max_length=100, null=True)  # потом расписывется после процента за что
    transport_tax = models.CharField(max_length=100, null=True)
    insurance_premiums = models.CharField(max_length=100, null=True)
    other_benefits = models.TextField(max_length=500, null=True)

    availability_of_a_free_customs_zone = models.CharField(choices=Availability_of_a_free_customs_zone, max_length=255)
    how_to_become_a_residents = models.TextField(max_length=500, null=True)
    minimum_investment_amount = models.CharField(max_length=200, null=True)
    coordinates = models.CharField(null=True,
                                   max_length=255)  # аналогично изменил на charField, так как плохая зависимость

    class Meta:
        verbose_name = "Специальные экономические зоны?"

    def __str__(self):
        return self.name or ''

    filter_class = SpecialEconomicsFilter


class RegionalSupportsMeasures(models.Model):
    region = models.CharField(max_length=30, null=True)  # Вообще всегда Москва
    name = models.CharField(max_length=255, null=True)
    support_type = models.CharField(max_length=255, null=True)
    support_level = models.CharField(max_length=255, null=True)  # Всегда написано региональный
    main_idea = models.CharField(max_length=2000, null=True)
    npa_requisite = models.CharField(max_length=2000, null=True)  # В том которого нет, написано "нет"
    npa_url = models.URLField(max_length=1000, null=True)  # Одного нет
    npa_download_url = models.URLField(max_length=1000, null=True)  # Одного нет
    application_form_link = models.URLField(max_length=1000, null=True)
    name_of_the_responsible_authority = models.CharField(max_length=1000, null=True)
    min_investment_volume = models.CharField(max_length=100,
                                             null=True)  # Нет ни одного элемента пока поставил чар, но судя по названию должно быть float
    okved = models.CharField(max_length=16000, null=True)
    restrictions_on_type_of_activities = models.CharField(max_length=2000, null=True)

    class Required_entry_into_sme(models.TextChoices):
        YES = "Да",
        NO = "Нет"

    required_entry_into_sme = models.CharField(choices=Required_entry_into_sme, max_length=255)
    requirements_for_the_applicant = models.CharField(max_length=8000, null=True)
    application_procedure = models.CharField(max_length=4000, null=True)
    required_documents = models.CharField(max_length=16000, null=True)

    def __str__(self):
        return self.name or ''

    filter_class = RegionalSupportsMeasuresFilter
