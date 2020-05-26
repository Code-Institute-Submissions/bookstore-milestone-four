from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("thanks/<int:order_id>", views.thanks, name="thanks"),
    path("<int:order_id>/", views.viewOrder, name="order_details"),
]
