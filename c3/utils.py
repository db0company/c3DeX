from django.conf import settings as django_settings

def getCachedCCC(id):
    return django_settings.CCCS.get(id, {})

def getAttendedCCCsFromSession(request):
    if not request or not request.user.is_authenticated():
        return []
    if 'attended_cccs' not in request.session:
        request.session['attended_cccs'] = u','.join([
            str(pk) for pk in request.user.accounts.values_list('ccc_id', flat=True)])
    return [int(pk) for pk in request.session['attended_cccs'].split(',')]
