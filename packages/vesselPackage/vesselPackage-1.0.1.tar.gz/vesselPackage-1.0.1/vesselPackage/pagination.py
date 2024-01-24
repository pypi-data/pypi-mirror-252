from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data,page=None, elipse=None):

        if page is None or elipse is None:
            return super().get_paginated_response(data)
        
        return Response({
            'next': self.get_next_link(),
            "next_page_number": self.page.next_page_number() if self.page.has_next() else None,
            'previous': self.get_previous_link(),
             "previous_page_number": self.page.previous_page_number() if self.page.has_previous() else None,
            'count': self.page.paginator.count,
            "page":page,
            "elipse":elipse,
            'results': data
        })