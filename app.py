import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta
from utils import (
    # Import all new and existing functions
    get_project_portfolio_data, get_itsm_ticket_data, get_tco_data,
    get_predictive_maintenance_data, get_team_performance, get_global_kpis,
    get_assay_impact_data, get_reagent_genealogy_data,
    get_clinical_sample_journey, get_qms_query_result,
    get_systemic_risk_insight, get_living_system_file_log,
    get_automation_roi_data, get_risk_adjusted_vmp_data,
    # "10+" Enhancement Functions
    get_action_center_items, generate_weekly_briefing_text,
    generate_capex_proposal_text, get_finops_data,
    get_instrument_utilization_data, run_digital_twin_simulation,
    search_audit_log, get_resource_allocation_data
)

# ==============================================================================
# Page Configuration & Initial State
# ==============================================================================
st.set_page_config(
    page_title="DTE West Coast Sentient Platform | Vertex",
    page_icon="🚀",
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
# Helper Functions (Retained for completeness)
# ==============================================================================
def create_spc_chart(data, mttr_series):
    """Creates a Statistical Process Control (SPC) chart for MTTR."""
    if mttr_series.empty or data.empty:
        return go.Figure().update_layout(title_text="No Data for SPC Chart")
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
    fig.update_layout(title_text="Service Stability SPC Chart (ITIL)", yaxis_title="Ticket Volume", xaxis_title="Date")
    fig.update_yaxes(title_text="Avg. Resolution (Hours)", secondary_y=True)
    return fig

def create_pareto_chart(df):
    """Creates a true Pareto chart to identify the 'vital few' root causes."""
    if df.empty:
        return go.Figure().update_layout(title_text="No Data for Pareto Chart")
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
    """Loads all data, now including data for 10+ enhancements."""
    portfolio_df = get_project_portfolio_data()
    tickets_df, mttr_data = get_itsm_ticket_data()
    team_perf_df, skills_gap = get_team_performance()
    data = {
        "portfolio_df": portfolio_df,
        "tco_df": get_tco_data(),
        "tickets_df": tickets_df,
        "mttr_data": mttr_data,
        "team_perf_df": team_perf_df,
        "skills_gap": skills_gap,
        "global_kpis": get_global_kpis(),
        "assay_impact_df": get_assay_impact_data(),
        "sample_journey": get_clinical_sample_journey(),
        "systemic_risk": get_systemic_risk_insight(),
        "living_system_log": get_living_system_file_log(),
        "automation_roi": get_automation_roi_data(),
        "risk_vmp_df": get_risk_adjusted_vmp_data(),
        # 10+ Enhancement Data
        "finops_df": get_finops_data(),
        "utilization_df": get_instrument_utilization_data(),
        "resource_allocation_df": get_resource_allocation_data(portfolio_df),
    }
    return data

data = load_all_data()
# Load action items into state
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

    # --- Enhancement #1: Action Center & Approval Workflow ---
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

    # --- Enhancement #2: "Generate Weekly Briefing" AI Agent ---
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
# Site-Specific Data Filtering (Helper)
# ==============================================================================
def filter_df_by_site(df, site_col='Site'):
    if site_selection != "West Coast (Overall)" and site_col in df.columns:
        return df[df[site_col] == site_selection].copy()
    return df.copy()

# ==============================================================================
# Page Implementations
# ==============================================================================
if page == "🏠 **Home Cockpit**":
    st.header(f"🏠 Home Cockpit for **{site_selection}**")
    st.caption("A high-level summary of all strategic and operational domains.")

    col1, col2, col3 = st.columns(3)
    portfolio_df_filtered = filter_df_by_site(data["portfolio_df"])
    col1.metric("Active Projects", portfolio_df_filtered.shape[0])
    col2.metric("Projects At Risk", portfolio_df_filtered[portfolio_df_filtered['Status'] == 'At Risk'].shape[0])
    col3.metric("Pending Approvals", len(pending_items))

    st.divider()
    st.subheader("Systemic Risk Insights")
    risk = data["systemic_risk"]
    st.error(f"**{risk['title']}**\n\n{risk['insight']}", icon="🔥")
    st.info(f"**Recommendation:** {risk['recommendation']}")
    st.info("Welcome to the Sentient Platform. Use the navigation on the left to dive into specific domains.")


elif page == "📈 **Interactive Portfolio Modeler**":
    st.header("📈 Interactive Portfolio Modeler")
    st.caption("Simulate project delays to instantly see downstream impacts on dependencies and timelines.")
    portfolio_df = filter_df_by_site(data["portfolio_df"])

    if st.session_state.edited_portfolio is None or st.button('Reset Simulation'):
        st.session_state.edited_portfolio = portfolio_df.copy()

    st.info("Select a project to simulate a delay and see the calculated impact on dependent tasks.")

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_task = st.selectbox("Select Project to Delay:", options=st.session_state.edited_portfolio['Task'])
    with col2:
        delay_weeks = st.slider("Delay (Weeks):", 0, 12, 0)

    # Prepare DataFrame for Gantt chart
    gantt_df = st.session_state.edited_portfolio.copy()

    if delay_weeks > 0 and selected_task:
        task_idx_list = gantt_df.index[gantt_df['Task'] == selected_task].tolist()
        if task_idx_list:
            task_idx = task_idx_list[0]
            original_finish = gantt_df.loc[task_idx, 'Finish']
            gantt_df.loc[task_idx, 'Finish'] = original_finish + timedelta(weeks=delay_weeks)

            # Check for dependency impact
            dependency_impacted = gantt_df[gantt_df['Dependencies'] == selected_task]
            if not dependency_impacted.empty:
                impacted_task_name = dependency_impacted.iloc[0]['Task']
                st.error(f"**Impact Alert!** Delaying '{selected_task}' will directly impact the start date of **'{impacted_task_name}'**.")

    # Create Gantt chart with Plotly
    fig = px.timeline(
        gantt_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Site",
        title="Project Portfolio Gantt"
    )
    fig.update_yaxes(autorange="reversed")  # To display tasks from top to bottom
    st.plotly_chart(fig, use_container_width=True)


elif page == "💼 **Financial Intelligence & FinOps**":
    st.header(f"💼 Financial Intelligence & FinOps for **{site_selection}**")
    tco_df = filter_df_by_site(data["tco_df"])

    tab1, tab2 = st.tabs(["Asset TCO & CapEx", "Cloud FinOps"])

    with tab1:
        st.subheader("Asset TCO & CapEx Proposal Generator")
        fig_tco = px.treemap(tco_df, path=[px.Constant(site_selection), 'Asset Type', 'Asset ID'],
                             values='TCO ($k)', color='Uptime (%)',
                             color_continuous_scale='RdYlGn', title='Asset TCO Treemap (Size=Cost, Color=Reliability)')
        st.plotly_chart(fig_tco, use_container_width=True)

        st.info("Select a poorly performing asset to auto-generate a CapEx proposal.")
        selected_asset_id = st.selectbox("Select Asset for CapEx Proposal:", options=tco_df['Asset ID'])
        if st.button("🤖 Generate CapEx Proposal", type="primary"):
            asset_details = tco_df[tco_df['Asset ID'] == selected_asset_id].iloc[0]
            with st.spinner(f"AI is drafting a proposal for {selected_asset_id}..."):
                proposal_text = generate_capex_proposal_text(asset_details)
                st.session_state.proposal = proposal_text
        if 'proposal' in st.session_state:
            st.text_area("Generated CapEx Draft:", st.session_state.proposal, height=300)
            st.download_button("Download as .txt", st.session_state.proposal, f"CapEx_{selected_asset_id}.txt")

    with tab2:
        st.subheader("Cloud Cost (FinOps) Dashboard")
        finops_df = data['finops_df']
        fig_cost = px.area(finops_df, x='Date', y='Cost ($)', color='Project', title='Cloud Spend Over Time by Project')
        st.plotly_chart(fig_cost, use_container_width=True)
        st.info("**AI Insight:** 'AI Drug Discovery' project spend is forecast to increase by 30% next month. Consider reserving instances to optimize cost.")
        st.dataframe(finops_df.groupby('Service')['Cost ($)'].sum().reset_index(), use_container_width=True)


elif page == "🔬 **Scientific & Lab Operations**":
    st.header(f"🔬 Scientific & Lab Operations at **{site_selection}**")
    tab1, tab2 = st.tabs(["Instrument Utilization", "Scientific Impact Analysis"])

    with tab1:
        st.subheader("Live Instrument Utilization")
        util_df = filter_df_by_site(data["utilization_df"])
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Current Instrument Status**")
            st.dataframe(util_df[['Instrument', 'Status']], use_container_width=True, hide_index=True)
        with c2:
            st.markdown("**Utilization (Last 7 Days)**")
            fig_util = px.bar(util_df, x='Instrument', y='Utilization (Last 7 Days %)', color='Instrument', title="Instrument Utilization")
            fig_util.update_yaxes(range=[0, 100])
            st.plotly_chart(fig_util, use_container_width=True)
    
    with tab2:
        st.subheader("Reagent & Assay Impact Analysis")
        st.graphviz_chart(get_reagent_genealogy_data("R-45B-XYZ"))
        assay_data = data["assay_impact_df"]
        if assay_data and assay_data['labels']:
            fig_sankey = go.Figure(data=[go.Sankey(
                node = dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=assay_data['labels'], color=assay_data['colors']),
                link = dict(source=assay_data['sources'], target=assay_data['targets'], value=assay_data['values'])
            )])
            fig_sankey.update_layout(title_text="Instrument -> Assay -> Project Dependency Flow", font_size=10)
            st.plotly_chart(fig_sankey, use_container_width=True)


elif page == "⚙️ **Autonomous Operations**":
    st.header(f"⚙️ Autonomous Operations for **{site_selection}**")
    pred_maint_df_filtered = filter_df_by_site(st.session_state.pred_maint_data)

    tab1, tab2 = st.tabs(["Predictive Maintenance & Work Orders", "GxP Change Simulation"])

    with tab1:
        st.subheader("Predictive Maintenance with Work Order Integration")
        st.info("Assets needing approval appear in the Action Center. Once approved, you can create a work order.")
        
        df_to_display = pred_maint_df_filtered.copy()
        
        for idx, row in df_to_display.iterrows():
            item_id = f"pm_{row['Asset ID']}"
            action_item = next((item for item in st.session_state.action_items if item['id'] == item_id), None)
            
            if action_item and action_item['status'] == 'Approved' and row['Status'] != 'Work Order Created':
                if st.button(f"Create Work Order for {row['Asset ID']}", key=f"wo_{row['Asset ID']}"):
                    st.session_state.pred_maint_data.loc[idx, 'Status'] = 'Work Order Created'
                    st.success(f"Work Order #WO12345 created in ServiceNow for {row['Asset ID']}.")
                    st.rerun()

        st.dataframe(df_to_display.style.highlight_max(subset=['Predicted Failure Risk (%)'], color='lightcoral'), use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Digital Twin for GxP Change Simulation")
        st.info("Simulate the impact of a software change on a critical GxP system before deployment.")
        change_desc = st.text_input("Describe the change for simulation:", "Apply security patch KB5034122 to LIMS-PROD server")
        if st.button("🚀 Run Simulation in Digital Twin", type="primary"):
            with st.spinner("Simulation in progress..."):
                result = run_digital_twin_simulation(change_desc)
                st.session_state.sim_result = result
        
        if 'sim_result' in st.session_state:
            st.markdown(f"**Simulation Complete!**")
            st.metric("Assessed Risk Level", st.session_state.sim_result['risk'])
            st.text_area("Simulation Impact Report", st.session_state.sim_result['impact'], height=150)


elif page == "📋 **GxP & Audit Readiness**":
    st.header(f"📋 GxP & Audit Readiness for **{site_selection}**")
    living_log_df = data['living_system_log']
    
    st.subheader("Interactive Audit Trail Navigator (21 CFR Part 11)")
    query = st.text_input("Search the audit trail (e.g., \"Show actions by user 'davis_c' on LIMS-PROD\")", help="Search by user or system name.")
    
    if query:
        with st.spinner("Searching secure log..."):
            results_df = search_audit_log(living_log_df, query)
    else:
        results_df = living_log_df

    st.dataframe(results_df, use_container_width=True, hide_index=True)
    st.divider()
    
    st.subheader("Risk-Adjusted Validation Master Plan")
    risk_vmp_df_filtered = filter_df_by_site(data["risk_vmp_df"])
    fig_risk_vmp = px.scatter(
        risk_vmp_df_filtered, x="Days Until Due", y="System Criticality",
        size="Validation Effort (Hours)", color="Status", hover_name="System/Instrument",
        title=f"Risk-Adjusted Validation Priority Matrix for {site_selection}", size_max=50
    )
    st.plotly_chart(fig_risk_vmp, use_container_width=True)


elif page == "👥 **Leadership & Resource Planning**":
    st.header(f"👥 Leadership & Resource Planning for **{site_selection}**")
    tab1, tab2 = st.tabs(["Resource Allocation Heatmap", "Team Skills & KPIs"])
    
    with tab1:
        st.subheader("Matrix Resource Allocation Heatmap")
        st.info("Forecasted workload for each team member across all projects. Red indicates potential over-allocation (>100%).")
        heatmap_df = data['resource_allocation_df']
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_df.values,
            x=heatmap_df.columns,
            y=heatmap_df.index,
            colorscale='RdYlGn_r'
        ))
        fig_heatmap.update_layout(title='Resource Allocation Forecast (%)')
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with tab2:
        st.subheader("Team Skills & Performance")
        team_perf_df_filtered = filter_df_by_site(data['team_perf_df'])
        
        st.markdown("**Team Skills & Training Matrix**")
        st.dataframe(team_perf_df_filtered.style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''), use_container_width=True, hide_index=True)

        st.markdown("**AI-Identified Skill Gap**")
        st.warning(f"**GAP:** {data['skills_gap']['gap']}\n\n**Recommendation:** {data['skills_gap']['recommendation']}")
        
        st.divider()
        st.subheader("Site vs. Global KPI Benchmark")
        global_kpis = data["global_kpis"]
        
        if site_selection != "West Coast (Overall)":
            for _, row in global_kpis.iterrows():
                site_value = row[site_selection]
                delta_val = site_value - row['Global Avg']
                st.metric(
                    label=f"{row['KPI']}",
                    value=f"{site_value:.1f}{row.get('unit','')}",
                    delta=f"{delta_val:.1f}{row.get('unit','')}",
                    help=f"vs. Global Average of {row['Global Avg']}{row.get('unit','')}"
                )
        else:
             st.info("Select a specific site (San Diego or Seattle) to view KPI benchmarks.")
