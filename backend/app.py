# backend/app.py - FINAL, PRODUCTION-READY BACKEND WITH CORS

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # <-- 1. IMPORT THE LIBRARY
import joblib
import pandas as pd
import numpy as np # <-- Make sure numpy is imported for the summary endpoint
import google.generativeai as genai
import os
import base64
from math import radians, cos, sin, asin, sqrt

# --- SETUP ---
app = Flask(__name__)
CORS(app)  # <-- 2. ENABLE CORS FOR YOUR ENTIRE FLASK APP

# --- LOAD MODELS AND CONFIGURE AI ---
try:
    lgbm_model = joblib.load('aquasense_classifier.pkl')
    print("✅ LightGBM classifier loaded successfully.")
except Exception as e:
    print(f"❌ Error loading LightGBM model: {e}")
    lgbm_model = None

try:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'Your API')
    if 'YOUR_API_KEY_HERE' in GEMINI_API_KEY:
        print("⚠️ WARNING: Gemini API key not set. AI advisory features will be disabled.")
        gemini_model, vision_model = None, None
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash') # Using stable versions
        vision_model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Gemini text and vision models configured successfully.")
except Exception as e:
    print(f"❌ Error configuring Gemini AI: {e}")
    gemini_model, vision_model = None, None

# --- HELPER FUNCTIONS ---
# (Your helper functions like create_gemini_prompt and haversine remain unchanged)
def create_gemini_prompt(prediction, confidence, data):
    return f"""Act as a public health expert in Haiti. Analyze this water sample data and provide a clear, simple, and actionable advisory in markdown.

    **Data:**
    - AI Model Prediction: **{prediction}**
    - AI Model Confidence: **{confidence[prediction]:.2f}%**
    - Key Sensor Values: pH: {data.get('ph', 'N/A')}, Turbidity: {data.get('Turbidity', 'N/A')} NTU, Solids: {data.get('Solids', 'N/A')} mg/L

    **Response Structure:**
    ### Simple Summary:
    ### Recommended Actions (How to Control & Prevent):
    ### Permitted Uses (What purpose we can use the water):
    ### Important Note:
    """

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 6371

# --- IN-MEMORY DATABASE (For Demo) ---
# (Your sample_water_points list remains unchanged)
sample_water_points = [
    {"id": 1, "name": "Community Well - Cité Soleil", "lat": 18.5794, "lon": -72.3375, "status": "Not Potable", "verified": False, "history": {"Sulfate": [380, 385, 392, 405], "Turbidity": [5.1, 5.3, 5.2, 5.8]}},
    {"id": 2, "name": "Verified NGO Tap - Pétion-Ville", "lat": 18.5135, "lon": -72.2852, "status": "Potable", "verified": True, "history": {"Sulfate": [330, 332, 331, 334], "Turbidity": [3.1, 3.0, 3.2, 3.1]}},
    {"id": 3, "name": "River Outlet - Mariani", "lat": 18.5020, "lon": -72.3995, "status": "Potable", "verified": False, "history": {"Sulfate": [340, 338, 342, 345], "Turbidity": [3.8, 3.9, 3.7, 4.0]}}
]


# --- FLASK ROUTES ---
# (Your existing routes like '/', '/api/water_points', '/predict', '/analyze_image' remain unchanged)
@app.route('/')
def home():
    return "AquaLERT Backend is running."

@app.route('/api/water_points')
def get_water_points():
    return jsonify(sample_water_points)

@app.route('/predict', methods=['POST'])
def predict():
    if not lgbm_model: return jsonify({'error': 'Prediction model is not loaded'}), 500
    try:
        data = request.get_json()
        features = pd.DataFrame(data, index=[0])
        lgbm_pred = lgbm_model.predict(features)[0]
        lgbm_proba = lgbm_model.predict_proba(features)[0]
        
        prediction_text = 'Potable' if lgbm_pred == 1 else 'Not Potable'
        confidence = {'Not Potable': lgbm_proba[0], 'Potable': lgbm_proba[1]}
        
        alert_message = None
        if prediction_text == 'Not Potable' and data.get('lat') and data.get('lon'):
            lat, lon = float(data['lat']), float(data['lon'])
            for point in sample_water_points:
                dist = haversine(lon, lat, point['lon'], point['lat'])
                if point['status'] == 'Potable' and dist < 5:
                    point['status'] = 'Caution'
                    alert_message = f"PROACTIVE ALERT: A new unsafe source was reported nearby. The status of '{point['name']}' has been changed to 'Caution' on the map. Please re-test before use."
                    break

        gemini_advice = "AI advisory is currently unavailable."
        if gemini_model:
            prompt = create_gemini_prompt(prediction_text, confidence, data)
            gemini_response = gemini_model.generate_content(prompt)
            gemini_advice = gemini_response.text

        return jsonify({
            'prediction': prediction_text,
            'confidence': {k: round(v * 100, 2) for k, v in confidence.items()},
            'gemini_advice': gemini_advice,
            'alert_message': alert_message
        })
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 400

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if not vision_model: return jsonify({'error': 'Vision model not available.'}), 500
    try:
        data = request.get_json()
        if 'image' not in data: return jsonify({'error': 'No image data provided.'}), 400
        image_b64 = data['image'].split(',')[1]
        image_parts = [{"mime_type": "image/jpeg", "data": base64.b64decode(image_b64)}]
        
        prompt = "You are a water safety expert. Analyze this image for visual signs of contamination (turbidity, color, particles, oil). Provide a cautious, preliminary assessment in markdown including ### Visual Assessment, ### Potential Risks, and an ### URGENT RECOMMENDATION."
        response = vision_model.generate_content([prompt, *image_parts])
        return jsonify({'analysis': response.text})
    except Exception as e:
        return jsonify({'error': f"Error during visual analysis: {str(e)}"}), 500

# --- THE NEW ENDPOINT FOR THE DASHBOARD ---
@app.route('/api/community_summary')
def get_community_summary():
    """Provides aggregated data for the Streamlit dashboard."""
    try:
        # In a real app, this would query a database. Here, we simulate it.
        regions = ['Ouest', 'Artibonite', 'Nord', 'Sud-Est', 'Grand-Anse']
        num_records = 200
        
        simulated_data = {
            'timestamp': pd.to_datetime(np.random.choice(pd.date_range('2024-03-01', '2024-05-20'), num_records)),
            'region': np.random.choice(regions, num_records, p=[0.4, 0.2, 0.2, 0.1, 0.1]),
            'sulfate': np.random.uniform(250, 450, num_records),
            'prediction': np.random.choice([0, 1], num_records, p=[0.4, 0.6]) # 0=Unsafe, 1=Safe
        }
        df = pd.DataFrame(simulated_data)
        df['prediction_label'] = df['prediction'].apply(lambda x: 'Safe' if x == 1 else 'Unsafe')
        
        # Convert DataFrame to JSON format that's easy to use
        return df.to_json(orient='records', date_format='iso')
    except Exception as e:
        return jsonify({'error': f"Error generating summary data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
