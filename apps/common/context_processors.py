def debug_mode(request):
    from django.conf import settings
    return {'debug_mode': settings.DEBUG}


def template_view_mode(request):
    print request
    
    return {}
