from django.contrib import admin
from .models import *

@admin.register(InvestPlace)
class InvestPlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(RegionalSupportsMeasures)
class RegionalSupportsMeasures(admin.ModelAdmin):
    pass

@admin.register(SpecialEconomicsZonesAndTechn)
class SpecialEconomicZoneAndTechnAdmin(admin.ModelAdmin):
    pass