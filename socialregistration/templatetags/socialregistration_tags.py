import re
from django import template
from django.conf import settings
from django.template import resolve_variable, Variable

register = template.Library()

@register.tag
def social_csrf_token(parser, token):
    """
    Wrapper around the ``{% csrf_token %}`` template tag to make socialregistration
    work with both Django v1.2 and Django < v1.2
    """
    return CsrfNode()
    
class CsrfNode(template.Node):
    def render(self, context):
        try:
            from django.template.defaulttags import CsrfTokenNode
            return CsrfTokenNode().render(context)
        except ImportError:
            return u''


@register.tag
def open_id_errors(parser, token):
    """
    Retrieve OpenID errors and the provider that caused them from session for display to the user.
    """

    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    request = m.groups()[0]
    return OpenIDErrorsNode(request)

class OpenIDErrorsNode(template.Node):
    def __init__(self, request):
        self.request = Variable(request)

    def render(self, context):
        request = self.request.resolve(context)
        context['openid_error'] = request.session.get('openid_error', False)
        context['openid_provider'] = request.session.get('openid_provider', '')

        # clear the error once it's been displayed once
        if request.session.get('openid_error', False):
            del request.session['openid_error']
        if request.session.get('openid_provider', False):
            del request.session['openid_provider']

        return u''


class AuthEnabledNode(template.Node):
    def __init__(self, network, var_name):
        self.network = network
        self.var_name = var_name

    def render(self, context):
        if self.network.lower().strip() == 'facebook':
            if getattr(settings, 'FACEBOOK_API_KEY', False) and getattr(settings, 'FACEBOOK_SECRET_KEY', False):
                context[self.var_name] = True
        elif self.network.lower().strip() == 'twitter':
            if getattr(settings, 'TWITTER_CONSUMER_KEY', False) and getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', False) and getattr(settings, 'TWITTER_REQUEST_TOKEN_URL', False) and getattr(settings, 'TWITTER_ACCESS_TOKEN_URL', False) and getattr(settings, 'TWITTER_AUTHORIZATION_URL', False):
                context[self.var_name] = True
        else:
            context[self.var_name] = False
        return u''

@register.tag
def auth_enabled(parser, token):
    """
    Determine whether or not the requested service is configured and their login buttons should be displayed.
    """

    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    network, var_name = m.groups()
    return AuthEnabledNode(network, var_name)
