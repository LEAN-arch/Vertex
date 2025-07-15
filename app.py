# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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
    # --- NEW: Import functions for 10++ Generative/Autonomous features ---
    generate_gxp_document,
    generate_capex_proposal,
    run_mitigation_simulation
)

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="DTE Strategic Orchestration Engine | Vertex Pharmaceuticals",
    page_icon="🧬",
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
    fig.add_trace(go.Bar(x=data['Date'], y=data['Ticket Count'], name='New Tickets', marker_color='#1f77b4'), secondary_y=False)
    fig.add_trace(go.Scatter(x=mttr_series.index, y=mttr_series, name='MTTR (Hours)', mode='lines+markers', line=dict(color='#d62728')), secondary_y=True)
    fig.add_hline(y=mean, line_dash="dash", line_color="green", annotation_text="Mean", annotation_position="bottom right", secondary_y=True)
    fig.add_hline(y=ucl, line_dash="dot", line_color="red", annotation_text="UCL (3σ)", annotation_position="top right", secondary_y=True)
    outliers = mttr_series[(mttr_series > ucl) | (mttr_series < lcl)]
    fig.add_trace(go.Scatter(x=outliers.index, y=outliers, mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Special Cause Variation'), secondary_y=True)
    fig.update_layout(title_text="Service Stability SPC Chart: Volume & MTTR")
    fig.update_yaxes(title_text="Ticket Volume", secondary_y=False)
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
# Main Application
# ==============================================================================
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Vertex_Pharmaceuticals_logo.svg/2560px-Vertex_Pharmaceuticals_logo.svg.png", width=200)
st.title("DTE Strategic Orchestration Engine: West Coast")
st.markdown("##### Prescriptive, Generative, and Autonomous Platform for the Associate Director, Laboratory Engineering & Technology")

# --- Data Loading ---
strategic_df = get_strategic_alignment_data()
portfolio_df = get_project_portfolio_data()
tickets_df, mttr_data = get_itsm_ticket_data()
assets_df = get_asset_inventory_data()
tech_radar_df = get_tech_radar_data()
vmp_df = get_vmp_tracker_data()
audit_df = get_audit_readiness_data()
vos_data = get_voice_of_scientist_data()
vendor_data = get_vendor_scorecards()
team_df, skills_gap = get_team_performance()
global_kpis_df = get_global_kpis()
pred_maint_df = get_predictive_maintenance_data()
cap_asset_df = get_capital_asset_model_data()
portfolio_df = get_project_forecast_data(portfolio_df)

# --- Tabbed Interface ---
tab_list = ["📈 **Executive Strategy**", "⚙️ **Autonomous Operations**", "💼 **Asset & CapEx Engine**", "🚀 **Project Orchestration**", "📋 **Generative GxP & Compliance**", "👥 **Leadership & Global Alignment**"]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_list)

# ==============================================================================
# TAB 1: EXECUTIVE STRATEGY
# ==============================================================================
with tab1:
    st.header("Executive Command & Strategy Hub")
    st.caption("This module addresses the **Vision and Strategy** duties, enabling high-level communication and alignment.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lab System Uptime", "99.8%")
    col2.metric("P1/P2 Incident MTTR (Hours)", "3.8", delta="-0.5h")
    col3.metric("Project Health Score (Avg)", "81%", delta="3%")
    col4.metric("GxP Compliance Gaps", "0", delta="-1", delta_color="normal")
    
    st.divider()

    st.subheader("Generative Strategic Communication")
    st.caption("Lead engagement by generating high-quality, data-driven narratives for any audience.")
    
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("**AI-Generated Value Story of the Month**")
        st.info("🔬 **Value Story:** The **Autonomous Reliability Module** proactively identified a pump seal degradation on HPLC-007, preventing an estimated 2 days of downtime for the VT-101 program. The system autonomously scheduled maintenance, verified parts inventory, and closed the loop with the vendor, requiring only one-click approval from leadership.", icon="💡")
    with c2:
        st.markdown("**AI Stakeholder Briefing Generator**")
        audience = st.selectbox("Select Audience:", ["Site Leadership (SD)", "Global DTE Leadership", "Lab Scientists"])
        if st.button("Generate Briefing", use_container_width=True):
            briefing = get_ai_briefing(audience, {"uptime": "99.8%", "mttr": "3.8h", "projects_on_time": "85%"})
            st.text_area("Generated Draft:", briefing, height=150)
    
    st.divider()

    st.subheader("Strategic Portfolio Quadrant Analysis")
    st.caption("Categorizing strategic initiatives to align resources with impact, changing the conversation from 'What are we doing?' to 'Why are we doing it?'")
    
    median_effort = portfolio_df['Effort (Person-Weeks)'].median()
    median_impact = portfolio_df['Strategic Impact Score'].median()
    fig_portfolio = px.scatter(
        portfolio_df, x="Effort (Person-Weeks)", y="Strategic Impact Score",
        size="Budget ($k)", color="Strategic Theme", hover_name="Project",
        size_max=60, title="DTE Strategic Projects: Impact vs. Effort Matrix"
    )
    # Add quadrant annotations
    st.plotly_chart(fig_portfolio, use_container_width=True)

# ==============================================================================
# TAB 2: AUTONOMOUS OPERATIONS
# ==============================================================================
with tab2:
    st.header("Autonomous Lab Service Operations (ITIL Evolved)")
    st.caption("This module transforms **Operational Execution** by integrating prescriptive ML and automation, fulfilling the ITIL framework's highest potential.")

    st.subheader("Autonomous Reliability & Prescriptive Control Module")
    st.markdown("This **10++** feature moves beyond prediction to **prescription and autonomous action**. It identifies potential failures, simulates the optimal fix, and initiates the entire service workflow for one-click leadership approval.")
    
    cols = st.columns(len(pred_maint_df.columns) + 1)
    headers = list(pred_maint_df.columns) + ["Autonomous Action"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
        
    for i, row in pred_maint_df.iterrows():
        cols[0].write(row['Asset ID'])
        cols[1].write(row['Instrument Type'])
        cols[2].progress(int(row['Predicted Failure Risk (%)']))
        cols[3].write(row['Predicted Failure Type'])
        cols[4].info(row['Prescribed Fix']) # Highlight the prescription
        if cols[5].button("Initiate Workflow", key=f"auto_{i}", help="Click to autonomously draft work order, check parts inventory via SAP, and schedule maintenance."):
            with st.spinner("Executing autonomous workflow..."):
                time.sleep(2)
                st.success(f"Workflow for {row['Asset ID']} initiated. Awaiting final approval in ServiceNow.")

    st.divider()
    
    st.subheader("Proactive Problem Management & Service Stability")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Incident Pareto Analysis**")
        st.caption("Utilizes the **Pareto Principle** to identify the vital few problems, justifying strategic CAPA initiatives.")
        incident_categories = tickets_df[tickets_df['Type'] == 'Incident']['Category'].value_counts().reset_index(name='count')
        st.plotly_chart(create_pareto_chart(incident_categories), use_container_width=True)
        
    with c2:
        st.markdown("**Service Stability SPC Chart**")
        st.caption("Applies **Statistical Process Control** to distinguish normal 'noise' from significant 'special cause' events requiring investigation.")
        ticket_counts_by_date = tickets_df.groupby('Date').size().reset_index(name='Ticket Count')
        st.plotly_chart(create_spc_chart(ticket_counts_by_date, mttr_data), use_container_width=True)

# ==============================================================================
# TAB 3: ASSET & CAPEX ENGINE
# ==============================================================================
with tab3:
    st.header("Asset Lifecycle & Generative CapEx Engine")
    st.caption("This module evolves asset management into strategic capital planning, addressing duties related to evaluation, vendor management, and financial stewardship as required by **21 CFR 820**.")

    st.subheader("Intelligent Capital Asset Refresh Modeler")
    st.markdown("This ML model provides an objective, data-driven prioritization for capital expenditure. The **10++** Generative Engine below transforms this analysis into a board-ready proposal.")
    fig_cap_asset = px.scatter(
        cap_asset_df, x="Total Cost of Ownership ($)", y="Scientific Need Score",
        size="Asset Age (Yrs)", color="Asset Type", hover_name="Asset ID",
        title="Capital Asset Replacement Priority Matrix", size_max=40
    )
    st.plotly_chart(fig_cap_asset, use_container_width=True)

    st.divider()

    st.subheader("Generative Capital Expenditure (CapEx) Engine")
    st.markdown("Select a high-priority asset identified by the model above and let the **Vertex-GPT** generate a comprehensive, multi-page CapEx proposal in the official finance template. This elevates the AD from analyst to executive reviewer.")
    
    high_priority_asset = st.selectbox("Select Asset for CapEx Proposal:", cap_asset_df['Asset ID'].unique())
    if st.button(f"✍️ Generate Full CapEx Proposal for {high_priority_asset}", use_container_width=True):
        asset_details = cap_asset_df[cap_asset_df['Asset ID'] == high_priority_asset].to_dict('records')[0]
        with st.spinner(f"Generating comprehensive proposal for {high_priority_asset}..."):
            proposal = generate_capex_proposal(asset_details)
            time.sleep(3)
            st.text_area("Generated CapEx Proposal Draft", proposal, height=400)

# ==============================================================================
# TAB 4: PROJECT ORCHESTRATION
# ==============================================================================
with tab4:
    st.header("Innovation Radar & Project Orchestration Engine")
    st.caption("This module transforms project oversight from passive monitoring to active, data-driven orchestration.")

    st.subheader("Project Mitigation & Simulation Engine")
    st.markdown("This **10++** feature moves beyond risk prediction to **prescriptive risk resolution**. For at-risk projects, the AD can now simulate the impact of leadership decisions to identify the optimal path forward.")

    at_risk_project = portfolio_df[portfolio_df['Health Score (%)'] < 60].iloc[0]
    with st.expander(f"**Run Mitigation Scenarios for At-Risk Project: {at_risk_project['Project']} (Health: {at_risk_project['Health Score (%)']}%)**"):
        st.warning(f"AI Forecaster predicts a {at_risk_project['Predicted Finish'].strftime('%Y-%m-%d')} finish date, a {(at_risk_project['Predicted Finish'] - at_risk_project['Planned Finish']).days}-day delay.")
        
        scenario = st.radio("Select Mitigation Strategy to Simulate:", 
                            ["Add 1 Validation Engineer", "Authorize Overtime", "De-scope Non-Critical Feature"],
                            horizontal=True)
        
        if st.button("Simulate Scenario Impact", use_container_width=True):
            with st.spinner(f"Running 10,000 Monte Carlo simulations for '{scenario}'..."):
                results = run_mitigation_simulation(scenario)
                time.sleep(2)
                st.success(f"Simulation Complete for '{scenario}'")
                res_col1, res_col2, res_col3 = st.columns(3)
                res_col1.metric("New Predicted Finish", results['new_finish_date'])
                res_col2.metric("Budget Impact", f"${results['budget_impact']:,}k")
                res_col3.metric("Probability of On-Time Finish", f"{results['success_prob']}%")

    st.subheader("Automated Project Risk & Timeline Forecaster")
    st.dataframe(portfolio_df[['Project', 'Status', 'Health Score (%)', 'Planned Finish', 'Predicted Finish']], use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 5: GENERATIVE GXP & COMPLIANCE
# ==============================================================================
with tab5:
    st.header("Generative GxP Documentation & Compliance Suite")
    st.caption("This module addresses compliance duties by leveraging AI to generate GxP documents, drastically reducing documentation overhead and ensuring consistency with **GAMP 5** and **21 CFR Part 11**.")

    st.subheader("Generative GxP Documentation Suite")
    st.markdown("This **10++** feature accelerates the entire validation lifecycle. Select a system and document type, and let the GAMP 5-trained LLM generate a high-quality first draft, turning weeks of writing into hours of reviewing.")
    
    gxp_col1, gxp_col2 = st.columns(2)
    with gxp_col1:
        system_to_validate = st.selectbox("Select System from VMP:", vmp_df['System/Instrument'].unique())
        doc_type = st.selectbox("Select GxP Document to Generate:", ["Validation Plan (VP)", "Installation Qualification (IQ)", "Operational Qualification (OQ)", "Validation Summary Report (VSR)"])
    
    with gxp_col2:
        st.write(" ") # for spacing
        st.write(" ")
        if st.button(f"📄 Generate {doc_type} Draft for {system_to_validate}", use_container_width=True):
            with st.spinner(f"Generating {doc_type} draft..."):
                doc_draft = generate_gxp_document(system_to_validate, doc_type)
                time.sleep(3)
                st.text_area(f"Generated {doc_type} Draft:", doc_draft, height=300)

    st.divider()
    st.subheader("Validation & Audit Readiness")
    st.dataframe(audit_df.style.map(lambda val: 'background-color: lightcoral' if val == 'Gap Identified' else 'background-color: lightyellow' if val == 'Needs Review' else '', subset=['Status']), use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 6: LEADERSHIP & GLOBAL ALIGNMENT
# ==============================================================================
with tab6:
    st.header("Leadership: Team Performance & Global Alignment")
    st.caption("This module addresses duties related to team leadership and matrix leadership, ensuring personnel are qualified as per **GxP** requirements.")

    st.subheader("Team Performance & Development Hub")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("**Team Skills & Training Matrix**")
        st.dataframe(team_df.style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**Identified Skill Gap & Training Need**")
        st.warning(f"**GAP:** {skills_gap['gap']}\n\n**Recommendation:** {skills_gap['recommendation']}")

    st.divider()

    st.subheader("Matrix Leadership: Global Alignment Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**West Coast vs. Global KPI Benchmark**")
        for index, row in global_kpis_df.iterrows():
            st.metric(label=f"{row['KPI']}", value=f"{row['West Coast']}{row.get('unit','')}", delta=f"{(row['West Coast'] - row['Global Avg']):.1f}{row.get('unit','')}", help=f"vs. Global Average of {row['Global Avg']}{row.get('unit','')}")
    
    with col2:
        st.markdown("**Global Best Practice Exchanger (AI Identified)**")
        st.success("**New Best Practice Identified (from Boston DTE):**\n- **Issue:** 'Lab Printer Offline' incidents.\n- **Boston's Solution:** Proactive ping script to auto-generate low-priority tickets before user reports.\n- **Impact:** Reduced user-reported printer incidents by 90%.\n- **Recommendation:** Pilot this solution in the San Diego lab.")
