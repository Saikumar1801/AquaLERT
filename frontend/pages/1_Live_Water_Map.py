# frontend/pages/1_🌍_Live_Water_Map.py
import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Configuration
FLASK_BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Live Water Map - AquaLERT", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .safe { background-color: #4CAF50; }
    .unsafe { background-color: #f44336; }
    .caution { background-color: #ff9800; }
    .unknown { background-color: #9e9e9e; }
    
    .map-controls {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    .legend-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .last-updated {
        background: #e3f2fd;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        color: #1565c0;
        display: inline-block;
    }
    
    .alert-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div style="text-align: center; padding: 1.5rem 0;">
    <h1>🌍 Live Water Quality Map</h1>
    <p style="font-size: 1.2rem; color: #666;">
        Real-time monitoring of water safety across Haiti
    </p>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=30)  # Cache for 30 seconds for more frequent updates
def get_water_points():
    """Fetches water point data from the Flask backend."""
    try:
        response = requests.get(f"{FLASK_BACKEND_URL}/api/water_points", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Backend returned status code: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        st.warning("Request timed out. Server may be slow.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

@st.cache_data(ttl=60)
def get_water_statistics():
    """Fetches aggregated water quality statistics."""
    try:
        response = requests.get(f"{FLASK_BACKEND_URL}/api/water_stats", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Sidebar Controls
with st.sidebar:
    st.markdown("### 🎛️ Map Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
    
    # Filter options
    st.markdown("### 🔍 Filters")
    show_potable = st.checkbox("✅ Show Safe Water", value=True)
    show_not_potable = st.checkbox("❌ Show Unsafe Water", value=True)
    show_caution = st.checkbox("⚠️ Show Caution Areas", value=True)
    show_unverified = st.checkbox("❓ Show Unverified Points", value=True)
    
    # Map style
    st.markdown("### 🗺️ Map Style")
    map_style = st.selectbox(
        "Choose map appearance:",
        ["OpenStreetMap", "Satellite", "Terrain"],
        index=0
    )
    
    # Refresh button
    if st.button("🔄 Refresh Data Now", type="primary"):
        st.cache_data.clear()
        st.experimental_rerun()

# Auto-refresh logic
if auto_refresh:
    time.sleep(1)  # Small delay to prevent too frequent requests
    st.experimental_rerun()

# Fetch data
water_points = get_water_points()
water_stats = get_water_statistics()

if water_points is None:
    st.markdown("""
    <div class="alert-banner">
        <h3>⚠️ Backend Connection Issue</h3>
        <p>Cannot connect to AquaLERT backend server. Please ensure the Flask server is running on port 5000.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show demo data message
    st.info("💡 **Demo Mode:** Displaying sample data for demonstration purposes.")
    
    # Sample data for demo
    water_points = [
        {"name": "Port-au-Prince Central", "lat": 18.5944, "lon": -72.3074, "status": "Potable", "verified": True, "last_tested": "2024-01-15", "confidence": 0.95},
        {"name": "Cap-Haïtien North", "lat": 19.7578, "lon": -72.2014, "status": "Not Potable", "verified": True, "last_tested": "2024-01-14", "confidence": 0.89},
        {"name": "Jacmel Southeast", "lat": 18.2341, "lon": -72.5321, "status": "Caution", "verified": False, "last_tested": "2024-01-13", "confidence": 0.76},
        {"name": "Gonaïves Central", "lat": 19.4515, "lon": -72.6890, "status": "Potable", "verified": True, "last_tested": "2024-01-15", "confidence": 0.92},
        {"name": "Les Cayes South", "lat": 18.2006, "lon": -73.7500, "status": "Not Potable", "verified": True, "last_tested": "2024-01-12", "confidence": 0.87}
    ]

# Convert to DataFrame for easier handling
df = pd.DataFrame(water_points)

# Calculate statistics
total_points = len(df)
if total_points > 0:
    safe_points = len(df[df['status'] == 'Potable'])
    unsafe_points = len(df[df['status'] == 'Not Potable'])
    caution_points = len(df[df['status'] == 'Caution'])
    verified_points = len(df[df['verified'] == True])
    
    safety_rate = (safe_points / total_points) * 100
    verification_rate = (verified_points / total_points) * 100
else:
    safe_points = unsafe_points = caution_points = verified_points = 0
    safety_rate = verification_rate = 0

# Statistics Dashboard
st.markdown("### 📊 Real-Time Statistics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h2>{total_points}</h2>
        <p>Total Monitoring Points</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);">
        <h2>{safe_points}</h2>
        <p>Safe Water Sources</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);">
        <h2>{unsafe_points}</h2>
        <p>Unsafe Water Sources</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);">
        <h2>{caution_points}</h2>
        <p>Caution Areas</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);">
        <h2>{safety_rate:.1f}%</h2>
        <p>Safety Rate</p>
    </div>
    """, unsafe_allow_html=True)

# Quick Stats Row
col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <h4>🎯 Verification Status</h4>
        <p><strong>{verification_rate:.1f}%</strong> of water points have been verified by trained personnel</p>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <h4>⏰ Last Updated</h4>
        <p class="last-updated">Data refreshed: {current_time}</p>
    </div>
    """, unsafe_allow_html=True)

# Map Legend
st.markdown("""
<div class="legend-container">
    <h4>🗺️ Map Legend</h4>
    <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
        <div><span class="status-indicator safe"></span><strong>Safe Water</strong> - Potable for consumption</div>
        <div><span class="status-indicator unsafe"></span><strong>Unsafe Water</strong> - Not suitable for drinking</div>
        <div><span class="status-indicator caution"></span><strong>Caution</strong> - Requires treatment before use</div>
        <div><span class="status-indicator unknown"></span><strong>Unknown/Unverified</strong> - Needs testing</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Create enhanced map
if total_points > 0:
    # Determine map tiles based on style selection
    tiles_map = {
        "OpenStreetMap": "OpenStreetMap",
        "Satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "Terrain": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}"
    }
    
    # Create map with enhanced styling
    m = folium.Map(
        location=[18.5944, -72.3074], 
        zoom_start=8,
        tiles=tiles_map.get(map_style, "OpenStreetMap"),
        attr="AquaLERT Water Quality Monitoring"
    )
    
    # Enhanced color and icon mapping
    color_map = {
        "Potable": {"color": "green", "icon": "tint"},
        "Not Potable": {"color": "red", "icon": "exclamation-triangle"},
        "Caution": {"color": "orange", "icon": "exclamation-circle"},
        "Unknown": {"color": "gray", "icon": "question-circle"}
    }
    
    # Apply filters and add markers
    for _, point in df.iterrows():
        status = point.get("status", "Unknown")
        verified = point.get("verified", False)
        
        # Apply filters
        if status == "Potable" and not show_potable:
            continue
        if status == "Not Potable" and not show_not_potable:
            continue
        if status == "Caution" and not show_caution:
            continue
        if not verified and not show_unverified:
            continue
        
        # Enhanced popup with more information
        confidence = point.get("confidence", 0.0)
        last_tested = point.get("last_tested", "Unknown")
        
        popup_html = f"""
        <div style="min-width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">📍 {point['name']}</h4>
            <div style="border-left: 4px solid {color_map[status]['color']}; padding-left: 10px;">
                <p><strong>Status:</strong> <span style="color: {color_map[status]['color']};">{status}</span></p>
                <p><strong>Verified:</strong> {'✅ Yes' if verified else '❓ Pending'}</p>
                <p><strong>Confidence:</strong> {confidence:.1%}</p>
                <p><strong>Last Tested:</strong> {last_tested}</p>
                <p><strong>Coordinates:</strong> {point['lat']:.4f}, {point['lon']:.4f}</p>
            </div>
        </div>
        """
        
        # Create marker with custom styling
        marker_color = color_map[status]["color"]
        marker_icon = color_map[status]["icon"]
        
        # Add different marker styles for verified vs unverified
        if verified:
            folium.Marker(
                location=[point['lat'], point['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{point['name']} - {status}",
                icon=folium.Icon(
                    color=marker_color, 
                    icon=marker_icon, 
                    prefix='fa'
                )
            ).add_to(m)
        else:
            # Use circle markers for unverified points
            folium.CircleMarker(
                location=[point['lat'], point['lon']],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{point['name']} - {status} (Unverified)",
                color=marker_color,
                fillColor=marker_color,
                fillOpacity=0.6,
                weight=2
            ).add_to(m)
    
    # Add a custom control legend to the map
    legend_html = '''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>AquaLERT Status</b></p>
    <p><i class="fa fa-tint" style="color:green"></i> Safe Water</p>
    <p><i class="fa fa-exclamation-triangle" style="color:red"></i> Unsafe Water</p>
    <p><i class="fa fa-exclamation-circle" style="color:orange"></i> Caution</p>
    <p><i class="fa fa-question-circle" style="color:gray"></i> Unknown</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Display the enhanced map
    st.markdown("### 🗺️ Interactive Water Quality Map")
    map_data = st_folium(m, width=1200, height=650, returned_objects=["last_object_clicked"])
    
    # Display clicked location info
    if map_data["last_object_clicked"]:
        clicked_point = map_data["last_object_clicked"]
        st.success(f"📍 **Selected Location:** Latitude: {clicked_point['lat']:.4f}, Longitude: {clicked_point['lng']:.4f}")

else:
    st.warning("🤷‍♂️ No water point data available to display.")

# Additional Statistics Charts
if total_points > 0:
    st.markdown("### 📈 Analysis Dashboard")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Status distribution pie chart
        status_counts = df['status'].value_counts()
        fig_pie = px.pie(
            values=status_counts.values, 
            names=status_counts.index,
            title="Water Quality Distribution",
            color_discrete_map={
                'Potable': '#4CAF50',
                'Not Potable': '#f44336', 
                'Caution': '#ff9800'
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with chart_col2:
        # Verification status bar chart
        verified_counts = df['verified'].value_counts()
        fig_bar = px.bar(
            x=['Verified', 'Unverified'], 
            y=[verified_counts.get(True, 0), verified_counts.get(False, 0)],
            title="Verification Status",
            color=['Verified', 'Unverified'],
            color_discrete_map={'Verified': '#2196F3', 'Unverified': '#FFC107'}
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# Action Items and Alerts
if unsafe_points > 0:
    st.markdown("### 🚨 Action Required")
    st.error(f"**{unsafe_points} water sources** require immediate attention. Health officials should prioritize these locations for intervention.")

if caution_points > 0:
    st.warning(f"**{caution_points} water sources** need additional testing or treatment before safe consumption.")

# Footer with instructions
st.markdown("---")
st.markdown("""
<div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; text-align: center;">
    <h4>💡 How to Use This Map</h4>
    <p>
        • <strong>Click markers</strong> to view detailed information about each water point<br>
        • <strong>Use filters</strong> in the sidebar to focus on specific water quality statuses<br>
        • <strong>Enable auto-refresh</strong> to see real-time updates every 30 seconds<br>
        • <strong>Share coordinates</strong> with field teams for rapid response to unsafe water sources
    </p>
</div>
""", unsafe_allow_html=True)