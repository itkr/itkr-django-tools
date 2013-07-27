# -*- coding: utf-8 -*-
from django.db import models


class DateTimeFieldMixin(models.Model):
    """
    Mixin which adds the field of creation date and update date
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)