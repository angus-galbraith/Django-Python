from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="darts"),
    path("rtbstart", views.rtbstart, name="rtb"),
    path("rtb/", views.rtb, name="rtb"),
    path("rtbover", views.rtbover, name="rtbover"),
    path("finishes/", views.finishes, name="finishes"),
    path("highscores", views.highscores, name="highscores")




]