from rest_framework.throttling import AnonRateThrottle


class CourseRateThrottle(AnonRateThrottle):
    scope = 'course'
