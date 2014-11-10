from django.template.response import TemplateResponse
from django.template import RequestContext

def render(request, templates, dictionary=None, context_instance=None,
           **kwargs):
    """
    It was transferred from Mezzanine 3.1.9.
    Mimics ``django.shortcuts.render`` but uses a TemplateResponse for
    ``mezzanine.core.middleware.TemplateForDeviceMiddleware``
    """

    dictionary = dictionary or {}
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = RequestContext(request, dictionary)
    return TemplateResponse(request, templates, context_instance, **kwargs)