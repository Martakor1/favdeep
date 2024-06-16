import json

from django.db.models import Q
from django_filters import filters, FilterSet

from core.choices import OwnreshipType, TradeType, PlaceType


class InvestPlaceFilter(FilterSet):
    support_object_type = filters.ChoiceFilter(label='Отбор по типу поддержки',
                                               choices=(("Технопарк", "Технопарк"),
                                                        ("Без льгот", "Без льгот")))

    preferential_treatment = filters.ChoiceFilter(label="Преференции инвестиционного положения",
                                                  choices=(
                                                      ('Отсутствуют', 'Отсутствуют'),
                                                      ('Особая экономическая зона', 'Особая экономическая зона')
                                                  ))
    trade_type = filters.ChoiceFilter(label="Тип сделки", choices=TradeType)

    ownership = filters.ChoiceFilter(label="Право собственности", choices=OwnreshipType)

    place_type = filters.ChoiceFilter(label="Тип места", choices=PlaceType)

    class Meta:
        fields = ['support_object_type', 'preferential_treatment_type', 'trade_type', 'ownership',
                  'place_type']


class SpecialEconomicsFilter(FilterSet):
    object_category = filters.ChoiceFilter(label="Категория экономической зоны", choices=(
        ('Особая экономическая зона', 'Особая экономическая зона'),
        ('Технопарк', 'Технопарк')
    ))

    possibility_buying_premises = filters.ChoiceFilter(label="Возможность покупки недвижемости",
                                                       choices=(("да", "да"), ('нет', 'нет')))
    list_industries = filters.ChoiceFilter(label="Специализация зоны", lookup_expr='in',
                                           choices=(
                                               ([74, 72], 'Наука'),
                                               ([63, 62, 61, 60], 'Информационные технологии и телекоммуницая',),
                                               ([27, 26], 'Производство электрического оборудования'),
                                               ([23], 'Производство неметаллической минеральной продукции'),
                                               ([31, 16], 'Обработка древесины и прозводство мебели'),
                                               ([20, 21, 19], 'Производство химической продукции'),
                                               ([80, 79, 18, 13, 14, 15, 17], 'Прочее')
                                           ), method='filter_list_industries')

    class Meta:
        fields = ['possibility_buying_premises', 'restrictions_on_types_activities']

    def filter_list_industries(self, queryset, name, value):
        q = Q()
        value = json.loads(value)

        for item in value:
            print(item)
            q |= Q(list_industries__icontains=str(item))

        return queryset.filter(q)


class RegionalSupportsMeasuresFilter(FilterSet):
    support_type = filters.ChoiceFilter(label="Вид поддержки", choices=(
        ('образовательная поддержка', 'образовательная поддержка'),
        ('льготное кредитование и гарантии', 'льготное кредитование и гарантии'),
        ('Меры поддержки ВЭД', 'Меры поддержки ВЭД'),
        ('субсидии и гранты', 'субсидии и гранты'),
        ('льготы по аренде', 'льготы по аренде'),
        ('налоговые и тарифные льготы', 'налоговые и тарифные льготы'),
        ('консультационная поддержка', 'консультационная поддержка'),
        ('прочие нефинансовые меры поддержки', 'прочие нефинансовые меры поддержки'),
        ('сопровождение проектов по принципу «одного окна»', 'сопровождение проектов по принципу «одного окна»')
    ))

    class Meta:
        filters = ['support_type']
