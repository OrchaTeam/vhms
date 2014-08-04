AUTH_PROFILE_MODULE = "profiles.Profile"

ACCOUNTS_PROFILE_FORM_CLASS = "apps.profiles.forms.VHMSProfileForm"

# VHMS variables

# there are only profile fields, not user
VHMS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "related_profile",
    )