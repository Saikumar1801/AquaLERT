import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
from io import StringIO # <-- 1. IMPORT StringIO

# Configuration
FLASK_BACKEND_URL = "http://127.0.0.1:5000"
UNSAFE_THRESHOLD = 400

# Page Configuration
st.set_page_config(
    page_title="AquaLERT Community Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2a5298;
        margin-bottom: 1rem;
    }
    
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border-left-color: #dc3545;
        color: #721c24;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }
    
    .alert-success {
        background-color: #d4edda;
        border-left-color: #28a745;
        color: #155724;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💧 AquaLERT Community Dashboard</h1>
    <p>Real-time water quality monitoring and community insights</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Dashboard Controls")
    
    auto_refresh = st.checkbox("Auto-refresh data", value=False)
    refresh_interval = st.selectbox("Refresh interval", [30, 60, 300, 600], index=2, format_func=lambda x: f"{x} seconds")
    
    st.markdown("---")
    
    st.header("📊 Filters")
    date_range = st.date_input(
        "Select date range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )
    
    st.markdown("---")
    
    st.header("ℹ️ About")
    st.info("""
    This dashboard aggregates water quality test results from the community.
    
    **Key Features:**
    - Real-time data updates
    - Regional analysis
    - Safety threshold monitoring
    - Trend analysis
    """)

@st.cache_data(ttl=300)
def get_dashboard_data():
    """Fetches summary data from the Flask backend with enhanced error handling."""
    try:
        with st.spinner("🔄 Fetching latest data..."):
            response = requests.get(
                f"{FLASK_BACKEND_URL}/api/community_summary",
                timeout=10
            )
            
        if response.status_code == 200:
            # FIX: Wrap the JSON string in a StringIO object to adhere to modern pandas standards.
            df = pd.read_json(StringIO(response.text))
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                # Add additional computed columns
                df['is_safe'] = df['prediction'] == 1
                df['safety_margin'] = UNSAFE_THRESHOLD - df['sulfate']
                return df
            else:
                return pd.DataFrame()
        else:
            st.error(f"Server returned status code: {response.status_code}")
            return pd.DataFrame()
            
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return pd.DataFrame()

def create_enhanced_pie_chart(data):
    """Creates an enhanced pie chart with better styling."""
    pie_data = data['prediction_label'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=pie_data.index,
        values=pie_data.values,
        hole=0.4,
        marker=dict(
            colors=['#28a745', '#dc3545'],
            line=dict(color='#FFFFFF', width=2)
        ),
        textfont=dict(size=14),
        textinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text="Water Safety Distribution",
            x=0.5,
            font=dict(size=18, color='#2c3e50')
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=400,
        margin=dict(t=60, b=60, l=20, r=20)
    )
    
    return fig

def create_enhanced_bar_chart(data):
    """Creates an enhanced bar chart for regional data."""
    bar_data = data['region'].value_counts()
    
    fig = go.Figure(data=[go.Bar(
        x=bar_data.index,
        y=bar_data.values,
        marker=dict(
            color=bar_data.values,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Number of Tests")
        ),
        hovertemplate='<b>%{x}</b><br>Tests: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text="Tests by Region",
            x=0.5,
            font=dict(size=18, color='#2c3e50')
        ),
        xaxis_title="Region",
        yaxis_title="Number of Tests",
        height=400,
        margin=dict(t=60, b=60, l=40, r=40)
    )
    
    return fig

def create_trend_chart(data):
    """Creates an enhanced trend chart with multiple traces."""
    if data.empty:
        return go.Figure()
    
    # Resample data
    daily_data = data.set_index('timestamp').resample('D').agg({
        'sulfate': ['mean', 'min', 'max'],
        'prediction': 'count'
    }).dropna()
    
    daily_data.columns = ['avg_sulfate', 'min_sulfate', 'max_sulfate', 'test_count']
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Sulfate Levels', 'Daily Test Count'),
        vertical_spacing=0.12,
        row_heights=[0.7, 0.3]
    )
    
    # Sulfate trend
    fig.add_trace(
        go.Scatter(
            x=daily_data.index,
            y=daily_data['avg_sulfate'],
            mode='lines+markers',
            name='Average Sulfate',
            line=dict(color='#2a5298', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>Avg Sulfate: %{y:.1f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add confidence band
    fig.add_trace(
        go.Scatter(
            x=daily_data.index,
            y=daily_data['max_sulfate'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            name='Max'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=daily_data.index,
            y=daily_data['min_sulfate'],
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(42, 82, 152, 0.2)',
            fill='tonexty',
            showlegend=False,
            name='Range'
        ),
        row=1, col=1
    )
    
    # Unsafe threshold line
    fig.add_hline(
        y=UNSAFE_THRESHOLD,
        line_dash="dash",
        line_color="red",
        annotation_text="Unsafe Threshold (400)",
        annotation_position="top right",
        row=1, col=1
    )
    
    # Test count bars
    fig.add_trace(
        go.Bar(
            x=daily_data.index,
            y=daily_data['test_count'],
            name='Daily Tests',
            marker_color='#17a2b8',
            hovertemplate='<b>%{x}</b><br>Tests: %{y}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title=dict(
            text="Water Quality Trends Over Time",
            x=0.5,
            font=dict(size=18, color='#2c3e50')
        ),
        height=600,
        margin=dict(t=80, b=60, l=60, r=60),
        hovermode='x unified'
    )
    
    return fig

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# Main dashboard logic
dashboard_data = get_dashboard_data()

if dashboard_data is None:
    st.markdown("""
    <div class="alert-box alert-danger">
        <h4>🚫 Connection Error</h4>
        <p>Could not connect to the AquaLERT backend. Please ensure the Flask server is running on <code>http://127.0.0.1:5000</code></p>
    </div>
    """, unsafe_allow_html=True)
    
elif dashboard_data.empty:
    st.markdown("""
    <div class="alert-box alert-warning">
        <h4>📭 No Data Available</h4>
        <p>No water test data found. Submit your first test to see dashboard insights!</p>
    </div>
    """, unsafe_allow_html=True)
    
else:
    # Filter data by date range
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (dashboard_data['timestamp'].dt.date >= start_date) & (dashboard_data['timestamp'].dt.date <= end_date)
        dashboard_data = dashboard_data.loc[mask]
    
    if dashboard_data.empty:
        st.warning("No data available for the selected date range.")
    else:
        # Key Metrics Section
        st.markdown("## 📈 Key Metrics")
        
        total_tests = len(dashboard_data)
        unsafe_tests = len(dashboard_data[dashboard_data['prediction'] == 0])
        safe_tests = total_tests - unsafe_tests
        unsafe_percentage = (unsafe_tests / total_tests) * 100 if total_tests > 0 else 0
        avg_sulfate = dashboard_data['sulfate'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Tests",
                f"{total_tests:,}",
                delta=f"+{len(dashboard_data[dashboard_data['timestamp'] >= (datetime.now() - timedelta(days=7))])}" if total_tests > 0 else None,
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "Safe Reports",
                f"{safe_tests:,}",
                delta=f"{100-unsafe_percentage:.1f}%" if total_tests > 0 else "0%",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                "Unsafe Reports",
                f"{unsafe_tests:,}",
                delta=f"{unsafe_percentage:.1f}%" if total_tests > 0 else "0%",
                delta_color="inverse"
            )
        
        with col4:
            st.metric(
                "Avg Sulfate Level",
                f"{avg_sulfate:.1f}",
                delta=f"{'Above' if avg_sulfate > UNSAFE_THRESHOLD else 'Below'} threshold",
                delta_color="inverse" if avg_sulfate > UNSAFE_THRESHOLD else "normal"
            )
        
        # Safety Alert
        if unsafe_percentage > 50:
            st.markdown("""
            <div class="alert-box alert-danger">
                <h4>⚠️ High Risk Alert</h4>
                <p>More than 50% of recent tests show unsafe water quality. Immediate attention required!</p>
            </div>
            """, unsafe_allow_html=True)
        elif unsafe_percentage > 25:
            st.markdown("""
            <div class="alert-box alert-warning">
                <h4>⚡ Moderate Risk</h4>
                <p>Elevated unsafe water reports detected. Monitor closely.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-box alert-success">
                <h4>✅ Good Status</h4>
                <p>Water quality levels are within acceptable ranges.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Visualizations Section
        st.markdown("## 📊 Analytics")
        
        # First row of charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.plotly_chart(
                create_enhanced_pie_chart(dashboard_data),
                use_container_width=True,
                config={'displayModeBar': False}
            )
        
        with col_chart2:
            st.plotly_chart(
                create_enhanced_bar_chart(dashboard_data),
                use_container_width=True,
                config={'displayModeBar': False}
            )
        
        # Trend chart
        st.plotly_chart(
            create_trend_chart(dashboard_data),
            use_container_width=True,
            config={'displayModeBar': True}
        )
        
        # Data Table Section
        with st.expander("📋 Raw Data Preview", expanded=False):
            st.markdown("### Recent Test Results")
            display_data = dashboard_data.sort_values('timestamp', ascending=False).head(100)
            st.dataframe(
                display_data[['timestamp', 'region', 'sulfate', 'prediction_label']],
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name=f"water_quality_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🔄 Last updated: {}</p>
    <p>💧 AquaLERT Community Dashboard | Powered by Streamlit & Flask</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)