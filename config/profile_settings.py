AUTH_PROFILE_MODULE = "profiles.Profile"

ACCOUNTS_PROFILE_FORM_CLASS = "apps.profiles.forms.VHMSProfileForm"

ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "is_merchant",
    "related_profile",
    "profiletype",
    "first_name",
    "last_name",
    )

VHMS_SIGNUP_PROFILE_FIELDS = (
    "first_name",
    "last_name",
    )

VHMS_PROFILE_PROFILE_FIELDS = (
    "first_name",
    "last_name",
    "avatar",
    )

# VHMSUserBaseForm
USER_BLACKLIST = (
    "huy",
)

# VHMSUserSignupForm
USER_MIN_PASSWORD_LENGTH = 6

# VHMSUserSignupView
USER_VERIFICATION_REQUIRED = True