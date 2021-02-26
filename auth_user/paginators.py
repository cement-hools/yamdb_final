from rest_framework.pagination import PageNumberPagination


class APIPagination(PageNumberPagination):
    """Паджинатор."""
    page_size = 10
