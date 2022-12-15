import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = [x for x in request.form.values()]
    final_features = []
    final_features.append(int(features[0]))
    final_features.append(float(features[1]))
    final_features.append(int(features[2]))
    if features[3] == 'male':
        final_features.append(0)
        final_features.append(1)
    else:
        final_features.append(1)
        final_features.append(0)
    if features[4] == 'yes':
        final_features.append(0)
        final_features.append(1)
    else:
        final_features.append(1)
        final_features.append(0)
    
    final_features = [np.array(final_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Health Insurance could be $ {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)