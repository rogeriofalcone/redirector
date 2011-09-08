from webtheme.models import SiteSkin

def current_skin(request):
    skin = SiteSkin.objects.get_current_skin()
    return {'current_skin': skin}
