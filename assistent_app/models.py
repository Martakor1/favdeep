from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework.exceptions import PermissionDenied
from treebeard.mp_tree import MP_Node

from core.models import InvestPlaceFilter, SpecialEconomicsZonesAndTechn


# Create your models here.

class AssistentThemeModel(models.Model):
    title = models.CharField('Тема ассистента', max_length=256, null=True, blank=True)
    is_active = models.BooleanField("Тема активная?", default=True)

    class Meta:
        verbose_name = "Тема ассистента"
        verbose_name_plural = "Темы ассистента"

    def __str__(self):
        return self.title


class FilterConfig(models.Model):
    model_class = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=['model_class'])]

    def __str__(self):
        return self.model_class.name

    def get_model_class(self):
        return self.model_class.model_class()

    #Получить имена фильтров
    def get_available_filters(self, prev_filter={}):
        filters = self.get_model_class().filter_class.get_filters()

        available_filters = []
        for filter_name in filters.keys():
            if filter_name not in prev_filter:
                available_filters.append({
                    "filter_name": filter_name,
                    "name": filters[filter_name].label
                })



        return available_filters

    # Получить пункты выбора для поля
    def get_availabable_choices(self, filter_name, prev_filter={}):
        # Мы должны показывать только пункты, которые имееют предложения.

        if prev_filter:
            return self.get_model_class().objects.filter(**prev_filter).values_list(filter_name, flat=True).distinct()
        else:
            return self.get_model_class().objects.values_list(filter_name,flat=True).distinct()



class FilterFields(models.Model):
    config = models.ForeignKey(FilterConfig, verbose_name="Модель фильтрации", null=True, blank=False,
                               on_delete=models.CASCADE)
    field_name = models.CharField("Поле для фильтрации", max_length=50)
    message = RichTextField(verbose_name="Текст сообщения", null=True, blank=True)

    def __str__(self):
        return f'{self.field_name} - {self.message}'

    class Meta:
        verbose_name = "Фильтрация"

    def get_choices(self):
        model_class = self.config.get_model_class()
        filterset = model_class.filter_class.get_filters()

        choices = filterset[self.field_name].extra['choices']

        return choices


class ChatMessageModel(MP_Node):
    theme = models.ForeignKey(to=AssistentThemeModel, verbose_name="Тема", null=True, blank=False,
                              on_delete=models.SET_NULL)

    is_active = models.BooleanField(verbose_name="Ветка сообщения активна?", default=True)

    message = RichTextField(verbose_name="Текст сообщения", null=True, blank=False)

    is_filter_question = models.BooleanField("Вопрос на фильтрацию товаров", default=False)

    filter_model = models.OneToOneField(FilterConfig, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['theme']
        verbose_name = "Дерево сообщений чата"

    def __str__(self):
        return self.message or ''

    class Meta:
        verbose_name = "Сообщение ассистента"
        verbose_name_plural = "Сообщения ассистента"
