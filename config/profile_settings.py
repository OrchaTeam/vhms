AUTH_PROFILE_MODULE = "profiles.Profile"

ACCOUNTS_PROFILE_FORM_CLASS = "apps.profiles.forms.VHMSProfileForm"

VHMS_SIGNUP_FORM_EXCLUDE_FIELDS = (
    "type",
    "is_merchant",
    "related_profile",
    "user",
    "birthday",
    )

# Exclude profile form
ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "is_merchant",
    "related_profile",
)
