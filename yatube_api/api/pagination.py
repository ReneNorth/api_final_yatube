from rest_framework.pagination import LimitOffsetPagination


class PostsPaginator(LimitOffsetPagination):
    page_size = 10
