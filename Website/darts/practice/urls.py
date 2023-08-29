from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="darts"),
    path("rtbstart", views.rtbstart, name="rtb"),
    path("rtb/", views.rtb, name="rtb"),
    path("finishesstart", views.finishesstart, name="finishesstart"),
    path("finishes/", views.finishes, name="finishes"),
    path("highscores", views.highscores, name="highscores")




]