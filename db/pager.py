# -*- coding: utf-8 -*-
from django.db import models


class _Pager(object):

    page_length = 20

    def __init__(self, cls, *args, **kwargs):
        page = 1
        self._filter = self._make_filter(cls, *args, **kwargs)
        self.count = self._get_count()
        self.data = self._get_data(page)
        self._update_information(page)

    def _make_filter(self, cls, *args, **kwargs):
        def _filter():
            return cls.objects.filter(*args, **kwargs)
        return _filter

    def _get_count(self):
        return self._filter().count()

    def _get_data(self, page):
        start = (page - 1) * self.page_length
        end = page * self.page_length
        return self._filter()[start:end]

    def _update_information(self, page):
        max_page = self.count / self.page_length
        if self.count % self.page_length:
            max_page += 1
        self.current_page = page
        self.prev_page = page - 1
        self.next_page = page + 1 if page < max_page else 0
        self.max_page = max_page

    def get_dict(self, page):
        self._update_information(page)
        return {
            "data": self._get_data(page),
            "current_page": self.current_page,
            "prev_page": self.prev_page,
            "next_page": self.next_page,
            "max_page": self.max_page,
        }


class PagerMixin(models.Model):
    """
    pager機能を追加する
    """

    class Meta:
        abstract = True

    @classmethod
    def get_pager(cls, *args, **kwargs):
        return _Pager(cls, *args, **kwargs)
