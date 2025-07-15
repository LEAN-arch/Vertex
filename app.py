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
    get_living_system_file_log
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
    data = {
        "strategic_df": get_strategic_alignment_data(),
        "portfolio_df": get_project_portfolio_data(),
        "vmp_df": get_vmp_tracker_data(),
        "self_healing_log": get_self_healing_log(),
        "autonomous_rec": get_autonomous_resource_recommendation(),
        "lslf_log": get_living_system_file_log(),
        "cap_asset_df": get_capital_asset_model_data(),
        "team_df": get_team_performance()[0],
        "skills_gap": get_team_performance()[1],
        "global_kpis_df": get_global_kpis(),
    }
    data["portfolio_df"] = get_project_forecast_data(data["portfolio_df"])
    return data

data = load_all_data()
autonomous_rec = data["autonomous_rec"]

# ==============================================================================
# Sidebar - Global Navigation & Action Center
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Vertex_Pharmaceuticals_logo.svg/2560px-Vertex_Pharmaceuticals_logo.svg.png", width=150)
    st.title("DTE Glass Box Engine")
    st.markdown("West Coast")
    
    page = st.radio(
        "Navigation",
        ["📈 Strategic Architecture", "🤖 Autonomous Operations", "💼 Dynamic Financial Modeling", "🚀 Portfolio Orchestration", "📋 Continuous GxP Compliance", "👥 Leadership & Global Alignment"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.header("Action Center")
    st.caption("Your high-priority decisions pending review, now with full transparency.")

    # Action Item with Explainability
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
    st.info("🔬 **AI-Generated Value Story:** The **Dynamic Financial Modeler** was used to simulate the 5-year impact of accelerating our C> program. The model provided a data-driven forecast that informed a successful $50M strategic investment from the board. The **Autonomous Resource Orchestrator** then automatically allocated key personnel from global sites to support the initiative's kickoff, ensuring alignment from day one.", icon="💡")
    
elif page == "🤖 Autonomous Operations":
    st.header("🤖 Self-Healing Lab Infrastructure")
    st.caption("This module transforms operational support into a fully autonomous function, moving beyond prediction to self-diagnosis and self-resolution.")

    st.subheader("Autonomous Reliability & Resolution Log")
    st.markdown("The platform continuously monitors all GxP systems. Below is the real-time log of detected anomalies and the autonomous actions taken. Expand any row to see the full, auditable reasoning behind the AI's decision.")
    
    for i, row in data["self_healing_log"].iterrows():
        with st.expander(f"**{row['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')} | {row['System']} | Status: {row['Status']}**"):
            st.markdown(f"**Event Detected:** {row['Event Detected']}")
            st.markdown(f"**Autonomous Diagnosis (RCA):** {row['Autonomous Diagnosis (RCA)']}")
            st.info(f"**Autonomous Resolution:** {row['Autonomous Resolution']}", icon="✅")
            
            with st.container(border=True):
                st.markdown("**Underlying Logic & Data:**")
                st.code(f"""
Reasoning for '{row['Autonomous Diagnosis (RCA)']}':
- Correlated events from data sources: [Logfile_A.log, Network_Switch_B_MIB, Server_C_Perfmon]
- ML Model Confidence Score: 92%
- Matched against historical incident pattern: INC-54321
- GxP Impact Assessment: High - affects data integrity for active batches.
- Action chosen based on SOP-DTE-1138 for High GxP Impact incidents.
                """, language="text")

elif page == "💼 Dynamic Financial Modeling":
    st.header("💼 Dynamic Financial & Strategic Modeler")
    st.caption("This module evolves capital planning into strategic business architecture, allowing the AD to model the multi-year financial and operational impact of C-suite level decisions.")

    st.subheader("Generative Strategic Scenario Modeler")
    st.markdown("Ask complex, multi-variable strategic questions. The engine will run thousands of simulations and provide a comprehensive forecast with fully transparent assumptions.")
    
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
- Data Sources: [Workday HR API, SAP S/4HANA Finance API, Planisware Portfolio DB]
                 """, language="text")

elif page == "🚀 Portfolio Orchestration":
    st.header("🚀 Autonomous Resource & Portfolio Orchestration")
    st.caption("This module transforms project management from human-led allocation to AI-driven orchestration, with full transparency into its recommendations.")

    st.subheader("Autonomous Resource Orchestrator")
    st.markdown("When the system detects a project is at risk, it autonomously generates the single most optimal resource recommendation. Below is the recommendation and the clear, data-driven logic behind it.")
    
    st.error(f"**Project At Risk:** The **{autonomous_rec['project']}** project health has dropped to **{autonomous_rec['health_score']}%**.", icon="🚨")
    
    with st.expander("**Show Full Recommendation & Reasoning**", expanded=True):
        st.info(f"**Autonomous Recommendation:** Temporarily allocate **{autonomous_rec['recommended_resource']}** from **{autonomous_rec['resource_location']}** for **{autonomous_rec['duration']}**.")
        
        st.markdown("**Decision Factors (Why this recommendation was chosen):**")
        reason_cols = st.columns(3)
        reason_cols[0].markdown(f"**1. Skill Match:**\n`{autonomous_rec['recommended_resource']}` has an **Expert** rating in **'{autonomous_rec['skills_needed']}'**, the critical skill gap for this project.")
        reason_cols[1].markdown(f"**2. Availability:**\nThe model identified a **non-critical window** in this individual's current project, minimizing disruption to their primary team.")
        reason_cols[2].markdown(f"**3. Predicted Impact:**\nSimulation predicts this action will restore the project timeline with **{autonomous_rec['confidence']}% confidence**, the highest of all available options.")

        if st.button(f"Go to Action Center to Approve", use_container_width=True):
            st.toast("Action item is waiting in the sidebar.", icon="✅")

elif page == "📋 Continuous GxP Compliance":
    st.header("📋 The 'Living' System Lifecycle & Continuous Validation Platform")
    st.caption("This module achieves a state of perpetual audit readiness. It provides a verifiable, real-time audit trail with full explainability.")

    st.subheader("Living System Lifecycle File (LSLF) Explorer")
    st.markdown("Select a GxP system to view its immutable, real-time event log. This provides auditors with ultimate transparency and demonstrates a state of continuous, demonstrable control as mandated by **21 CFR Part 11**.")

    system_to_inspect = st.selectbox("Select GxP System to Inspect:", data["vmp_df"]['System/Instrument'].unique())
    
    df_lslf = data["lslf_log"]
    st.dataframe(df_lslf, use_container_width=True, hide_index=True)

    with st.expander("What is this? The 'Glass Box' Audit Trail"):
        st.markdown("""
        - **What:** This is the **Living System Lifecycle File (LSLF)**, a real-time, tamper-proof ledger of every single event that occurs on a GxP system.
        - **Why:** To provide an un-reputable, transparent, and complete history of the system, satisfying the most stringent **21 CFR Part 11** and **Data Integrity (ALCOA+)** requirements. It proves that all data is **Attributable, Legible, Contemporaneous, Original, and Accurate**.
        - **How:** During an audit, you can filter this log by date, user, or event type to answer any question an auditor might have with complete, verifiable data. The cryptographic hash ensures that the record of events cannot be altered after the fact.
        """)
        
elif page == "👥 Leadership & Global Alignment":
    st.header("👥 Leadership: Team Performance & Global Alignment")
    st.caption("This module addresses duties related to team leadership and matrix leadership, ensuring personnel are qualified as per **GxP** requirements and fostering a culture of high performance.")
    
    with st.container(border=True):
        st.subheader("Team Performance & Development Hub")
        st.markdown("Strategic talent management to build a future-ready team. The Autonomous Orchestrator (Tab 4) uses this data to make optimal resource decisions.")
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("**Team Skills & Training Matrix**")
            st.dataframe(data["team_df"].style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''), use_container_width=True, hide_index=True)
        with col2:
            st.markdown("**AI-Identified Skill Gap**")
            st.warning(f"**GAP:** {data['skills_gap']['gap']}\n\n**Recommendation:** {data['skills_gap']['recommendation']}")

    with st.container(border=True):
        st.subheader("Matrix Leadership: Global Alignment")
        st.markdown("Fostering a culture of global excellence by benchmarking and sharing best practices, identified and automated by the platform's AI.")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**West Coast vs. Global KPI Benchmark**")
            for _, row in data["global_kpis_df"].iterrows():
                st.metric(label=f"{row['KPI']}", value=f"{row['West Coast']}{row.get('unit','')}", delta=f"{(row['West Coast'] - row['Global Avg']):.1f}{row.get('unit','')}", help=f"vs. Global Average of {row['Global Avg']}{row.get('unit','')}")
        with col2:
            st.markdown("**Global Best Practice (Autonomous Action)**")
            st.success("**New Best Practice Deployed:**\n- **Issue:** 'Lab Printer Offline' incidents globally.\n- **Origin:** Boston DTE's proactive ping script.\n- **Action:** This practice has been autonomously tested and deployed to the West Coast monitoring system. No manual action required.")
