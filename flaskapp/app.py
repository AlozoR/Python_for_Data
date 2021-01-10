from flask import Flask, current_app
from flask import (make_response,
                   redirect,
                   abort,
                   session,
                   render_template,
                   url_for,
                   flash,
                   request)

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField,
                     IntegerField,
                     FloatField,
                     SelectField,
                     BooleanField)
from wtforms.validators import (DataRequired,
                                InputRequired,
                                Length,
                                NumberRange)

app = Flask(__name__, template_folder="templates")


class EnterDataForm(FlaskForm):
    administrative = IntegerField("Number of administrative pages visited",
                                  validators=[DataRequired(),
                                              NumberRange(min=0, max=30)])

    informational = IntegerField("Number of informational pages visited",
                                 validators=[DataRequired(),
                                             NumberRange(min=0, max=15)])

    product_related = IntegerField("Number of product related pages visited",
                                   validators=[DataRequired(),
                                               NumberRange(min=0, max=500)])

    month = IntegerField("Month of the visit",
                         validators=[DataRequired(),
                                     NumberRange(min=1, max=12)])

    visitor_type = SelectField("Visitor type",
                               choices=[(0, "Returning visitor"),
                                        (1, "New_Visitor")],
                               validators=[InputRequired()],
                               coerce=int)

    weekend = BooleanField("Are you visiting during the weekend",
                           default=False)

    submit = SubmitField("Submit")


@app.route("/")
def home():
    form = EnterDataForm()
    if request.method == "POST" and form.validate_on_submit():



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
