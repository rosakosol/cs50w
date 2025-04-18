
<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h1 align="center">Cookery - CS50W Final Project</h1>

</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
    </li>
    <li>
      <a href="#distinctiveness-and-complexity">Distinctiveness and Complexity</a>
    </li>
      <li>
      <a href="#file-contents">File Contents</a>
    </li>
    <li>
      <a href="#prerequisites">Prerequisites</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About

This is a Django web app that allows users to create, edit, and delete recipes. Users can:

### Features
* Login and register as a user 
* Add, edit and remove recipes
* Rate recipes on a scale of 1-5 stars
* Select ingredients to be added to new recipes from a pre-populated database
* Sort, filter and search for recipes based on select attributes
* Share recipes with friends via email or social media
* Generate a printer-friendly version of the recipes


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Django
* Javascript
* Bootstrap
* HTML
* CSS

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Distinctiveness and Complexity -->
## Distinctiveness and Complexity

Cookery is distinct from other projects in the CS50W course as it incorporates ModelForms and Formsets
to create a relationship between the Recipe and RecipeIngredient models, wherein a RecipeIngredient
is a model that is linked to an Ingredient model as a ForeignKey. This adds a layer of complexity as
RecipeIngredients are based off a database of Ingredient objects, and whilst a Recipe can have multiple 
RecipeIngredients, a RecipeIngredient is mapped to a singular Recipe. Users can dynamically add and remove numerous RecipeIngredients 
when creating a new Recipe, without the need to submit an additional form (hence the use of an inline formset). 

Users can rate recipes, similar to how users could place a bid on an item in the Commerce project, however there is an additional distinction of the recipe's 
average rating being calculated and displayed from all available ratings. Additionally, the average rating is displayed
in star form as is best practice, rather than in the standard integer format. This required the use of more complex Javascript
functions to facilitate colouring in of stars that aligned with the user interacting with the rating form. Users can also update their rating if they have already rating a recipe, and their current rating of the recipe is displayed by default on the rating form.

Furthermore, another distinction between Cookery and other projects is the ability to filter and sort through recipes according to a range of attributes including
tags, cuisine, and mealtype. Users can not only search for recipes using the searchbar, they can also curate their recipe view by selecting a range of filters,
and then sorting the resulting selection alphabetically or in chronological order based on when the recipe was created. On the more detailed recipe view,
users can also click on attribute buttons including tags, cuisine and mealtype, as another method to view recipes that are aggregated under those attributes.

Finally, users can share recipes with friends and family via email, Facebook or X, and can generate a printer-friendly version with custom CSS that minimises 
graphic contents.

<!-- Distinctiveness and Complexity -->
## File/Folder Contents
* app/static
  *  bootstrap/_breakpoints.scss
      * This contains breakpoint variables from Bootstrap
  *  css/print.css
      * This contains all styling applied only when the website is in print form (CTRL + P)
  * css/style.css
      * This all styling applied to the website
  * images/
      * This contains images and icons for styling such as the logo, favicon, and background
  * index.js
      * This contains all Javascript functions that enables features such as star rating for recipes, editing recipes and deleting recipes

* app/templates
  * access_denied.html
    * This page displays when a user attempts to access a page without the correct authorisation

  * add_recipe.html
    * This page displays the add recipe form

  * favourites.html
    * This page displays a user's favourite recipes

  * index.html
    * This page displays the default home page displaying all recipes

  * layout.html
    * This is a template displaying the navbar and footer

  * login.html
    * This page displays the login form

  * no_results.html
    * This page displays when no search results are found

  * recipe.html
    * This page displays a detailed single recipe view

  * register.html
    * This page displays the registration form

  * search.html
    * This page displays the search results for recipes

* media/images
  * This contains images uploaded when creating a new recipe



## Prerequisites


* Python 3.x
* Django
* pip install python-decouple
* pip install pillow


## How to run the webapp

1. Clone the repo
   ```sh
   git clone https://github.com/me50/rosak456/blob/web50/projects/2020/x/capstone/
   ```
2. Change directory
   ```sh
   cd cookery
   ```

3. Generate secret key
   ```sh
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. Create .env file in root directory and paste secret key like so:
   ```sh
   SECRET_KEY='XXXX'
   ```

4. Load demo data
   ```sh
   python manage.py loaddata data.json
   ```

5. Make migrations
    ```sh
    python manage.py makemigrations app
    python manage.py migrate
    ```  

6. Create superuser
   ```sh
   python manage.py createsuperuser
   ```

7. Populate data
   ```sh
   python manage.py populate_data
   ```

8. Run server
    ```sh
    python manage.py runserver
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Copyright (c) 2025 Rosa Kosol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Rosa Kosol - [Email](kosolrosa@gmail.com) | [Github](github.com/rosakosol) 

[Cookery Personal Github Project Link](https://github.com/rosakosol/cs50w/week8/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

