# -*- coding:utf-8 -*-


class DynamoDBField(object):
    def __init__(self, **kwargs):
        self.unique = kwargs.get('unique') or False
        self.null = kwargs.get('null') or False


class DynamoDBStringField(DynamoDBField):
    pass
