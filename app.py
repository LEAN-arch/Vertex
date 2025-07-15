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
    page_title="DTE Sentient Orchestration Platform | Vertex",
    page_icon="🧠",
    layout="wide"
)

# ==============================================================================
# Helper Functions for Advanced, Actionable Visualizations
# ==============================================================================
def create_spc_chart(data, mttr_series):
    """Creates a Statistical Process Control (SPC) chart for MTTR."""
    mean = mttr_series.mean()
    std_dev = mttr_series.std()
    ucl = mean + (3 * std_dev)
    lcl = mean - (3 * std_dev) if (mean - (3 * std_dev)) > 0 else 0
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data.index, y=data['Ticket Count'], name='New Tickets', marker_color='#1f77b4'), secondary_y=False)
    fig.add_trace(go.Scatter(x=mttr_series.index, y=mttr_series, name='MTTR (Hours)', mode='lines+markers', line=dict(color='#d62728')), secondary_y=True)
    fig.add_hline(y=mean, line_dash="dash", line_color="green", annotation_text="Mean", secondary_y=True)
    fig.add_hline(y=ucl, line_dash="dot", line_color="red", annotation_text="UCL (3σ)", secondary_y=True)
    outliers = mttr_series[(mttr_series > ucl) | (mttr_series < lcl)]
    fig.add_trace(go.Scatter(x=outliers.index, y=outliers, mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Special Cause Variation'), secondary_y=True)
    fig.update_layout(title_text="Service Stability SPC Chart", yaxis_title="Ticket Volume", xaxis_title="Date")
    fig.update_yaxes(title_text="Avg. Resolution (Hours)", secondary_y=True)
    return fig

def create_pareto_chart(df):
    """Creates a true Pareto chart to identify the 'vital few' root causes."""
    df = df.sort_values(by='count', ascending=False)
    df['Cumulative Percentage'] = (df['count'].cumsum() / df['count'].sum()) * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df['Category'], y=df['count'], name='Incident Count', marker_color='#1f77b4'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['Category'], y=df['Cumulative Percentage'], name='Cumulative %', line=dict(color='#d62728')), secondary_y=True)
    fig.update_layout(title_text="Incident Pareto Analysis: Focusing on the Vital Few", yaxis_title="Incident Count", xaxis_title="Incident Category")
    fig.update_yaxes(title_text="Cumulative Percentage", secondary_y=True, range=[0, 101])
    return fig

# ==============================================================================
# Data Loading (Cached for performance)
# ==============================================================================
@st.cache_data
def load_all_data():
    tickets_df, mttr_data = get_itsm_ticket_data()
    data = {
        "portfolio_df": get_project_portfolio_data(),
        "vmp_df": get_vmp_tracker_data(),
        "autonomous_rec": get_autonomous_resource_recommendation(),
        "tco_df": get_tco_data(),
        "automation_roi": get_automation_roi_data(),
        "risk_vmp_df": get_risk_adjusted_vmp_data(),
        "assay_impact_df": get_assay_impact_data(),
        "sample_journey": get_clinical_sample_journey(),
        "systemic_risk": get_systemic_risk_insight(),
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
# Sidebar - Global Navigation & AI Advisor
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Vertex_Pharmaceuticals_logo.svg/2560px-Vertex_Pharmaceuticals_logo.svg.png", width=150)
    st.title("DTE Sentient Platform")
    
    page = st.radio(
        "Navigation",
        ["📈 **Strategic Hub**", "💼 **Financial Intelligence**", "🔬 **Scientific Impact & Data Fusion**", "⚙️ **Predictive & Autonomous Operations**", "📋 **Generative GxP & Compliance**", "👥 **Leadership & Global Alignment**"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.header("🤖 AI Strategic Advisor")
    st.caption("Your integrated partner for synthesis, drafting, and querying.")

    with st.expander("Natural Language QMS Query"):
        qms_query = st.text_input("Ask a question of the QMS...", "Show CAPAs for software bugs in the last 18 months.")
        if st.button("Query QMS", key="qms_query"):
            with st.spinner("Querying Quality Management System..."):
                st.dataframe(get_qms_query_result(qms_query))

    with st.container(border=True):
        st.markdown("🚨 **AI-Generated Systemic Risk Insight**")
        risk = data["systemic_risk"]
        st.error(f"**{risk['title']}**\n\n{risk['insight']}", icon="🔥")
        st.info(f"**Recommendation:** {risk['recommendation']}")

# ==============================================================================
# Main Content Area - Render selected page
# ==============================================================================
if page == "📈 **Strategic Hub**":
    st.header("📈 Strategic Hub: Vision, Strategy & Orchestration")
    st.caption("Design future strategy, knowing that execution is being autonomously optimized and financially modeled by the platform.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Autonomous Resolution Rate", "85%")
    col2.metric("Portfolio Health Score (Avg)", "92%", delta="11%")
    col3.metric("GxP Compliance State", "Continuous")
    col4.metric("Leadership Decisions Pending", "3")
    
    st.divider()

    st.subheader("Autonomous Resource & Portfolio Orchestration")
    st.markdown("When the system detects a project is at risk, it autonomously generates the optimal resource recommendation. This is **matrix leadership** in action.")
    st.error(f"**Project At Risk:** The **{autonomous_rec['project']}** project health has dropped to **{autonomous_rec['health_score']}%**.", icon="🚨")
    st.info(f"**Autonomous Recommendation:** Temporarily allocate **{autonomous_rec['recommended_resource']}** from **{autonomous_rec['resource_location']}** for **{autonomous_rec['duration']}**. This action is predicted to bring the project **back on track** with a **{autonomous_rec['confidence']}%** confidence level.")

elif page == "💼 **Financial Intelligence**":
    st.header("💼 Full-Cycle Financial Intelligence & TCO")
    st.caption("This module moves from managing assets to managing a financial portfolio of technology, framing every decision in terms of ROI, TCO, and risk-adjusted value.")
    
    st.subheader("Total Cost of Ownership (TCO) Dashboard for GxP Assets")
    st.markdown("This treemap instantly reveals which assets are 'value drains'—high TCO with low reliability—providing clear targets for replacement.")
    fig_tco = px.treemap(data["tco_df"], path=[px.Constant("All Assets"), 'Asset Type', 'Asset ID'], values='TCO ($k)',
                  color='Uptime (%)', hover_data=['Maintenance Costs ($k)'],
                  color_continuous_scale='RdYlGn',
                  title='Asset TCO Treemap (Size = Cost, Color = Reliability)')
    st.plotly_chart(fig_tco, use_container_width=True)
    
    st.divider()
    
    st.subheader("Automation Program ROI & Vendor Performance")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Automation ROI Tracker**")
        fig_roi = go.Figure()
        fig_roi.add_trace(go.Scatter(x=data["automation_roi"]['Month'], y=data["automation_roi"]['Cumulative Value ($k)'], fill='tozeroy', name='Value Realized'))
        fig_roi.add_hline(y=0, line_dash="dash")
        fig_roi.add_annotation(x=4, y=5, text="Break-Even Point", showarrow=True)
        fig_roi.update_layout(title="Automation Program: Cumulative Value Realization")
        st.plotly_chart(fig_roi, use_container_width=True)
    with c2:
        st.markdown("**Vendor Spend vs. Performance**")
        vendor_df = pd.DataFrame(get_vendor_scorecards()).T.reset_index().rename(columns={'index':'Vendor'})
        fig_vendor = px.scatter(vendor_df, x='annual_spend_k', y='performance_score', size='incidents', color='Vendor', hover_name='Vendor', title='Vendor Spend vs. Performance')
        st.plotly_chart(fig_vendor, use_container_width=True)

elif page == "🔬 **Scientific Impact & Data Fusion**":
    st.header("🔬 Cross-Functional Data Fusion & Scientific Impact Analysis")
    st.caption("This module breaks down organizational silos to answer the question: 'How is our technology performance directly impacting the speed and quality of Vertex's science?'")

    st.subheader("Clinical Sample Journey Tracker")
    st.markdown("A 'God-mode' view for a single sample, invaluable for deep OOS investigations for critical products like Cologuard® and Oncotype DX®. This provides ultimate **end-to-end traceability**.")
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
                label = assay_data['labels'], color = assay_data['colors'],
                font=dict(color="black", size=10) # UX Fix for readability
            ),
            link = dict(
                source = assay_data['sources'], target = assay_data['targets'], value = assay_data['values']
            )
        )])
        fig.update_layout(title_text="Instrument -> Assay -> Project Dependency Flow", font_size=10)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("**Reagent Lot Genealogy**")
        reagent_lot = st.text_input("Enter Problematic Reagent Lot ID:", "R-45B-XYZ")
        st.graphviz_chart(get_reagent_genealogy_data(reagent_lot))

elif page == "⚙️ **Predictive & Autonomous Operations**":
    st.header("⚙️ Predictive & Prescriptive Operations Engine")
    st.caption("This module evolves from a 'health score' to an intelligent, risk-based scheduling and resource allocation engine.")

    st.subheader("Predictive Maintenance Scheduler")
    st.markdown("The ML model's prediction automatically creates a provisional work order and pencils-in a PM on the instrument schedule.")
    st.dataframe(get_predictive_maintenance_data().style.highlight_max(subset=['Predicted Failure Risk (%)'], color='lightcoral'), use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Service Stability & Problem Management")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Incident Pareto Analysis**")
        st.plotly_chart(create_pareto_chart(data["incident_categories"]), use_container_width=True)
    with c2:
        st.markdown("**Service Stability SPC Chart**")
        st.plotly_chart(create_spc_chart(data["ticket_counts_by_date"], data["mttr_data"]), use_container_width=True)

elif page == "📋 **Generative GxP & Compliance**":
    st.header("📋 Generative GxP & Continuous Validation")
    st.caption("This module leverages Generative AI to accelerate the validation lifecycle and provides a 'Living' system file for ultimate audit readiness and **21 CFR Part 11** compliance.")

    st.subheader("Risk-Adjusted Validation Scheduling")
    st.markdown("The VMP is now prioritized not just by date, but by a **Validation Risk Score** that combines GxP criticality with system age and incident history.")
    fig_risk_vmp = px.scatter(
        data["risk_vmp_df"], x="Days Until Due", y="System Criticality",
        size="Validation Effort (Hours)", color="Status", hover_name="System/Instrument",
        title="Risk-Adjusted Validation Priority Matrix", size_max=50
    )
    st.plotly_chart(fig_risk_vmp, use_container_width=True)

    with st.expander("🔬 'What-If' Scenario Planner for Validation"):
        scenario_query = st.text_input("Enter Validation Scenario:", "What is the impact if we delay the Hamilton-01 validation by 2 weeks?")
        if st.button("Run Validation Scenario", key="what_if_v"):
            st.error(run_what_if_scenario(scenario_query), icon="⚠️")
    
    st.divider()

    st.subheader("Generative AI V&V Report Drafter")
    st.markdown("After a validation is complete, the AI can automatically generate the narrative for the final validation report.")
    vmp_completed = data["vmp_df"][data["vmp_df"]['Status'] == 'Completed']
    selected_report = st.selectbox("Select Completed Validation to Draft Report:", vmp_completed['System/Instrument'].unique())
    if st.button("🤖 Draft Validation Summary Report", key="draft_vsr", type="primary"):
        st.info("Draft VSR generated and saved to the document management system for review.", icon="📄")

elif page == "👥 **Leadership & Global Alignment**":
    st.header("👥 Leadership: Team Performance & Global Alignment")
    st.caption("This module addresses duties related to **team leadership** and **matrix leadership**, ensuring personnel are qualified as per **GxP** requirements and fostering a culture of high performance.")
    
    with st.container(border=True):
        st.subheader("Team Performance & Development Hub")
        # BUG FIX: Added the column definitions that were missing.
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("**Team Skills & Training Matrix**")
            st.dataframe(get_team_performance()[0].style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''), use_container_width=True, hide_index=True)
        with col2:
            st.markdown("**AI-Identified Skill Gap**")
            st.warning(f"**GAP:** {get_team_performance()[1]['gap']}\n\n**Recommendation:** {get_team_performance()[1]['recommendation']}")

    with st.container(border=True):
        st.subheader("Matrix Leadership: Global Alignment")
        # BUG FIX: Added the column definitions that were missing.
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**West Coast vs. Global KPI Benchmark**")
            for _, row in get_global_kpis().iterrows():
                st.metric(label=f"{row['KPI']}", value=f"{row['West Coast']}{row.get('unit','')}", delta=f"{(row['West Coast'] - row['Global Avg']):.1f}{row.get('unit','')}", help=f"vs. Global Average of {row['Global Avg']}{row.get('unit','')}")
        with col2:
            st.markdown("**Global Best Practice (Autonomous Action)**")
            st.success("**New Best Practice Deployed:**\n- **Issue:** 'Lab Printer Offline' incidents globally.\n- **Origin:** Boston DTE's proactive ping script.\n- **Action:** This practice has been autonomously tested and deployed to the West Coast monitoring system.")
