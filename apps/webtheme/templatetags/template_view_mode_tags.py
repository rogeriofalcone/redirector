from django import template
 
from webtheme.conf.settings import TEMPLATE_VIEW_MODES
from webtheme.models import SiteSkin
from webtheme.literals import TEMPLATE_VIEW_MODE_FULL, \
    TEMPLATE_VIEW_MODE_PLAIN
 
register = template.Library()

'''
class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        #context[self.var_name] = value
        # Global context varialbe, accesble from outside it's own block
        context.dicts[0][self.var_name] = value
        print context

        return u''
        
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
'''

#register.tag('set', set_var)

class TemplateViewModeNode(template.Node):
 
    #def __init__(self, template_id):
    #    self.template_id = template_id
 
    def render(self, context):
        try:
            print context
            template_id = template.Variable('template_id').resolve(context)
            mode = TEMPLATE_VIEW_MODES.get(SiteSkin.objects.get_current_skin(), {}).get(template_id, TEMPLATE_VIEW_MODE_FULL)
        except template.VariableDoesNotExist:
            mode = ''

        #context[self.var_name] = value
        context['template_view_mode'] = mode
        # Global context varialbe, accesble from outside it's own block
        #context.dicts[0][self.var_name] = value
        return u''

@register.tag
def template_view_mode(parser, token):
    return TemplateViewModeNode()
