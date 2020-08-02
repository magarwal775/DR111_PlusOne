from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def alumni_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a alumni,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_alumni,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def faculty_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_faculty,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def verify_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/verify'):
    decorator = user_passes_test(
        lambda u: (u.is_verified and u.is_active) or u.is_superuser,
        login_url = login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return decorator(function)
    return decorator
