from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from assistent_app.models import AssistentThemeModel, ChatMessageModel, FilterFields, FilterConfig


@admin.register(AssistentThemeModel)
class AssistentTheme(admin.ModelAdmin):
    pass


class FieldsFilterAdmin(admin.StackedInline):
    model = FilterFields


@admin.register(FilterConfig)
class FilterConfigModel(admin.ModelAdmin):
    inlines = [FieldsFilterAdmin]

@admin.register(ChatMessageModel)
class AssistPromptAdmin(TreeAdmin):
    change_form_template = 'change_form.html'
    list_display = ['message', 'theme', 'is_active']

    form = movenodeform_factory(ChatMessageModel)
