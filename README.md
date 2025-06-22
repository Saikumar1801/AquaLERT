# AquaLERT: AI-Powered Water Intelligence for a Safer Haiti

![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)


![alt text](https://img.shields.io/badge/python-3.9+-blue.svg)


![alt text](https://img.shields.io/badge/Frontend-Streamlit-red.svg)


![alt text](https://img.shields.io/badge/Backend-Flask-black.svg)


![alt text](https://img.shields.io/badge/Built%20for-%23Hack4Haiti-brightgreen.svg)

**Our Mission:** To empower communities, NGOs, and public health officials in Haiti with accessible, real-time, AI-driven data to ensure water safety and prevent waterborne diseases.

AquaLERT is an end-to-end water quality monitoring and analysis platform built for the #Hack4Haiti initiative. It combines machine learning, computer vision, and generative AI to provide instant, actionable insights on water potability, bridging the critical information gap that endangers millions.

## 🌪️ The Critical Challenge

In Haiti, over 4 million people lack access to a basic water source, and waterborne diseases remain a leading cause of mortality. The primary barriers to ensuring water safety are:

💰 Cost & Accessibility: Traditional laboratory testing is prohibitively expensive (50−200 per sample) and inaccessible to remote communities.

⏰ Time Delay: Lab results can take days or weeks, while contaminated water can cause illness within hours.

📊 Data Gap: Public health officials lack the real-time, high-level data needed to identify contamination hotspots, predict outbreaks, and allocate resources effectively.

## ✨ Our Solution: The Three Pillars of AquaLERT

AquaLERT tackles this challenge with a comprehensive, three-pillar solution:

### 1. 🔬 Instant Field Testing

ML-Powered Predictions: Uses a highly-tuned LightGBM model to predict water potability from low-cost sensor data with high accuracy.

Immediate Results: Provides a clear "Potable" or "Not Potable" verdict in under 30 seconds.

Offline Capability: Designed to work in remote areas with limited connectivity.

### 2. 🤖 AI-Powered Advisory

Google Gemini Integration: Translates complex data into clear, actionable public health advice.

Multilingual Support: Delivers recommendations in both English and Haitian Creole to ensure accessibility for all users.

Contextual Guidance: Provides specific instructions for treating water, securing sources, and long-term planning.

### 3. 🌍 Community Monitoring

Live Interactive Map: Every test is geotagged and contributes to a live map, creating a crowdsourced water quality network.

Hotspot Detection: Empowers NGOs and health officials to identify high-risk areas and deploy resources efficiently.

Data-Driven Dashboards: Provides aggregated statistics and trend analysis for strategic planning and impact assessment.

## 🔧 How It Works: System Architecture

AquaLERT follows a simple yet powerful four-step data flow:

Collect Data: A user in the field inputs sensor readings or uploads a photo of a water sample via the Streamlit frontend.

AI Analysis: The Flask backend receives the data.

For sensor data, the pre-trained LightGBM model makes a potability prediction.

For images, a computer vision model provides a preliminary visual assessment.

Get Results: The model's output is passed to the Google Gemini API, which generates a detailed, multilingual advisory. This complete report is sent back to the user.

Share Impact: The geotagged result is saved to a central database, instantly updating the Live Water Map and community dashboards.

## 🛠️ Technology Stack
Category	Technologies
Frontend	Streamlit, Folium, Plotly, Pandas
Backend	Flask, Python
ML & AI	Scikit-learn, LightGBM, Prophet (for forecasting), Computer Vision (e.g., TensorFlow/PyTorch), Google Gemini API
Database	SQLite (for development), PostgreSQL (for production)
Deployment	Docker, Render / Heroku / AWS Elastic Beanstalk
## 🚀 Getting Started

Follow these instructions to set up and run the AquaLERT platform on your local machine.

### Prerequisites

Python 3.9 or higher

pip package manager

Git

Installation & Setup

Clone the repository:

Generated bash
git clone https://github.com/your-username/aqualert.git
cd aqualert


Set up the Python virtual environment:

Generated bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Install dependencies:
The project is split into a frontend and backend. Install requirements for both.

Generated bash
# Install backend requirements
pip install -r backend/requirements.txt

# Install frontend requirements
pip install -r frontend/requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Set up environment variables:
You will need an API key for Google Gemini.

Create a file named .env inside the backend directory: backend/.env

Add your API key to this file:

Generated code
GEMINI_API_KEY="YOUR_API_KEY_HERE"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
Running the Application

You need to run two separate processes in two different terminals.

Run the Flask Backend:

Generated bash
# In your first terminal
cd backend
flask run
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

The backend server will start, typically on http://127.0.0.1:5000.

Run the Streamlit Frontend:

Generated bash
# In your second terminal
cd frontend
streamlit run Home.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

The Streamlit application will open in your web browser, usually at http://localhost:8501.

You can now interact with the full AquaLERT platform!

📂 Project Structure
Generated code
aqualert/
├── backend/
│   ├── app.py                # Flask application logic and API endpoints
│   ├── models/
│   │   └── potability_model.pkl # Pre-trained LightGBM model
│   ├── .env                    # Environment variables (API keys)
│   └── requirements.txt        # Backend Python dependencies
│
├── frontend/
│   ├── Home.py                 # Main landing page for the Streamlit app
│   ├── pages/
│   │   ├── 1_Live_Water_Map.py # The interactive map page
│   │   ├── 2_Real-Time_Test.py # The sensor data input and analysis page
│   │   └── 3_Visual_Analysis.py# The image upload and analysis page
│   └── requirements.txt        # Frontend Python dependencies
│
├── notebooks/
│   ├── 1_Data_Exploration.ipynb # EDA on the water quality dataset
│   ├── 2_Model_Training.ipynb   # Final model training and evaluation
│   └── 3_Forecasting_POC.ipynb  # Prophet forecasting proof-of-concept
│
├── .gitignore
└── README.md
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
👥 Team & Acknowledgements

[Your Name] - Project Lead & Backend/ML Developer

[Team Member 2 Name] - Frontend Developer

[Team Member 3 Name] - Data Scientist & UI/UX

We would like to thank the organizers of #Hack4Haiti for this incredible opportunity to work on a project with meaningful social impact. We also acknowledge the public datasets from Kaggle that made our initial model training possible.
