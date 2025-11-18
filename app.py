from flask import Flask, render_template, request, redirect, url_for, flash
import requests
app = Flask(__name__)
app.config["SECRET_KEY"] = "una_clave_muy_larga_y_dificil_de_adivinar"

API_KEY = "KEt2KxXrP5arcpqYARbhnpuR2wrD2UlzH6IGTnxb"

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/buscar", methods=["POST"])
def search():
    alimento = request.form.get("alimento", "").strip().lower()

    if not alimento:
        flash("Por favor, ingresa un alimento para buscar.", "error")
        return redirect(url_for("base"))

    try:
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}&query={alimento}"
        resp = requests.get(url)

        if resp.status_code != 200:
            flash("Error en la comunicación con USDA. Intenta nuevamente.", "error")
            return redirect(url_for("base"))

        datos = resp.json()

        if "foods" not in datos or len(datos["foods"]) == 0:
            flash(f"No se encontraron resultados para '{alimento}'.", "error")
            return redirect(url_for("base"))

   
        food = datos["foods"][0]

        alimento_info = {
            "description": food.get("description", "Sin descripción"),
            "fdcId": food.get("fdcId", "Desconocido"),
            "brand": food.get("brandOwner", "Desconocida"),
            "ingredients": food.get("ingredients", "No especificados"),
            "nutrients": [
                {
                    "name": n["nutrientName"],
                    "value": n.get("value", 0),
                    "unit": n.get("unitName", "")
                }
                for n in food.get("foodNutrients", [])
            ]
        }

        return render_template("alimento.html", alimento=alimento_info)

    except requests.exceptions.RequestException:
        flash("Error al consultar la API USDA.", "error")
        return redirect(url_for("base"))

if __name__ == "__main__":
    app.run(debug=True)
