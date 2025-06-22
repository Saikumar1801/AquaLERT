# frontend/pages/3_📸_Visual_Analysis.py
import streamlit as st
import requests
import base64
import time
from PIL import Image
import io
from datetime import datetime

# Configuration
FLASK_BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Visual Analysis - AquaLERT", 
    page_icon="📸", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .analysis-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .upload-zone {
        border: 2px dashed #4CAF50;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: #f8fff8;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #45a049;
        background: #f0fff0;
    }
    
    .disclaimer-box {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(255, 152, 0, 0.2);
    }
    
    .analysis-result {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
    }
    
    .confidence-bar {
        background: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .tip-card {
        background: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .warning-card {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .success-card {
        background: #e8f5e8;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .error-card {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .feature-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with information and controls
with st.sidebar:
    st.markdown("### 📸 Visual Analysis Guide")
    
    st.markdown("#### 📋 What to Photograph")
    st.markdown("""
    **✅ Good Photos:**
    - Clear, well-lit water sample
    - Container against plain background
    - Natural or bright white lighting
    - Multiple angles if possible
    
    **❌ Avoid:**
    - Dark or shadowy images
    - Blurry or out-of-focus shots
    - Colored lighting (yellow, blue tints)
    - Reflective surfaces blocking view
    """)
    
    st.markdown("#### 🔍 What AI Analyzes")
    st.info("""
    • **Turbidity** - Water clarity/cloudiness
    • **Color** - Unusual discoloration
    • **Particles** - Visible contaminants
    • **Surface conditions** - Foam, films, debris
    • **Overall appearance** - General visual quality
    """)
    
    st.markdown("#### ⚠️ Important Notes")
    st.warning("""
    - Visual analysis is **preliminary only**
    - Cannot detect invisible contaminants
    - Always follow up with sensor testing
    - Not suitable for final safety decisions
    """)

# Header Section
st.markdown("""
<div class="analysis-header">
    <h1>📸 AI-Powered Visual Water Analysis</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        Get instant preliminary assessment of water quality through advanced computer vision
    </p>
</div>
""", unsafe_allow_html=True)

# How It Works Section
st.markdown("### 🔬 How Visual Analysis Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-item">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📱</div>
        <h4>Upload Photo</h4>
        <p>Take a clear photo of your water sample</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-item">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
        <h4>AI Analysis</h4>
        <p>Google Gemini Vision processes the image</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-item">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
        <h4>Assessment</h4>
        <p>Receive detailed visual quality report</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-item">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
        <h4>Next Steps</h4>
        <p>Get recommendations for further testing</p>
    </div>
    """, unsafe_allow_html=True)

# Main Disclaimer
st.markdown("""
<div class="disclaimer-box">
    <h3>⚠️ Important Disclaimer</h3>
    <p style="margin: 0; font-size: 1.1rem;">
        This visual analysis provides <strong>preliminary assessment only</strong> and should 
        <strong>NOT replace proper sensor-based testing</strong>. Many harmful contaminants 
        are invisible to the naked eye and require laboratory or field sensor analysis.
    </p>
</div>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown("### 📤 Upload Water Sample Image")

# Custom upload area
uploaded_file = st.file_uploader(
    "Choose an image of your water sample...", 
    type=["jpg", "png", "jpeg", "bmp", "tiff"],
    help="Supported formats: JPG, PNG, JPEG, BMP, TIFF (Max size: 10MB)"
)

# Photo Guidelines
with st.expander("📋 **Photography Guidelines for Best Results**"):
    guide_col1, guide_col2 = st.columns(2)
    
    with guide_col1:
        st.markdown("""
        **🌟 Best Practices:**
        - Use natural daylight or bright white LED light
        - Hold camera steady or use tripod
        - Fill frame with water container
        - Take multiple photos from different angles
        - Ensure water surface is visible
        - Use plain, neutral background
        """)
    
    with guide_col2:
        st.markdown("""
        **❌ Common Mistakes:**
        - Fluorescent or colored lighting
        - Photos taken in shadows
        - Camera too far from sample
        - Reflections blocking water view
        - Blurry or out-of-focus images
        - Dark or poorly lit conditions
        """)

# Image Analysis Section
if uploaded_file is not None:
    # Create two columns for image and info
    img_col, info_col = st.columns([2, 1])
    
    with img_col:
        st.markdown("### 🖼️ Uploaded Image")
        
        # Display image with better formatting
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Water Sample - {uploaded_file.name}", use_column_width=True)
        
        # Image metadata
        st.markdown("#### 📋 Image Information")
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Size:** {file_size:.1f} KB")
        st.write(f"**Dimensions:** {image.size[0]} × {image.size[1]} pixels")
        st.write(f"**Format:** {image.format}")
    
    with info_col:
        st.markdown("### ✅ Image Quality Check")
        
        # Basic image quality assessment
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        min_dimension = min(image.size)
        
        # Quality indicators
        if file_size_mb > 0.1:
            st.markdown('<div class="success-card">✅ <strong>File Size:</strong> Good quality</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-card">⚠️ <strong>File Size:</strong> May be too small</div>', unsafe_allow_html=True)
        
        if min_dimension >= 300:
            st.markdown('<div class="success-card">✅ <strong>Resolution:</strong> Sufficient detail</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-card">⚠️ <strong>Resolution:</strong> Low resolution detected</div>', unsafe_allow_html=True)
        
        # Analysis readiness
        st.markdown("### 🚀 Ready for Analysis")
        st.info("Image uploaded successfully. Click the button below to start AI analysis.")
    
    # Analysis Button and Results
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        analyze_button = st.button(
            "🤖 Analyze Image with AI", 
            type="primary", 
            use_container_width=True,
            help="Send image to Google Gemini AI for visual analysis"
        )
    
    if analyze_button:
        with st.spinner("🔍 AI is analyzing your water sample image..."):
            # Progress bar for better UX
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Simulate analysis steps
                status_text.text("📤 Uploading image...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                # Encode image to base64
                bytes_data = uploaded_file.getvalue()
                base64_encoded_data = base64.b64encode(bytes_data).decode('utf-8')
                
                status_text.text("🤖 Sending to AI for analysis...")
                progress_bar.progress(50)
                
                payload = {
                    "image": f"data:image/{uploaded_file.type.split('/')[-1]};base64,{base64_encoded_data}",
                    "filename": uploaded_file.name,
                    "timestamp": datetime.now().isoformat()
                }
                
                status_text.text("⚡ Processing with Google Gemini...")
                progress_bar.progress(75)
                
                response = requests.post(
                    f"{FLASK_BACKEND_URL}/analyze_image", 
                    json=payload,
                    timeout=30
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results in professional format
                    st.markdown("## 🎯 AI Analysis Results")
                    
                    # Main analysis result
                    st.markdown("""
                    <div class="analysis-result">
                        <h3>🤖 Visual Assessment Report</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Parse and display analysis
                    analysis_text = result.get('analysis', 'No analysis available.')
                    
                    # Display the main analysis
                    st.markdown(f"### 📝 Detailed Analysis")
                    st.markdown(analysis_text)
                    
                    # Extract confidence if available
                    confidence = result.get('confidence', None)
                    if confidence:
                        st.markdown("### 📊 Confidence Level")
                        confidence_pct = confidence * 100
                        
                        # Visual confidence bar
                        if confidence_pct >= 80:
                            color = "#4CAF50"
                            status = "High Confidence"
                        elif confidence_pct >= 60:
                            color = "#ff9800"
                            status = "Medium Confidence"
                        else:
                            color = "#f44336"
                            status = "Low Confidence"
                        
                        st.markdown(f"""
                        <div style="margin: 1rem 0;">
                            <p><strong>{status}:</strong> {confidence_pct:.1f}%</p>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {confidence_pct}%; background: {color};"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Recommendations section
                    recommendations = result.get('recommendations', [])
                    if recommendations:
                        st.markdown("### 💡 AI Recommendations")
                        for i, rec in enumerate(recommendations, 1):
                            st.markdown(f"{i}. {rec}")
                    
                    # Next steps
                    st.markdown("### 🎯 Recommended Next Steps")
                    st.markdown("""
                    <div class="tip-card">
                        <h4>🔬 For Accurate Testing:</h4>
                        <ul>
                            <li><strong>Use sensor testing</strong> - Navigate to "Real-Time Test" for precise measurements</li>
                            <li><strong>Test multiple parameters</strong> - pH, turbidity, dissolved solids, etc.</li>
                            <li><strong>Professional lab analysis</strong> - For drinking water certification</li>
                            <li><strong>Regular monitoring</strong> - Water quality can change over time</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Save results option
                    st.markdown("### 💾 Save Results")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # Create downloadable report
                    report_content = f"""
                    AquaLERT Visual Analysis Report
                    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    
                    Image: {uploaded_file.name}
                    File Size: {file_size:.1f} KB
                    Dimensions: {image.size[0]} × {image.size[1]} pixels
                    
                    AI Analysis:
                    {analysis_text}
                    
                    Confidence: {f'{confidence * 100:.1f}%' if confidence is not None else 'Not provided'}
                    
                    Disclaimer: This is a preliminary visual analysis only. 
                    Professional testing is recommended for final safety assessment.
                    """
                    
                    st.download_button(
                        label="📄 Download Analysis Report",
                        data=report_content,
                        file_name=f"aqualert_visual_analysis_{timestamp}.txt",
                        mime="text/plain"
                    )
                    
                else:
                    st.markdown(f"""
                    <div class="error-card">
                        <h4>❌ Analysis Error</h4>
                        <p>Server returned status code: {response.status_code}</p>
                        <p><strong>Error details:</strong> {response.text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except requests.exceptions.ConnectionError:
                st.markdown("""
                <div class="error-card">
                    <h4>🔌 Connection Error</h4>
                    <p><strong>Could not connect to AquaLERT backend.</strong></p>
                    <p>Please ensure the Flask server is running on port 5000.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Demo mode fallback
                st.markdown("### 🎭 Demo Mode Analysis")
                st.info("Since the backend is unavailable, here's a sample analysis:")
                
                demo_analysis = """
                **AI Visual Assessment (Demo):**
                
                Based on the uploaded image, the water sample appears to have:
                
                🔍 **Visual Characteristics:**
                - Moderate clarity with slight turbidity
                - No obvious discoloration detected
                - Some particulate matter visible
                - Surface appears calm with no foam
                
                ⚠️ **Potential Concerns:**
                - Slight cloudiness may indicate suspended particles
                - Recommend filtration before consumption
                - Further testing needed to assess microbial content
                
                📊 **Visual Quality Score:** 6.5/10
                
                **Recommendation:** Proceed with sensor-based testing for accurate safety assessment.
                """
                
                st.markdown(demo_analysis)
                
            except requests.exceptions.Timeout:
                st.markdown("""
                <div class="warning-card">
                    <h4>⏱️ Request Timeout</h4>
                    <p>The analysis is taking longer than expected. This may be due to:</p>
                    <ul>
                        <li>Large image file size</li>
                        <li>Server processing load</li>
                        <li>Network connectivity issues</li>
                    </ul>
                    <p>Please try again with a smaller image or check your connection.</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-card">
                    <h4>⚠️ Unexpected Error</h4>
                    <p>An unexpected error occurred during analysis:</p>
                    <p><code>{str(e)}</code></p>
                    <p>Please try again or contact support if the problem persists.</p>
                </div>
                """, unsafe_allow_html=True)

else:
    # No file uploaded - show upload encouragement
    st.markdown("""
    <div class="upload-zone">
        <h3>📸 Ready to Analyze Your Water Sample?</h3>
        <p style="font-size: 1.1rem; margin: 1rem 0;">
            Upload a clear photo of your water sample to get started with AI-powered visual analysis.
        </p>
        <p style="color: #666;">
            Drag and drop your image above, or click to browse your files.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Educational Content
st.markdown("---")
st.markdown("### 🎓 Understanding Visual Water Quality Assessment")

edu_col1, edu_col2 = st.columns(2)

with edu_col1:
    st.markdown("""
    #### 👁️ What Visual Analysis Can Detect
    
    **✅ Visible Indicators:**
    - Turbidity (cloudiness)
    - Color changes
    - Floating particles or debris
    - Surface films or foam
    - Unusual textures or consistency
    
    **📊 Assessment Factors:**
    - Overall clarity
    - Color intensity
    - Particle density
    - Surface conditions
    """)

with edu_col2:
    st.markdown("""
    #### ❌ What Visual Analysis Cannot Detect
    
    **🔬 Invisible Contaminants:**
    - Bacteria and viruses
    - Chemical pollutants
    - Heavy metals
    - Dissolved gases
    - pH levels
    
    **⚗️ Requires Lab Testing:**
    - Microbial contamination
    - Chemical composition
    - Mineral content
    - Toxin levels
    """)

# Footer with action items
st.markdown("""
<div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin-top: 2rem;">
    <h4>🎯 Next Steps After Visual Analysis</h4>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🔬</div>
            <h5>Sensor Testing</h5>
            <p>Use "Real-Time Test" for precise measurements</p>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🗺️</div>
            <h5>Report Location</h5>
            <p>Add findings to the community map</p>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">📊</div>
            <h5>Track Trends</h5>
            <p>Monitor changes over time</p>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">👥</div>
            <h5>Share Results</h5>
            <p>Inform community and health officials</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)