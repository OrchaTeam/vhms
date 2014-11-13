from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from apps.utils.urls import next_url

# {WORKAROUND: delete dependencies}
from mezzanine.conf.context_processors import settings as context_settings

def subject_template(template, context):
    """
    It was transferred from Mezzanine 3.1.9
    Loads and renders an email subject template, returning the
    subject string.
    """

    subject = loader.get_template(template).render(Context(context))
    return " ".join(subject.splitlines()).strip()

def send_mail_template(subject, template, addr_from, addr_to, context=None,
                       attachments=None, fail_silently=None, addr_bcc=None,
                       headers=None):
    """
    It was transferred from Mezzanine 3.1.9
    Send email rendering text and html versions for the specified
    template name using the context dictionary passed in.
    """

    if context is None:
        context = {}
    if attachments is None:
        attachments = []
    if fail_silently is None:
        fail_silently = settings.EMAIL_FAIL_SILENTLY
    # Add template accessible settings from Mezzanine to the context
    # (normally added by a context processor for HTTP requests)
    context.update(context_settings())
    # Allow for a single address to be passed in.
    # Python 3 strings have an __iter__ method, so the following hack
    # doesn't work: if not hasattr(addr_to, "__iter__"):
    if isinstance(addr_to, str) or isinstance(addr_to, bytes):
        addr_to = [addr_to]
    if addr_bcc is not None and (isinstance(addr_bcc, str) or
                                 isinstance(addr_bcc, bytes)):
        addr_bcc = [addr_bcc]
    # Loads a template passing in vars as context.
    render = lambda type: loader.get_template("%s.%s" %
                          (template, type)).render(Context(context))
    # Create and send email.
    msg = EmailMultiAlternatives(subject, render("txt"),
                                 addr_from, addr_to, addr_bcc,
                                 headers=headers)
    msg.attach_alternative(render("html"), "text/html")
    for attachment in attachments:
        msg.attach(*attachment)
    msg.send(fail_silently=fail_silently)

def send_verification_mail(request, user, verification_type):
    """
    It was transferred from Mezzanine 3.1.9
    Sends an email with a verification link to users when
    ``USER_VERIFICATION_REQUIRED`` is ```True`` and they're signing
    up, or when they reset a lost password.
    The ``verification_type`` arg is both the name of the urlpattern for
    the verification link, as well as the names of the email templates
    to use.
    """

    verify_url = reverse(verification_type, kwargs={
        "uidb36": int_to_base36(user.id),
        "token": default_token_generator.make_token(user),
    }) + "?next=" + (next_url(request) or "/")
    context = {
        "request": request,
        "user": user,
        "verify_url": verify_url,
    }
    subject_template_name = "email/%s_subject.txt" % verification_type
    subject = subject_template(subject_template_name, context)
    send_mail_template(subject, "email/%s" % verification_type,
                       settings.DEFAULT_FROM_EMAIL, user.email,
                       context=context)