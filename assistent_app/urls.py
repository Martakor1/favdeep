from django.urls import path

from .views import *

urlpatterns = [
    path('get_filters', FetchFilterAPIView.as_view()),
    path('get_choices', FetchChooseFilterAPIView.as_view()),
    path('apply_filter', ApplyFilterAPIView.as_view()),

    path('', AssistentTreeAPIView.as_view()),
]