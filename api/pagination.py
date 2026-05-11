from typing import TypeVar, Generic, List
from pydantic import BaseModel
from django.db.models import QuerySet
from math import ceil

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    page: int
    page_size: int
    total_pages: int
    results: List[T]

def paginate(queryset: QuerySet, page: int, page_size: int) -> dict:
    count = queryset.count()
    total_pages = ceil(count / page_size) if page_size > 0 else 1
    
    start = (page - 1) * page_size
    end = start + page_size
    
    results = list(queryset[start:end])
    
    return {
        "count": count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "results": results
    }
