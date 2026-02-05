from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("setup/", views.profile_setup, name="profile_setup"),
    path("budget/", views.budget, name="budget"),
    path("goals/", views.goals, name="goals"),
    path("resources/", views.resources, name="resources"),
    path("tracker/", views.tracker, name="tracker"),
    path("timeline/", views.timeline, name="timeline"),

]