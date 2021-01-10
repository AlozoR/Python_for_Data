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
import os

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = os.urandom(32)
bootstrap = Bootstrap(app)


class EnterDataForm(FlaskForm):
    administrative = IntegerField("Number of administrative pages visited",
                                  validators=[InputRequired(),
                                              NumberRange(min=0, max=30)],
                                  default=7)

    informational = IntegerField("Number of informational pages visited",
                                 validators=[InputRequired(),
                                             NumberRange(min=0, max=15)],
                                 default=1)

    product_related = IntegerField("Number of product related pages visited",
                                   validators=[InputRequired(),
                                               NumberRange(min=0, max=500)],
                                   default=310)

    month = IntegerField("Month of the visit",
                         validators=[DataRequired(),
                                     NumberRange(min=1, max=12)],
                         default=7)

    visitor_type = SelectField("Visitor type",
                               choices=[(0, "Returning visitor"),
                                        (1, "New visitor")],
                               validators=[InputRequired()],
                               coerce=int,
                               default=0)

    weekend = BooleanField("Are you visiting during the weekend",
                           default=False)

    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def home():
    form = EnterDataForm()
    if request.method == "POST" and form.validate_on_submit():
        import joblib
        loaded_model = joblib.load("saved_model.pkl")
        visitor_type = [0, 0, 1] if form.visitor_type.data == 0 else [1, 0, 0]
        prediction = bool(loaded_model.predict(
            [[form.administrative.data, form.informational.data,
              form.product_related.data, form.weekend.data,
              form.month.data, *visitor_type]]))
        session["bought"] = prediction
        return redirect(url_for("show_result"))
    return render_template("home.html", form=form)


@app.route("/results")
def show_result():
    return render_template("results.html",
                           success=session.get("bought", "first"))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
