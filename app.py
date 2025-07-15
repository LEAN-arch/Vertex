# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils import (
    get_strategic_alignment_data, get_project_portfolio_data,
    get_itsm_ticket_data, get_asset_inventory_data,
    get_tech_radar_data, get_vmp_tracker_data,
    get_audit_readiness_data,
    get_voice_of_scientist_data, get_ai_briefing,
    get_ai_root_cause, get_vendor_scorecards,
    get_team_performance, get_global_kpis,
    # --- NEW: Import functions for ML modules ---
    get_predictive_maintenance_data,
    get_capital_asset_model_data,
    get_project_forecast_data
)

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="DTE Command Center | Vertex Pharmaceuticals",
    page_icon="🧬",
    layout="wide"
)

# ==============================================================================
# Helper Functions for Advanced Visualizations
# ==============================================================================
def create_wordcloud(text_data):
    """Generates and displays a word cloud."""
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(text_data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def create_spc_chart(data, mttr_series):
    """Creates a Statistical Process Control (SPC) chart for MTTR."""
    mean = mttr_series.mean()
    std_dev = mttr_series.std()
    ucl = mean + (3 * std_dev)
    lcl = mean - (3 * std_dev)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data['Date'], y=data['Ticket Count'], name='New Tickets', marker_color='#1f77b4'), secondary_y=False)
    fig.add_trace(go.Scatter(x=data['Date'], y=mttr_series, name='MTTR (Hours)', mode='lines+markers', line=dict(color='#d62728')), secondary_y=True)
    
    # Add SPC lines
    fig.add_hline(y=mean, line_dash="dash", line_color="green", annotation_text="Mean", annotation_position="bottom right", secondary_y=True)
    fig.add_hline(y=ucl, line_dash="dot", line_color="red", annotation_text="UCL", annotation_position="top right", secondary_y=True)
    fig.add_hline(y=lcl, line_dash="dot", line_color="red", annotation_text="LCL", secondary_y=True)
    
    # Highlight points outside control limits
    outliers = mttr_series[ (mttr_series > ucl) | (mttr_series < lcl) ]
    fig.add_trace(go.Scatter(x=data['Date'][outliers.index], y=outliers, mode='markers',
                             marker=dict(color='red', size=12, symbol='x'),
                             name='Special Cause Variation'), secondary_y=True)

    fig.update_layout(title_text="Service Stability SPC Chart: Volume & MTTR")
    fig.update_yaxes(title_text="Ticket Volume", secondary_y=False)
    fig.update_yaxes(title_text="Avg. Resolution (Hours)", secondary_y=True)
    return fig

def create_pareto_chart(df):
    """Creates a true Pareto chart with cumulative percentage line."""
    df = df.sort_values(by='count', ascending=False)
    df['Cumulative Percentage'] = (df['count'].cumsum() / df['count'].sum()) * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df['Category'], y=df['count'], name='Incident Count', marker_color='#1f77b4'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['Category'], y=df['Cumulative Percentage'], name='Cumulative %', line=dict(color='#d62728')), secondary_y=True)
    
    fig.update_layout(title_text="Incident Pareto Analysis: The 'Vital Few' Problems")
    fig.update_yaxes(title_text="Incident Count", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Percentage", secondary_y=True, range=[0, 101])
    return fig

# ==============================================================================
# Main Application
# ==============================================================================
st.title("🧬 DTE Command Center: West Coast (San Diego & Seattle)")
st.markdown("##### Strategic Dashboard for the Associate Director, Laboratory Engineering & Technology (LE&W)")

# --- Data Loading (Simulated backend/database calls) ---
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
# --- NEW: Data loading for ML modules ---
pred_maint_df = get_predictive_maintenance_data()
cap_asset_df = get_capital_asset_model_data()
portfolio_df = get_project_forecast_data(portfolio_df) # Augment existing portfolio data


# --- Tabbed Interface ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 **Executive Command & Strategy**",
    "🎟️ **Lab Service Operations (ITIL)**",
    "💻 **Asset & Vendor Lifecycle**",
    "🚀 **Innovation & Project Pipeline**",
    "📋 **Compliance & GxP Posture**",
    "👥 **Leadership & Global Alignment**"
])

# ==============================================================================
# TAB 1: EXECUTIVE COMMAND & STRATEGY
# ==============================================================================
with tab1:
    st.header("Executive Summary: DTE Performance & Strategic Alignment")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lab System Uptime (West Coast)", "99.8%")
    col2.metric("P1/P2 Incident MTTR (Hours)", "3.8", delta="-0.5h")
    col3.metric("Strategic Projects On-Time", "85%", delta="-5%", delta_color="inverse")
    col4.metric("Overdue GxP Validations", "1", delta="1", delta_color="inverse")
    
    st.divider()

    st.subheader("DTE Strategic Value & Stakeholder Communication")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("**AI-Generated Value Story of the Month**")
        st.info("🔬 **Value Story:** In May, the LE&W team successfully deployed the new automated liquid handlers for the San Diego Cell Therapy workflow. **Impact:** This reduced manual sample prep time by an estimated **70%** (120 hours/month), directly accelerating candidate screening for the VT-101 program and improving data consistency.", icon="💡")
    with c2:
        st.markdown("**AI Stakeholder Briefing Generator**")
        audience = st.selectbox("Select Audience:", ["Site Leadership (SD)", "Global DTE Leadership", "Lab Scientists"])
        if st.button("Generate Briefing", use_container_width=True):
            briefing = get_ai_briefing(audience, {"uptime": "99.8%", "mttr": "3.8h", "projects_on_time": "85%"})
            st.text_area("Generated Draft:", briefing, height=150)

    st.divider()

    st.subheader("Strategic Portfolio Quadrant Analysis")
    st.caption("Categorizing strategic initiatives to align resources with impact. This answers 'Why are we doing this?'")
    
    # Enhanced Portfolio Quadrant Chart
    median_effort = portfolio_df['Effort (Person-Weeks)'].median()
    median_impact = portfolio_df['Strategic Impact Score'].median()
    
    fig_portfolio = px.scatter(
        portfolio_df, x="Effort (Person-Weeks)", y="Strategic Impact Score",
        size="Budget ($k)", color="Strategic Theme", hover_name="Project",
        size_max=60, title="DTE Strategic Projects: Impact vs. Effort"
    )
    fig_portfolio.add_vline(x=median_effort, line_dash="dash", line_color="gray")
    fig_portfolio.add_hline(y=median_impact, line_dash="dash", line_color="gray")
    fig_portfolio.add_annotation(x=median_effort*1.5, y=median_impact*1.1, text="Strategic Bets", showarrow=False, font=dict(color="green", size=14))
    fig_portfolio.add_annotation(x=median_effort*0.5, y=median_impact*1.1, text="Quick Wins", showarrow=False, font=dict(color="blue", size=14))
    fig_portfolio.add_annotation(x=median_effort*0.5, y=median_impact*0.9, text="Foundational Tasks", showarrow=False, font=dict(color="grey", size=14))
    fig_portfolio.add_annotation(x=median_effort*1.5, y=median_impact*0.9, text="Reconsider / Automate", showarrow=False, font=dict(color="orange", size=14))
    st.plotly_chart(fig_portfolio, use_container_width=True)


# ==============================================================================
# TAB 2: LAB SERVICE OPERATIONS (ITIL)
# ==============================================================================
with tab2:
    st.header("Lab Service Operations Dashboard (ITSM/ITIL Framework)")

    p1_incidents = tickets_df[tickets_df['Priority'] == 'P1 - Critical'].shape[0]
    sla_met_pct = tickets_df[tickets_df['SLA Met'] == True].shape[0] / len(tickets_df) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active P1 Incidents", p1_incidents)
    col2.metric("SLA Adherence (Last 30d)", f"{sla_met_pct:.1f}%")
    col3.metric("Avg. Resolution Time (MTTR, Last 30d)", f"{mttr_data.mean():.1f} hours")

    st.divider()

    # --- NEW: ML Module 1 Integration ---
    st.subheader("ML Module: Predictive Instrument Failure & Service Foresight")
    st.caption("Moving from break-fix to predict-and-prevent to maximize scientific uptime.")
    st.dataframe(pred_maint_df.style.highlight_max(subset=['Predicted Failure Risk (%)'], color='lightcoral'), use_container_width=True, hide_index=True)

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Proactive Problem Management")
        incident_categories = tickets_df[tickets_df['Type'] == 'Incident']['Category'].value_counts().reset_index(name='count')
        fig_pareto = create_pareto_chart(incident_categories)
        st.plotly_chart(fig_pareto, use_container_width=True)
        
    with c2:
        st.subheader("Service Stability & User Experience")
        st.markdown("**Voice of the Scientist (Analysis of Tickets & Surveys)**")
        fig_wc = create_wordcloud(vos_data)
        st.pyplot(fig_wc)

    st.subheader("Operational Performance Analysis")
    ticket_counts_by_date = tickets_df.groupby('Date').size().reset_index(name='Ticket Count')
    fig_spc = create_spc_chart(ticket_counts_by_date, mttr_data)
    st.plotly_chart(fig_spc, use_container_width=True)
    

# ==============================================================================
# TAB 3: ASSET & VENDOR LIFECYCLE
# ==============================================================================
with tab3:
    st.header("Asset & Vendor Lifecycle Management")
    
    st.subheader("West Coast GxP Asset Inventory")
    def style_assets(df):
        style = pd.DataFrame('', index=df.index, columns=df.columns)
        style.loc[df['Validation Status'] == 'Overdue', 'Validation Status'] = 'background-color: #D32F2F; color: white;'
        style.loc[df['Warranty Status'] == 'Expiring Soon', 'Warranty Status'] = 'background-color: #F57C00; color: white;'
        style.loc[df['OS Support Status'] == 'Unsupported', 'OS Support Status'] = 'background-color: #FFEE58;'
        return style
    st.dataframe(assets_df.style.apply(style_assets, axis=None), use_container_width=True, hide_index=True)

    st.divider()

    # --- NEW: ML Module 2 Integration ---
    st.subheader("ML Module: Intelligent Capital Asset Refresh Modeler")
    st.caption("Data-driven prioritization for capital expenditure planning, balancing cost, risk, and scientific need.")
    fig_cap_asset = px.scatter(
        cap_asset_df, x="Total Cost of Ownership ($)", y="Scientific Need Score",
        size="Asset Age (Yrs)", color="Asset Type", hover_name="Asset ID",
        title="Capital Asset Replacement Priority Matrix", size_max=40
    )
    st.plotly_chart(fig_cap_asset, use_container_width=True)

    st.divider()
    
    st.subheader("Key Vendor Performance Scorecards")
    for vendor_name, data in vendor_data.items():
        with st.expander(f"**{vendor_name}** - Overall Status: {data['qbr_status']}"):
            v_col1, v_col2, v_col3 = st.columns(3)
            v_col1.metric("SLA Compliance", f"{data['sla_compliance']}%", delta=f"{data['sla_delta']}%")
            v_col2.metric("Avg. Support MTTR (h)", data['mttr'], delta=f"{data['mttr_delta']}h")
            v_col3.metric("Hardware Reliability (MTBF days)", data['mtbf'], help="Mean Time Between Failures")


# ==============================================================================
# TAB 4: INNOVATION & PROJECT PIPELINE
# ==============================================================================
# NEW: Title changed
with tab4:
    st.header("Innovation Radar & Strategic Project Pipeline")
    
    # --- NEW: ML Module 3 Integration ---
    st.subheader("ML Module: Automated Project Risk & Timeline Forecaster")
    st.caption("Proactively identify at-risk projects using NLP analysis of status reports and historical data.")
    st.dataframe(
        portfolio_df[['Project', 'Status', 'Health Score (%)', 'Planned Finish', 'Predicted Finish']].style.apply(
            lambda x: ['background-color: lightcoral' if v < 60 else 'background-color: lightyellow' if v < 85 else '' for v in x],
            subset=['Health Score (%)']
        ),
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Emerging Technology Radar")
        fig_radar_tech = px.scatter(
            tech_radar_df, x="theta", y="r", color="Quadrant", text="Technology",
            hover_name="Details", title="DTE Lab Technology Radar", polar=True
        )
        fig_radar_tech.update_layout(polar=dict(radialaxis=dict(showticklabels=False, ticks='', gridcolor='lightgrey'), angularaxis=dict(showticklabels=False, ticks='')))
        st.plotly_chart(fig_radar_tech, use_container_width=True)

    with c2:
        st.subheader("Process Automation Impact")
        automation_data = pd.DataFrame({'Project': ['Automated HPLC Report Generation', 'NGS FASTQ File Transfer Script', 'LIMS Data Entry Bot'], 'Hours Saved / Month': [40, 25, 60]})
        fig_automation = px.bar(automation_data, x='Project', y='Hours Saved / Month', text='Hours Saved / Month', title='Impact of Lab Automation Initiatives')
        st.plotly_chart(fig_automation, use_container_width=True)


# ==============================================================================
# TAB 5: COMPLIANCE & GXP POSTURE
# ==============================================================================
with tab5:
    st.header("Compliance & GxP Posture Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("GxP Systems in Validated State", "95%")
    col2.metric("Open Quality Deviations", "3")
    col3.metric("21 CFR Part 11 Readiness", "98%")

    st.divider()

    st.subheader("Validation & Audit Readiness")
    # Enhanced Validation Gantt Chart
    vmp_df['Delta'] = (vmp_df['Finish'] - vmp_df['Start']).dt.days
    fig_vmp = px.timeline(
        vmp_df, x_start="Start", x_end="Finish", y="System/Instrument", color="Phase", 
        hover_name="Validation Lead", title="Interactive Validation Master Plan (VMP)",
        custom_data=['Status']
    )
    fig_vmp.update_traces(
        marker=dict(line=dict(width=1)),
        opacity=0.8,
        text=vmp_df.apply(lambda row: f"Status: {row['Status']}", axis=1)
    )
    st.plotly_chart(fig_vmp, use_container_width=True)

    st.subheader("Internal Audit Readiness Checklist")
    def style_audit_status(val):
        if val == 'Ready': return 'background-color: #2ca02c; color: white;'
        if val == 'Needs Review': return 'background-color: #ffc107; color: black;'
        if val == 'Gap Identified': return 'background-color: #d62728; color: white;'
        return ''
    st.dataframe(audit_df.style.map(style_audit_status, subset=['Status']), use_container_width=True, hide_index=True)


# ==============================================================================
# TAB 6: LEADERSHIP & GLOBAL ALIGNMENT
# ==============================================================================
with tab6:
    st.header("Leadership: Team Performance & Global Alignment")

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
            kpi_name = row['KPI']
            wc_val = row['West Coast']
            global_val = row['Global Avg']
            delta = f"{wc_val - global_val:.1f}{row.get('unit','')}"
            st.metric(label=f"{kpi_name}", value=f"{wc_val}{row.get('unit','')}", delta=delta, help=f"vs. Global Average of {global_val}{row.get('unit','')}")
    
    with col2:
        st.markdown("**Global Best Practice Exchanger (AI Identified)**")
        st.success(
            """
            **New Best Practice Identified (from Boston DTE):**
            - **Issue:** 'Lab Printer Offline' incidents.
            - **Boston's Solution:** Implemented a proactive script that pings all networked printers every 15 minutes. If a printer fails to respond twice, it auto-generates a low-priority ticket before a scientist reports it.
            - **Impact:** Reduced user-reported printer incidents by 90%.
            - **Recommendation:** Pilot this solution in the San Diego lab.
            """
        )
