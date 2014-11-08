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

#Используется в VHMSUserBaseForm
USERNAME_BLACKLIST = ("huy",

)

#Используется в VHMSUserSignupForm
ACCOUNTS_MIN_PASSWORD_LENGTH = 6

ACCOUNTS_APPROVAL_REQUIRED = True