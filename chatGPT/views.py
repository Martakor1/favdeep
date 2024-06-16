from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import GptSerializer, GptSerializerFilter
import requests
from django.db import connection
from core.models import InvestPlace, SpecialEconomicsZonesAndTechn, RegionalSupportsMeasures
from django.db.models.functions import Lower


# generic viewset
class ChadGPTAPIView(GenericAPIView):
    serializer_class = GptSerializer
    queryset = None

    def post(self, request, *args, **kwargs):

        serializer = GptSerializer(data=request.data)

        if serializer.is_valid():
            message = request.data.get("message", "Как дела?")
            request_json = {
                "message": message,
                "api_key": "chad-c647e5d4d8fa4f0ca5457d4e62f965812ra1iudl",
                "history": [
                    {"role": "system",
                     "content": "Ты - полезный ассистент в области инвестиций. Ты знаешь только все, что касается инвестиций! Если человек задает вопрос не по делу, отвечай <<Это не моя компетенция>>."},
                ]
            }
            response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-3.5', json=request_json)
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json['is_success']:
                    return Response({
                        'response': resp_json['response'],
                        'used_words_count': resp_json['used_words_count']
                    })
                else:
                    return Response({'error': resp_json['error_message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': f'Error! Code answer: {response.status_code}'}, status=response.status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChadGPTFiltreCategoryView(GenericAPIView):
    serializer_class = GptSerializerFilter
    queryset = None

    def parse_and_search_in_db(self, data_str, model):
        data_parts = data_str.split(', ')
        search_results = {}
        id_search_result = set()
        for part in data_parts:

            key, value = part.split(': ')
            key = key.strip()
            value = value.strip()
            print(key, value)
            query = {f'{key}__contains': value.lower()}
            try:
                search_results = model.objects.annotate(
                    lower_field=Lower(key)
                ).filter(
                    lower_field__contains=value.lower()
                ).values_list('name', flat=True)
                print(key, value, search_results)
            except Exception as e:
                search_results = model.objects.filter(**query).values_list('name')
            if not id_search_result:
                id_search_result.update(search_results)
            if id_search_result.intersection(search_results):
                id_search_result.intersection_update(search_results)
        print(id_search_result)
        return id_search_result

    def post(self, request, *args, **kwargs):
        list_of_industries = {
            '01': 'Растениеводство и животноводство, охота и предоставление соответствующих услуг в этих областях',
            '02': 'Лесоводство и лесозаготовки',
            '03': 'Рыболовство и рыбоводство',
            '05': 'Добыча угля',
            '06': 'Добыча сырой нефти и природного газа',
            '07': 'Добыча металлических руд',
            '08': 'Добыча прочих полезных ископаемых',
            '09': 'Предоставление услуг в области добычи полезных ископаемых',
            '10': 'Производство пищевых продуктов',
            '23': 'Производство прочей неметаллической минеральной продукции',
            '24': 'Производство металлургическое',
            '25': 'Производство готовых металлических изделий, кроме машин и оборудования',
            '26': 'Производство компьютеров, электронных и оптических изделий',
            '27': 'Производство электрического оборудования',
            '28': 'Производство машин и оборудования, не включенных в другие группировки',
            '29': 'Производство автотранспортных средств, прицепов и полуприцепов',
            '30': 'Производство прочих транспортных средств и оборудования',
            '31': 'Производство мебели',
            '32': 'Производство прочих готовых изделий',
            '22': 'Производство резиновых и пластмассовых изделий',
            '21': 'Производство лекарственных средств и материалов, применяемых в медицинских целях',
            '11': 'Производство напитков',
            '12': 'Производство табачных изделий',
            '13': 'Производство текстильных изделий',
            '14': 'Производство одежды',
            '15': 'Производство кожи и изделий из кожи',
            '16': 'Обработка древесины и производство изделий из дерева и пробки, кроме мебели, производство изделий из соломки и материалов для плетения',
            '17': 'Производство бумаги и бумажных изделий',
            '18': 'Деятельность полиграфическая и копирование носителей информации',
            '19': 'Производство кокса и нефтепродуктов 20 Производство химических веществ и химических продуктов',
            '33': 'Ремонт и монтаж машин и оборудования',
            '35': 'Обеспечение электрической энергией, газом и паром; кондиционирование воздуха',
            '36': 'Забор, очистка и распределение воды',
            '37': 'Сбор и обработка сточных вод',
            '38': 'Сбор, обработка и утилизация отходов; обработка вторичного сырья',
            '39': 'Предоставление услуг в области ликвидации последствий загрязнений и прочих услуг, связанных с удалением отходов',
            '41': 'Строительство зданий',
            '42': 'Строительство инженерных сооружений',
            '43': 'Работы строительные специализированные',
            '45': 'Торговля оптовая и розничная автотранспортными средствами и мотоциклами и их ремонт',
            '46': 'Торговля оптовая, кроме оптовой торговли автотранспортными средствами и мотоциклами',
            '47': 'Торговля розничная, кроме торговли автотранспортными средствами и мотоциклами',
            '49': 'Деятельность сухопутного и трубопроводного транспорта',
            '50': 'Деятельность водного транспорта',
            '51': 'Деятельность воздушного и космического транспорта',
            '52': 'Складское хозяйство и вспомогательная транспортная деятельность',
            '53': 'Деятельность почтовой связи и курьерская деятельность',
            '55': 'Деятельность по предоставлению мест для временного проживания',
            '56': 'Деятельность по предоставлению продуктов питания и напитков',
            '58': 'Деятельность издательская',
            '59': 'Производство кинофильмов, видеофильмов и телевизионных программ, издание звукозаписей и нот',
            '60': 'Деятельность в области телевизионного и радиовещания',
            '61': 'Деятельность в сфере телекоммуникаций',
            '62': 'Разработка компьютерного программного обеспечения, консультационные услуги в данной области и другие сопутствующие услуги',
            '63': 'Деятельность в области информационных технологий',
            '64': 'Деятельность по предоставлению финансовых услуг, кроме услуг по страхованию и пенсионному обеспечению',
            '65': 'Страхование, перестрахование, деятельность негосударственных пенсионных фондов, кроме обязательного социального обеспечения',
            '66': 'Деятельность вспомогательная в сфере финансовых услуг и страхования',
            '68': 'Операции с недвижимым имуществом',
            '69': 'Деятельность в области права и бухгалтерского учета',
            '70': 'Деятельность головных офисов; консультирование по вопросам управления',
            '71': 'Деятельность в области архитектуры и инженерно-технического проектирования; технических испытаний, исследований и анализа',
            '72': 'Научные исследования и разработки',
            '73': 'Деятельность рекламная и исследование конъюнктуры рынка',
            '74': 'Деятельность профессиональная научная и техническая прочая',
            '75': 'Деятельность ветеринарная',
            '77': 'Аренда и лизинг',
            '78': 'Деятельность по трудоустройству и подбору персонала',
            '79': 'Деятельность туристических агентств и прочих организаций, предоставляющих услуги в сфере туризма',
            '80': 'Деятельность по обеспечению безопасности и проведению расследований',
            '81': 'Деятельность по обслуживанию зданий и территорий',
            '82': 'Деятельность административно-хозяйственная, вспомогательная деятельность по обеспечению функционирования организации, деятельность по предоставлению прочих вспомогательных услуг для бизнеса',
            '84': 'Деятельность органов государственного управления по обеспечению военной безопасности, обязательному социальному обеспечению',
            '85': 'Образование',
            '86': 'Деятельность в области здравоохранения',
            '87': 'Деятельность по уходу с обеспечением проживания',
            '88': 'Предоставление социальных услуг без обеспечения проживания',
            '90': 'Деятельность творческая, деятельность в области искусства и организации развлечений',
            '91': 'Деятельность библиотек, архивов, музеев и прочих объектов культуры',
            '92': 'Деятельность по организации и проведению азартных игр и заключению пари, по организации и проведению лотерей',
            '93': 'Деятельность в области спорта, отдыха и развлечений',
            '94': 'Деятельность общественных организаций',
            '95': 'Ремонт компьютеров, предметов личного потребления и хозяйственно-бытового назначения',
            '96': 'Деятельность по предоставлению прочих персональных услуг',
            '97': 'Деятельность домашних хозяйств с наемными работниками',
            '98': 'Деятельность недифференцированная частных домашних хозяйств по производству товаров и предоставлению услуг для собственного потребления',
            '99': 'Деятельность экстерриториальных организаций и органов'}

        regional = {'region': 'Регион', 'name': 'Наименование меры поддержки', 'support_type': 'Вид поддержки',
                    'support_level': 'Уровень поддержки', 'main_idea': 'Суть механизма',
                    'npa_requisite': 'Реквизиты НПА',
                    'npa_url': 'Ссылка на НПА', 'npa_download_url': 'Загрузить НПА',
                    'application_form_link': 'Ссылка на форму подачи заявки',
                    'name_of_the_responsible_authority': 'Наименование ответственного органа власти, администрирующего данную меру поддержки',
                    'min_investment_volume': 'Минимальный объем инвестиций', 'okved': 'ОКВЭД',
                    'OKVED': 'ОКВЭД', 'OKVED': ' Список отраслей', 'okved': 'Список отраслей',
                    'restrictions_on_type_of_activities': 'Ограничения по видам деятельности',
                    'required_entry_into_sme': 'Требуется вхождение в реестр МСП',
                    'requirements_for_the_applicant': 'Требования к заявителю',
                    'application_procedure': 'Процедура подачи заявки',
                    'required_documents': 'Необходимые документы'}

        technoparks = {'object_category': 'Категория объекта', 'sez': 'ОЭЗ', 'top': 'ТОР',
                       'name': 'Наименование объекта',
                       'region': 'Регион', 'municipal_formation': 'Муниципальное образование',
                       'nearest_city': 'Ближайший город',
                       'number_residents': 'Количество резидентов', 'photos_object_url': 'Фотографии объекта',
                       'documents_object_url': 'Документы по объекту',
                       'year_object_formation': 'Год формирования объекта',
                       'validation_period_object': 'Срок действия объекта', 'total_area': 'Общая площадь',
                       'minimal_rental_price': 'Минимальная стоимость аренды',
                       'possibility_buying_premises': 'Возможность выкупа помещения / участка (да / нет)',
                       'list_industries': 'Список отраслей',
                       'restrictions_on_types_activities': 'Ограничения по видам деятельности',
                       'infrastructure_and_services': 'Инфраструктура и сервисы',
                       'additional_services_management_company': 'Дополнительные услуги управляющей компании',
                       'name_admin_object': 'Название администратора объекта',
                       'address_admin_object': 'Адрес администратора объекта',
                       'link_site': 'Ссылка на сайт', 'working_hours': 'Время работы', 'income_tax': 'Налог на прибыль',
                       'property_tax': 'Налог на имущество', 'land_tax': 'Земельный налог',
                       'transport_tax': 'Транспортный налог',
                       'insurance_premiums': 'Страховые взносы', 'other_benefits': 'Прочие льготы',
                       'availability_of_a_free_customs_zone': 'Наличие режима свободной таможенной зоны (да/нет), условия',
                       'how_to_become_a_residents': 'Как стать резидентом',
                       'minimum_investment_amount': 'Минимальный объем инвестиций',
                       'coordinates': 'Координаты'}

        invest_dic = {'name': 'Название площадки', 'preferential_treatment': 'Преференциальный режим',
                      'preferential_treatment_id': 'Наименование объекта преференциального режима',
                      'preferential_treatment_name': 'Наименование объекта преференциального режима_наименование',
                      'support_object_type': 'Объект инфраструктуры поддержки',
                      'support_object_id': 'Наименование объекта инфраструктуры поддержки',
                      'support_object_name': 'Наименование объекта инфраструктуры поддержки_наименование',
                      'region': 'Регион',
                      'municipality': 'Муниципальное образование', 'address': 'Адрес объекта',
                      'nearest_city': 'Ближайший город', 'place_type': 'Формат площадки',
                      'novelty_type': 'Тип площадки',
                      'ownership': 'Форма собственности объекта', 'trade_type': 'Форма сделки',
                      'price': 'Стоимость объекта',
                      'year_price_ga': 'Стоимость, руб./год за га', 'year_price_m2': 'Стоимость, руб./год за кв.м.',
                      'rent_time_constraits': 'min и max сроки аренды',
                      'price_setting_rule': 'Порядок определения стоимости', 'danger_class': 'Класс опасности объекта',
                      'capital_constructions_description': 'Характеристики расположенных объектов капитального строительства',
                      'free_land_ga': 'Свободная площадь', 'cadastral_number_land': 'Кадастровый номер ЗУ',
                      'allowed_buisnesses': 'Варианты разрешенного использования', 'surveying': 'Межевание ЗУ',
                      'land_category': 'Категория земель',
                      'free_room_m2': 'Свободная площадь здания, сооружения, помещения',
                      'cadastral_number_room': 'Кадастровый номер здания, сооружения, помещения',
                      'tech_building_characteristics': 'Технические характеристики здания, сооружения, помещения',
                      'owner_name': 'Наименование собственника / администратора объекта',
                      'owner_inn': 'ИНН собственника',
                      'owner_url': 'Сайт', 'note': 'Примечание', 'water_supply': 'Водоснабжение Наличие (Да/Нет)',
                      'water_cost': 'Водоснабжение Тариф на потребление, руб./куб. м',
                      'water_cost_transportation': 'Водоснабжение Тариф на транспортировку, руб./куб. м',
                      'water_facilities_max_power': 'Объекты водоснабжения Максимально допустимая мощность, куб. м/ч',
                      'water_facilities_free_power': 'Объекты водоснабжения Свободная мощность, куб.м/ч',
                      'water_facilities_note': 'Объекты водоснабжения Иные характеристики',
                      'water_throughput': 'Сети водоснабжения Пропускная способность, куб. м/ч',
                      'sewage_supply': 'Водоотведение Наличие (Да/Нет)',
                      'sewage_cost': 'Водоотведение Тариф на потребление, руб./куб. м',
                      'sewage_cost_transportation': 'Водоотведение Тариф на транспортировку, руб./куб. м',
                      'sewage_facilities_max_power': 'Объекты водоотведения Максимально допустимая мощность, куб. м/ч',
                      'sewage_facilities_free_power': 'Объекты водоотведения Свободная мощность, куб. м/ч',
                      'sewage_facilities_note': 'Объекты водоотведения Иные характеристики',
                      'sewage_throughput': 'Сети водоотведения Пропускная способность, куб. м/ч',
                      'gas_supply': 'Газоснабжение Наличие (Да/Нет)',
                      'gas_cost': 'Газоснабжение Тариф на потребление',
                      'gas_cost_transportation': 'Газоснабжение Тариф на транспортировку,',
                      'gas_facilities_max_power': 'Объекты газоснабжения Максимально допустимая мощность, куб. м./ч',
                      'gas_facilities_free_power': 'Объекты газоснабжения Свободная мощность, куб. м/ч',
                      'gas_facilities_note': 'Объекты газоснабжения Иные характеристики',
                      'gas_throughput': 'Сети газоснабжения Пропускная способность, куб. м/ч',
                      'electricity_supply': 'Электроснабжение Наличие (Да/Нет)',
                      'electricity_cost': 'Электроснабжение Тариф на потребление, руб./МВт*ч',
                      'electricity_cost_transportation': 'Электроснабжение Тариф на транспортировку, руб./МВт*ч',
                      'electricity_facilities_max_power': 'Объекты электроснабжения Максимально допустимая мощность, МВт/ч',
                      'electricity_facilities_free_power': 'Объекты электроснабжения Свободная мощность, МВт/ч',
                      'electricity_facilities_note': 'Объекты электроснабжения Иные характеристики',
                      'electricity_throughput': 'Сети электроснабжения Пропускная способность, МВт/ч',
                      'heat_supply': 'Теплоснабжение Наличие (Да/Нет)',
                      'heat_cost': 'Теплоснабжение Тариф на потребление, руб./Гкал*ч',
                      'heat_cost_transportation': 'Теплоснабжение Тариф на транспортировку, руб./Гкал*ч',
                      'heat_facilities_max_power': 'Объекты теплоснабжения Максимально допустимая мощность, Гкал/ч',
                      'heat_facilities_free_power': 'Объекты теплоснабжения Свободная мощность, Гкал/ч',
                      'heat_facilities_note': 'Объекты теплоснабжения Иные характеристики',
                      'heat_throughput': 'Сети теплоснабжения Пропускная способность, Гкал/ч',
                      'tko_availability': 'Вывоз ТКО Наличие (Да/Нет)', 'tko_cost_ton': 'Вывоз ТКО Тариф, руб./тонна',
                      'tko_cost_m3': 'Вывоз ТКО Тариф, руб./куб. м',
                      'access_roads_availability': 'Наличие подъездных путей (Да/Нет)',
                      'raild_roads_availability': 'Наличие ж/д (Да/Нет)',
                      'cargo_parking_availability': 'Наличие парковки грузового транспорта',
                      'other_characteristics': 'Иные характеристики',
                      'application_process_description': 'Описание процедуры подачи заявки',
                      'application_documents': 'Перечень документов, необходимых для подачи заявки',
                      'application_url': 'Ссылка на форму подачи заявки',
                      'possible_businesses': 'Список отраслей',
                      'urban_planning_characteristics_and_limitations': 'Градостроительные характеристики и ограничения',
                      'territorial_planining_documents': 'Документы территориального планирования',
                      'other_information': 'Иные сведения', 'photos_object_url': 'Фотографии объекта',
                      'availability_maip': 'Наличие МАИП', 'description_benefit': 'Описание льготы',
                      'coordinates': 'Координаты (точка)'}
        serializer = GptSerializerFilter(data=request.data)
        if serializer.is_valid():
            message = request.data.get("message", "Как дела?")
            category = request.data.get("category", "Технопарк")
            if (category == "4" or category == "4"):
                request_json = {
                    "message": message,
                    "api_key": "chad-c647e5d4d8fa4f0ca5457d4e62f965812ra1iudl",
                    "history": [
                        {"role": "system",
                         "content": "Ты - полезный ассистент в области инвестиций. "
                                    "Если человек задает вопрос не по делу, отвечай <<Это не моя компетенция>>."
                                    " Тебе дан список категорий  и дано сообщение пользователя. "
                                    "Если человек имеет ввиду категорию которая есть в списке категорий,"
                                    " то ответь  этой категорией и через двоеточие напиши значение, "
                                    "которое относится к этой категории ,если в сообщении пользователя категорий несколько, "
                                    "то напиши несколько категорий  о которых вел речь пользователь и через двоеточие их значения."
                                    "Если подразумевает, что значение категории о которой идет речь равна нулю или отсутсвует, то через двоеточие напиши <<0>>"
                                    "Если категория подразумевает численное значение или дату, то всегда через двоеточие пиши число."
                                    "Если ни к одной категории не относится,  "
                                    "то напиши <<Извините я не понимаю о чем вы>>. Любые налоги или категории которые подразумевают числа, записывай числом, даже если написано слово."
                                    " Сам список категорий: Наименование объекта, Муниципальное образование, Количество резидентов ,"
                                    "Год формирования объекта ,Срок действия объекта,Общая площадь ,Список отраслей, "
                                    "Налог на прибыль, Налог на имущество ,Земельный налог, Транспортный налог,Страховые взносы "
                                    ",Минимальный объем инвестиций. Выдай как в примере.  Пример: Налог : 0, Наименование объекта: Технополис"},

                    ]
                }
            if (category == "5"):
                request_json = {
                    "message": message,
                    "api_key": "chad-c647e5d4d8fa4f0ca5457d4e62f965812ra1iudl",
                    "history": [
                        {"role": "system",
                         "content": "Ты - полезный ассистент в области инвестиций. "
                                    "Если человек задает вопрос не по делу, отвечай <<Это не моя компетенция>>."
                                    " Тебе дан список категорий  и дано сообщение пользователя. "
                                    "Если человек имеет ввиду категорию которая есть в списке категорий,"
                                    " то ответь  этой категорией и через двоеточие напиши значение, "
                                    "которое относится к этой категории ,если в сообщении пользователя категорий несколько, "
                                    "то напиши несколько категорий  о которых вел речь пользователь и через двоеточие их значения."
                                    "Если подразумевает, что значение категории, о которой идет речь равна нулю или отсутсвует, то через двоеточие напиши <<0>>"
                                    "Если ни к одной категории не относится,  "
                                    "то напиши <<Извините я не понимаю о чем вы>>. "
                                    "Сам список категорий: Список отраслей,"
                                    "Минимальный объем инвестиций.  "
                                    "Выдай как в примере.  Пример: Налог : 0, Наименование объекта: Технополис"},
                    ]
                }
            if (category == "3"):
                request_json = {
                    "message": message,
                    "api_key": "chad-c647e5d4d8fa4f0ca5457d4e62f965812ra1iudl",
                    "history": [
                        {"role": "system",
                         "content": "Ты - полезный ассистент в области инвестиций. "
                                    "Если человек задает вопрос не по делу, отвечай <<Это не моя компетенция>>."
                                    " Тебе дан список категорий  и дано сообщение пользователя. "
                                    "Если человек имеет ввиду категорию которая есть в списке категорий,"
                                    " то ответь  этой категорией и через двоеточие напиши значение, "
                                    "которое относится к этой категории ,если в сообщении пользователя категорий несколько, "
                                    "то напиши несколько категорий  о которых вел речь пользователь и через двоеточие их значения."
                                    "Если подразумевает, что значение категории, о которой идет речь равна нулю или отсутсвует, то через двоеточие напиши <<0>>"
                                    "Если ни к одной категории не относится,  "
                                    "то напиши <<Извините я не понимаю о чем вы>>.Любые налоги или категории которые подразумевают числа, записывай числом, даже если написано слово. "
                                    "Сам список категорий: Муниципальное образование, Тип площадки, Форма собственности объекта,"
                                    "Стоимость объекта ,Стоимость руб./год за га, Стоимость, руб./год за м.кв.,min и max сроки аренды ,"
                                    "Список отраслей, Свободная площадь, "
                                    "Водоснабжение Наличие,Водоотведение Наличие,Газоснабжение Наличие,Электроснабжение Наличие,"
                                    "Теплоснабжение Наличие,Вывоз ТКО Наличие,Наличие подъездных путей,Наличие ж/д,Наличие парковки грузового транспорта "
                                    " Выдай как в примере.  Пример: Налог : 0, Наименование объекта: Технополис"},
                    ]
                }
            response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-3.5', json=request_json)
            if response.status_code == 200:
                resp_json = response.json()
                if ':' in resp_json['response']:
                    if (category == "5"):
                        if ("Список отраслей" in resp_json['response'].lower()):
                            request_json_2 = {
                                "message": resp_json['response'],
                                "api_key": "chad-c647e5d4d8fa4f0ca5457d4e62f965812ra1iudl",
                                "history": [
                                    {"role": "system",
                                     "content": "Ты получаешь список отраслей. За каждым названием прикплен номер. Также ты получаешь сообщение пользователя."
                                                f"Твоя задача заменить сообщение пользователя на номер из списка отраслей о которой идет речь в сообщении пользователя, не меняя при этом остальное! Вот список отраслей:{list_of_industries} "},
                                ]
                            }
                            response2 = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-3.5',
                                                      json=request_json_2)
                            resp_json = response2.json()
                        a = resp_json['response']
                        for i in regional:
                            a = a.replace(regional[i], i)
                        result = self.parse_and_search_in_db(a, RegionalSupportsMeasures)

                    if (category == "4" or category == "4"):
                        if ("Список отраслей" in resp_json['response']):
                            request_json_2 = {
                                "message": resp_json['response'],
                                "api_key": "chad-c647e5d4d8fa4f0ca5457d4e62f965812ra1iudl",
                                "history": [
                                    {"role": "system",
                                     "content": "Ты получаешь список отраслей. За каждым названием прикплен номер этой отрасли. Также ты получаешь сообщение пользователя."
                                                f"Твоя задача заменить сообщение пользователя на номер из списка отраслей, не меняя при этом остальное! Вот список отраслей:{list_of_industries}"},
                                ]
                            }
                            response2 = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-3.5',
                                                      json=request_json_2)
                            resp_json = response2.json()
                        b = resp_json['response']
                        for i in technoparks:
                            b = b.replace(technoparks[i], i)
                        result = self.parse_and_search_in_db(b, SpecialEconomicsZonesAndTechn)

                    if (category == "3"):
                        if ("Список отраслей" in resp_json['response']):
                            request_json_2 = {
                                "message": resp_json['response'],
                                "api_key": "chad-c647e5d4d8fa4f0ca5457d4e62f965812ra1iudl",
                                "history": [
                                    {"role": "system",
                                     "content": "Ты получаешь список отраслей. За каждым названием прикплен номер. Также ты получаешь сообщение пользователя."
                                                f"Твоя задача заменить сообщение пользователя на номер из списка отраслей, не меняя при этом остальное! Вот список отраслей:{list_of_industries}"},
                                ]
                            }
                            response2 = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-3.5',
                                                      json=request_json_2)
                            resp_json = response2.json()
                        c = resp_json['response']
                        for i in invest_dic:
                            c = c.replace(invest_dic[i], i)
                        result = self.parse_and_search_in_db(c, InvestPlace)
                        print(result)
                else:
                    result = resp_json['response']
                if resp_json['is_success']:
                    return Response({
                        'response': result,
                        'used_words_count': resp_json['used_words_count']
                    })
                else:
                    return Response({'error': resp_json['error_message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': f'Error! Code answer: {response.status_code}'}, status=response.status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)