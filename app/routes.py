from app import app
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Pokemon, User_Pokemon
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
                    flash(f'Successfully logged in! Welcome back {user.username}', category='success')                    
                    return redirect(url_for('pokedex'))

                else:
                    flash('wrong password', category='danger')

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
@login_required
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

            existing_pokemon = Pokemon.query.filter_by(Name=pokemon_dict["Name"].lower()).first()
            if existing_pokemon:
                return redirect(url_for('encounterPokemon', pokemon_id=existing_pokemon.id, pk=pokemon_dict))
            else:
                poke = Pokemon(Name=pokemon_dict["Name"].lower(), HP=pokemon_dict["Base HP"], ATK=pokemon_dict["Base ATK"], DEF=pokemon_dict["Base DEF"], SPD=pokemon_dict["Base SPD"], Ability=pokemon_dict["Ability"], ImgURL=pokemon_dict["Front Shiny"])
                poke.saveToDB()
                return redirect(url_for('encounterPokemon', pokemon_id=poke.id, pk=pokemon_dict))
        return render_template('pokedex.html', form=form)  
    return render_template('pokedex.html', form=form)  
                
               
   

@app.route('/pokedex/encounter/<int:pokemon_id>', methods=["GET", "POST"])
@login_required
def encounterPokemon(pokemon_id):
    form = PokemonForm()
    existing_pokemon = Pokemon.query.filter_by(id=pokemon_id).first()
    if existing_pokemon:
        my_pokemon = User_Pokemon.query.filter_by(user_id=current_user.id).all()
        # check if the pokemon is owned by another user
        owned_by_other = User_Pokemon.query.filter(User_Pokemon.pokemon_id == pokemon_id, User_Pokemon.user_id != current_user.id).first()
        if owned_by_other:
            flash('This Pokemon is already owned by another user!', category='danger')
            return redirect(url_for('pokedex'))
        else:
            # check the number of pokemon the user has
            owned = {catch.pokemon_id for catch in my_pokemon}
            if pokemon_id in owned:
                return render_template('encounter.html', form=form, pokemon=existing_pokemon, owned=True)
            else:
                return render_template('encounter.html', form=form, pokemon=existing_pokemon, owned=False)
    return redirect(url_for('pokedex'))

@app.route('/pokedex/encounter/<int:pokemon_id>/catch', methods=["GET"])
@login_required
def catchPokemon(pokemon_id):
    existing_pokemon = Pokemon.query.filter_by(id=pokemon_id).first()
    if existing_pokemon:
        my_pokemon = User_Pokemon.query.filter_by(user_id=current_user.id).all()
        # check the number of pokemon the user has
        if len(my_pokemon) >= 5:
            flash('Your party is full!', category='danger')
        else:
            owned = {catch.pokemon_id for catch in my_pokemon}
            if pokemon_id in owned:
                flash('You already own this Pokemon!', category='danger')
                return  redirect(url_for('release'))
            else:
                pokeball = User_Pokemon(current_user.id, pokemon_id)
                pokeball.saveToDB()
                flash('Congratulations, you caught a new Pokemon!', category='success')
                return redirect(url_for('pokedex'))
    return


@app.route('/pokedex/encounter/<int:pokemon_id>/release', methods=["GET"])
@login_required
def releasePokemon(pokemon_id):
    existing_pokemon = User_Pokemon.query.filter_by(user_id=current_user.id, pokemon_id=pokemon_id).first()
    if existing_pokemon:
        existing_pokemon.deleteFromDB()
        flash('You have released your Pokemon', category='warning')
        return redirect(url_for('pokedex'))
