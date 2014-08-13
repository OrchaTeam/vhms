AUTH_PROFILE_MODULE = "profiles.Profile"

ACCOUNTS_PROFILE_FORM_CLASS = "apps.profiles.forms.VHMSProfileForm"

ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "is_merchant",
    "related_profile",
    "profiletype",
    )

VHMS_SIGNUP_USER_FIELDS = (
    "username",
    "email",
    )

VHMS_PROFILE_USER_FIELDS = (
    "username",
    "email",
    )

VHMS_SIGNUP_PROFILE_FIELDS = (
    "first_name",
    "last_name",
    )

VHMS_PROFILE_PROFILE_FIELDS = (
    "first_name",
    "last_name",
    )