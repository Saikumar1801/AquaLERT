# frontend/pages/2_🔬_Real-Time_Test.py
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import time

# Configuration
FLASK_BACKEND_URL = "http://127.0.0.1:5000"

# Page Configuration
st.set_page_config(
    page_title="AquaLERT Real-Time Test",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .test-form {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e8ed;
        margin-bottom: 2rem;
    }
    
    .result-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .safe-result {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .unsafe-result {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .parameter-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border: 1px solid #e1e8ed;
    }
    
    .alert-banner {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    
    .info-tooltip {
        color: #666;
        font-size: 0.8em;
        font-style: italic;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔬 Real-Time Water Quality Analysis</h1>
    <p>Advanced AI-powered water testing with instant results and professional advisory</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.header("🔍 Testing Information")
    st.markdown("### Parameters Analyzed")
    st.markdown("""
    - **pH Level**: Acidity/Alkalinity measure
    - **Hardness**: Mineral content indicator
    - **Total Dissolved Solids**: Purity measure
    - **Chloramines**: Disinfection byproducts
    - **Sulfate**: Mineral content
    - **Conductivity**: Electrical conductivity
    - **Organic Carbon**: Organic matter content
    - **Trihalomethanes**: Chemical compounds
    - **Turbidity**: Water clarity measure
    """)
    st.markdown("---")
    st.header("📊 Quick Presets")
    if st.button("🏠 Typical Tap Water"): st.session_state.preset = "tap_water"
    if st.button("🏔️ Mountain Spring"): st.session_state.preset = "spring_water"
    if st.button("🏭 Industrial Area"): st.session_state.preset = "industrial_water"
    if st.button("🌊 Coastal Region"): st.session_state.preset = "coastal_water"
    st.markdown("---")
    st.info("💡 **Tip**: Use presets to quickly load typical values for different water sources.")

# === FIX 1: Ensure all numeric values are floats ===
PARAMETERS = {
    "ph": {"min": 0.0, "max": 14.0, "safe_min": 6.5, "safe_max": 8.5, "unit": "", "desc": "Measure of acidity/alkalinity"},
    "Hardness": {"min": 0.0, "max": 500.0, "safe_min": 60.0, "safe_max": 120.0, "unit": "mg/L", "desc": "Calcium and magnesium content"},
    "Solids": {"min": 0.0, "max": 50000.0, "safe_min": 0.0, "safe_max": 500.0, "unit": "ppm", "desc": "Total dissolved solids"},
    "Chloramines": {"min": 0.0, "max": 15.0, "safe_min": 0.5, "safe_max": 4.0, "unit": "ppm", "desc": "Disinfection byproducts"},
    "Sulfate": {"min": 0.0, "max": 1000.0, "safe_min": 0.0, "safe_max": 250.0, "unit": "mg/L", "desc": "Sulfate mineral content"},
    "Conductivity": {"min": 0.0, "max": 2000.0, "safe_min": 50.0, "safe_max": 800.0, "unit": "μS/cm", "desc": "Electrical conductivity"},
    "Organic_carbon": {"min": 0.0, "max": 30.0, "safe_min": 0.0, "safe_max": 4.0, "unit": "ppm", "desc": "Total organic carbon"},
    "Trihalomethanes": {"min": 0.0, "max": 200.0, "safe_min": 0.0, "safe_max": 80.0, "unit": "μg/L", "desc": "Chemical compounds"},
    "Turbidity": {"min": 0.0, "max": 10.0, "safe_min": 0.0, "safe_max": 1.0, "unit": "NTU", "desc": "Water clarity measure"}
}

PRESETS = {
    "tap_water": {"ph": 7.2, "Hardness": 150.0, "Solids": 200.0, "Chloramines": 2.5, "Sulfate": 180.0, "Conductivity": 350.0, "Organic_carbon": 8.0, "Trihalomethanes": 45.0, "Turbidity": 0.5},
    "spring_water": {"ph": 7.8, "Hardness": 85.0, "Solids": 120.0, "Chloramines": 0.8, "Sulfate": 20.0, "Conductivity": 150.0, "Organic_carbon": 2.0, "Trihalomethanes": 10.0, "Turbidity": 0.1},
    "industrial_water": {"ph": 6.8, "Hardness": 280.0, "Solids": 450.0, "Chloramines": 8.5, "Sulfate": 380.0, "Conductivity": 650.0, "Organic_carbon": 18.0, "Trihalomethanes": 95.0, "Turbidity": 2.8},
    "coastal_water": {"ph": 8.1, "Hardness": 320.0, "Solids": 380.0, "Chloramines": 3.2, "Sulfate": 290.0, "Conductivity": 580.0, "Organic_carbon": 12.0, "Trihalomethanes": 65.0, "Turbidity": 1.2}
}

if 'preset' in st.session_state:
    preset_values = PRESETS[st.session_state.preset]
    for key, value in preset_values.items():
        st.session_state[f"param_{key}"] = float(value) # Ensure preset value is float
    del st.session_state.preset

def get_safety_indicator(param_name, value):
    param_info = PARAMETERS[param_name]
    if param_info["safe_min"] <= value <= param_info["safe_max"]:
        return "🟢 Normal", "safe"
    elif value < param_info["safe_min"]:
        return "🟡 Low", "warning"
    else:
        return "🔴 High", "danger"

def create_parameter_radar_chart(input_data):
    categories, values, safe_ranges = [], [], []
    for param, value in input_data.items():
        if param in PARAMETERS:
            categories.append(param.replace('_', ' ').title())
            param_info = PARAMETERS[param]
            normalized_value = (value / param_info["max"]) * 100
            values.append(normalized_value)
            safe_max_norm = (param_info["safe_max"] / param_info["max"]) * 100
            safe_ranges.append(safe_max_norm)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=safe_ranges, theta=categories, fill='toself', name='Safe Range', line_color='green', fillcolor='rgba(0, 255, 0, 0.1)'))
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name='Current Values', line_color='blue', fillcolor='rgba(0, 0, 255, 0.1)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, title="Parameter Analysis Overview", height=500)
    return fig

st.markdown("## 📋 Enter Water Sample Parameters")

with st.form("prediction_form"):
    st.markdown("### 🌡️ Physical Properties")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        ph = st.number_input("pH Level", min_value=PARAMETERS["ph"]["min"], max_value=PARAMETERS["ph"]["max"], value=st.session_state.get("param_ph", 7.0), step=0.1, key="param_ph", help="Measure of water acidity/alkalinity (6.5-8.5 is ideal)")
        indicator, _ = get_safety_indicator("ph", ph)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        turbidity = st.number_input("Turbidity (NTU)", min_value=PARAMETERS["Turbidity"]["min"], max_value=PARAMETERS["Turbidity"]["max"], value=st.session_state.get("param_Turbidity", 4.0), step=0.1, key="param_Turbidity", help="Water clarity measure (lower is better)")
        indicator, _ = get_safety_indicator("Turbidity", turbidity)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        conductivity = st.number_input("Conductivity (μS/cm)", min_value=PARAMETERS["Conductivity"]["min"], max_value=PARAMETERS["Conductivity"]["max"], value=st.session_state.get("param_Conductivity", 420.0), step=10.0, key="param_Conductivity", help="Electrical conductivity measure")
        indicator, _ = get_safety_indicator("Conductivity", conductivity)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### ⚗️ Chemical Properties")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        hardness = st.number_input("Hardness (mg/L)", min_value=PARAMETERS["Hardness"]["min"], max_value=PARAMETERS["Hardness"]["max"], value=st.session_state.get("param_Hardness", 195.0), step=5.0, key="param_Hardness", help="Mineral content (calcium and magnesium)")
        indicator, _ = get_safety_indicator("Hardness", hardness)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        solids = st.number_input("Total Dissolved Solids (ppm)", min_value=PARAMETERS["Solids"]["min"], max_value=PARAMETERS["Solids"]["max"], value=st.session_state.get("param_Solids", 20000.0), step=100.0, key="param_Solids", help="Total dissolved solids content")
        indicator, _ = get_safety_indicator("Solids", solids)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        sulfate = st.number_input("Sulfate (mg/L)", min_value=PARAMETERS["Sulfate"]["min"], max_value=PARAMETERS["Sulfate"]["max"], value=st.session_state.get("param_Sulfate", 330.0), step=10.0, key="param_Sulfate", help="Sulfate mineral content")
        indicator, _ = get_safety_indicator("Sulfate", sulfate)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🧪 Contaminants & Additives")
    col7, col8, col9 = st.columns(3)
    with col7:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        chloramines = st.number_input("Chloramines (ppm)", min_value=PARAMETERS["Chloramines"]["min"], max_value=PARAMETERS["Chloramines"]["max"], value=st.session_state.get("param_Chloramines", 7.0), step=0.1, key="param_Chloramines", help="Disinfection byproducts")
        indicator, _ = get_safety_indicator("Chloramines", chloramines)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col8:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        organic_carbon = st.number_input("Organic Carbon (ppm)", min_value=PARAMETERS["Organic_carbon"]["min"], max_value=PARAMETERS["Organic_carbon"]["max"], value=st.session_state.get("param_Organic_carbon", 14.0), step=0.5, key="param_Organic_carbon", help="Total organic carbon content")
        indicator, _ = get_safety_indicator("Organic_carbon", organic_carbon)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col9:
        st.markdown('<div class="parameter-card">', unsafe_allow_html=True)
        trihalomethanes = st.number_input("Trihalomethanes (μg/L)", min_value=PARAMETERS["Trihalomethanes"]["min"], max_value=PARAMETERS["Trihalomethanes"]["max"], value=st.session_state.get("param_Trihalomethanes", 65.0), step=1.0, key="param_Trihalomethanes", help="Chemical compounds from disinfection")
        indicator, _ = get_safety_indicator("Trihalomethanes", trihalomethanes)
        st.markdown(f"<div class='info-tooltip'>Status: {indicator}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    col_options1, col_options2 = st.columns(2)
    with col_options1: location = st.text_input("📍 Sample Location (Optional)", placeholder="e.g., Kitchen tap, Well, etc.")
    with col_options2: sample_source = st.selectbox("🚰 Water Source", ["Tap Water", "Well Water", "Bottled Water", "Spring Water", "Other"], index=0)

    # === FIX 2: Move the submit button INSIDE the form block ===
    submitted = st.form_submit_button("🔬 Analyze Water Sample", use_container_width=True)

if submitted:
    input_data = {"ph": ph, "Hardness": hardness, "Solids": solids, "Chloramines": chloramines, "Sulfate": sulfate, "Conductivity": conductivity, "Organic_carbon": organic_carbon, "Trihalomethanes": trihalomethanes, "Turbidity": turbidity}
    
    with st.spinner("🔄 Analyzing water sample with AI... Please wait."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        try:
            response = requests.post(f"{FLASK_BACKEND_URL}/predict", json=input_data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                progress_bar.empty()
                st.markdown("## 📊 Analysis Results")
                prediction = result.get('prediction', 'N/A')
                confidence = result.get('confidence', {})
                if prediction == 'Potable':
                    st.markdown('<div class="safe-result"><h2>✅ WATER IS SAFE TO DRINK</h2><p>The analysis indicates this water sample meets safety standards for consumption.</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="unsafe-result"><h2>⚠️ WATER MAY NOT BE SAFE</h2><p>The analysis indicates potential safety concerns with this water sample.</p></div>', unsafe_allow_html=True)
                
                st.markdown("### 🎯 Confidence Analysis")
                col_conf1, col_conf2 = st.columns(2)
                with col_conf1:
                    potable_conf = confidence.get('Potable', 0.0)
                    st.markdown(f"""<div style="background:#f8f9fa;padding:1rem;border-radius:8px;"><h4 style="color:#28a745;">🟢 Safe Water Confidence</h4><div style="font-size:2em;font-weight:bold;">{potable_conf:.1f}%</div></div>""", unsafe_allow_html=True)
                with col_conf2:
                    unsafe_conf = confidence.get('Not Potable', 100.0 - potable_conf)
                    st.markdown(f"""<div style="background:#f8f9fa;padding:1rem;border-radius:8px;"><h4 style="color:#dc3545;">🔴 Unsafe Water Confidence</h4><div style="font-size:2em;font-weight:bold;">{unsafe_conf:.1f}%</div></div>""", unsafe_allow_html=True)

                st.markdown("### 📈 Parameter Analysis")
                radar_chart = create_parameter_radar_chart(input_data)
                st.plotly_chart(radar_chart, use_container_width=True)
                
                st.markdown("### 🔍 Detailed Parameter Assessment")
                params_list = []
                for param, value in input_data.items():
                    if param in PARAMETERS:
                        param_info = PARAMETERS[param]
                        indicator, _ = get_safety_indicator(param, value)
                        params_list.append({"Parameter": param.replace('_', ' ').title(), "Value": f"{value} {param_info['unit']}", "Safe Range": f"{param_info['safe_min']}-{param_info['safe_max']} {param_info['unit']}", "Status": indicator})
                st.dataframe(pd.DataFrame(params_list), use_container_width=True, hide_index=True)
                
                st.markdown("### 🤖 AI Public Health Advisory")
                advisory_text = result.get('gemini_advice', 'No advisory available.')
                st.markdown(f'<div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;padding:1.5rem;border-radius:10px;"><h4>🎯 Professional Recommendation</h4><p>{advisory_text}</p></div>', unsafe_allow_html=True)
                
                if result.get('alert_message'):
                    st.markdown(f'<div class="alert-banner"><h4>🚨 Important Notice</h4><p>{result["alert_message"]}</p></div>', unsafe_allow_html=True)
                
                st.markdown("### 📥 Export Results")
                export_data = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "prediction": prediction, "confidence_safe": potable_conf, "location": location, "source": sample_source, **input_data}
                st.download_button("📄 Download JSON Report", json.dumps(export_data, indent=2), f"water_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "application/json")
                st.download_button("📊 Download CSV Data", pd.DataFrame([export_data]).to_csv(index=False), f"water_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "text/csv")
            else:
                st.error(f"❌ Server Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to the backend. Please ensure the Flask server is running.")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #666; padding: 2rem;"><p>🔬 AquaLERT Real-Time Water Quality Analysis</p><p>Powered by Advanced AI & Machine Learning</p></div>', unsafe_allow_html=True)