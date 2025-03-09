from .models import Ingredient, Unit, RecipeIngredient, Cuisine, Rating, Tag, MealType, Recipe, Favourites
from django import forms
from django.forms import ModelForm, inlineformset_factory

    
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value",]

    value = forms.ChoiceField(
        choices=[(str(i), i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={"class": "star-rating"}),
        required=True
    )

    
class CreateRecipeForm(forms.Form):
    name = forms.CharField(
            max_length=64,
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter recipe name"})
        )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control-file"})
    )
    image_alt_text = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter alt text for image"}),
        required=False
    )
    meal_type = forms.ModelMultipleChoiceField(
        queryset=MealType.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )
    cuisine = forms.ModelMultipleChoiceField(
        queryset=Cuisine.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )
    servings = forms.IntegerField(
        min_value=1,
        max_value=99,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    cook_time = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    prep_time = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 10, "cols": 80})
    )
    instructions = forms.CharField(
        label="Instructions",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 10, "cols": 80})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Recipe.objects.filter(name=name).exists():
            raise forms.ValidationError("A recipe with this name already exists.")
        return name
    
        # Initialise form so all fields are optional
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
        # Sort display of tags and cuisines from a-z
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
        self.fields["cuisine"].queryset = Cuisine.objects.all().order_by("name")
    
class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        required=True
    )    
    quantity = forms.DecimalField(
        min_value=0,
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
            "cuisine": forms.CheckboxSelectMultiple(),
            "meal_type": forms.CheckboxSelectMultiple()
        }
        
    # Initialise form so all fields are optional
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            
        # Sort display of tags and cuisines from a-z
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
        self.fields["cuisine"].queryset = Cuisine.objects.all().order_by("name")
        
        
        
        
class SortForm(forms.Form):
    SORT_CHOICES = [
        ("name_asc", "A-Z"),
        ("name_desc", "Z-A"),
        ("-created_at", "Newest to Oldest"),
        ("created_at", "Oldest to Newest"),
    ]
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False
    )
    
    
    
class FavouriteForm(forms.Form):
    recipe_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[("add", "Add"), ("remove", "Remove")], widget=forms.HiddenInput())
    