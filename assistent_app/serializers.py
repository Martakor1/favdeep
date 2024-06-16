from rest_framework import serializers

from assistent_app.models import ChatMessageModel


class AssistentSerializer(serializers.Serializer):
    theme = serializers.BooleanField(label="Показывать темы", required=False)

    theme_id = serializers.IntegerField(label="Выбранная тема", required=False)

    answer_id = serializers.IntegerField(label="Выбранный ответ", required=False)

    class Meta:
        fields = ['theme', 'theme_id', 'answer_id']


class FetchFilterSerializer(serializers.Serializer):
    answer = serializers.PrimaryKeyRelatedField(queryset=ChatMessageModel.objects.all(),
                                                   required=True,label="Вопрос с которога началась фильтрация")
    prev_filters = serializers.JSONField(label="Предыдущие фильтры", required=True)

    class Meta:
        fields = ['answer','prev_filters']

class FetchChoiceSerializer(serializers.Serializer):
    answer = serializers.PrimaryKeyRelatedField(queryset=ChatMessageModel.objects.all(),
                                                required=True, label="Вопрос с которога началась фильтрация")
    prev_filters = serializers.JSONField(label="Предыдущие фильтры", required=True)

    filter_name = serializers.CharField(label="Название фильтра",required=True)

    class Meta:
        fields = ['answer','prev_filters']

class ApplyFilterSerializer(serializers.Serializer):
    answer = serializers.PrimaryKeyRelatedField(queryset=ChatMessageModel.objects.all(),
                                                required=True, label="Вопрос с которога началась фильтрация")
    filters = serializers.JSONField(label="фильтры", required=True)

    class Meta:
        fields = ['answer','filters']
