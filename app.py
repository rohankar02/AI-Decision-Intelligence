import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_engine.data_processor import DataProcessor
from src.analytics.metrics_engine import MetricsEngine
from src.analytics.analysis_engine import AnalysisEngine
from src.ai_module.ai_analyzer import AIAnalyzer
from src.simulation.simulation_engine import SimulationEngine

# Page Config
st.set_page_config(page_title="AI Decision Intelligence", layout="wide", page_icon="📈")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #fbfbfb; }
    .kpi-card { background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #eee; }
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Intelligence Console")
    uploaded_file = st.file_uploader("Upload Business Data", type=["csv"])
    api_key = st.text_input("OpenAI API Key", type="password")
    st.divider()
    st.info("Upload a sales/customer CSV to generate AI-driven growth strategies.")

# --- MAIN DASHBOARD ---
if uploaded_file:
    # 1. Processing
    processor = DataProcessor()
    df, metadata = processor.process(uploaded_file)
    
    # 2. Engines
    metrics_engine = MetricsEngine(df)
    kpi_results = metrics_engine.calculate_all_kpis()
    
    analysis_engine = AnalysisEngine(df)
    analysis_report = analysis_engine.run_exploratory_analysis()
    
    summary = kpi_results['summary']

    st.title("📊 Business Intelligence Dashboard")
    
    # Row 1: KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Revenue", f"${summary['total_revenue']:,.0f}")
    with c2: st.metric("Avg Order", f"${summary['average_order_value']:.2f}")
    with c3: st.metric("Customers", f"{summary['unique_customers']:,}")
    with c4: st.metric("Repeat Rate", f"{kpi_results['retention']['repeat_customer_rate_percent']}%")

    st.divider()

    # Row 2: AI Insights & Recommendations
    st.header("🤖 AI Growth Strategy")
    if st.button("Generate Strategic Recommendations"):
        with st.spinner("Consulting AI..."):
            ai = AIAnalyzer(api_key=api_key)
            report = ai.generate_business_insights(kpi_results, analysis_report)
            
            if "insight_report" in report:
                st.markdown(report["insight_report"])
                st.session_state['recommendations'] = ai.generate_structured_recommendations(report["insight_report"])
            else:
                st.error("Could not generate report. Check API Key.")

    # Interaction: Selection & Simulation
    if 'recommendations' in st.session_state and st.session_state['recommendations']:
        st.subheader("🎯 Select an Action to Simulate")
        rec_list = st.session_state['recommendations']
        options = [r['action'] for r in rec_list]
        selected_action = st.selectbox("Which strategy would you like to test?", options)
        
        # Find selected recommendation details
        selected_rec = next(r for r in rec_list if r['action'] == selected_action)
        
        # Simulation Logic
        sim = SimulationEngine(kpi_results)
        
        # Map recommendation type to simulation scenario (Simple mapping)
        scenario = 'retention' if 'retention' in selected_action.lower() or 'loyalty' in selected_action.lower() else 'price'
        if 'acquisition' in selected_action.lower() or 'new' in selected_action.lower():
            scenario = 'customer_acquisition'
            
        change_pct = st.slider(f"Simulate Impact: {selected_action} (%)", 1, 50, 10)
        
        if st.button("Run Simulation"):
            sim_res = sim.simulate_scenario(scenario, change_pct)
            
            col_l, col_r = st.columns([1, 1.5])
            with col_l:
                st.markdown("#### Impact Comparison")
                st.table(pd.DataFrame(sim_res['comparison_table']))
            
            with col_r:
                gain = sim_res['total_revenue_improvement']
                pct = sim_res['improvement_pct']
                st.success(f"**Projected Growth:** +${gain:,.2f} ({pct}%)")
                
                # Visual Gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = summary['total_revenue'] + gain,
                    delta = {'reference': summary['total_revenue']},
                    title = {'text': "Revenue Projection"},
                    gauge = {'axis': {'range': [None, summary['total_revenue'] * 1.5]}}
                ))
                st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a CSV file in the sidebar to begin analysis.")
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80")
