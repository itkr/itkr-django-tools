# -*- coding: utf-8 -*-
from django.db import models


class MasterModel(models.Model):

    class Meta:
        abstract=True
    
    @classmethod
    def get(cls, object_id):
        return cls.objects.get(id=object_id)
    
    @classmethod
    def get_all(cls):
        return cls.objects.all()


class CacheMasterModel(MasterModel):
    pass