# -*- coding:utf-8 -*-


class DynamoDBModelError(StandardError):
    pass


class DynamoDBIntegrityError(DynamoDBModelError):
    pass
