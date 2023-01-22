from app import app
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from .models import User
from .forms import Pokemon, UserCreationForm, LoginForm
import requests as r


# @app.route('/')
# def homePage():
#     text = "Enter your Pokedex"
#     return render_template('login.html', my_text=text)

@app.route('/signup', methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            firstName = form.firstName.data
            lastName = form.lastName.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            

            # add user to database
            user = User(firstName, lastName, username, email, password)

            user.saveToDB()

            return redirect(url_for('loginPage'))


    return render_template('signup.html', form = form )

@app.route('/login', methods=["GET", "POST"])
def loginPage():
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            # check is user with that username even exists
            user = User.query.filter_by(username=username).first()
            if user:
                #if user exists, check if passwords match
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('pokeTeam'))

                else:
                    print('wrong password')

            else:
                return redirect(url_for('signUpPage'))
    return render_template('login.html', form = form)



@app.route('/logout', methods=["GET"])
@login_required
def logoutRoute():
    logout_user()
    return redirect(url_for('login'))











@app.route('/poke_team', methods=["GET", "POST"])
def pokeTeam():
    form = Pokemon()
    print(request.method)
    if request.method == 'POST':
        url = f'https://pokeapi.co/api/v2/pokemon/{form.pokemon.data}'
        response = r.get(url)

        if response.ok:
            my_dict = response.json()

            pokemon_dict = {}
            pokemon_dict["Front Shiny"] = my_dict["sprites"]["front_shiny"]
            pokemon_dict["Name"] = my_dict["name"]
            pokemon_dict["Base HP"] = my_dict["stats"][0]["base_stat"]
            pokemon_dict["Base ATK"] = my_dict["stats"][1]["base_stat"]
            pokemon_dict["Base DEF"] = my_dict["stats"][2]["base_stat"]
            pokemon_dict["Base SPD"] = my_dict["stats"][5]["base_stat"]
            pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]

            # poke = Pokemon(, img_url,title caption, current_user.id)
            # poke.saveToDB()
            return render_template('poke_team.html', form=form, pk=pokemon_dict)

        else:
            return render_template('poke_team.html', form=form)

    return render_template('poke_team.html', form=form)

    
# Change to accept pk and save to db

# @app.route('/posts/create', methods=["GET","POST"])
# @login_required
# def createPost():
#     form = PostForm()
#     if request.method == "POST":
#         if form.validate():
#             title = form.title.data
#             caption = form.caption.data
#             img_url = form.img_url.data

#             post = Post(title, img_url, caption, current_user.id)
#             post.saveToDB()
#     return render_template('createpost.html', form = form)


# change for pokemon team update

# @app.route('/posts/<int:post_id>/update', methods=["GET", "POST"])
# @login_required
# def updatePost(post_id):
#     post = Post.query.get(post_id)
#     if current_user.id != post.author.id:
#         return redirect(url_for('getPosts'))
#     form = PostForm()
#     if request.method == "POST":
#         if form.validate():
#             title=form.title.data
#             img_url=form.img_url.data
#             caption=form.caption.data
#             post.title = title
#             post.img_url = img_url
#             post.caption = caption
#             post.saveChanges()
#             return redirect(url_for('getPost', post_id=post.id))
#     return render_template('updatepost.html', post=post, form= form)


# delete user or delete pokemon

# @app.route('/posts/<int:post_id>/delete', methods=["GET"])
# @login_required
# def deletePost(post_id):
#     post = Post.query.get(post_id)
#     if current_user.id != post.author.id:
#         return redirect(url_for('getPosts'))

#     post.deleteFromDB()


#     return redirect(url_for('getPosts'))
