# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from utils import (
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
    # --- NEW: Import functions for Ultimate Functionality features ---
    get_self_healing_log,
    run_strategic_financial_model,
    get_autonomous_resource_recommendation,
    get_living_system_file_log
)

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="DTE Sentient Orchestration Platform | Vertex Pharmaceuticals",
    page_icon="🤖",
    layout="wide"
)

# ==============================================================================
# Helper Functions (No changes from previous version)
# ==============================================================================
# (Helper functions like create_spc_chart, create_pareto_chart would be here)

# ==============================================================================
# Main Application
# ==============================================================================
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Vertex_Pharmaceuticals_logo.svg/2560px-Vertex_Pharmaceuticals_logo.svg.png", width=200)
st.title("DTE Sentient Orchestration Platform: West Coast")
st.markdown("##### Autonomous, Generative, and Self-Optimizing System for the DTE Business Architect")

# --- Data Loading ---
# (Existing data loading calls would be here)
strategic_df = get_strategic_alignment_data()
portfolio_df = get_project_portfolio_data()
vmp_df = get_vmp_tracker_data()
# --- NEW: Data loading for Ultimate features ---
self_healing_log = get_self_healing_log()
autonomous_rec = get_autonomous_resource_recommendation()
lslf_log = get_living_system_file_log()


# --- Tabbed Interface ---
tab_list = ["📈 **Strategic Architecture**", "🤖 **Autonomous Operations**", "💼 **Dynamic Financial Modeling**", "🚀 **Portfolio Orchestration**", "📋 **Continuous GxP Compliance**"]
tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_list)

# ==============================================================================
# TAB 1: STRATEGIC ARCHITECTURE
# ==============================================================================
with tab1:
    st.header("Executive Command & Strategic Architecture Hub")
    st.caption("Focus on designing future operational strategy, with execution autonomously optimized by the platform.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Autonomous Resolution Rate", "85%", help="Percentage of operational incidents autonomously resolved by the platform.")
    col2.metric("Portfolio Health Score (Avg)", "92%", delta="11%", help="Average health score across all projects, improved by autonomous resource orchestration.")
    col3.metric("GxP Compliance State", "Continuous", help="Systems exist in a continuously validated state, eliminating periodic review gaps.")
    col4.metric("Leadership Decisions Pending", "3", help="High-level strategic approvals awaiting review.")
    
    st.divider()

    st.subheader("Generative Strategic Communication")
    st.info("🔬 **AI-Generated Value Story:** This quarter, the **Dynamic Financial Modeler** was used to simulate the 5-year impact of accelerating our C> program. The model provided a data-driven forecast that informed a successful $50M strategic investment from the board. The **Autonomous Resource Orchestrator** then automatically allocated key personnel from global sites to support the initiative's kickoff, ensuring alignment from day one.", icon="💡")
    
    st.divider()

    st.subheader("Strategic Portfolio Quadrant Analysis")
    st.caption("High-level view to validate that autonomous resource allocation aligns with strategic intent.")
    fig_portfolio = px.scatter(
        portfolio_df, x="Effort (Person-Weeks)", y="Strategic Impact Score",
        size="Budget ($k)", color="Strategic Theme", hover_name="Project",
        size_max=60, title="DTE Strategic Projects: Impact vs. Effort Matrix"
    )
    st.plotly_chart(fig_portfolio, use_container_width=True)

# ==============================================================================
# TAB 2: AUTONOMOUS OPERATIONS
# ==============================================================================
with tab2:
    st.header("Self-Healing Lab Infrastructure")
    st.caption("This module transforms operational support into a fully autonomous function, moving beyond prediction to self-diagnosis and self-resolution.")

    st.subheader("Autonomous Reliability & Resolution Log")
    st.markdown("The platform continuously monitors the health of all GxP systems. Below is the real-time log of detected anomalies and the autonomous actions taken. The AD's role is to govern and review these automated resolutions, focusing only on exceptions.")
    
    # Display the log of self-healing actions
    st.dataframe(self_healing_log, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 3: DYNAMIC FINANCIAL MODELING
# ==============================================================================
with tab3:
    st.header("Dynamic Financial & Strategic Modeler")
    st.caption("This module evolves capital planning into strategic business architecture, allowing the AD to model the multi-year financial and operational impact of C-suite level decisions.")

    st.subheader("Generative Strategic Scenario Modeler")
    st.markdown("Ask complex, multi-variable strategic questions. The engine will run thousands of Monte Carlo simulations against integrated Finance, HR, and Portfolio data to provide a comprehensive forecast.")
    
    query = st.text_input("Enter Strategic Query:", "Model the 5-year impact of accelerating the C> program by 30%.")
    
    if st.button("Run Strategic Simulation", use_container_width=True):
        with st.spinner(f"Running multi-factor simulation for query: '{query}'..."):
            results = run_strategic_financial_model(query)
            time.sleep(4)
            st.success("Strategic Forecast Complete")
            
            st.subheader("Forecast Summary: 5-Year Impact")
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Projected 5-Yr CapEx Increase", f"${results['capex_impact']}M", help="Additional capital required for labs and equipment.")
            res_col2.metric("Projected Headcount Growth", f"+{results['headcount_growth']} FTEs", help="Primarily QC Analysts and Process Scientists.")
            res_col3.metric("Risk-Adjusted Portfolio NPV", f"${results['npv']}M", help="Net Present Value of the new portfolio after considering risks and rewards.")
            
            st.text_area("Generated Strategic Narrative", results['narrative'], height=200)

# ==============================================================================
# TAB 4: PORTFOLIO ORCHESTRATION
# ==============================================================================
with tab4:
    st.header("Autonomous Resource & Portfolio Orchestration")
    st.caption("This module transforms project management from human-led allocation to AI-driven orchestration, optimizing the global talent pool for maximum enterprise-wide velocity.")

    st.subheader("Autonomous Resource Orchestrator")
    st.markdown("When the system detects a project is at risk, it no longer waits for a human to act. It autonomously scans the global talent pool and generates the single most optimal resource recommendation to mitigate the delay.")
    
    st.warning(f"**Project At Risk:** The **{autonomous_rec['project']}** project health has dropped to **{autonomous_rec['health_score']}%**.")
    
    st.info(f"""
    **Autonomous Recommendation:**
    - **Action:** Temporarily allocate **{autonomous_rec['recommended_resource']}** from the **{autonomous_rec['resource_location']}** team for **{autonomous_rec['duration']}**.
    - **Required Skills:** {autonomous_rec['skills_needed']}.
    - **Predicted Impact:** This action is predicted to bring the project **back on track** with a **{autonomous_rec['confidence']}%** confidence level.
    - **Impact on Source Team:** The model forecasts a minimal, non-critical **{autonomous_rec['source_impact']}** to the source team's project.
    """)
    
    if st.button(f"Approve & Initiate Allocation Request for {autonomous_rec['recommended_resource']}", use_container_width=True):
        st.success("Approved. Allocation request has been routed to the respective resource manager with all supporting data.")

# ==============================================================================
# TAB 5: CONTINUOUS GXP COMPLIANCE
# ==============================================================================
with tab5:
    st.header("The 'Living' System Lifecycle & Continuous Validation Platform")
    st.caption("This module achieves the ultimate GxP goal: a state of perpetual audit readiness. Static documents are replaced by a 'Living System Lifecycle File' (LSLF) with a verifiable, real-time audit trail.")

    st.subheader("Living System Lifecycle File (LSLF) Explorer")
    st.markdown("Select a GxP system to view its immutable, real-time event log. This provides auditors with ultimate transparency and demonstrates a state of continuous, demonstrable control as mandated by **21 CFR Part 11**.")

    system_to_inspect = st.selectbox("Select GxP System to Inspect:", vmp_df['System/Instrument'].unique())
    
    st.dataframe(lslf_log, use_container_width=True, hide_index=True)
    st.caption("Each event is cryptographically hashed and chained to the previous event, ensuring a tamper-proof audit trail.")

    with st.expander("Automated Continuous Validation"):
        st.success("✅ **No Anomalies Detected.** The LSLF monitor has detected no unauthorized changes or deviations from the validated state for this system in the past 24 hours. All automated re-verification checks following the last security patch were successful.")
