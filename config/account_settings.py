LOGIN_URL = '/accounts/login/'

LOGOUT_URL = '/accounts/logout/'

LOGIN_REDIRECT_URL = '/'

ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = ("optional")

SOCIALACCOUNT_QUERY_EMAIL = False

SOCIALACCOUNT_EMAIL_REQUIRED = False

SOCIALACCOUNT_EMAIL_VERIFICATION = ("none")

#Email confirmation settings
EMAIL_USE_TLS = True

SERVER_EMAIL = 'orcha@user.z8.ru'

DEFAULT_FROM_EMAIL = 'orcha@user.z8.ru'

EMAIL_HOST = 'smtp.peterhost.ru'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'orcha_00'

EMAIL_HOST_PASSWORD = '9D3kIExyi5V'

# there are only profile fields, not user
ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "is_merchant",
    "related_profile",
    )