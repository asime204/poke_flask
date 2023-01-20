from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# pokemon properties to include:
#   pokemon name

# from the stats section:
#   base stat for hp
#   base stat for defense
#   base stat for attack

# from the sprites section:
#   front_shiny (URL to the image) or any other image you like more 

# from the abilities section:
#   At Least One Ability

# and any other properties you might find that interest you.



class Pokemon(FlaskForm):
    pokemon = StringField("Pokemon name or number", validators = [DataRequired()])
    submit = SubmitField()