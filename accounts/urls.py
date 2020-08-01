from django.urls import path, include

from accounts.views import (
    alumni_signup_view,
    faculty_signup_view,
    logout_view,
    login_view,
    signup_view,
    complete_alumni_profile,
    complete_faculty_profile,
    update_alumni_profile,
    verify,
)

app_name = "accounts"


urlpatterns = [
    path(
        "complete_faculty_profile/",
        complete_faculty_profile,
        name="complete_faculty_profile",
    ),
    path(
        "complete_alumni_profile/",
        complete_alumni_profile,
        name="complete_alumni_profile",
    ),
    path("signup/alumni/", alumni_signup_view.as_view(), name="alumni_signup_view"),
    path("signup/faculty/", faculty_signup_view.as_view(), name="faculty_signup_view"),
    path("profile/edit", update_alumni_profile, name="update_alumni_profile"),
    path("signup/", signup_view, name="signup_view"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("verify", verify, name="verify"),
]
