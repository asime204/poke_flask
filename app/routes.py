from app import app
from flask import render_template, request
from .forms import Pokemon
import requests as r

@app.route('/')
def homePage():
    text = "Enter your Pokedex"
    return render_template('index.html', my_text = text )



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
            pokemon_dict["Name"] = my_dict["name"] 
            pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
            pokemon_dict["Base XP"] = my_dict["base_experience"]
            pokemon_dict["Front Shiny"] = my_dict["sprites"]["front_shiny"]
            pokemon_dict["Base ATK"] = my_dict["stats"][1]["base_stat"]
            pokemon_dict["Base HP"] = my_dict["stats"][0]["base_stat"]
            pokemon_dict["Base DEF"] = my_dict["stats"][2]["base_stat"]
            return render_template('poke_team.html', form = form, pk = pokemon_dict )
        else:
            return render_template('poke_team.html', form = form )


    return render_template('poke_team.html', form = form )