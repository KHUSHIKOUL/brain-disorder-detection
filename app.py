from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

# Load model
model = joblib.load("model.pkl")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        name = request.form['name']
        age = int(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        glucose = float(request.form['glucose'])
        bmi = float(request.form['bmi'])

        # Prediction
        prediction = model.predict([[age, hypertension, heart_disease, glucose, bmi]])

        # Probability (Confidence)
        probability = model.predict_proba([[age, hypertension, heart_disease, glucose, bmi]])

        confidence = round(probability[0][prediction[0]] * 100, 2)

        risk = "High" if prediction[0] == 1 else "Low"

        return render_template("result.html",
                               name=name,
                               age=age,
                               risk=risk,
                               confidence=confidence)

    return render_template("index.html")

print("Running from:", os.getcwd())
if __name__ == '__main__':
    app.run(debug=True)