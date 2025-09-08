# Miri's Recipes Website

Welcome to Miri's Recipes Website! This project is a comprehensive platform for users to manage and explore recipes. Whether you're a home cook or a professional chef, this site offers features to add, edit, browse, and organize recipes easily.

#### Video Demo: [https://www.youtube.com/watch?v=n_H5CNl7urY](https://www.youtube.com/watch?v=n_H5CNl7urY)

## Description
A web application that includes a register and login/logout system. The web application allows users to manage recipes by adding, editing, deleting, and viewing them. The site is built using Flask, with Jinja as the templating engine, providing a user-friendly interface for managing ingredients, measurements, and instructions.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Templating Engine**: Jinja
- **Database**: SQLite

## Features
- **Browse Recipes By Type**: Explore and view all available recipes in the application based on their categories.
- **User Authentication**: Register or log in to manage your own recipes.
- **Add Recipes**: Create a new recipe with a title, description, ingredients, directions, and an image.
- **Edit Recipes**: Modify existing recipes with updated details.
- **Delete Recipes**: Remove recipes that you no longer need.
- **Search Recipes**: Search for recipes by name (or part of the name).
- **Search Recipes to Edit**: Search for recipes by name (or part of the name) in the edit section to edit.
- **Browse User's Recipes**: Browse and view your added recipes.

## Usage
### 1. **Register an Account**:
   - Go to the Register page by clicking on the **Register** button on the right of the navigation bar and fill out the registration form.

### 2. **Login**:
   - Click the **Login** button on the right of the navigation bar.
   - Fill in the login form.

### 3. **Logout**:
   - When logged in, click the **Logout** button on the right of the navigation bar. Once logged out, the user can't add, delete, or edit recipes.

### 4. **Browse Recipes by Type**:
   - Click on the category of the recipes you want to view (mains, desserts, breads, fish, etc.).
   - Click on the recipe you want to view.

### 5. **Searching for a Recipe**:
   - Use the search bar to find recipes by name (or part of the name).

### 6. **Adding a Recipe**:
   - Click on **Add** in the navigation menu.
   - Fill out the form with the recipe details and submit.

### 7. **Viewing Your Recipes**:
   - Click on **Mine** in the navigation menu.
   - Click on the specific recipe of yours you want to see.

### 8. **Searching for a Recipe in Edit**:
   - Click on **Edit** in the navigation menu.
   - Use the search bar to find your added recipe for editing by name (or part of the name).

### 9. **Editing a Recipe**:
   - Click on **Edit** in the navigation menu.
   - (Optional) Use the search bar to find the recipe to edit.
   - Click on the recipe you want to edit.
   - Make your changes and then click **Update**.

### 10. **Deleting a Recipe**:
   - On the editing recipe page, click the red **Delete Recipe** button at the bottom of the page.
   - Confirm the deletion when prompted.

## Project Structure
/flask_session              # Contains Flask-related sessions and configurations
/static                     # Contains static files (CSS, images)
│   ├── styles.css          # Main stylesheet for the website
│   └── /images             # Images used in the website
/templates                  # HTML templates for the website
│   ├── add.html            # Page for adding new recipes
│   ├── apology.html        # Error page for handling user errors
│   ├── edit.html           # Page for editing existing recipes
│   ├── index.html          # Home page
│   ├── layout.html         # Base layout used by other templates
│   ├── login.html          # User login page
│   ├── main_edit.html      # Page for choosing a recipe to edit
│   ├── mine.html           # Page showing user's own recipes
│   ├── recipe_type.html    # Page showing food categories
│   ├── recipe.html         # Detailed view of a single recipe
│   ├── register.html       # User registration page
│   ├── search_results.html # Page displaying search results
│   ├── search_results_edit.html # Page displaying search results for user's recipes (to edit)
/app.py                     # Main application code (Flask routes, etc.)
/helpers.py                 # Helper functions used in app.py
/project.db                 # SQLite database for storing recipes and user data
/README.md                  # Documentation for the project

## Future Enhancements
- Implement user favorites: Utilize the existing Favorites table in the database to allow users to mark and view their favorite recipes.
- Add recipe reviews: Enable users to leave reviews and ratings for recipes, displaying them at the bottom of the recipe pages.
- Implement recipe sharing: Allow users to share recipes via social media or email.
- Add user profiles: Let users create and customize their profiles with bio information and a list of their favorite or created recipes.

## Acknowledgements
- **Father**: For providing continuous support and valuable advice throughout the development process.
- **Mother**: For her keen eye and suggestions that helped improve the project.
- **ChatGPT**: For assisting with implementation details and providing guidance.
- **BootStrap**: For enabling functionalities enhancing the appearance of the graphical-user-interface.
