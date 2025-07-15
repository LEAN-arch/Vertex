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
# Helper Functions for Advanced, Actionable Visualizations
# ==============================================================================
def create_wordcloud(text_data):
    """Generates and displays a word cloud."""
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(text_data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def create_spc_chart(data, mttr_series):
    """Creates a Statistical Process Control (SPC) chart for MTTR, distinguishing common vs. special cause variation."""
    mean = mttr_series.mean()
    std_dev = mttr_series.std()
    ucl = mean + (3 * std_dev)
    lcl = mean - (3 * std_dev) if (mean - (3 * std_dev)) > 0 else 0
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data['Date'], y=data['Ticket Count'], name='New Tickets', marker_color='#1f77b4'), secondary_y=False)
    fig.add_trace(go.Scatter(x=data['Date'], y=mttr_series, name='MTTR (Hours)', mode='lines+markers', line=dict(color='#d62728')), secondary_y=True)
    
    fig.add_hline(y=mean, line_dash="dash", line_color="green", annotation_text="Mean", annotation_position="bottom right", secondary_y=True)
    fig.add_hline(y=ucl, line_dash="dot", line_color="red", annotation_text="UCL (3σ)", annotation_position="top right", secondary_y=True)
    fig.add_hline(y=lcl, line_dash="dot", line_color="red", annotation_text="LCL (3σ)", secondary_y=True)
    
    outliers = mttr_series[(mttr_series > ucl) | (mttr_series < lcl)]
    fig.add_trace(go.Scatter(x=outliers.index, y=outliers, mode='markers',
                             marker=dict(color='red', size=12, symbol='x'),
                             name='Special Cause Variation'), secondary_y=True)

    fig.update_layout(title_text="Service Stability SPC Chart: Volume & MTTR")
    fig.update_yaxes(title_text="Ticket Volume", secondary_y=False)
    fig.update_yaxes(title_text="Avg. Resolution (Hours)", secondary_y=True)
    return fig

def create_pareto_chart(df):
    """Creates a true Pareto chart to identify the 'vital few' root causes based on the 80/20 rule."""
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
st.title("DTE Command Center: West Coast (San Diego & Seattle)")
st.markdown("##### Strategic Dashboard for the Associate Director, Laboratory Engineering & Technology (LE&W)")

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
tab_list = [
    "📈 **Executive Command & Strategy**",
    "🎟️ **Lab Service Operations (ITIL)**",
    "💻 **Asset & Vendor Lifecycle**",
    "🚀 **Innovation & Project Pipeline**",
    "📋 **Compliance & GxP Posture**",
    "👥 **Leadership & Global Alignment**"
]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_list)

# ==============================================================================
# TAB 1: EXECUTIVE COMMAND & STRATEGY
# ==============================================================================
with tab1:
    st.header("Executive Summary: DTE Performance & Strategic Alignment")
    st.caption("This module addresses the **Vision and Strategy** duties, enabling high-level communication and alignment with site and global leadership.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lab System Uptime (West Coast)", "99.8%", help="Measures Data Integrity principle of Availability.")
    col2.metric("P1/P2 Incident MTTR (Hours)", "3.8", delta="-0.5h", help="Mean Time to Resolution for high-priority incidents.")
    col3.metric("Strategic Projects On-Time", "85%", delta="-5%", delta_color="inverse")
    col4.metric("GxP Compliance Gaps", "1", delta="1", delta_color="inverse", help="Count of overdue validations or critical audit findings.")
    
    st.divider()

    st.subheader("DTE Strategic Value & Stakeholder Communication")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("**AI-Generated Value Story of the Month**")
        st.info("🔬 **Value Story:** In May, the LE&W team successfully deployed the new automated liquid handlers for the San Diego Cell Therapy workflow. **Impact:** This reduced manual sample prep time by an estimated **70%** (120 hours/month), directly accelerating candidate screening for the VT-101 program and improving data consistency.", icon="💡")
    with c2:
        st.markdown("**AI Stakeholder Briefing Generator**")
        st.caption("Lead engagement and representation of DTE with tailored, impactful updates.")
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
    st.header("Lab Service Operations (ITIL Framework)")
    st.caption("This module addresses **Operational Execution** duties, ensuring day-to-day stability and compliance with the ITIL framework, a key GxP expectation for demonstrating control.")

    st.subheader("ML Module: Predictive Instrument Failure & Service Foresight")
    st.markdown("This ML model addresses the duty to **ensure robust instrumentation** by moving from a reactive break-fix model to a proactive predict-and-prevent strategy. This directly supports **GMP/GLP** requirements for qualified and reliable equipment.")
    st.dataframe(pred_maint_df.style.highlight_max(subset=['Predicted Failure Risk (%)'], color='lightcoral'), use_container_width=True, hide_index=True)
    st.divider()
    
    st.subheader("Proactive Problem Management & Service Stability")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Incident Pareto Analysis**")
        st.caption("Utilizes the **Pareto Principle (80/20 Rule)** to identify the vital few problems causing the most disruption, enabling data-driven resource allocation for **CAPA** initiatives.")
        incident_categories = tickets_df[tickets_df['Type'] == 'Incident']['Category'].value_counts().reset_index(name='count')
        fig_pareto = create_pareto_chart(incident_categories)
        st.plotly_chart(fig_pareto, use_container_width=True)
        
    with c2:
        st.markdown("**Service Stability SPC Chart**")
        st.caption("Applies **Statistical Process Control (SPC)** to distinguish normal operational 'noise' from significant 'special cause' events that require immediate investigation, transforming the AD into an active process controller.")
        ticket_counts_by_date = tickets_df.groupby('Date').size().reset_index(name='Ticket Count')
        fig_spc = create_spc_chart(ticket_counts_by_date, mttr_data)
        st.plotly_chart(fig_spc, use_container_width=True)

# ==============================================================================
# TAB 3: ASSET & VENDOR LIFECYCLE
# ==============================================================================
with tab3:
    st.header("GxP Asset & Vendor Lifecycle Management")
    st.caption("This module addresses the duty to oversee all lab hardware and software, ensuring a compliant, secure, and cost-effective technology lifecycle as required by **21 CFR 820** and **GAMP 5**.")

    st.subheader("ML Module: Intelligent Capital Asset Refresh Modeler")
    st.markdown("This ML model provides an objective, data-driven foundation for capital expenditure planning. It replaces subjective requests with a strategic, risk-based investment proposal based on TCO and scientific impact.")
    fig_cap_asset = px.scatter(
        cap_asset_df, x="Total Cost of Ownership ($)", y="Scientific Need Score",
        size="Asset Age (Yrs)", color="Asset Type", hover_name="Asset ID",
        title="Capital Asset Replacement Priority Matrix", size_max=40
    )
    st.plotly_chart(fig_cap_asset, use_container_width=True)
    
    st.divider()

    st.subheader("Key Vendor Performance Scorecards")
    st.caption("Manage vendor relationships with data-driven insights to hold partners accountable to Vertex's high standards for support and reliability.")
    for vendor_name, data in vendor_data.items():
        with st.expander(f"**{vendor_name}** - Overall Status: {data['qbr_status']}"):
            v_col1, v_col2, v_col3 = st.columns(3)
            v_col1.metric("SLA Compliance", f"{data['sla_compliance']}%", delta=f"{data['sla_delta']}%")
            v_col2.metric("Avg. Support MTTR (h)", data['mttr'], delta=f"{data['mttr_delta']}h")
            v_col3.metric("Hardware Reliability (MTBF days)", data['mtbf'], help="Mean Time Between Failures")

# ==============================================================================
# TAB 4: INNOVATION & PROJECT PIPELINE
# ==============================================================================
with tab4:
    st.header("Innovation Radar & Strategic Project Pipeline")
    st.caption("This module addresses the duties to **monitor emerging technologies** and **oversee the execution of projects**, ensuring innovation is managed with discipline and projects are delivered on time.")

    st.subheader("ML Module: Automated Project Risk & Timeline Forecaster")
    st.markdown("This ML model provides foresight into project timelines, enabling proactive intervention. This is crucial for managing projects with **CSV** components, where delays can have significant compliance and business impact.")
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
        st.caption("A strategic framework for managing the innovation lifecycle from assessment to adoption.")
        fig_radar_tech = px.scatter(
            tech_radar_df, x="theta", y="r", color="Quadrant", text="Technology",
            hover_name="Details", title="DTE Lab Technology Radar", polar=True
        )
        fig_radar_tech.update_layout(polar=dict(radialaxis=dict(showticklabels=False, ticks='', gridcolor='lightgrey'), angularaxis=dict(showticklabels=False, ticks='')))
        st.plotly_chart(fig_radar_tech, use_container_width=True)

    with c2:
        st.subheader("Process Automation Impact")
        st.caption("Quantifies the business value of automation initiatives, translating technical work into operational efficiency gains.")
        automation_data = pd.DataFrame({'Project': ['Automated HPLC Report Generation', 'NGS FASTQ File Transfer Script', 'LIMS Data Entry Bot'], 'Hours Saved / Month': [40, 25, 60]})
        fig_automation = px.bar(automation_data, x='Project', y='Hours Saved / Month', text='Hours Saved / Month', title='Impact of Lab Automation Initiatives')
        st.plotly_chart(fig_automation, use_container_width=True)

# ==============================================================================
# TAB 5: COMPLIANCE & GXP POSTURE
# ==============================================================================
with tab5:
    st.header("Compliance & GxP Posture Dashboard")
    st.caption("This module provides a centralized view to **ensure compliance with regulatory standards**, making audits a non-event by demonstrating robust, continuous control.")

    st.subheader("Interactive Validation Master Plan (VMP)")
    st.markdown("The primary tool for managing the **GAMP 5** lifecycle for all computerized systems. It provides a clear view of the validation pipeline, ensuring new instruments are brought online in a compliant and timely manner.")
    fig_vmp = px.timeline(
        vmp_df, x_start="Start", x_end="Finish", y="System/Instrument", color="Status", 
        hover_name="Validation Lead", title="Validation Master Plan (VMP) - Status & Timeline",
        custom_data=['Phase']
    )
    fig_vmp.update_traces(text=vmp_df['Phase'])
    st.plotly_chart(fig_vmp, use_container_width=True)

    st.subheader("Internal Audit Readiness Checklist")
    st.markdown("A proactive self-assessment tool demonstrating a mature, risk-based approach to **21 CFR Part 11** and **Data Integrity (ALCOA+)** requirements.")
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
    st.caption("This module addresses duties related to **team leadership** and **matrix leadership**, fostering a high-performance culture and ensuring a globally aligned, locally enabled experience.")

    st.subheader("Team Performance & Development Hub")
    st.markdown("Strategic talent management to build a future-ready team, ensuring personnel are qualified as per **GxP** requirements.")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("**Team Skills & Training Matrix**")
        st.dataframe(team_df.style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**Identified Skill Gap & Training Need**")
        st.warning(f"**GAP:** {skills_gap['gap']}\n\n**Recommendation:** {skills_gap['recommendation']}")

    st.divider()

    st.subheader("Matrix Leadership: Global Alignment Dashboard")
    st.markdown("Fostering a culture of global excellence by benchmarking and sharing best practices.")
    
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
