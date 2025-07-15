# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils import (
    # All functions from all previous versions are included for completeness
    get_strategic_alignment_data, get_project_portfolio_data,
    get_itsm_ticket_data, get_asset_inventory_data,
    get_tech_radar_data, get_vmp_tracker_data,
    get_audit_readiness_data,
    get_voice_of_scientist_data, get_ai_briefing,
    get_ai_root_cause, get_vendor_scorecards,
    get_team_performance, get_global_kpis,
    get_predictive_maintenance_data,
    get_capital_asset_model_data,
    get_project_forecast_data,
    generate_gxp_document,
    generate_capex_proposal,
    run_mitigation_simulation,
    get_self_healing_log,
    run_strategic_financial_model,
    get_autonomous_resource_recommendation,
    get_living_system_file_log,
    get_tco_data, get_automation_roi_data,
    get_risk_adjusted_vmp_data, run_what_if_scenario,
    get_assay_impact_data, get_reagent_genealogy_data,
    get_clinical_sample_journey, get_qms_query_result,
    get_systemic_risk_insight
)

# ==============================================================================
# Page Configuration & Styling
# ==============================================================================
st.set_page_config(
    page_title="DTE Glass Box Engine | Vertex",
    page_icon="🔍",
    layout="wide"
)

# ==============================================================================
# Data Loading (Cached for performance)
# ==============================================================================
@st.cache_data
def load_all_data():
    tickets_df, mttr_data = get_itsm_ticket_data()
    data = {
        "strategic_df": get_strategic_alignment_data(),
        "portfolio_df": get_project_portfolio_data(),
        "vmp_df": get_vmp_tracker_data(),
        "autonomous_rec": get_autonomous_resource_recommendation(),
        "tco_df": get_tco_data(),
        "automation_roi": get_automation_roi_data(),
        "risk_vmp_df": get_risk_adjusted_vmp_data(),
        "assay_impact_df": get_assay_impact_data(),
        "sample_journey": get_clinical_sample_journey(),
        "systemic_risk": get_systemic_risk_insight(),
        "self_healing_log": get_self_healing_log(),
        "lslf_log": get_living_system_file_log(),
        "cap_asset_df": get_capital_asset_model_data(),
        "team_df": get_team_performance()[0],
        "skills_gap": get_team_performance()[1],
        "global_kpis_df": get_global_kpis(),
        "tickets_df": tickets_df,
        "mttr_data": mttr_data,
        "incident_categories": tickets_df[tickets_df['Type'] == 'Incident']['Category'].value_counts().reset_index(name='count'),
        "ticket_counts_by_date": tickets_df.groupby('Date').size().reset_index(name='Ticket Count').set_index('Date'),
    }
    data["portfolio_df"] = get_project_forecast_data(data["portfolio_df"])
    return data

data = load_all_data()
autonomous_rec = data["autonomous_rec"]

# ==============================================================================
# Helper Functions (omitted for brevity)
# ==============================================================================

# ==============================================================================
# Sidebar - Global Navigation & Action Center
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Vertex_Pharmaceuticals_logo.svg/2560px-Vertex_Pharmaceuticals_logo.svg.png", width=150)
    st.title("DTE Glass Box Engine")
    st.markdown("West Coast")
    
    page = st.radio(
        "Navigation",
        ["📈 Strategic Architecture", "🔬 Scientific Impact & Data Fusion", "⚙️ Predictive & Autonomous Operations", "💼 Financial Intelligence", "📋 Generative GxP & Compliance", "👥 Leadership & Global Alignment"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.header("Action Center")
    st.caption("Your high-priority decisions pending review, now with full transparency.")

    with st.container(border=True):
        st.markdown("⚠️ **Autonomous Maintenance Workflow**")
        st.write("Approve proactive fix for `SD-HPLC-007`")
        if st.button("Review & Approve", key="action1", type="primary"):
            st.toast("Workflow for SD-HPLC-007 approved!", icon="✅")
        with st.expander("Show Reasoning"):
            st.markdown("""
            - **Observation:** Anomalous pressure signature detected by the ML model.
            - **Correlation:** This signature has an 85% statistical match with historical data from 12 previous pump seal failures.
            - **Recommendation:** Proactive replacement is the most cost-effective solution vs. risking an unplanned failure during a GxP run.
            """)

# ==============================================================================
# Main Content Area - Render selected page
# ==============================================================================
if page == "📈 Strategic Architecture":
    st.header("📈 Executive Command & Strategic Architecture Hub")
    st.caption("Focus on designing future operational strategy, with execution autonomously optimized by the platform.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Autonomous Resolution Rate", "85%")
    col2.metric("Portfolio Health Score (Avg)", "92%", delta="11%")
    col3.metric("GxP Compliance State", "Continuous")
    col4.metric("Leadership Decisions Pending", "3")
    
    st.divider()

    st.subheader("Generative Strategic Communication")
    st.info("🔬 **AI-Generated Value Story:** The **Dynamic Financial Modeler** was used to simulate the 5-year impact of accelerating our C> program...", icon="💡")
    
elif page == "🔬 Scientific Impact & Data Fusion":
    st.header("🔬 Cross-Functional Data Fusion & Scientific Impact Analysis")
    st.caption("This module breaks down organizational silos to answer the question: 'How is our technology performance directly impacting the speed and quality of Vertex's science?'")

    st.subheader("Clinical Sample Journey Tracker")
    st.markdown("A 'God-mode' view for a single sample, invaluable for deep OOS investigations...")
    sample_id = st.text_input("Enter a Clinical Sample ID:", "CL-2024-00123")
    st.dataframe(data["sample_journey"], use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("Assay & Reagent Impact Analysis")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Instrument-to-Assay Impact View**")
        assay_data = data["assay_impact_df"]
        fig = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15, thickness = 20, line = dict(color = "black", width = 0.5), 
                label = assay_data['label'], color = assay_data['color'],
                # UX FIX: Explicitly setting font color to black for better readability
                font=dict(color="black", size=10)
            ),
            link = dict(
                source = assay_data['source'], target = assay_data['target'], value = assay_data['value']
            )
        )])
        fig.update_layout(title_text="Instrument -> Assay -> Project Dependency Flow", font_size=10)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("**Reagent Lot Genealogy**")
        reagent_lot = st.text_input("Enter Problematic Reagent Lot ID:", "R-45B-XYZ")
        # DIGITAL GENERATION: Replaced st.image with st.graphviz_chart
        st.graphviz_chart(get_reagent_genealogy_data(reagent_lot))


elif page == "⚙️ Predictive & Autonomous Operations":
    st.header("⚙️ Predictive & Autonomous Operations Engine")
    st.caption("This module evolves from a 'health score' to an intelligent, risk-based scheduling and resource allocation engine...")

    st.subheader("Predictive Maintenance Scheduler")
    st.markdown("The ML model's 'Runs to Failure' prediction automatically creates a provisional work order...")
    st.dataframe(get_predictive_maintenance_data().style.highlight_max(subset=['Predicted Failure Risk (%)'], color='lightcoral'), use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Risk-Adjusted Validation Scheduling")
    st.markdown("The VMP is now prioritized not just by date, but by a **Validation Risk Score**...")
    fig_risk_vmp = px.scatter(
        data["risk_vmp_df"], x="Days Until Due", y="System Criticality",
        size="Validation Effort (Hours)", color="Status", hover_name="System/Instrument",
        title="Risk-Adjusted Validation Priority Matrix", size_max=50
    )
    st.plotly_chart(fig_risk_vmp, use_container_width=True)

elif page == "💼 Financial Intelligence":
    st.header("💼 Dynamic Financial & Strategic Modeler")
    st.caption("This module evolves capital planning into strategic business architecture...")

    st.subheader("Generative Strategic Scenario Modeler")
    st.markdown("Ask complex, multi-variable strategic questions. The engine will run thousands of simulations...")
    
    query = st.text_input("Enter Strategic Query:", "Model the 5-year impact of accelerating the C> program by 30%.")
    
    if st.button("Run Strategic Simulation", use_container_width=True, type="primary"):
        with st.spinner(f"Running multi-factor simulation for query: '{query}'..."):
            results = run_strategic_financial_model(query)
            time.sleep(2)
            st.subheader("Forecast Summary: 5-Year Impact")
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Projected 5-Yr CapEx Increase", f"${results['capex_impact']}M")
            res_col2.metric("Projected Headcount Growth", f"+{results['headcount_growth']} FTEs")
            res_col3.metric("Risk-Adjusted Portfolio NPV", f"${results['npv']}M")
            
            with st.expander("Show Model Assumptions & Reasoning"):
                 st.markdown(results['narrative'])
                 st.code(f"""
Model Parameters & Assumptions:
- C> Program Acceleration: 30% reduction in pre-clinical timelines.
- Financial Model: Based on Vertex FY24 Q2 financial model.
- HR Model: Assumes 6-month hiring lead time for specialized roles.
- Risk Model: Monte Carlo simulation (10,000 runs) factoring in a 15% probability of a key vendor delay.
                 """, language="text")

elif page == "🚀 Portfolio Orchestration":
    st.header("🚀 Autonomous Resource & Portfolio Orchestration")
    st.caption("This module transforms project management from human-led allocation to AI-driven orchestration...")

    st.subheader("Autonomous Resource Orchestrator")
    st.markdown("When the system detects a project is at risk, it autonomously generates the single most optimal resource recommendation...")
    
    st.error(f"**Project At Risk:** The **{autonomous_rec['project']}** project health has dropped to **{autonomous_rec['health_score']}%**.", icon="🚨")
    
    with st.expander("**Show Full Recommendation & Reasoning**", expanded=True):
        st.info(f"**Autonomous Recommendation:** Temporarily allocate **{autonomous_rec['recommended_resource']}** from **{autonomous_rec['resource_location']}** for **{autonomous_rec['duration']}**.")
        
        st.markdown("**Decision Factors (Why this recommendation was chosen):**")
        reason_cols = st.columns(3)
        reason_cols[0].markdown(f"**1. Skill Match:**\n`{autonomous_rec['recommended_resource']}` has an **Expert** rating in **'{autonomous_rec['skills_needed']}'**.")
        reason_cols[1].markdown(f"**2. Availability:**\nThe model identified a **non-critical window** in this individual's current project.")
        reason_cols[2].markdown(f"**3. Predicted Impact:**\nSimulation predicts this action will restore the project timeline with **{autonomous_rec['confidence']}% confidence**.")

elif page == "📋 Generative GxP & Compliance":
    st.header("📋 The 'Living' System Lifecycle & Continuous Validation Platform")
    st.caption("This module achieves a state of perpetual audit readiness...")

    st.subheader("Living System Lifecycle File (LSLF) Explorer")
    st.markdown("Select a GxP system to view its immutable, real-time event log...")
    system_to_inspect = st.selectbox("Select GxP System to Inspect:", data["vmp_df"]['System/Instrument'].unique())
    st.dataframe(get_living_system_file_log(), use_container_width=True, hide_index=True)

elif page == "👥 Leadership & Global Alignment":
    st.header("👥 Leadership: Team Performance & Global Alignment")
    st.caption("This module addresses duties related to **team leadership** and **matrix leadership**...")
    
    with st.container(border=True):
        st.subheader("Team Performance & Development Hub")
        # BUG FIX: Added the column definitions that were missing.
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("**Team Skills & Training Matrix**")
            st.dataframe(get_team_performance()[0].style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''), use_container_width=True, hide_index=True)
        with c2:
            st.markdown("**AI-Identified Skill Gap**")
            st.warning(f"**GAP:** {get_team_performance()[1]['gap']}\n\n**Recommendation:** {get_team_performance()[1]['recommendation']}")
