import re

from users.models import User

def replaceMention(val, user_list: list):
    u = re.sub(r'@', '', val.group())
    try:
        user = User.objects.get(username=u)
        if user:
            result = '<RouterLink :to="{name: `user-profile`, params: {username: \'' + u + '\'}}" :exact="true">@' + u + '</RouterLink>'
            user_list.append(user)
            return result
        else:
            return val
    except User.DoesNotExist:
        return r'{0}'.format(val.group())
    
def replaceLink(val):
    URL_REGEX = re.compile(r'((http|https)://[^\s]+)')

    return URL_REGEX.sub(r'<a target="_blank" href="\1">\1</a>', val)