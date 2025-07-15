import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from utils import (
    # Explicitly import all required functions for clarity and error prevention
    get_project_portfolio_data,
    get_tco_data,
    get_team_performance,
    get_global_kpis,
    get_assay_impact_data,
    get_clinical_sample_journey,
    get_systemic_risk_insight,
    get_living_system_file_log,
    get_risk_adjusted_vmp_data,
    get_predictive_maintenance_data,
    # "10++" Enhancement Functions
    get_oee_data,
    get_compliance_risk_score,
    get_project_financials,
    get_finops_data,
    get_instrument_utilization_data,
    get_utilization_heatmap_data,
    get_mtbf_data,
    get_resource_allocation_data,
    get_action_center_items,
    generate_weekly_briefing_text,
    generate_capex_proposal_text,
    run_digital_twin_simulation,
    search_audit_log,
    get_reagent_genealogy_data
)

# ==============================================================================
# Page Configuration & Initial State
# ==============================================================================
st.set_page_config(
    page_title="DTE West Coast Sentient Platform | Vertex",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state for interactive elements
if 'action_items' not in st.session_state:
    st.session_state.action_items = None
if 'pred_maint_data' not in st.session_state:
    st.session_state.pred_maint_data = get_predictive_maintenance_data()
if 'edited_portfolio' not in st.session_state:
    st.session_state.edited_portfolio = None

# ==============================================================================
# Data Loading (Cached for performance)
# ==============================================================================
@st.cache_data
def load_all_data():
    """Loads all data, now including data for 10++ enhancements."""
    portfolio_df = get_project_portfolio_data()
    team_perf_df, skills_gap = get_team_performance()
    return {
        "portfolio_df": portfolio_df,
        "tco_df": get_tco_data(),
        "team_perf_df": team_perf_df,
        "skills_gap": skills_gap,
        "global_kpis": get_global_kpis(),
        "assay_impact_df": get_assay_impact_data(),
        "sample_journey": get_clinical_sample_journey(),
        "systemic_risk": get_systemic_risk_insight(),
        "living_system_log": get_living_system_file_log(),
        "risk_vmp_df": get_risk_adjusted_vmp_data(),
        # 10++ Enhancement Data
        "oee_data": get_oee_data(),
        "compliance_risk": get_compliance_risk_score(),
        "project_financials": get_project_financials(),
        "finops_df": get_finops_data(),
        "utilization_df": get_instrument_utilization_data(),
        "utilization_heatmap": get_utilization_heatmap_data(),
        "mtbf_df": get_mtbf_data(),
        "resource_allocation_df": get_resource_allocation_data(portfolio_df),
    }

data = load_all_data()
if st.session_state.action_items is None:
    st.session_state.action_items = get_action_center_items(st.session_state.pred_maint_data)

# ==============================================================================
# Sidebar
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Vertex_Pharmaceuticals_logo.svg/2560px-Vertex_Pharmaceuticals_logo.svg.png", width=150)
    st.title("DTE West Coast Sentient Platform")
    site_selection = st.selectbox("Select Site View:", ["West Coast (Overall)", "San Diego", "Seattle"])
    page = st.radio(
        "Navigation",
        ["🏠 **Home Cockpit**",
         "📈 **Interactive Portfolio Modeler**",
         "💼 **Financial Intelligence & FinOps**",
         "🔬 **Scientific & Lab Operations**",
         "⚙️ **Autonomous Operations**",
         "📋 **GxP & Audit Readiness**",
         "👥 **Leadership & Resource Planning**"],
        label_visibility="collapsed"
    )
    st.divider()

    pending_items = [item for item in st.session_state.action_items if item['status'] == 'Pending']
    st.header(f"Action Center ({len(pending_items)})")
    if not pending_items:
        st.success("No pending approvals.")
    else:
        for item in pending_items:
            with st.expander(f"📌 {item['type']}: {item['id']}"):
                st.write(item['description'])
                c1, c2 = st.columns(2)
                if c1.button("✅ Approve", key=f"app_{item['id']}", use_container_width=True):
                    item['status'] = 'Approved'
                    st.success(f"Approved: {item['id']}")
                    st.rerun()
                if c2.button("❌ Reject", key=f"rej_{item['id']}", use_container_width=True):
                    item['status'] = 'Rejected'
                    st.warning(f"Rejected: {item['id']}")
                    st.rerun()
    st.divider()

    st.header("🤖 AI Strategic Advisor")
    with st.expander("Generate Weekly Briefing"):
        if st.button("🚀 Generate Briefing for Leadership", type="primary"):
            with st.spinner("AI is synthesizing data from all modules..."):
                briefing_text = generate_weekly_briefing_text(site_selection if site_selection != "West Coast (Overall)" else "San Diego", data)
                st.session_state.briefing = briefing_text
        if 'briefing' in st.session_state:
            st.text_area("Generated Briefing:", st.session_state.briefing, height=200)
            st.download_button("Download as .txt", st.session_state.briefing, "weekly_briefing.txt")

# ==============================================================================
# Site-Specific Data Filtering Helper
# ==============================================================================
def filter_df_by_site(df, site_col='Site'):
    if site_selection != "West Coast (Overall)" and site_col in df.columns:
        return df[df[site_col] == site_selection].copy()
    return df.copy()

# ==============================================================================
# Page Implementations - SUBSTANTIALLY ENHANCED
# ==============================================================================

if page == "🏠 **Home Cockpit**":
    st.header(f"🎯 Home Cockpit: Strategic Overview for **{site_selection}**")
    st.caption("Your command center for at-a-glance strategic assessment and actionability.")

    oee_data = data['oee_data']
    portfolio_df_filtered = filter_df_by_site(data["portfolio_df"])

    st.subheader("Key Performance Indicators (KPIs)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="🔬 Lab Operations (OEE)",
            value=f"{oee_data['oee']:.1%}",
            help="Overall Equipment Effectiveness: A composite score of Availability (uptime), Performance (speed), and Quality (error-free runs). Target >90%."
        )
        st.progress(oee_data['oee'])
    with kpi2:
        at_risk_count = portfolio_df_filtered[portfolio_df_filtered['Status'] == 'At Risk'].shape[0]
        total_count = portfolio_df_filtered.shape[0]
        st.metric(
            label="📈 Portfolio Health",
            value=f"{total_count - at_risk_count} / {total_count} Projects",
            delta=f"-{at_risk_count} At Risk" if at_risk_count > 0 else "All On Track",
            delta_color="inverse" if at_risk_count > 0 else "normal",
            help="The number of projects currently on track versus the total active projects for the selected site."
        )
    with kpi3:
        st.metric(
            label="📋 Compliance Risk Score",
            value=data['compliance_risk'],
            delta="5 points from last week",
            delta_color="inverse",
            help="A weighted score of compliance deviations (e.g., overdue validations, open CAPAs). Lower is better."
        )
    with kpi4:
        spend = sum(fin['spend'] for fin in data['project_financials'].values())
        budget = sum(fin['budget'] for fin in data['project_financials'].values())
        st.metric(
            label="💵 Financial Velocity",
            value=f"{spend/budget:.1%}",
            help=f"Percentage of total project budget spent (${spend}k of ${budget}k). Monitors burn rate against project timelines."
        )
        st.progress(spend/budget)

    st.divider()
    st.subheader("Systemic Risk & AI Recommendations")
    risk = data["systemic_risk"]
    st.error(f"**{risk['title']}**\n\n{risk['insight']}", icon="🔥")
    st.info(f"**Recommendation:** {risk['recommendation']}")

elif page == "📈 **Interactive Portfolio Modeler**":
    st.header("📈 Interactive Portfolio Modeler")
    st.caption("Simulate project delays to instantly see the calculated impact on budget, resources, and dependent timelines.")
    portfolio_df = filter_df_by_site(data["portfolio_df"])

    if st.session_state.edited_portfolio is None or st.button('Reset Simulation'):
        st.session_state.edited_portfolio = portfolio_df.copy()

    sim_col, impact_col = st.columns([2, 1])
    with sim_col:
        selected_task = st.selectbox("Select Project to Delay:", options=st.session_state.edited_portfolio['Task'])
        delay_weeks = st.slider("Delay (Weeks):", 0, 12, 0)

    gantt_df = st.session_state.edited_portfolio.copy()
    impact_text = ""
    cost_impact = 0

    if delay_weeks > 0 and selected_task:
        task_row_list = gantt_df[gantt_df['Task'] == selected_task]
        if not task_row_list.empty:
            task_row = task_row_list.iloc[0]
            task_idx = task_row.name
            gantt_df.loc[task_idx, 'Finish'] += timedelta(weeks=delay_weeks)
            cost_impact = delay_weeks * task_row['Weekly_Cost_k']

            dependency_impacted = gantt_df[gantt_df['Dependencies'] == selected_task]
            if not dependency_impacted.empty:
                impacted_task_name = dependency_impacted.iloc[0]['Task']
                impact_text = f"🚨 **Dependency Alert:** Delaying '{selected_task}' will cause a cascading delay to **'{impacted_task_name}'**."

    with impact_col:
        st.subheader("Simulation Impact")
        st.metric("Calculated Budget Impact", f"${cost_impact:,.0f}k", help="Estimated additional cost due to extended resource allocation for the delayed project.")
        if impact_text:
            st.error(impact_text)
        else:
            st.success("✅ No direct dependency conflicts detected.")

    fig = px.timeline(gantt_df, x_start="Start", x_end="Finish", y="Task", color="Site", title="Project Portfolio Gantt Simulation")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

elif page == "💼 **Financial Intelligence & FinOps**":
    st.header(f"💼 Financial Intelligence & FinOps for **{site_selection}**")
    tco_df_filtered = filter_df_by_site(data["tco_df"])

    st.subheader("Asset Value Quadrant: Identifying Actionable Priorities")
    st.caption("This plot helps prioritize asset lifecycle management. Ideal assets are in the bottom-right (low cost, high uptime). Assets in the top-left are prime candidates for replacement.")

    fig_quad = px.scatter(
        tco_df_filtered,
        x="Uptime (%)",
        y="TCO ($k)",
        size="Scientific Impact",
        color="Asset Type",
        hover_name="Asset ID",
        title="Asset Value & Lifecycle Priority Matrix",
        size_max=60,
        labels={"Uptime (%)": "Reliability (Uptime %)", "TCO ($k)": "Total Cost of Ownership ($k)"}
    )
    if not tco_df_filtered.empty:
        fig_quad.add_vline(x=tco_df_filtered['Uptime (%)'].mean(), line_dash="dash", annotation_text="Avg. Uptime")
        fig_quad.add_hline(y=tco_df_filtered['TCO ($k)'].mean(), line_dash="dash", annotation_text="Avg. TCO")
    st.plotly_chart(fig_quad, use_container_width=True)

    with st.expander("Generate CapEx Proposal"):
        if not tco_df_filtered.empty:
            selected_asset_id = st.selectbox("Select Asset for CapEx Proposal:", options=tco_df_filtered['Asset ID'])
            if st.button("🤖 Generate CapEx Proposal", type="primary"):
                asset_details = tco_df_filtered[tco_df_filtered['Asset ID'] == selected_asset_id].iloc[0]
                with st.spinner(f"AI is drafting a proposal for {selected_asset_id}..."):
                    st.session_state.proposal = generate_capex_proposal_text(asset_details)
            if 'proposal' in st.session_state:
                st.text_area("Generated CapEx Draft:", st.session_state.proposal, height=300)
                st.download_button("Download as .txt", st.session_state.proposal, f"CapEx_{selected_asset_id}.txt")
        else:
            st.warning("No assets to display for the selected site.")

    st.divider()
    st.subheader("Cloud FinOps: Cost Optimization & Forecasting")
    finops_df = data['finops_df']
    cost_kpi1, cost_kpi2 = st.columns(2)
    wasted_spend = finops_df[finops_df['Service'].isin(['EC2 (Compute)', 'S3 (Storage)']) ]['Cost ($)'].sum() * 0.15
    cost_kpi1.metric("Cloud Spend (Last 90d)", f"${finops_df['Cost ($)'].sum():,.0f}")
    cost_kpi2.metric("Est. Wasted Spend", f"${wasted_spend:,.0f}", help="Estimated cost of idle or over-provisioned resources. Target for optimization.")

    fig_cost = px.area(finops_df, x='Date', y='Cost ($)', color='Project', title='Cloud Spend Over Time by Project')
    st.plotly_chart(fig_cost, use_container_width=True)

elif page == "🔬 **Scientific & Lab Operations**":
    st.header(f"🔬 Scientific & Lab Operations at **{site_selection}**")

    st.subheader("Instrument Utilization Patterns")
    st.caption("Analyze instrument usage by time of day to identify bottlenecks and opportunities for scheduling optimization.")

    heatmap_df = data['utilization_heatmap']
    fig_heatmap = px.imshow(heatmap_df, text_auto=True, aspect="auto", color_continuous_scale='RdYlGn_r', title=f"Instrument Group Utilization Heatmap ({site_selection})")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.divider()
    st.subheader("End-to-End Sample Journey & Turnaround Time (TTR)")
    sample_journey_df = data['sample_journey']
    ttr = (sample_journey_df['Timestamp'].max() - sample_journey_df['Timestamp'].min())
    st.metric("Sample Turnaround Time (TTR)", f"{ttr.total_seconds()/3600:.1f} Hours", help="Total time from 'Sample Received' to 'Result Certified'.")
    st.dataframe(sample_journey_df)

elif page == "⚙️ **Autonomous Operations**":
    st.header(f"⚙️ Autonomous Operations for **{site_selection}**")

    st.subheader("Reliability & Maintenance KPIs")
    op_kpi1, op_kpi2 = st.columns(2)
    pred_maint_df = data['pred_maint_data']
    op_kpi1.metric("Downtime Events Avoided (YTD)", int(pred_maint_df['Downtime Avoided (Hours)'].sum() / 8), help="Number of major downtime events (assuming 8 hours/event) prevented by predictive maintenance.")

    mtbf_df = data['mtbf_df']
    last_mtbf = mtbf_df['MTBF (Hours)'].iloc[-1]
    prev_mtbf = mtbf_df['MTBF (Hours)'].iloc[-2]
    op_kpi2.metric("Mean Time Between Failures (MTBF)", f"{last_mtbf:.0f} Hours", delta=f"{last_mtbf - prev_mtbf:.0f}h vs last month")

    fig_mtbf = px.line(mtbf_df, x='Month', y='MTBF (Hours)', title='MTBF Trend (Higher is Better)', markers=True)
    st.plotly_chart(fig_mtbf, use_container_width=True)

    with st.expander("Predictive Maintenance Workflow & Digital Twin Simulation"):
        st.subheader("Predictive Maintenance with Work Order Integration")
        pred_maint_df_filtered = filter_df_by_site(st.session_state.pred_maint_data)
        st.dataframe(pred_maint_df_filtered.style.highlight_max(subset=['Predicted Failure Risk (%)'], color='lightcoral'), use_container_width=True, hide_index=True)

        st.subheader("Digital Twin for GxP Change Simulation")
        change_desc = st.text_input("Describe the change for simulation:", "Apply security patch KB5034122 to LIMS-PROD server")
        if st.button("🚀 Run Simulation in Digital Twin", type="primary"):
            with st.spinner("Simulation in progress..."):
                st.session_state.sim_result = run_digital_twin_simulation(change_desc)
        if 'sim_result' in st.session_state:
            st.metric("Assessed Risk Level", st.session_state.sim_result['risk'])
            st.text_area("Simulation Impact Report", st.session_state.sim_result['impact'], height=150)

elif page == "📋 **GxP & Audit Readiness**":
    st.header(f"📋 GxP & Audit Readiness for **{site_selection}**")

    st.subheader("Compliance Posture KPIs")
    gxp_kpi1, gxp_kpi2 = st.columns(2)
    risk_vmp_df = filter_df_by_site(data['risk_vmp_df'])
    if not risk_vmp_df.empty:
        validated_count = risk_vmp_df[risk_vmp_df['Status'] != 'At Risk'].shape[0]
        gxp_kpi1.metric("GxP Validation Coverage", f"{validated_count / risk_vmp_df.shape[0]:.1%}", help="Percentage of GxP-critical systems currently in a validated state.")
        gxp_kpi2.metric("High-Risk Systems Due Validation (<30d)", risk_vmp_df[(risk_vmp_df['Days Until Due'] < 30) & (risk_vmp_df['System Criticality'] > 7)].shape[0])

    st.subheader("Risk-Adjusted Validation Master Plan")
    fig_risk_vmp = px.scatter(risk_vmp_df, x="Days Until Due", y="System Criticality", size="Validation Effort (Hours)", color="Status", hover_name="System/Instrument", title="Validation Priority Matrix")
    fig_risk_vmp.add_annotation(x=30, y=8, text="High Urgency/Risk Zone ->", showarrow=True, arrowhead=1)
    st.plotly_chart(fig_risk_vmp, use_container_width=True)

    with st.expander("Interactive Audit Trail Navigator (21 CFR Part 11)"):
        living_log_df = data['living_system_log']
        query = st.text_input("Search the audit trail (e.g., \"Show actions by user 'davis_c' on LIMS-PROD\")", help="Search by user or system name.")
        if query:
            results_df = search_audit_log(living_log_df, query)
        else:
            results_df = living_log_df
        st.dataframe(results_df, use_container_width=True, hide_index=True)

elif page == "👥 **Leadership & Resource Planning**":
    st.header(f"👥 Leadership & Resource Planning for **{site_selection}**")

    st.subheader("AI-Powered Strategic Skill Development")
    st.caption("Cross-referencing upcoming project needs with current team skills to identify and mitigate future resource gaps.")

    team_perf_df, skills_gap = data['team_perf_df'], data['skills_gap']

    col1, col2 = st.columns(2)
    with col1:
        st.info("**Upcoming Project Skill Demand:**\n- 'AI Drug Discovery': Advanced Python, Cloud (FinOps)\n- 'LIMS v3 Upgrade': Advanced CSV/Validation")
    with col2:
        st.warning(f"**AI-Identified Gap:** {skills_gap['gap']}\n\n**Recommendation:** {skills_gap['recommendation']}")

    st.subheader("Team Skills Matrix")
    st.dataframe(filter_df_by_site(team_perf_df).style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''))

    st.subheader("Resource Allocation Heatmap")
    heatmap_df = data['resource_allocation_df']
    fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_df.values, x=heatmap_df.columns, y=heatmap_df.index, colorscale='RdYlGn_r'))
    fig_heatmap.update_layout(title='Resource Allocation Forecast (%)')
    st.plotly_chart(fig_heatmap, use_container_width=True)
