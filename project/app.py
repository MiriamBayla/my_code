import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required
import sqlite3

# Configure application
app = Flask(__name__)
app.secret_key = '462vgbhn147854nm785'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define database path
db_path = "sqlite:///project.db"

# Configure CS50 Library to use SQLite database
db = SQL(db_path)

# Modifies response headers to ensure that responses are not cached by browser
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Create tables
# Users table:
db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL, hash TEXT NOT NULL, user_id INTEGER PRIMARY KEY AUTOINCREMENT)")
# Recipe_type table:
db.execute("CREATE TABLE IF NOT EXISTS Recipe_type(recipe_type_id INTEGER, type_name TEXT, image_name TEXT)")
# Create a unique index on Recipe_type_id - to avoid duplication in index page
db.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_recipe_type_id ON Recipe_type(recipe_type_id);''')
# Recipes table:
db.execute("CREATE TABLE IF NOT EXISTS Recipes (recipe_id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT, title TEXT NOT NULL, description TEXT NOT NULL, user_id INTEGER NOT NULL, recipe_type_id INTEGER NOT NULL)")
# Ingredients table:
db.execute("CREATE TABLE IF NOT EXISTS Ingredients (name TEXT NOT NULL, amount INTEGER NOT NULL, measurement TEXT NOT NULL, place INTEGER NOT NULL, recipe_id INTEGER NOT NULL)")
# Directions table:
db.execute("CREATE TABLE IF NOT EXISTS Directions (direction TEXT, place INTEGER NOT NULL, recipe_id INTEGER NOT NULL)")
# Images table:
db.execute("CREATE TABLE IF NOT EXISTS Images (image_name TEXT NOT NULL, recipe_id INTEGER NOT NULL)")
# Favorites table:
db.execute("CREATE TABLE IF NOT EXISTS Favorites (recipe_id INTEGER NOT NULL, user_id INTEGER NOT NULL)")
# Mine table:
db.execute("CREATE TABLE IF NOT EXISTS Mine (recipe_id INTEGER NOT NULL, user_id INTEGER NOT NULL)")
# Reviews table:
db.execute("CREATE TABLE IF NOT EXISTS Reviews (recipe_id INTEGER NOT NULL, user_id INTEGER NOT NULL, review TEXT NOT NULL)")

# Inserting the Recipe_type values
db.execute("INSERT OR IGNORE INTO Recipe_type(recipe_type_id, type_name, image_name) VALUES (1, 'Salads', 'salads.jpg')")
db.execute("INSERT OR IGNORE INTO Recipe_type(recipe_type_id, type_name, image_name) VALUES (2, 'Breads', 'breads.jpg')")
db.execute("INSERT OR IGNORE INTO Recipe_type(recipe_type_id, type_name, image_name) VALUES (3, 'Soups', 'soups.jpg')")
db.execute("INSERT OR IGNORE INTO Recipe_type(recipe_type_id, type_name, image_name) VALUES (4, 'Desserts', 'desserts.jpg')")
db.execute("INSERT OR IGNORE INTO Recipe_type(recipe_type_id, type_name, image_name) VALUES (5, 'Mains', 'mains.jpg')")
db.execute("INSERT OR IGNORE INTO Recipe_type(recipe_type_id, type_name, image_name) VALUES (6, 'Appetizers', 'appetizers.jpg')")
db.execute("INSERT OR IGNORE INTO Recipe_type(recipe_type_id, type_name, image_name) VALUES (7, 'Fish', 'fish.jpg')")


# Index page function - I used some chatgpt
@app.route('/')
def index():
    recipe_types = db.execute('''
        SELECT recipe_type_id, type_name, image_name
        FROM Recipe_type
    ''')
    return render_template('index.html', recipe_types=recipe_types)

# Mine page function
@app.route('/mine')
@login_required
def mine():
    user_id = session.get("user_id")
    if not user_id:
        return apology("User not logged in", 403)

    recipes = db.execute('''
        SELECT Recipes.recipe_id, Recipes.title, Recipes.description, Images.image_name
        FROM Recipes
        LEFT JOIN Images ON Recipes.recipe_id = Images.recipe_id
        INNER JOIN Mine ON Recipes.recipe_id = Mine.recipe_id
        WHERE Mine.user_id = ? AND Recipes.status = "on"
    ''', user_id)
    return render_template('mine.html', recipes=recipes)

# Recipe_type page function - used chatgpt
@app.route('/recipe_type/<int:recipe_type_id>')
def recipe_type(recipe_type_id):
    # Fetch recipes of the selected type with only one image per recipe
    recipes = db.execute('''
        SELECT DISTINCT Recipes.recipe_id, Recipes.title, Recipes.description,
               (SELECT Images.image_name
                FROM Images
                WHERE Images.recipe_id = Recipes.recipe_id
                LIMIT 1) AS image_name
        FROM Recipes
        WHERE Recipes.recipe_type_id = ? AND Recipes.status = 'on'
    ''', recipe_type_id)

    # Fetch the recipe type name for display
    recipe_type = db.execute('SELECT type_name FROM Recipe_type WHERE recipe_type_id = ?', recipe_type_id)

    return render_template('recipe_type.html', recipes=recipes, recipe_type=recipe_type[0])

# Login function
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # After successful login
        username = request.form.get("username")
        session['username'] = username
        flash(f"Hi, {username}. You are logged in.")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Logout function
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Register function
@app.route("/register", methods=["GET", "POST"])
def register():
    """New user can register"""

    # User reacher out via get (wants to register)
    if request.method == "GET":
        return render_template("register.html")

    # User reached out via post (Doing the register)
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Return apology if user didn't fill out one of the fields
        if not password or not confirmation or not username:
            return apology("Password, confirmation and name required", 400)
        # Return apology if user's password and confirmation don't match
        elif password != confirmation:
            return apology("Password and confirmation did not match", 400)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            # Return apology if username already exists
            if len(rows) > 0:
                return apology("Username already exists", 400)
        hash = generate_password_hash(password)
        # Store in user's info his name and hash-code
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        # Updating session to the current user id
        session["user_id"] = new_user_id

        # After successful Registery
        username = request.form.get("username")
        session['username'] = username
        flash(f"Hi, {username}. You have successfully registered.")

        # Redirect user to home page
        return redirect("/")

# Add function - I used chatgpt with this function
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Retrieve form data
        recipe_title = request.form.get('recipe_title')
        description = request.form.get('description')
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_amounts = request.form.getlist('ingredient_amount[]')
        ingredient_measurements = request.form.getlist('ingredient_measurement[]')
        directions = request.form.getlist('direction[]')
        recipe_type = request.form.get('recipe_type')

        # Validate description length
        if len(description) > 80:
            return "Description cannot exceed 80 characters", 400

        # Validate ingredient amounts
        try:
            ingredient_amounts = [float(amount) for amount in ingredient_amounts]
            if any(amount <= 0 for amount in ingredient_amounts):
                return "Ingredient amounts must be positive numbers", 400
        except ValueError:
            return "Ingredient amounts must be valid numbers", 400

        user_id = session.get("user_id")

        # Handle image upload
        image = request.files['image']
        image_filename = None

        if image:
            # Secure the filename and save it to a directory
            image_filename = secure_filename(image.filename)
            image.save(os.path.join("static/images", image_filename))

        try:
            # Get the recipe_type_id from the Recipe_type table
            recipe_type = request.form.get('recipe_type')
            recipe_type_id_query = db.execute('SELECT recipe_type_id FROM Recipe_type WHERE type_name = ?', recipe_type)
            recipe_type_id = recipe_type_id_query[0]['recipe_type_id']

            # Insert new recipe with the recipe_type_id
            result = db.execute(
                'INSERT INTO Recipes (title, description, user_id, recipe_type_id, status) VALUES (?, ?, ?, ?, ?)',
                recipe_title, description, user_id, recipe_type_id, "on"
            )

            # Get the id of the newly inserted recipe
            recipe_id = db.execute('SELECT last_insert_rowid() AS recipe_id')[0]['recipe_id']

            # Insert ingredients
            for i, (name, amount, measurement) in enumerate(zip(ingredient_names, ingredient_amounts, ingredient_measurements)):
                db.execute(
                    'INSERT INTO Ingredients (name, amount, measurement, place, recipe_id) VALUES (?, ?, ?, ?, ?)',
                    name, amount, measurement, i + 1, recipe_id
                )

            # Insert into Mine table
            db.execute(
                'INSERT INTO Mine (recipe_id, user_id) VALUES (?, ?)',
                recipe_id, user_id
            )

            # Insert directions
            for i, direction in enumerate(directions):
                db.execute(
                    'INSERT INTO Directions (direction, place, recipe_id) VALUES (?, ?, ?)',
                    direction, i + 1, recipe_id
                )

            # Insert image into Images table
            if image_filename:
                db.execute(
                    'INSERT INTO Images (recipe_id, image_name) VALUES (?, ?)',
                    recipe_id, image_filename
                )

            return redirect(url_for('add'))
        except Exception as e:
            print(f"Error: {e}")
            return str(e)

    return render_template('add.html', ingredient_count=1, direction_count=1)

# Main-edit page
@app.route('/main_edit')
@login_required
def main_edit():
    recipes = db.execute('''
        SELECT Recipes.recipe_id, Recipes.title, Recipes.description, Images.image_name
        FROM Recipes
        LEFT JOIN Images ON Recipes.recipe_id = Images.recipe_id
        WHERE Recipes.user_id = ? AND Recipes.status = "on"
    ''', session["user_id"])
    return render_template('main_edit.html', recipes=recipes)


# Edit function - used chatgpt
@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit(recipe_id):
    if request.method == 'POST':
        # Handle form submmition:
        # Extract form data
        recipe_title = request.form.get('recipe_title')
        description = request.form.get('description')
        recipe_type = request.form.get('recipe_type')
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_amounts = request.form.getlist('ingredient_amount[]')
        ingredient_measurements = request.form.getlist('ingredient_measurement[]')
        directions = request.form.getlist('direction[]')

        # Validate and update recipe details
        if len(description) > 80:
            return "Description cannot exceed 80 characters", 400

        try:
            ingredient_amounts = [float(amount) for amount in ingredient_amounts]
            if any(amount <= 0 for amount in ingredient_amounts):
                return "Ingredient amounts must be positive numbers", 400
        except ValueError:
            return "Ingredient amounts must be valid numbers", 400

        image = request.files.get('image')
        image_filename = None

        if image and image.filename:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join("static/images", image_filename))

        # Update recipe
        recipe_type = request.form.get('recipe_type')
        recipe_type_id_query = db.execute('SELECT recipe_type_id FROM Recipe_type WHERE LOWER(type_name) = LOWER(?)', recipe_type.lower())
        if recipe_type_id_query:
            recipe_type_id = recipe_type_id_query[0]['recipe_type_id']
            db.execute(
                        'UPDATE Recipes SET title = ?, description = ?, recipe_type_id = ? WHERE recipe_id = ?',
                        recipe_title, description, recipe_type_id, recipe_id
                    )

        else:
            # Handle the case where no matching type_name was found
            print("No matching recipe type found.")


        # Update Ingredients
        db.execute('DELETE FROM Ingredients WHERE recipe_id = ?', recipe_id)
        for i, (name, amount, measurement) in enumerate(zip(ingredient_names, ingredient_amounts, ingredient_measurements)):
            db.execute(
                'INSERT INTO Ingredients (name, amount, measurement, place, recipe_id) VALUES (?, ?, ?, ?, ?)',
                name, amount, measurement, i + 1, recipe_id
            )

        # Update Directions
        db.execute('DELETE FROM Directions WHERE recipe_id = ?', recipe_id)
        for i, direction in enumerate(directions):
            db.execute(
                'INSERT INTO Directions (direction, place, recipe_id) VALUES (?, ?, ?)',
                direction, i + 1, recipe_id
            )

        # Update Image
        if image_filename:
            db.execute('DELETE FROM Images WHERE recipe_id = ?', recipe_id)
            db.execute(
                'INSERT INTO Images (recipe_id, image_name) VALUES (?, ?)',
                recipe_id, image_filename
            )

        return redirect(url_for('edit', recipe_id=recipe_id))

    # For GET request, load existing recipe details
    recipe = db.execute('SELECT * FROM Recipes WHERE recipe_id = ?', recipe_id)[0]
    ingredients = db.execute('SELECT * FROM Ingredients WHERE recipe_id = ?', recipe_id)
    directions = db.execute('SELECT * FROM Directions WHERE recipe_id = ?', recipe_id)

    # Query to get the image
    image_result = db.execute('SELECT image_name FROM Images WHERE recipe_id = ?', recipe_id)

    # Handle the case where no image is found
    image = image_result[0] if image_result else None

    # Pass existing details to template
    return render_template(
        'edit.html',
        recipe=recipe,
        ingredients=ingredients,
        directions=directions,
        image=image,
        ingredient_count=len(ingredients),
        direction_count=len(directions)
    )

# Deletion of recipe - used chatgpt
@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    # Update the recipe status to 'off'
    db.execute("UPDATE Recipes SET status = ? WHERE recipe_id = ?", 'off', recipe_id)

    return redirect(url_for('main_edit'))


# Recipe function - I used chatgpt
@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    # Query the database for the recipe details
    recipe = db.execute('SELECT * FROM Recipes WHERE recipe_id = ?', recipe_id)[0]
    ingredients = db.execute('SELECT name, amount, measurement FROM Ingredients WHERE recipe_id = ?', recipe_id)
    directions = db.execute('SELECT place, direction FROM Directions WHERE recipe_id = ? ORDER BY place ASC', recipe_id)
    images = db.execute('SELECT image_name FROM Images WHERE recipe_id = ?', recipe_id)
    contributer = db.execute('SELECT username FROM users WHERE user_id = (SELECT user_id FROM Recipes WHERE recipe_id = ?)', recipe_id)
    contributer_name = contributer[0]['username'] if contributer else 'Unknown'

    return render_template('recipe.html', recipe=recipe, ingredients=ingredients, directions=directions, images=images, contributer_name=contributer_name)

# Search bar - main: I used chatgpt
def get_recipes_by_title(title):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.recipe_id, r.title, r.description, i.image_name
        FROM Recipes r
        LEFT JOIN Images i ON r.recipe_id = i.recipe_id
        WHERE r.title LIKE ? AND r.status = 'on'
    """, ('%' + title + '%',))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

# Search bar - edit: I used chatgpt
def get_recipes_by_title_edit(title):
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.recipe_id, r.title, r.description, i.image_name
        FROM Recipes r
        LEFT JOIN Images i ON r.recipe_id = i.recipe_id
        WHERE r.title LIKE ? AND r.status = 'on' AND user_id = ?
    """, ('%' + title + '%', session["user_id"]))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

@app.route('/search')
def search_recipes():
    query = request.args.get('query', '')
    recipes = get_recipes_by_title(query)
    return render_template('search_results.html', recipes=recipes)

@app.route('/search-edit')
def search_recipes_edit():
    query = request.args.get('query', '')
    recipes = get_recipes_by_title_edit(query)
    return render_template('search_results_edit.html', recipes=recipes)


@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    recipe = db.execute("""
        SELECT r.recipe_id, r.title, r.description, i.image_name
        FROM Recipes r
        LEFT JOIN Images i ON r.recipe_id = i.recipe_id
        WHERE r.recipe_id = ?
    """, recipe_id)

    if recipe:
        return render_template('recipe.html', recipe=recipe[0])
    else:
        return "Recipe not found", 404
