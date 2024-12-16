from base64 import b64decode
import os

import random
from MonsterLab import Monster
from flask import Flask, render_template, request
from pandas import DataFrame
from datetime import datetime
from app.data import Database
from app.graph import chart
from app.machine import Machine

SPRINT = 3
APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data")
def data():
    if SPRINT < 1:
        return render_template("data.html")
    db = Database()
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    if SPRINT < 2:
        return render_template("view.html")
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]
    graph = chart(
        df=db.dataframe(),
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()
    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )


@APP.route("/model", methods=["GET", "POST"])
def model():
    if SPRINT < 3:
        return render_template("model.html")
    
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    filepath = os.path.join("app", "model.joblib")

    
    if not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)
    
    # Generate input data
    stats = [round(random.uniform(1, 250), 2) for _ in range(3)]
    level = request.values.get("level", type=int) or random.randint(1, 20)
    health = request.values.get("health", type=float) or stats.pop()
    energy = request.values.get("energy", type=float) or stats.pop()
    sanity = request.values.get("sanity", type=float) or stats.pop()
    
   
    input_data = DataFrame(
        [dict(zip(options, (level, health, energy, sanity)))]
    )
    
  
    prediction, confidence = machine(input_data)
    
  
    formatted_confidence = f"{float(confidence[0].max()):.2%}"

 
    info = machine.info()
    formatted_info = {
        "base_model": info["model_type"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
        "train_accuracy": f"{info['train_accuracy']:.0%}",
        "test_accuracy": f"{info['test_accuracy']:.0%}",
        "features": ", ".join(info["features"]),
    }
    
    return render_template(
        "model.html",
        info=formatted_info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction[0],  
        confidence=formatted_confidence,  
    )


if __name__ == '__main__':
    APP.run()
