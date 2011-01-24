from django import template
from django.conf import settings
from socialregistration.models import TwitterProfile

register = template.Library()

@register.inclusion_tag('socialregistration/twitter_button.html', takes_context=True)
def twitter_button(context):
    if not 'request' in context:
        raise AttributeError, 'Please add the ``django.core.context_processors.request`` context processors to your settings.TEMPLATE_CONTEXT_PROCESSORS set'
    logged_in = context['request'].user.is_authenticated()
    if 'next' in context:
        next = context['next']
    else:
        next = None

    if 'socialregistration_connect_object' in context:
        # need to use this info to pass a GET parameter to the redirect so the object can be used when the user comes back
        obj = context['socialregistration_connect_object']
        cobj = {'app_label': obj._meta.app_label, 'model': obj._meta.module_name, 'key': obj.pk}
    else:
        cobj = {}

    return dict(next=next, logged_in=logged_in, MEDIA_URL=getattr(settings, 'MEDIA_URL', ''), STATIC_MEDIA_URL=getattr(settings, 'STATIC_MEDIA_URL', ''), content_object=cobj)

class TwitterInfoNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        # if the object is required, look for a Twitter account for it.
        if 'socialregistration_connect_object' in context:
            cobj = context['socialregistration_connect_object']
        # if not, check for the current user and make sure they're logged in and not anonymous
        else:
            cobj = context['request'].user
            if not cobj.is_authenticated():
                context[self.var_name] = None
                return ''

        try:
            profile = TwitterProfile.objects.for_object(cobj)
            context[self.var_name] = profile
            return ''
        except TwitterProfile.DoesNotExist:
            context[self.var_name] = None
            return ''

@register.tag
def twitter_info(parser, token):
    """
    Usage: {% twitter_info as tw %} Returns their Twitter Profile.
    """
    try:
        tag_info = token.split_contents()
        if len(tag_info) == 3:
            var_name = tag_info[2]
            return TwitterInfoNode(var_name)
        else:
            raise template.TemplateSyntaxError, "%r tag takes arguments." % token.contents.split()[0]
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag takes arguments." % token.contents.split()[0]
