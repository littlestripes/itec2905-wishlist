from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def place_list(request):
    """Differentiates between POST and GET requests.

    POST request -> we know that the user clicked Add. validate form data, then
        save the new Place to the db and redirect to the same page (GET)

    GET request -> renders the page with the form and the place list
    """

    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)  # create a new Place but don't save
        place.user = request.user
        if form.is_valid():
            place.save()  # save to db
            return redirect("place_list")
            # redirects to GET view with name place_list (this same view)

    # if not POST or invalid form, render page w/ form to add place, show list
    places = (
        Place.objects.filter(user=request.user).filter(visited=False).order_by("name")
    )
    new_place_form = NewPlaceForm()
    return render(
        request,
        "travel_wishlist/wishlist.html",
        {"places": places, "new_place_form": new_place_form},
    )


@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, "travel_wishlist/visited.html", {"visited": visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == "POST":
        # grab corresponding Place object from db based on pk/id
        place = get_object_or_404(Place, pk=place_pk)
        # place = Place.objects.get(pk=place_id) would work too
        if place.user == request.user:  # only allow users to do this
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect("place_list")


@login_required
def place_details(request, place_pk):

    place = get_object_or_404(Place, pk=place_pk)

    # check if place is owned by current user
    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # instance is the model object to update w/ form data

        if form.is_valid():
            form.save()
            messages.info(request, "Trip information updated!")
        else:
            messages.error(request, form.errors)

        return redirect("place_details", place_pk=place_pk)

    else:  # GET request
        if place.visited:
            # pre-populate w/ data from this Place instance
            review_form = TripReviewForm(instance=place)
            return render(
                request,
                "travel_wishlist/place_detail.html",
                {"place": place, "review_form": review_form},
            )
        else:
            return render(
                request, "travel_wishlist/place_detail.html", {"place": place}
            )


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # user requesting delete must also be the Place's owner
    if place.user == request.user:
        place.delete()
        return redirect("place_list")
    else:
        return HttpResponseForbidden()
