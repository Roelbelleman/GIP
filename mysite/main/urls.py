from django.conf.urls import handler500, handler404, handler403
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("scanIDs", views.scanIDs, name="scanIDs"),
    path("home", views.home, name="home"),
    path("scanningIDs", views.scanningIDs, name="scanningIDs"),
    path("makebagpack", views.makebagpack, name="makebagpack"),
    path("makebagpackDoneV", views.makebagpackDoneV, name="makebagpackDoneV"),
    path("Loguot", views.Loguot, name="Loguot"),
    path("chageKeys", views.chageKeys, name="chageKeys"),
    path("verwijderVak/<str:vak>", views.verwijderVak, name="verwijderVak"),
    path("voegToe/<str:vak>", views.voegToe, name="voegToe"),
]

handler500 = 'main.views.custom_error_view'
handler404 = 'main.views.custom_error_view'
handler403 = 'main.views.custom_error_view'
