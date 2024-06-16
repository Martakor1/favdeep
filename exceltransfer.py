from core.models import InvestPlace, RegionalSupportsMeasures, SpecialEconomicsZonesAndTechn
import pandas as pd
import numpy as np
from django.db import models

def transform_float(x):
    if type(x) == str:
        return float(x.replace(',', '.'))
    elif (type(x) == int):
        return float(x)
    else: return x
    
def transform_pos_integer(x: str):
    if (x is None):
        return None
    elif (type(x) == str): return int(x.strip())
    else: return int(x)
    
def transform_yes_to_bool(x):
    if (x == "Да" or x == "да"):
        return True
    elif (x == "Нет" or x == "нет"):
        return False
    else: return None

def transform_all(df: pd.DataFrame):
    df = df.replace({np.nan: None})
    #закомментил так как для каждой таблицы свой transform надо писать
    #легче трансформировать на ходу само значение в зависимости от типа models.Fields
    # df["Объекты электроснабжения Свободная мощность, МВт/ч"] = df["Объекты электроснабжения Свободная мощность, МВт/ч"].apply(transform_float)
    # yes_to_bool_columns = ["Межевание ЗУ", "Вывоз ТКО Наличие (Да/Нет)", "Наличие подъездных путей (Да/Нет)", "Наличие парковки грузового транспорта", "Наличие МАИП"]
    # for col in yes_to_bool_columns:
    #     df[col] = df[col].apply(transform_yes_to_bool)
    return df


def start_transfer():
    FOLDER = "C:/myfolder/Кейс инвестплощадки/5. ДИПП/"
    #df = pd.read_excel(FOLDER + "Помещения и сооружения.xlsx")
    #df = pd.read_excel(FOLDER + "Региональные меры поддержки Москва.xlsx")
    df = pd.read_excel(FOLDER + "ОЭЗ и Технопарки.xlsx")
    df = transform_all(df)
    MODEL_TYPE = SpecialEconomicsZonesAndTechn
    for i, row in df.iterrows():
        fields_dict = {}
        for j, field in enumerate(MODEL_TYPE._meta.get_fields()[1:]):
            #print(field.name, row.keys()[j]) #для проверки совпадения списков колонок
            val = row[row.keys()[j]]
            #print(val)
            if (not (type(field) == models.CharField or type(field) == models.TextField)):
                if (type(field) == models.FloatField):
                    val = transform_float(val)
                elif (type(field) == models.PositiveIntegerField):
                    val = transform_pos_integer(val)
                    #print(val)
                elif (type(field) == models.BooleanField):
                    val = transform_yes_to_bool(val)
            else:
                if (val is not None and type(field) != models.TextField):
                    if (len(val) > field.max_length): #для просмотра где ломается
                        print(field.name, len(val), field.max_length)
            fields_dict[field.name] = val #верим, что идут параллельно
        MODEL_TYPE.objects.get_or_create(**fields_dict)
        #break
        print("sucsess")
    