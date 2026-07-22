from flask import Flask, jsonify, request
from flask_cors import CORS

from world_bank import get_countries, get_country_summary

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return {
        "message": "Global Insights API funcionando 🚀"
    }


@app.route("/countries")
def countries():

    try:

        countries = get_countries()

        return jsonify(countries)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/compare")
def compare():

    country1 = request.args.get("country1")
    country2 = request.args.get("country2")

    if not country1 or not country2:

        return jsonify({
            "error": "Debe indicar country1 y country2"
        }), 400

    try:

        data = {
            "country1": get_country_summary(country1),
            "country2": get_country_summary(country2)
        }

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
    
