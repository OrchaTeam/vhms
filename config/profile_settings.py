# auth backend param for customization user profile
VHMS_PROFILE_USER_MODEL = 'apps.profiles Profile'

# replaced from account_settings
LOGIN_URL = '/accounts/login/'

# replaced from account_settings
LOGOUT_URL = '/accounts/logout/'

SIGNUP_URL = '/accounts/signup/'

# replaced from account_settings
LOGIN_REDIRECT_URL = '/'

# VHMSUserBaseForm
USER_BLACKLIST = (
    "huy",
)

# VHMSUserSignupForm
USER_MIN_PASSWORD_LENGTH = 6

# VHMSUserSignupView
USER_VERIFICATION_REQUIRED = True