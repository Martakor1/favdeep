from django.shortcuts import render, get_object_or_404
from rest_framework import generics, serializers, decorators
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from assistent_app.models import AssistentThemeModel, ChatMessageModel, FilterConfig, FilterFields
from assistent_app.serializers import *
from assistent_app.services import FactoryState, ShowAvailableFilters, ShowAvailableChoices, ApplyFilter
from authentication import serializer
from core.serializers import get_serializer_for_model


class FilterSuggestionSerializer(serializers.Serializer):
    config = serializers.PrimaryKeyRelatedField(queryset=FilterConfig.objects.all(), required=True, label="id вопроса")
    filters = serializers.JSONField(label="Фильтры", required=True)

    class Meta:
        fields = ['send_id', 'filters']


# Create your views here.
class AssistentTreeAPIView(generics.GenericAPIView):
    '''Диалог по дереву. У нас есть 3 поля и 3 возможных состояния чата.
    Сначала клиент должен запросить у нас возможные темы, для этого мы передаем один параметр theme со значением true.
    Когда пользователь выбрал тему, мы должны запросить первые сообщения, для этого мы отдаем одно поле theme_id с id темы.
    Дальнейшие наши действия зависят от параметря is_filter_question. Если is_filter_question=True, то мы делаем запрос на get_filters,
    чтобы получить фильтры объекта (см. get_filters, get_choice, apply_filters,
    иначе на api/ai с параметром answer_id (если он есть) и дальше весь диалог будет основан на answer_id'''
    queryset = ChatMessageModel.objects.all()

    serializer_class = AssistentSerializer

    def post(self, request, *args, **kwargs):
        chat_option = FactoryState.create_chat_option(request)

        result = chat_option.result()

        return Response(data=result, status=200)


class FetchFilterAPIView(GenericAPIView):
    '''Получить доступные поля фильтрации'''
    queryset = ChatMessageModel.objects.all()

    serializer_class = FetchFilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = ShowAvailableFilters.get_available_filters(
            answer=serializer.validated_data['answer'],
            prev_filters=serializer.validated_data['prev_filters']
        )

        return Response(status=200, data=data)


class FetchChooseFilterAPIView(GenericAPIView):
    '''Получить пункты выбора для фильтра'''
    queryset = ChatMessageModel.objects.all()
    serializer_class = FetchChoiceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = ShowAvailableChoices.get_available_choices(
            answer=serializer.validated_data['answer'],
            prev_filters=serializer.validated_data['prev_filters'],
            filter_name=serializer.validated_data['filter_name']
        )

        return Response(data=data,status=200)


class ApplyFilterAPIView(GenericAPIView):
    queryset = ChatMessageModel.objects.all()
    serializer_class = ApplyFilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        qs = ApplyFilter.filter(
            answer=serializer.validated_data['answer'],
            filters=serializer.validated_data['filters'],
        )

        model_class = serializer.validated_data['answer'].filter_model.get_model_class()

        return Response(data={
            "count": qs.count(),
            "top_10": get_serializer_for_model(model_class)(instance=qs[:10],many=True).data
        }, status=200)
