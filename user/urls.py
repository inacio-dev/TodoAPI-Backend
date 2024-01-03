from django.urls import path

from user.views import (
    AccountView,
    AccountCheckView
)

urlpatterns = [
    path("", AccountView.as_view(), name="accounts_list"),
    path("check/", AccountCheckView.as_view(), name="account_check"),
]