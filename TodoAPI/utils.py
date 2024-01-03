import base64
from functools import wraps
from rest_framework import permissions
from random import randint
from django.http import JsonResponse
from django.db import models
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.request import Request
from rest_framework import status
import urllib


class GenericPagination:
    def __init__(self) -> None:
        self.result = {
            "data": [],
            "per_page": 25,
            "pages": 0,
            "page": 0,
            "total": 0,
        }

    def generate_response(
        self,
        page: int,
        per_page: int,
        qry,
        serializer,
        many: bool,
        req_filter=[],
        req_order=[],
    ):

        self.result["page"] = page
        self.result["per_page"] = per_page

        if qry:
            paginator = Paginator(qry, per_page)
            data = serializer(paginator.page(page).object_list, many=many)

            self.result["pages"] = paginator.num_pages
            self.result["total"] = paginator.count
            self.result["data"] = data.data
            self.result["order"] = req_order
            self.result["filter"] = req_filter

        return self.result


class GenericSimpleApiView(APIView):

    PAGE = 1
    PER_PAGE = 10
    FILTERS = []
    ORDER_BY = []

    def get_paginator_vars(self, request: Request):

        try:
            page = int(request.query_params.get("page", 1))
            self.PAGE = page if page > 1 else 1
        except Exception:
            self.PAGE = 1

        self.FILTERS = request.query_params.getlist("filters", None)
        self.ORDER_BY = request.query_params.getlist("order_by", None)

        try:
            per_page = int(request.query_params["per_page"])
            self.PER_PAGE = (
                per_page if per_page > 0 and per_page <= 30 else self.PER_PAGE
            )
        except Exception:
            self.PER_PAGE = self.PER_PAGE

    def _list_with_pagination(
        self,
        request: Request,
        serializer,
        qry,
        ExceptDoesNotExist,
        pk: int = None,
        qry_params: dict = None,
        many=False,
    ):

        if pk:
            try:
                qry_params["pk"] = pk
                qry = qry(**qry_params)
                body = serializer(qry)
                return JsonResponse(data=body.data, status=status.HTTP_200_OK)
            except ExceptDoesNotExist:
                return JsonResponse(data={}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise e
        else:

            self.get_paginator_vars(request=request)

            qry = qry(**qry_params)
            qry = qry.order_by(*self.ORDER_BY)
            pagination = GenericPagination()
            data = pagination.generate_response(
                page=self.PAGE,
                per_page=self.PER_PAGE,
                qry=qry,
                serializer=serializer,
                many=many,
                req_filter=self.FILTERS,
                req_order=self.ORDER_BY,
            )

            return JsonResponse(data=data, status=status.HTTP_200_OK)


def random_password(total=10, special: bool = True):

    symbols = "!@#abcdefghijklmnoprstuvxywz0123456789ABCDEFGHIJKLMNOPRSTUVXYWZ"
    if special is False:
        symbols = "abcdefghijklmnoprstuvxywz0123456789ABCDEFGHIJKLMNOPRSTUVXYWZ"
    password = ""
    for i in range(total):
        password += symbols[randint(0, len(symbols) - 1)]

    return password


def add_order_filter(model, qry, filters=[], order_by=[]):

    fields = [field.name for field in model._meta.get_fields()]

    for field in order_by:
        field_name = field
        if field[0:1] == "-":
            field_name = field[1:]

        if field_name in fields:
            qry = qry.order_by(field)

    if filters and type(filters) == list:
        for filter in filters:
            try:
                decoded = urllib.parse.unquote(filter)
                field = decoded.split("=")
                if len(field) == 2:
                    if field[0] in fields:
                        res = {f"{field[0]}__icontains": field[1]}
                        if field[0] == "user":
                            res = {f"{field[0]}": field[1]}

                        qry = qry.filter(**res)
            except Exception as e:
                print(e)

    return qry
