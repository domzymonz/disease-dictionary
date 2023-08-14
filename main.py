from flask import Flask, render_template, request, jsonify, redirect, url_for
from gpt_text_parser import retrieve_information
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    return render_template("search.html",
        form = {
            "navbar-invisible": True,
            "class": "long"
        }
    )

@app.route("/disease", methods=["POST", "GET"])
def disease_information():
    disease = request.form.get("disease")
    if disease in ["", None]:
        return render_template("error.html",
        form = {
            "navbar-invisible": True,
            "class": "long"
        },
        text = {
            "heading": "There's... nothing.",
            "description": "You haven't asked for anything."
        })
    else:
        result = json.loads(retrieve_information(disease))
        jsonify(result)
        print(result)
        if result["existing"] == 0:
            return render_template("error.html",
            form = {
                "navbar-invisible": True,
                "class": "long"
            },
            text = {
                "heading": "What do you mean?",
                "description": "That search doesn't mean anything..."
            })
        else:
            return render_template("disease.html", result = result, title=f"{result['name']} - Disease Dictionary")

if __name__ =='__main__':
    app.run()