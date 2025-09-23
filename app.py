from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
from secrets import token_urlsafe
from random import choice
import database
import game
from appforms import *

SEX = ["F","M"]
MASHOPTS = []
MASH = ""

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///MashOptions.db"
app.secret_key = token_urlsafe(16)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

def randomize(lst, num=1, inputs:list=None):
    # include any typed values to ensure randomizer doesn't double
    dealer_choice = []
    if len(lst) < num:
        pass
        # need to add some error or note here about if not enough list items?
    else:
        while len(dealer_choice) < num:
            temp = choice(lst)
            if temp not in dealer_choice:
                dealer_choice.append(temp)
            elif inputs != None:
                if temp not in inputs and temp not in dealer_choice:
                    dealer_choice.append(temp)
    return dealer_choice

@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        global SEX 
        SEX = request.form.getlist("sex")
        return redirect(url_for("start"))

@app.route("/start", methods=["GET","POST"])
def start():
    global MASH
    MASH = MashForm()
    counter = {k:0 for k in ["spouse", "career", "vehicle", "kids", "salary"]}
    if request.method == "GET":
        return render_template("setup.html", form = MASH)

    elif MASH.validate_on_submit():
        need = []
        inputs = []
        global MASHOPTS
        MASHOPTS = []
        for fld in MASH._fields:
            if MASH[fld].data in ["", "Computer's Choice"]:
                counter[MASH[fld].label.text.lower()] += 1
                need.append(fld)
            # else append to inputs list
            else:
                inputs.append(fld)
            # add to randomize function below

        for k,v in counter.items():   
            if k == "spouse":
                temp = [x for x in need if "spouse" in x]
                lst = database.db_session.scalars(select(database.Spouse.name).where(database.Spouse.sex.in_(SEX))).all()
                chosen = randomize(lst, num=v, inputs=inputs)
                
                for i in range(len(temp)):
                    MASH[temp[i]].data = chosen[i]
                [MASHOPTS.append(game.MashOption("spouse", x.data)) for x in [MASH.spouse1, MASH.spouse2, MASH.spouse3, MASH.spouse4]]

            elif k == "kids":
                temp = [x for x in need if "kid" in x]
                chosen = randomize(range(0,20), num=v, inputs=inputs)
                
                for i in range(len(temp)):
                    MASH[temp[i]].data = chosen[i]
                [MASHOPTS.append(game.MashOption("kids", x.data)) for x in [MASH.kids1, MASH.kids2, MASH.kids3, MASH.kids4]]

            elif k == "career":
                temp = [x for x in need if "job" in x]
                lst = database.db_session.scalars(select(database.Career.title)).all()
                chosen = randomize(lst, num=v, inputs=inputs)
                
                for i in range(len(temp)):
                    MASH[temp[i]].data = chosen[i]
                [MASHOPTS.append(game.MashOption("career", x.data)) for x in [MASH.job1, MASH.job2, MASH.job3, MASH.job4]]
        
            elif k == "vehicle":
                temp = [x for x in need if "car" in x]
                lst = database.db_session.scalars(select(database.Vehicle)).all()
                chosen = [f"{x.desc} {x.make} {x.model}" if x.desc != "" else f"{x.make} {x.model}" for x in randomize(lst, v)]
                
                for i in range(len(temp)):
                    MASH[temp[i]].data = chosen[i]
                [MASHOPTS.append(game.MashOption("vehicle", x.data)) for x in [MASH.car1, MASH.car2, MASH.car3, MASH.car4]]

            elif k == "salary":
                temp = [x for x in need if "money" in x]
                lst = database.db_session.scalars(select(database.Salary.amount)).all()
                chosen = randomize(lst, num=v, inputs=inputs)
                
                for i in range(len(temp)):
                    # format here ? until formatting added to table
                    MASH[temp[i]].data = f"${chosen[i]:,.2f}"
                [MASHOPTS.append(game.MashOption("salary", x.data)) for x in [MASH.money1, MASH.money2, MASH.money3, MASH.money4]]
        return redirect(url_for('play_mash'))
    
@app.route("/play", methods=["GET","POST"])
def play_mash():
    global MASH 
    if request.method == "GET":
        return render_template("start.html", form=MASH)
    else:
        MASH = MashForm()
        spins = MASH.spun.data
        playing = game.Game(MASHOPTS, spins)
        playing.run()
        return render_template("result.html", options=MASHOPTS, selected=playing.final, spins=spins)
         
@app.get("/add")
def add_home():
    return render_template("add_index.html")

@app.route("/add-<kind>", methods=["GET", "POST"])
def add_option(kind):
    if request.method == "GET":
        if kind.lower() == "spouse":
            form = SpouseForm()
        elif kind.lower() == "career":
            form = CareerForm()
        elif kind.lower() == "vehicle":
            form = CarForm() 
        elif kind.lower() == "salary":
            form = SalaryForm() 
        return render_template("add_item.html", form=form)
    elif request.method == "POST":
        if kind.lower() == "spouse":
            new = database.Spouse(name=request.form["name"],
                                  sex = request.form["sex"])
        elif kind.lower() == "career":
            new = database.Career(title=request.form["job"])
        elif kind.lower() == "vehicle":
            new = database.Vehicle(make=request.form["make"],
                                   model=request.form["model"],
                                   desc=request.form["year"])
        elif kind.lower() == "salary":
            new = database.Salary(amount=request.form["money"])
        database.db_session.add(new)
        database.db_session.commit()
        return redirect(url_for("add_option", kind=kind))
        
     

if __name__ == "__main__":

    app.run()
