# frontend/Home.py
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="AquaLERT - Water Intelligence Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS Styling ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2a5298;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .impact-metric {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    .tech-badge {
        display: inline-block;
        background: #f0f2f6;
        color: #1f2937;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem 0.5rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #2a5298, #4CAF50, #2a5298);
        border: none;
        border-radius: 2px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="main-header">
    <h1>💧 AquaLERT</h1>
    <h2>Water Intelligence for a Safer Haiti</h2>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        Empowering communities with real-time AI-powered water safety analysis
    </p>
</div>
""", unsafe_allow_html=True)

# --- Key Statistics Section ---
st.markdown("""
<div class="stats-container">
    <h3>Our Impact</h3>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 1rem;">
        <div class="impact-metric">
            <h2>🎯</h2>
            <h4>95%+ Accuracy</h4>
            <p>ML Model Precision</p>
        </div>
        <div class="impact-metric">
            <h2>⚡</h2>
            <h4>< 30 Seconds</h4>
            <p>Real-time Analysis</p>
        </div>
        <div class="impact-metric">
            <h2>🌍</h2>
            <h4>Community-Driven</h4>
            <p>Collaborative Monitoring</p>
        </div>
        <div class="impact-metric">
            <h2>💡</h2>
            <h4>AI-Powered</h4>
            <p>Smart Recommendations</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Problem Statement with Visual Appeal ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

col_prob1, col_prob2 = st.columns([2, 1])

with col_prob1:
    st.markdown("## 🚨 The Critical Challenge")
    st.markdown("""
    <div style="background: #fef2f2; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ef4444;">
        <p style="font-size: 1.1rem; line-height: 1.6; margin: 0;">
            <strong>2.2 billion people</strong> worldwide lack access to safely managed drinking water. 
            In Haiti, <strong>waterborne diseases</strong> remain a leading cause of mortality, 
            with traditional testing methods being <strong>slow, expensive, and inaccessible</strong> 
            to vulnerable communities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Why This Matters")
    st.write("""
    - ⏰ **Time-Critical:** Contaminated water can cause illness within hours
    - 💰 **Cost Barrier:** Traditional lab tests cost $50-200 per sample
    - 📍 **Accessibility:** Remote communities lack testing infrastructure
    - 📊 **Data Gap:** No real-time monitoring systems for public health officials
    """)

with col_prob2:
    st.markdown("### Quick Facts")
    st.info("""
    🇭🇹 **Haiti Water Crisis:**
    - Only 69% have basic water access
    - Cholera outbreaks linked to water
    - Limited laboratory infrastructure
    - Need for rapid field testing
    """)

# --- Solution Overview ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("## 🎯 Our Three-Pillar Solution")

# Enhanced solution columns with better visual hierarchy
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">🔬</div>
            <h3 style="color: #2a5298; margin: 0.5rem 0;">Instant Field Testing</h3>
        </div>
        <p><strong>Machine Learning Prediction:</strong></p>
        <ul>
            <li>Input sensor data from low-cost devices</li>
            <li>Get immediate "Potable/Not Potable" results</li>
            <li>95%+ accuracy with LightGBM model</li>
            <li>Works offline in remote areas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">🤖</div>
            <h3 style="color: #2a5298; margin: 0.5rem 0;">AI-Powered Advisory</h3>
        </div>
        <p><strong>Google Gemini Integration:</strong></p>
        <ul>
            <li>Detailed public health recommendations</li>
            <li>Visual contamination analysis from photos</li>
            <li>Multilingual support (English/Haitian Creole)</li>
            <li>Contextual safety guidelines</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">🌍</div>
            <h3 style="color: #2a5298; margin: 0.5rem 0;">Community Monitoring</h3>
        </div>
        <p><strong>Real-time Intelligence:</strong></p>
        <ul>
            <li>Live interactive mapping system</li>
            <li>Trend analysis and hotspot detection</li>
            <li>NGO and health official dashboards</li>
            <li>Community-driven data collection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- How It Works Section ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("## 🔄 How AquaLERT Works")

# Process flow
process_col1, process_col2, process_col3, process_col4 = st.columns(4)

with process_col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 2rem;">📊</span>
        </div>
        <h4>1. Collect Data</h4>
        <p>Input sensor readings or upload water sample photos</p>
    </div>
    """, unsafe_allow_html=True)

with process_col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="background: #f3e5f5; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 2rem;">🧠</span>
        </div>
        <h4>2. AI Analysis</h4>
        <p>ML model processes data and AI provides insights</p>
    </div>
    """, unsafe_allow_html=True)

with process_col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 2rem;">📋</span>
        </div>
        <h4>3. Get Results</h4>
        <p>Receive safety assessment and recommendations</p>
    </div>
    """, unsafe_allow_html=True)

with process_col4:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="background: #fff3e0; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 2rem;">🗺️</span>
        </div>
        <h4>4. Share Impact</h4>
        <p>Data contributes to community monitoring</p>
    </div>
    """, unsafe_allow_html=True)

# --- Navigation Guide ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("## 🚀 Start Your Analysis")

st.markdown("""
<div style="background: linear-gradient(135deg, #f6f8fa 0%, #e1e8ed 100%); padding: 2rem; border-radius: 12px; margin: 1rem 0;">
    <h3 style="text-align: center; color: #2a5298;">Choose Your Tool</h3>
    <p style="text-align: center; font-size: 1.1rem;">Select from the sidebar to begin your water safety analysis</p>
</div>
""", unsafe_allow_html=True)

# Navigation options in an attractive grid
nav_col1, nav_col2 = st.columns(2, gap="large")

with nav_col1:
    st.markdown("""
    <div class="feature-card">
        <h4>🗺️ Live Water Map</h4>
        <p>View real-time status of water points across Haiti with interactive mapping.</p>
    </div>
    
    <div class="feature-card">
        <h4>🔬 Real-Time Test</h4>
        <p>Get instant potability predictions by inputting sensor data from your field testing kit.</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="feature-card">
        <h4>📷 Visual Analysis</h4>
        <p>Upload photos for AI-powered preliminary assessment of visual water contamination.</p>
    </div>
    
    <div class="feature-card">
        <h4>📊 Community Dashboard</h4>
        <p>Explore aggregated statistics, trends, and insights from all community submissions.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Technology Stack ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

with st.expander("🔧 **Technology Stack & Architecture**", expanded=False):
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("**Frontend & User Interface:**")
        st.markdown("""
        <div>
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">HTML/CSS</span>
            <span class="tech-badge">JavaScript</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Machine Learning & AI:**")
        st.markdown("""
        <div>
            <span class="tech-badge">LightGBM</span>
            <span class="tech-badge">scikit-learn</span>
            <span class="tech-badge">Google Gemini API</span>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("**Backend & Data:**")
        st.markdown("""
        <div>
            <span class="tech-badge">Flask</span>
            <span class="tech-badge">Python</span>
            <span class="tech-badge">REST APIs</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Visualization & Mapping:**")
        st.markdown("""
        <div>
            <span class="tech-badge">Plotly</span>
            <span class="tech-badge">Folium</span>
            <span class="tech-badge">Interactive Maps</span>
        </div>
        """, unsafe_allow_html=True)

# --- Call to Action Footer ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #2a5298 0%, #4CAF50 100%); color: white; border-radius: 12px; margin: 2rem 0;">
    <h3>Ready to Make a Difference?</h3>
    <p style="font-size: 1.1rem;">Join the movement for safer water access in Haiti</p>
    <p style="margin-top: 1.5rem;">
        <em>Built with passion for the <strong>#Hack4Haiti</strong> initiative 🇭🇹</em>
    </p>
</div>
""", unsafe_allow_html=True)

# --- Optional: Quick Start Guide ---
with st.expander("📋 **Quick Start Guide**"):
    st.markdown("""
    **For Field Workers:**
    1. Navigate to "Real-Time Test" in the sidebar
    2. Input your sensor readings (pH, turbidity, etc.)
    3. Get instant potability assessment
    4. Follow AI-generated safety recommendations
    
    **For Health Officials:**
    1. Check "Live Water Map" for regional overview
    2. Use "Community Dashboard" for trend analysis
    3. Monitor hotspots and contamination patterns
    4. Export data for further analysis
    
    **For Communities:**
    1. Use "Visual Analysis" for quick photo assessment
    2. Contribute data to help map water quality
    3. Access multilingual safety information
    4. Stay informed about local water conditions
    """)