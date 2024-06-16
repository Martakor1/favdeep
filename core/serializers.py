from rest_framework import serializers

from core.models import SpecialEconomicsZonesAndTechn, InvestPlace, RegionalSupportsMeasures


class SpecialEconomicsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = SpecialEconomicsZonesAndTechn

class InvestPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = InvestPlace

class RegionalSupportsMeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = RegionalSupportsMeasures

def get_serializer_for_model(model_class):
    data = {
        InvestPlace: InvestPlaceSerializer,
        SpecialEconomicsZonesAndTechn: SpecialEconomicsSerializer,
        RegionalSupportsMeasures: RegionalSupportsMeasuresSerializer

    }

    return data[model_class]

    #TODO: populate...


