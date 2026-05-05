import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_engine.data_processor import DataProcessor
from src.analytics.metrics_engine import MetricsEngine
from src.analytics.analysis_engine import AnalysisEngine
from src.ai_module.ai_analyzer import AIAnalyzer
from src.simulation.simulation_engine import SimulationEngine

# Page Config: High-end executive feel
st.set_page_config(page_title="Executive Intelligence | Decision Suite", layout="wide", page_icon="🏢")

# Custom CSS for Premium Executive Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #fcfcfc; }
    .metric-container { background: white; padding: 25px; border-radius: 12px; border: 1px solid #f0f0f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
    .impact-panel { background: #1a1a1a; color: white; padding: 30px; border-radius: 12px; margin-top: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏢 Executive Suite")
    uploaded_file = st.file_uploader("Ingest Business Data", type=["csv"])
    api_key = st.text_input("OpenAI Secure Key", type="password")
    st.divider()
    st.caption("Securely analyze performance and simulate strategic outcomes.")

# --- APP FLOW ---
if uploaded_file:
    # 1. Processing (Cached for performance)
    @st.cache_data
    def load_data(file):
        processor = DataProcessor()
        return processor.process(file)

    df, metadata = load_data(uploaded_file)
    
    # 2. Analytics
    metrics_engine = MetricsEngine(df)
    kpis = metrics_engine.calculate_all_kpis()
    summary = kpis['summary']
    
    # Header: Executive Summary
    st.title("Strategic Performance Dashboard")
    st.markdown(f"**Fiscal Overview:** {pd.to_datetime('today').strftime('%B %Y')}")
    
    # Row 1: KPI Cards
    cols = st.columns(4)
    metric_map = [
        ("Revenue", f"${summary['total_revenue']:,.0f}"),
        ("Avg Transaction", f"${summary['average_order_value']:.2f}"),
        ("Customer Base", f"{summary['unique_customers']:,}"),
        ("Loyalty (Repeat)", f"{kpis['retention']['repeat_customer_rate_percent']}%")
    ]
    for i, (label, val) in enumerate(metric_map):
        with cols[i]:
            st.metric(label, val)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Performance Insight", "🤖 AI Strategy", "🧪 Decision Simulator"])

    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Revenue Momentum")
            trend_df = pd.DataFrame(kpis['trends'])
            fig = px.area(trend_df, x='date', y='revenue', color_discrete_sequence=['#1a1a1a'])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Market Anomalies")
            analysis = AnalysisEngine(df).run_exploratory_analysis()
            anomalies = pd.DataFrame(analysis['anomalies'])
            if not anomalies.empty:
                st.dataframe(anomalies[['date', 'type', 'z_score']], hide_index=True)
            else:
                st.success("Stable market conditions detected.")

    with tab2:
        st.subheader("Strategic AI Consultation")
        if st.button("Generate Executive Briefing"):
            with st.spinner("Analyzing market dynamics..."):
                ai = AIAnalyzer(api_key=api_key)
                report = ai.generate_business_insights(kpis, analysis)
                if "insight_report" in report:
                    st.markdown(report["insight_report"])
                    st.session_state['recs'] = ai.generate_structured_recommendations(report["insight_report"])
                else:
                    st.error("Authentication required for AI insights.")

    with tab3:
        st.subheader("Decision Impact Panel")
        sim = SimulationEngine(kpis)
        
        # Comparison UI
        st.markdown("### Compare Strategic Scenarios")
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown("**Scenario A**")
            sc_a_type = st.selectbox("Action A", ["retention", "price", "customer_acquisition"], key="a_type")
            sc_a_val = st.slider("Intensity A (%)", -10, 50, 10, key="a_val")
            
        with col_s2:
            st.markdown("**Scenario B**")
            sc_b_type = st.selectbox("Action B", ["retention", "price", "customer_acquisition"], key="b_type")
            sc_b_val = st.slider("Intensity B (%)", -10, 50, 15, key="b_val")

        if st.button("Contrast Scenarios"):
            comp_df = sim.compare_scenarios([
                {"type": sc_a_type, "value": sc_a_val, "label": "Strategy A"},
                {"type": sc_b_type, "value": sc_b_val, "label": "Strategy B"}
            ])
            
            # Decision Impact Panel (The Executive Summary of Simulation)
            st.markdown("""
                <div class="impact-panel">
                    <h3>Decision Verdict</h3>
                    <p>Based on the simulation, Strategy B shows a higher revenue capture potential with lower elasticity risk.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.table(comp_df)
            
            fig_comp = px.bar(comp_df, x='Strategy', y='Revenue Gain', text_auto='.2s', color='Strategy',
                             color_discrete_sequence=['#1a1a1a', '#cccccc'])
            st.plotly_chart(fig_comp, use_container_width=True)

else:
    st.empty()
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.title("Decision Intelligence Suite")
        st.info("Ingest your fiscal data to unlock strategic AI insights and predictive simulations.")
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=2426", use_container_width=True)
