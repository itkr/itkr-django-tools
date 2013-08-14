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


class UserHasManyModelMixin(models.Model):

    class Meta:
        abstract = True

    user_id = models.IntegerField()

    @classmethod
    def get_by_user_id(cls, user_id):
        return list(cls.objects.filter(user_id=user_id))


class GroupHasManyModelMixin(models.Model):

    class Meta:
        abstract = True

    group_id = models.IntegerField()

    @classmethod
    def get_by_group_id(cls, group_id):
        return list(cls.objects.filter(group_id=group_id))


class UserHasOneModelMixin(models.Model):

    class Meta:
        abstract = True

    user_id = models.IntegerField()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.objects.get(user_id=user_id)


class GroupHasOneModelMixin(models.Model):

    class Meta:
        abstract = True

    user_id = models.IntegerField()

    @classmethod
    def get_by_group_id(cls, group_id):
        return cls.objects.get(group_id=group_id)











