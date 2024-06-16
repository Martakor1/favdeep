from django.urls import path

from .views import ChadGPTAPIView, ChadGPTFiltreCategoryView

urlpatterns = [
    path('ask/', ChadGPTAPIView.as_view(), name='ask-chadgpt'),
    path('ask/category/', ChadGPTFiltreCategoryView.as_view(), name='ask-chadgpt-filter-category'),
]
