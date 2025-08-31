# posts/pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # Number of posts per page
    page_size_query_param = 'page_size'  # Allows client to set page size (e.g., ?page_size=20)
    max_page_size = 100 # Maximum page size allowed