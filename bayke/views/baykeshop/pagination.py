from bayke.pagination import PageNumberPagination
from bayke.conf import bayke_settings


class HomeFloorPagination(PageNumberPagination):
    
    page_size = bayke_settings.HOME_NAV_COUNT