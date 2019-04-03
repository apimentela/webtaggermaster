from django import template
register = template.Library()
@register.filter(name='smooth_timedelta')
def smooth_timedelta(secs):
    timetot = ""
    if secs > 86400: # 60sec * 60min * 24hrs
        days = secs // 86400
        timetot += "{} dias".format(int(days))
        secs = secs - days*86400
    if secs > 3600:
        hrs = secs // 3600
        timetot += " {} horas".format(int(hrs))
        secs = secs - hrs*3600
    if secs > 60:
        mins = secs // 60
        timetot += " {} minutos".format(int(mins))
        secs = secs - mins*60
    if secs > 0:
        timetot += " {} segundos".format(int(secs))
    return timetot
