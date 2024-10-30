from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


def place_list(request):
    """Differentiates between POST and GET requests.

    POST request -> we know that the user clicked Add. validate form data, then
        save the new Place to the db and redirect to the same page (GET)

    GET request -> renders the page with the form and the place list
    """

    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save()  # create a new Place from the form data
        if form.is_valid():
            place.save()  # save to db
            return redirect("place_list")
            # redirects to GET view with name place_list (this same view)

    places = Place.objects.filter(visited=False).order_by("name")
    new_place_form = NewPlaceForm()
    return render(
        request,
        "travel_wishlist/wishlist.html",
        {"places": places, "new_place_form": new_place_form},
    )


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, "travel_wishlist/visited.html", {"visited": visited})


def place_was_visited(request, place_pk):
    if request.method == "POST":
        # grab corresponding Place object from db based on pk/id
        place = get_object_or_404(Place, pk=place_pk)
        # place = Place.objects.get(pk=place_id) would work too
        place.visited = True
        place.save()

    return redirect("place_list")
