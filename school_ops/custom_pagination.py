import typing
from django.db.models import QuerySet
from rest_framework import serializers


class Pagination:

    def get_paginated_response(
        self, queryset: QuerySet, offset: int, limit: int,
            Serializer: serializers.Serializer) -> typing.Tuple[
                dict, bool]:
        try:
            offset = int(offset)
            previous_limit = int(limit)
        except ValueError:
            raise serializers.ValidationError({
                "result": False,
                "msg": "limit or offset should be numbers"},
                code="validation_error",
            )
        try:
            limit = offset+previous_limit+1
            queryset_data = queryset[int(offset):limit]
            serializer_data = Serializer(queryset_data, many=True)
        except IndexError as e:
            raise serializers.ValidationError(str(e))
        if len(queryset_data) > previous_limit:
            next_link = True
            serialized_data = serializer_data.data[:-1]
        else:
            next_link = False
            serialized_data = serializer_data.data
        return serialized_data, next_link
