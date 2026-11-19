from rest_framework.pagination import PageNumberPagination


class PageSize20Pagination(PageNumberPagination):
    page_size = 20


def paginated_response(queryset, serializer_class, request):
    paginator = PageSize20Pagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(page, many=True)
    return paginator.get_paginated_response(serializer.data)
