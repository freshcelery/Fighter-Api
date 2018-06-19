from rest_framework.pagination import LimitOffsetPagination

class LimitOffsetPaginationWithMaximumLimit(LimitOffsetPagination):
    max_limit = 10