from enum import Enum

class SortType(str, Enum):
    FEATURED = "featured"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"