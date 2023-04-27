#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :pagination.py
@说明    :分页组件
@时间    :2023/04/22 16:09:59
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination


class PageNumberPagination(BasePageNumberPagination):
    """ 分页类扩展 """
    page_size = 20
    
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current'] = int(self.request.query_params.get(self.page_query_param, 1))
        return response
    
    def get_query_params(self):
        params = []
        query = self.request.query_params.dict()
        try:
            query.pop(self.page_query_param)
        except KeyError:
            pass
        for k, v in query.items():
            if f"{k}={v}" not in params:
                params.append(f"{k}={v}")
        params = '&'.join(params)
        return params
    
    def get_next_link(self):
        next = super().get_next_link()
        if self.get_query_params() and next:
            next += f"&{self.get_query_params()}"
        return next
    
    def get_previous_link(self):
        previous = super().get_previous_link()
        if self.get_query_params() and previous:
            previous += f"&{self.get_query_params()}"
        return previous