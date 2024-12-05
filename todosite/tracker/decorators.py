from django.contrib.auth.decorators import user_passes_test





def check_user_is_authenticated(user):
    return not user.is_authenticated

user_logout_required = user_passes_test(check_user_is_authenticated, '/', None)

def user_should_not_access(funcview):
    return user_logout_required(funcview)



