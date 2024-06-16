import psycopg2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from models import InvestPlace
 
 
params = {
    'dbname': "favdeep_database",
    'user': "favdeep_database_user",
    'password': "WozGFnbtNYYiubUfbcuBLhuoNZYr7YVl",
    'host': "dpg-cpir66kf7o1s73blgq70-a.frankfurt-postgres.render.com"
}
 
names_of_column = {
    'object_category' : 'Категория объекта',
    'sez' : 'ОЭЗ',
    'name' : 'Наименование объекта',
    'region' : 'Регион',
    'municipal_formation' : 'Муниципальное образование',
    'number_residents' : 'Количество резидентов',
    'documents_object_url' : 'Документы по объекту',
    'year_object_formation' : 'Год формирования объекта',
    'validation_period_object' : 'Срок действия объекта, лет',
    'total_area' : 'Общая площадь, кв. м',
    'minimal_rental_price' : 'Минимальная стоимость аренды, руб./кв.м/год',
    'possibility_buying_premises' : 'Возможность выкупа помещения / участка (да / нет)',
    'list_industries' : 'Список отраслей',
    'restrictions_on_types_activities' : 'Ограничения по видам деятельности',
    'infrastructure_and_services' : 'Инфраструктура и сервисы',
    'name_admin_object' : 'Название администратора объекта',
    'address_admin_object' : 'Адрес администратора объекта',
    'link_site' : 'Ссылка на сайт',
    'working_hours' : 'Время работы',
    'income_tax' : 'Налог на прибыль',
    'property_tax' : 'Налог на имущество',
    'land_tax' : 'Земельный налог',
    'transport_tax' : 'Транспортный налог',
    'insurance_premiums' : 'Страховые взносы',
    'other_benefits' : 'Прочие льготы',
    'availability_of_a_free_customs_zone' : 'Наличие режима свободной таможенной зоны (да/нет), условия',
    'minimum_investment_amount' : 'Минимальный объем инвестиций, руб.',
}
 
 
def create_pdf(data, needed_objects : set):
    pdf_filename = 'result.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
 
 
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
 
 
    normal_text = ParagraphStyle(name='Normal', fontName='DejaVuSans', fontSize=10, leading=12)
    bold_text = ParagraphStyle(name='Bold', fontName='DejaVuSans-Bold', fontSize=10, leading=12)
    elements = []
 
    header_text = 'Отчет по найденным объектам'
    header_style = ParagraphStyle(name='Header', fontName='DejaVuSans', fontSize=20, leading=22, textColor=colors.black)
    header_paragraph = Paragraph(header_text, header_style)
    elements.append(header_paragraph)
    elements.append(Spacer(1, 20))
 
    current = 0
    objects = InvestPlace.objects.all()
    for index, row in enumerate(objects):
        if index not in needed_objects: continue
        current += 1
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Объект {current}:", bold_text))
        elements.append(Spacer(1, 10))
        for col, value in zip(cursor.description, row):
            if value is not None and col.name not in {'top', 'nearest_city', 'how_to_become_a_residents', 'coordinates', 'photos_object_url'}: 
                if isinstance(value, str) and ('•' in value or ';' in value):
                        elements.append(Paragraph(f"{names_of_column[col.name]}:", bold_text))
                        if '•' in value:
                            for item in value.split('•'):
                                if item:
                                    elements.append(Paragraph(f" • {item}", normal_text))
                        else:
                            for item in value.split(';'):
                                if item:
                                    elements.append(Paragraph(f" {item}", normal_text))
                else:
                    elements.append(Paragraph(f"{names_of_column[col.name]}:", bold_text))
                    elements.append(Paragraph(f"{value}", normal_text))
        elements.append(Paragraph("", styles["Normal"]))
 
    doc.build(elements)
 
conn = psycopg2.connect(**params)
cursor = conn.cursor()
query = "SELECT object_category, sez, name, region, municipal_formation, number_residents, " \
        "documents_object_url, year_object_formation, validation_period_object, " \
        "total_area, minimal_rental_price, possibility_buying_premises, list_industries, " \
        "restrictions_on_types_activities, infrastructure_and_services, additional_services_management_company, " \
        "name_admin_object, address_admin_object, link_site, working_hours, income_tax, " \
        "property_tax, land_tax, transport_tax, insurance_premiums, other_benefits, " \
        "availability_of_a_free_customs_zone, minimum_investment_amount " \
        "FROM core_specialeconomicszonesandtechn"
cursor.execute(query)
data = cursor.fetchall()
 
 
needed_objects = [1, 3, 10] # тут передают айди тех объектов которые нужны в отчете
 
create_pdf(data, set(needed_objects))