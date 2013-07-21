# -*- coding: utf-8 -*-
from django.db import models


class DateTimeFieldMixin(models.Model):
    """
    作成日付・更新日付のフィールドを追加するMixin
    日付の更新は自動
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)