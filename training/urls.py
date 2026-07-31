from django.urls import path

from . import views

app_name = "training"

urlpatterns = [
    path("", views.ClassListView.as_view(), name="class_list"),
    path("schedule/", views.ScheduleView.as_view(), name="schedule"),
    path("pricing/", views.PricingView.as_view(), name="pricing"),
    path("<slug:slug>/", views.ClassDetailView.as_view(), name="class_detail"),
]
