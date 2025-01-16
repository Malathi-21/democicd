from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
# Load the pre-trained model
filename = 'final_model_sales.sav'
model = pickle.load(open(filename, 'rb'))

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input features from form
        tenure = int(request.form['tenure'])
        MonthlyCharges = float(request.form['MonthlyCharges'])
        TotalCharges = float(request.form['TotalCharges'])
        OnlineSecurity_Yes = float(request.form['OnlineSecurity_Yes'])
        Contract_Two_year = float(request.form['Contract_Two_year'])

        # Format the input data into a numpy array
        input_data = np.array([[tenure, MonthlyCharges, TotalCharges, OnlineSecurity_Yes, Contract_Two_year]])

        # Make prediction using the loaded model
        prediction = model.predict(input_data)
        print(prediction)
        # Map prediction to result
        result = 'Churn Predicted' if prediction[0] == 1 else 'No Churn'
        #result=prediction
        print(result)

        return render_template('output.html', result=result)
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)  # Bind to 0.0.0.0
