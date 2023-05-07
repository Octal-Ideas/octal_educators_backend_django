# Importing LimitOffsetPagination class from rest_framework.pagination module.
from rest_framework.pagination import (
    LimitOffsetPagination,
)

# Creating our own custom pagination class (PostLimitOffsetPagination) for controlling number of items to be displayed per page.
class CourseLimitOffsetPagination(LimitOffsetPagination):
    # Default limit for the pagination(in case it is not specified).
    default_limit = 10
    # Maximum limit that can be applied (for example, if it is set to 10 then user can't request more than 10 items at a time).
    max_limit = 10