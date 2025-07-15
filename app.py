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
        st.caption("Generate a pre-formatted weekly summary for site leadership using live data from all modules.")
        if st.button("🚀 Generate Briefing", type="primary"):
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
# Page Implementations - SUBSTANTIALLY ENHANCED WITH EXPLANATIONS
# ==============================================================================

if page == "🏠 **Home Cockpit**":
    st.header(f"🎯 Home Cockpit: Strategic Overview for **{site_selection}**")
    st.caption("This is your command center for at-a-glance strategic assessment. These top-level KPIs provide a summary of operational effectiveness, project execution, compliance posture, and financial health.")

    oee_data = data['oee_data']
    portfolio_df_filtered = filter_df_by_site(data["portfolio_df"])

    st.subheader("Key Performance Indicators (KPIs)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="🔬 Lab Operations (OEE)",
            value=f"{oee_data['oee']:.1%}",
            help="**Overall Equipment Effectiveness (OEE)** is the gold standard for measuring lab productivity. It is calculated as: **Availability x Performance x Quality**. An OEE score of 100% means you are running only good parts, as fast as possible, with no stop time. The target for a high-performing lab is typically >90%."
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
            help="**Portfolio Health** measures project execution against commitments. This KPI provides an immediate signal of delivery risk and is critical for discussions with site leadership and stakeholders."
        )
    with kpi3:
        st.metric(
            label="📋 Compliance Risk Score",
            value=data['compliance_risk'],
            delta="5 points from last week",
            delta_color="inverse",
            help="The **Compliance Risk Score** quantifies your GxP compliance posture into a single, trendable number. It is a weighted score of deviations like overdue validations, open CAPAs, and unresolved change controls. **A lower score is better.** This metric is essential for audit readiness and internal quality reporting."
        )
    with kpi4:
        spend = sum(fin['spend'] for fin in data['project_financials'].values())
        budget = sum(fin['budget'] for fin in data['project_financials'].values())
        st.metric(
            label="💵 Financial Velocity",
            value=f"{spend/budget:.1%}",
            help=f"Percentage of total project budget spent (${spend:,.0f}k of ${budget:,.0f}k). Monitors burn rate against project timelines. A low velocity might indicate stalled projects, while a high velocity could signal a risk of budget overrun."
        )
        st.progress(spend/budget)

    st.divider()
    st.subheader("Systemic Risk & AI Recommendations")
    st.caption("The platform continuously analyzes cross-functional data to identify hidden risks that might be missed in siloed systems. These are the most critical, high-impact issues requiring your attention.")
    risk = data["systemic_risk"]
    st.error(f"**{risk['title']}**\n\n{risk['insight']}", icon="🔥")
    st.info(f"**Recommendation:** {risk['recommendation']}")

elif page == "📈 **Interactive Portfolio Modeler**":
    st.header("📈 Interactive Portfolio Modeler")
    st.caption("This tool transforms static project plans into a dynamic simulation environment. Use it to proactively assess the impact of potential delays on timelines and budget *before* they happen. This is essential for strategic planning and resource negotiation.")

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
        st.subheader("Simulation Impact Analysis")
        st.caption("The calculated financial and schedule impact of the simulated delay.")
        st.metric("Calculated Budget Impact", f"${cost_impact:,.0f}k", help="The estimated additional cost from extended resource allocation (burn rate) during the delay period. Use this data to justify requests for additional resources or to push back on scope changes.")
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
    st.caption("This plot moves beyond simple TCO by adding the dimensions of **Reliability** and **Scientific Impact**. It is a powerful tool for making data-driven decisions about asset lifecycle management. Use it to identify which assets to replace, which to invest in, and which to simply maintain.")
    st.info("**How to interpret this chart:**\n- **Top-Left (Value Drains):** High Cost, Low Reliability. These are your prime candidates for replacement. Use the CapEx generator below.\n- **Bottom-Right (Workhorses):** Low Cost, High Reliability. These are your ideal assets. Protect and maintain them.\n- **Top-Right (Critical & Costly):** High Cost, High Reliability. High impact assets here are acceptable, but monitor their TCO closely.\n- **Bottom-Left (Nuisances):** Low Cost, Low Reliability. Assess if their low scientific impact justifies the support overhead.")

    fig_quad = px.scatter(
        tco_df_filtered, x="Uptime (%)", y="TCO ($k)", size="Scientific Impact", color="Asset Type",
        hover_name="Asset ID", title="Asset Value & Lifecycle Priority Matrix", size_max=60,
        labels={"Uptime (%)": "Reliability (Uptime %)", "TCO ($k)": "Total Cost of Ownership ($k)"}
    )
    if not tco_df_filtered.empty:
        fig_quad.add_vline(x=tco_df_filtered['Uptime (%)'].mean(), line_dash="dash", annotation_text="Avg. Uptime")
        fig_quad.add_hline(y=tco_df_filtered['TCO ($k)'].mean(), line_dash="dash", annotation_text="Avg. TCO")
    st.plotly_chart(fig_quad, use_container_width=True)
    
    with st.expander("🤖 Generate CapEx Proposal for a 'Value Drain' Asset"):
        st.write("Select an asset (ideally from the 'Value Drains' quadrant) to automatically generate a data-driven replacement proposal.")
        if not tco_df_filtered.empty:
            selected_asset_id = st.selectbox("Select Asset for CapEx Proposal:", options=tco_df_filtered['Asset ID'], key="capex_asset")
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
    st.caption("As scientific computing moves to the cloud, managing this variable spend is critical. This dashboard provides visibility into cloud costs by project and service, enabling you to identify waste and optimize spend.")
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
    st.caption("This heatmap shows the busiest and quietest times for lab instruments. Use this analysis to identify opportunities for scheduling optimization, justify the need for new equipment, or guide scientists to periods of lower usage to reduce wait times.")
    heatmap_df = data['utilization_heatmap']
    fig_heatmap = px.imshow(heatmap_df, text_auto=True, aspect="auto", color_continuous_scale='RdYlGn_r', title=f"Instrument Group Utilization Heatmap ({site_selection})")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.divider()
    st.subheader("End-to-End Sample Journey & Turnaround Time (TTR)")
    st.caption("This view provides complete traceability for a single sample, which is invaluable for Out-of-Specification (OOS) investigations. The TTR metric is a direct measure of the lab's velocity and its impact on scientific timelines.")
    sample_journey_df = data['sample_journey']
    ttr = (sample_journey_df['Timestamp'].max() - sample_journey_df['Timestamp'].min())
    st.metric("Sample Turnaround Time (TTR)", f"{ttr.total_seconds()/3600:.1f} Hours", help="**Turnaround Time** is the total time from 'Sample Received' to 'Result Certified'. A lower, consistent TTR is a key indicator of an efficient and predictable lab operation.")
    st.dataframe(sample_journey_df)

elif page == "⚙️ **Autonomous Operations**":
    st.header(f"⚙️ Autonomous Operations for **{site_selection}**")

    st.subheader("Reliability & Maintenance KPIs")
    st.caption("These KPIs measure the effectiveness of your maintenance strategy and the overall reliability of your lab technology. An upward trend in MTBF and an increasing number of avoided downtimes demonstrate a successful shift from reactive firefighting to proactive, predictive maintenance.")
    op_kpi1, op_kpi2 = st.columns(2)
    pred_maint_df = data['pred_maint_data']
    op_kpi1.metric("Downtime Events Avoided (YTD)", int(pred_maint_df['Downtime Avoided (Hours)'].sum() / 8), help="Number of major downtime events (assuming 8 hours/event) prevented by predictive maintenance.")

    mtbf_df = data['mtbf_df']
    last_mtbf = mtbf_df['MTBF (Hours)'].iloc[-1]
    prev_mtbf = mtbf_df['MTBF (Hours)'].iloc[-2]
    op_kpi2.metric("Mean Time Between Failures (MTBF)", f"{last_mtbf:.0f} Hours", delta=f"{last_mtbf - prev_mtbf:.0f}h vs last month")

    fig_mtbf = px.line(data['mtbf_df'], x='Month', y='MTBF (Hours)', title='Mean Time Between Failures (MTBF) Trend', markers=True)
    fig_mtbf.update_layout(yaxis_title="MTBF (Hours)", legend_title_text=None)
    st.plotly_chart(fig_mtbf, use_container_width=True)

    with st.expander("Predictive Maintenance Workflow & Digital Twin Simulation"):
        st.info("The tools below allow you to action the insights from the reliability KPIs.")
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
    st.caption("These metrics provide a quantifiable, real-time view of your compliance posture, transforming audit preparation from a periodic scramble into a state of continuous readiness.")
    gxp_kpi1, gxp_kpi2 = st.columns(2)
    risk_vmp_df = filter_df_by_site(data['risk_vmp_df'])
    if not risk_vmp_df.empty:
        validated_count = risk_vmp_df[risk_vmp_df['Status'] != 'At Risk'].shape[0]
        gxp_kpi1.metric("GxP Validation Coverage", f"{validated_count / risk_vmp_df.shape[0]:.1%}", help="Percentage of GxP-critical systems currently in a validated state.")
        gxp_kpi2.metric("High-Risk Systems Due Validation (<30d)", risk_vmp_df[(risk_vmp_df['Days Until Due'] < 30) & (risk_vmp_df['System Criticality'] > 7)].shape[0])

    st.subheader("Risk-Adjusted Validation Master Plan (VMP)")
    st.caption("This matrix moves beyond simple due dates to prioritize validation efforts based on **risk and criticality**. It ensures that your team's valuable time is spent on the systems that pose the greatest risk to GxP compliance and scientific outcomes if they fail. Focus on the top-right quadrant first.")
    fig_risk_vmp = px.scatter(risk_vmp_df, x="Days Until Due", y="System Criticality", size="Validation Effort (Hours)", color="Status", hover_name="System/Instrument", title="Validation Priority Matrix")
    if not risk_vmp_df.empty:
        fig_risk_vmp.add_annotation(x=30, y=8, text="High Urgency/Risk Zone ->", showarrow=True, arrowhead=1)
    st.plotly_chart(fig_risk_vmp, use_container_width=True)

    with st.expander("Interactive Audit Trail Navigator (21 CFR Part 11)"):
        st.caption("This tool provides a searchable, 'living' system file log. During an audit, you can answer data integrity questions instantly, demonstrating control and compliance with 21 CFR Part 11.")
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
    st.caption("Effective leadership requires not just managing the present, but preparing for the future. This module cross-references the skills required for upcoming projects with the current capabilities of your team to proactively identify and address strategic skill gaps.")
    
    team_perf_df, skills_gap = data['team_perf_df'], data['skills_gap']
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Upcoming Project Skill Demand:**\n- 'AI Drug Discovery': Advanced Python, Cloud (FinOps)\n- 'LIMS v3 Upgrade': Advanced CSV/Validation")
    with col2:
        st.warning(f"**AI-Identified Gap:** {skills_gap['gap']}\n\n**Recommendation:** {skills_gap['recommendation']}")
    
    st.subheader("Team Skills Matrix")
    st.caption("A current snapshot of your team's proficiency across key technology domains. Use this to inform training plans and make balanced project assignments.")
    st.dataframe(filter_df_by_site(team_perf_df).style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''))
    
    st.subheader("Resource Allocation Heatmap")
    st.caption("This heatmap visualizes your team's workload over the next six months. It provides an at-a-glance view to identify and prevent team member burnout (red cells) and find available capacity for new tasks (green cells). This is a critical tool for effective load-balancing and sustainable high performance.")
    heatmap_df = data['resource_allocation_df']
    fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_df.values, x=heatmap_df.columns, y=heatmap_df.index, colorscale='RdYlGn_r'))
    fig_heatmap.update_layout(title='Resource Allocation Forecast (%)')
    st.plotly_chart(fig_heatmap, use_container_width=True)
