from rest_framework.throttling import UserRateThrottle


class IPThrottle(UserRateThrottle):
    rate = '5/min'

