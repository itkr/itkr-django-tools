# -*- coding:utf-8 -*-
from datetime import timedelta
from django.conf import settings
try:
    from elasticsearch import Elasticsearch
except ImportError:
    print "Install 'elasticsearch'"


class ElasticsearchModel(object):

    """
    Elasticsearcを扱う
    """

    @classmethod
    def _target_indices(
        cls, index_name_format, timestamp_from, timestamp_to):

        """
        検索開始日時から、検索対象indexを決める
        :type timestamp_from: datetime.datetime
        :type timestamp_to: datetime.datetime
        :rtype: list of str
        """

        delta = timestamp_to - timestamp_from
        delta_days = delta.days + 1

        ret = []
        for i in xrange(delta_days):
            a = timestamp_to - timedelta(days=i)
            ret.append(index_name_format.format(a.year, a.month, a.day))
        return ret

    @classmethod
    def _search(cls, target_indices, query):
        es = Elasticsearch([{
            'host': settings.ELASTICSEARCH['HOST'],
            'port': settings.ELASTICSEARCH['PORT'],
        }])
        data = es.search(
            index=target_indices,
            body=query,
        )
        return data

    @classmethod
    def _query(cls):
        raise NotImplementedError

    @classmethod
    def get(cls, date_start_at, date_end_at, **kwargs):
        target_indices = cls._target_indices(
            cls.index_name_format, date_start_at, date_end_at)
        query = cls._query(**kwargs)

        data = cls._search(target_indices, query)

        return [cls(o['_source']) for o in data['hits']['hits']]
