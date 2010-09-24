from django import template
from django.conf import settings
from socialregistration.utils import _https

register = template.Library()

@register.inclusion_tag('socialregistration/facebook_js.html')
def facebook_js(requested_perms=""):
    return {'facebook_api_key' : getattr(settings, 'FACEBOOK_API_KEY', ''), 'is_https' : bool(_https()), 'requested_perms': requested_perms, 'MEDIA_URL': getattr(settings, 'MEDIA_URL', ''), 'STATIC_MEDIA_URL': getattr(settings, 'STATIC_MEDIA_URL', '')}

@register.inclusion_tag('socialregistration/facebook_button.html', takes_context=True)
def facebook_button(context):
    if not 'request' in context:
        raise AttributeError, 'Please add the ``django.core.context_processors.request`` context processors to your settings.TEMPLATE_CONTEXT_PROCESSORS set'
    logged_in = context['request'].user.is_authenticated()
    if 'next' in context:
        next = context['next']
    else:
        next = None

    if 'content_object' in context:
        # need to use this info to pass a GET parameter to the redirect so the object can be used when the user comes back
        obj = context['content_object']
        cobj = {'app_label': obj._meta.app_label, 'model': obj._meta.module_name, 'key': obj.pk}
    else:
        cobj = {}

    return dict(next=next, logged_in=logged_in, MEDIA_URL=getattr(settings, 'MEDIA_URL', ''), STATIC_MEDIA_URL=getattr(settings, 'STATIC_MEDIA_URL', ''), content_object=cobj)
