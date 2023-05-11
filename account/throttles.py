from rest_framework.throttling import AnonRateThrottle

class AccountsRateThrottle(AnonRateThrottle):
    scope = 'account'