from app import app
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Pokemon
from .forms import UserCreationForm, LoginForm, PokemonForm, EditAccountForm
import requests as r


@app.route('/', methods=["GET", "POST"])
def loginPage():
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            # check is user with that username even exists
            user = User.query.filter_by(username=username).first()
            if user:
                # if user exists, check if passwords match
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('pokedex'))

                else:
                    print('wrong password')

            else:
                return redirect(url_for('signUpPage'))
    return render_template('login.html', form=form)


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

    return render_template('signup.html', form=form)


@app.route('/account', methods=["GET", "POST"])
@login_required
def editAccount():
    form = EditAccountForm()

    if request.method == "POST":
        if form.validate():
            current_user.firstName = form.firstName.data
            current_user.lastName = form.lastName.data
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.password = form.password.data

            current_user.saveToDB()
            flash("Your account has been updated!")
            return redirect(url_for('pokeTeam'))

    return render_template('editAccount.html', form=form)


@app.route('/logout', methods=["GET"])
@login_required
def logoutRoute():
    logout_user()
    return redirect(url_for('loginPage'))


@app.route('/pokedex', methods=["GET", "POST"])
def pokedex():
    form = PokemonForm()
    print(request.method)
    if request.method == 'POST':
        url = f'https://pokeapi.co/api/v2/pokemon/{form.pokemon.data.lower()}'
        response = r.get(url)

        if response.ok:
            my_dict = response.json()

            pokemon_dict = {}

            pokemon_dict["Name"] = my_dict["name"]
            pokemon_dict["Base HP"] = my_dict["stats"][0]["base_stat"]
            pokemon_dict["Base ATK"] = my_dict["stats"][1]["base_stat"]
            pokemon_dict["Base DEF"] = my_dict["stats"][2]["base_stat"]
            pokemon_dict["Base SPD"] = my_dict["stats"][5]["base_stat"]
            pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
            pokemon_dict["Front Shiny"] = my_dict["sprites"]["front_shiny"]

            existing_pokemon = Pokemon.query.filter_by(
                Name=pokemon_dict["Name"]).first()
            if existing_pokemon:
                return render_template('pokedex.html', form=form, pk=pokemon_dict)
            else:
                poke = Pokemon(Name=pokemon_dict["Name"], HP=pokemon_dict["Base HP"], ATK=pokemon_dict["Base ATK"], DEF=pokemon_dict["Base DEF"],
                               SPD=pokemon_dict["Base SPD"], Ability=pokemon_dict["Ability"], ImgURL=pokemon_dict["Front Shiny"])
                poke.saveToDB()
                return render_template('pokedex.html', form=form, pk=pokemon_dict)

        else:
            return render_template('pokedex.html', form=form)

    return render_template('pokedex.html', form=form)
