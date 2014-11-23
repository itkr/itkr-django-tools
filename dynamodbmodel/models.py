# -*- coding:utf-8 -*-
from django.conf import settings
try:
    import dynamodb
    from boto.dynamodb2.table import Table
except ImportError:
    print "Install boto"

from .fields import DynamoDBField
from .exceptions import (
    DynamoDBModelError,
    DynamoDBIntegrityError,
)


class DynamoDBModel(object):

    """
    DynamoDBを扱う
    """

    class _Field(dict):
        __getattr__ = dict.__getitem__

    def __init__(self):
        self._connection = dynamodb.connect()
        self._table = Table(
            self._get_table_name(), connection=self._connection)

    @property
    def fields(self):

        """
        継承先で指定されたフィールド一覧
        """

        if not hasattr(self, "_fields"):
            self._fields = self._get_fields()
        return self._fields

    def _get_fields(self):

        """
        継承先で指定されたフィールド一覧を取得する

        :rtype _Field
        """

        fields = self._Field()
        items = self.__class__.__dict__.items()
        for k, v in items:
            if isinstance(v, DynamoDBField):
                fields[k] = v
        return fields

    def _get_table_name(self):

        """
        継承先で指定されたテーブル名を元に実際のテーブル名を返す
        （開発用ではsandbox sufixをつける）

        :rtype str
        """

        if settings.DEBUG:
            return "_".join([self.table_name, "sandbox"])
        return self.table_name

    def _check_data(self, data):

        """
        dictで与えられたデータとモデルのフィールドとの整合性がとれていることをチェックする

        :type data: dict
        :rtype None
        """

        field_keys = self.fields.keys()
        for k, v in data.items():
            # 存在しないフィールド
            if k not in field_keys:
                raise DynamoDBModelError(
                    "{} '{}' field is not specified".format(
                        self.__class__.__name__, k))
            # 空要素チェック
            if self.fields.get(k).null == False:
                if v is None or v == "":
                    raise DynamoDBModelError(
                        "{} '{}' value must not be empty".format(
                            self.__class__.__name__, k))

        data_keys = data.keys()
        for k, v in self.fields.items():
            # 必要なフィールドに対するキーが無い
            if not v.null and k not in data_keys:
                raise DynamoDBModelError(
                        "{} '{}' value must not be empty".format(
                            self.__class__.__name__, k))
            # 重複
            if v.unique:
                if self._table.has_item(**{k: data[k]}):
                    raise DynamoDBIntegrityError(
                        "{} key:'{}'".format(self.__class__.__name__, k))

    def get(self, **kwargs):
        return self._table.get_item(**kwargs)

    def put(self, **kwargs):
        self._check_data(kwargs)
        return self._table.put_item(kwargs, overwrite=False)
