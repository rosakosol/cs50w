from .models import Ingredient, Unit, RecipeIngredient, Cuisine, Rating, Tag, MealType, Recipe, Favourites
from django import forms
from django.forms import ModelForm, inlineformset_factory

    
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value",]

    value = forms.ChoiceField(
        choices=[(str(i), i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )

    
class CreateRecipeForm(forms.Form):
    name = forms.CharField(max_length=64)
    image = forms.ImageField(required=False)
    image_alt_text = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter alt text for image'}),
        required=False
    )
    meal_type = forms.ModelChoiceField(
        queryset=MealType.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )
    cuisine = forms.ModelChoiceField(
        queryset=Cuisine.objects.all(),
        empty_label="Select a cuisine",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            "rows": 10,
            "cols": 80
        }))
    instructions = forms.CharField(
        label="Instructions",
        widget=forms.Textarea(attrs={
            "rows": 10,
            "cols": 80
        }))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    servings = forms.IntegerField(
        min_value=1,
        max_value=99,
        required=True
    )
    cook_time = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True
    )
    prep_time = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True
    )
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Recipe.objects.filter(name=name).exists():
            raise forms.ValidationError("A recipe with this name already exists.")
        return name
    
class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        required=True
    )    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True
    )
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        required=True
    )   
    
    
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "quantity", "unit"]
        
RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient, 
    form=RecipeIngredientForm, 
    extra=1,
    can_delete=False
    )

    
class RecipeFilterForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["tags", "cuisine", "meal_type"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }
        
    # Initialise form so all fields are optional
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
        
        
        
        
class SortForm(forms.Form):
    SORT_CHOICES = [
        ('name_asc', 'A-Z'),
        ('name_desc', 'Z-A'),
        ('-created_at', 'Newest to Oldest'),
        ('created_at', 'Oldest to Newst'),
    ]
    
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    
class FavouriteForm(forms.Form):
    recipe_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[("add", "Add"), ("remove", "Remove")], widget=forms.HiddenInput())
    