"""
Provides features for non-staff user accounts, such as login, signup
with optional email verification, password reset, and integration
with user profiles models defined by the ``AUTH_PROFILE_MODULE``
setting. Some utility functions for probing the profile model are
included below.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from mezzanine.utils.models import get_user_model, get_model
from mezzanine.utils.importing import import_dotted_path


class ProfileNotConfigured(Exception):
    pass


def get_profile_model():
    """
    Returns the Mezzanine profile model, defined in
    ``settings.AUTH_PROFILE_MODULE``, or ``None`` if no profile
    model is configured.
    """

    if not getattr(settings, "AUTH_PROFILE_MODULE", None):
        raise ProfileNotConfigured

    try:
        return get_model(settings.AUTH_PROFILE_MODULE)
    except ValueError:
        raise ImproperlyConfigured("AUTH_PROFILE_MODULE must be of "
                                   "the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured("AUTH_PROFILE_MODULE refers to "
                                   "model '%s' that has not been installed"
                                   % settings.AUTH_PROFILE_MODULE)


def get_profile_for_user(user):
    """
    Returns site-specific profile for this user. Raises
    ``ProfileNotConfigured`` if ``settings.AUTH_PROFILE_MODULE`` is not
    set, and ``ImproperlyConfigured`` if the corresponding model can't
    be found.
    """
    if not hasattr(user, '_mezzanine_profile'):
        # Raises ProfileNotConfigured if not bool(AUTH_PROFILE_MODULE)
        profile_model = get_profile_model()
        profile_manager = profile_model._default_manager.using(user._state.db)

        user_field = get_profile_user_fieldname(profile_model, user.__class__)
        profile, created = profile_manager.get_or_create(**{user_field: user})

        profile.user = user
        user._mezzanine_profile = profile

    return user._mezzanine_profile


def get_profile_form():
    """
    Returns the profile form defined by
    ``settings.ACCOUNTS_PROFILE_FORM_CLASS``.
    """
    from mezzanine.conf import settings
    try:
        return import_dotted_path(settings.ACCOUNTS_PROFILE_FORM_CLASS)
    except ImportError:
        raise ImproperlyConfigured("Value for ACCOUNTS_PROFILE_FORM_CLASS "
                                   "could not be imported: %s" %
                                   settings.ACCOUNTS_PROFILE_FORM_CLASS)


def get_profile_user_fieldname(profile_model=None, user_model=None):
    """
    Returns the name of the first field on the profile model that
    points to the ``auth.User`` model.
    """
    Profile = profile_model or get_profile_model()
    User = user_model or get_user_model()
    for field in Profile._meta.fields:
        if field.rel and field.rel.to == User:
            return field.name
    raise ImproperlyConfigured("Value for AUTH_PROFILE_MODULE does not "
                               "contain a ForeignKey field for auth.User: %s"
                               % Profile.__name__)
