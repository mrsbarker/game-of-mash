from wtforms import DecimalField, IntegerField, StringField, SelectField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm

def validate_nums():
    def _validating(form, field):
        if "kid" in field.name:
            message = "Value for 'Kids' input must be an integer greater than or equal to 0."
        elif "money" in field.name:
            message = "Value for 'Salary' input must be a number (without currency symbols and commas)."
            
        if field.data == "":
            pass
        elif field.data != "" and field.data.isnumeric():
            if "kid" in field.name and int(field.data) < 0:
                validators.StopValidation()
                raise ValidationError(message)
        else:
            validators.StopValidation()
            raise ValidationError(message)


class MashForm(FlaskForm):
    spouse1 = StringField("Spouse", validators=[validators.Optional()], default="Computer's Choice") 
    spouse2 = StringField("Spouse", validators=[validators.Optional()], default="Computer's Choice")
    spouse3 = StringField("Spouse", validators=[validators.Optional()])
    spouse4 = StringField("Spouse", validators=[validators.Optional()])

    kids1 = StringField("Kids", validators=[validators.Length(0, 3), validate_nums(), validators.Optional()]) 
    kids2 = StringField("Kids", validators=[validators.Length(0, 3), validate_nums(), validators.Optional()])
    kids3 = StringField("Kids", validators=[validators.Length(0, 3), validate_nums(), validators.Optional()])
    kids4 = StringField("Kids", validators=[validators.Length(0, 3), validate_nums(), validators.Optional()])

    job1 = StringField("Career", validators=[validators.Optional()], default="Computer's Choice")
    job2 = StringField("Career", validators=[validators.Optional()], default="Computer's Choice")
    job3 = StringField("Career", validators=[validators.Optional()])
    job4 = StringField("Career", validators=[validators.Optional()])

    car1 = StringField("Vehicle", validators=[validators.Optional()], default="Computer's Choice")
    car2 = StringField("Vehicle", validators=[validators.Optional()], default="Computer's Choice")
    car3 = StringField("Vehicle", validators=[validators.Optional()])
    car4 = StringField("Vehicle", validators=[validators.Optional()])

    money1 = StringField("Salary", validators=[validate_nums(), validators.Optional()])
    money2 = StringField("Salary", validators=[validate_nums(), validators.Optional()])
    money3 = StringField("Salary", validators=[validate_nums(), validators.Optional()])
    money4 = StringField("Salary", validators=[validate_nums(), validators.Optional()])

    spun = IntegerField(id="spiral")

    
class SpouseForm(FlaskForm):
    name = StringField("Add Spouse", validators=[validators.DataRequired()])
    sex = SelectField("Sex", validators=[validators.DataRequired()], choices=["M","F"])
    #type = "spouse"
    submit = SubmitField("Submit")

class CarForm(FlaskForm):
    make = StringField("Make", validators=[validators.DataRequired()])
    model = StringField("Model", validators=[validators.DataRequired()])
    year = StringField("Year", validators=[validators.Optional()])
    #type = "vehicle"
    submit = SubmitField("Submit")

class CareerForm(FlaskForm):
    job = StringField("Career", validators=[validators.DataRequired()])
    #type = "career"
    submit = SubmitField("Submit")

class SalaryForm(FlaskForm):
    money = DecimalField("Salary", validators=[validators.DataRequired(), validators.Length(1, 12)])
    #type = "salary"
    submit = SubmitField("Submit")


