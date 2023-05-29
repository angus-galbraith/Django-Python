from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="darts"),
    path("rtb/", views.rtb, name="rtb"),
    path("finishes/", views.finishes, name="finishes"),




]