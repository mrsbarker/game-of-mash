from wtforms import DecimalField, IntegerField, StringField, SelectField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm

def validate_kids(form, field):
    if field.data != "":
        if int(field.data) >= 0:
            pass
        else:
            raise ValidationError('Input for kids must be an integer')
        
def validate_salary(form, field):
    if field.data != "":
        if float(field.data) >= 0:
            pass
        else:
            raise ValidationError("Input for salary must be a number")


class MashForm(FlaskForm):
    spouse1 = StringField("Spouse", validators=[validators.Optional()], default="Computer's Choice") 
    spouse2 = StringField("Spouse", validators=[validators.Optional()], default="Computer's Choice")
    spouse3 = StringField("Spouse", validators=[validators.Optional()])
    spouse4 = StringField("Spouse", validators=[validators.Optional()])

    kids1 = StringField("Kids", validators=[validators.Length(0, 3), validate_kids, validators.Optional()]) 
    kids2 = StringField("Kids", validators=[validators.Length(0, 3), validate_kids, validators.Optional()])
    kids3 = StringField("Kids", validators=[validators.Length(0, 3), validate_kids, validators.Optional()])
    kids4 = StringField("Kids", validators=[validators.Length(0, 3), validate_kids, validators.Optional()])

    job1 = StringField("Career", validators=[validators.Optional()], default="Computer's Choice")
    job2 = StringField("Career", validators=[validators.Optional()], default="Computer's Choice")
    job3 = StringField("Career", validators=[validators.Optional()])
    job4 = StringField("Career", validators=[validators.Optional()])

    car1 = StringField("Vehicle", validators=[validators.Optional()], default="Computer's Choice")
    car2 = StringField("Vehicle", validators=[validators.Optional()], default="Computer's Choice")
    car3 = StringField("Vehicle", validators=[validators.Optional()])
    car4 = StringField("Vehicle", validators=[validators.Optional()])

    money1 = StringField("Salary", validators=[validate_salary, validators.Optional()])
    money2 = StringField("Salary", validators=[validate_salary, validators.Optional()])
    money3 = StringField("Salary", validators=[validate_salary, validators.Optional()])
    money4 = StringField("Salary", validators=[validate_salary, validators.Optional()])

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

