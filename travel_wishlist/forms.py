from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ("name", "visited")


# custom date input field (instead of plain text default)
class DateInput(forms.DateInput):
    input_type = "date"  # override default input type


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ("notes", "date_visited", "photo")
        widgets = {
            "date_visited": DateInput()
        }
