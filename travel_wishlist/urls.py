from django.urls import path
from . import views

urlpatterns = [
    # connects to the place_list view (controller)
    path("", views.place_list, name="place_list"),
    # show visited places instead of not visited
    path("visited", views.places_visited, name="places_visited"),
    # visit a place (using pattern matching)
    path(
        "place/<int:place_pk>/was_visited",
        views.place_was_visited,
        name="place_was_visited",
    ),
    # place details
    path("place/<int:place_pk>", views.place_details, name="place_details"),
    # delete a place
    path("place/<int:place_pk>/delete", views.delete_place, name="delete_place"),
]
