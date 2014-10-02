# -*- coding: utf-8 -*-
from django.db import models


class LogicalDeleteMixin(models.Model):
    """
    logical delete
    とりあえず仮
    """

    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True)
    deleted_uuid = models.CharField(null=True)

    def delete(self):
        # TODO: ここの実装
        super(LogicalDeleteMixin, self).delete()
