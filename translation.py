# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from cabinet.models import LitWork


class LitWorkTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели LitWork.
    """

    fields = ('name', 'description',)


translator.register(LitWork, LitWorkTranslationOptions)