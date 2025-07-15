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
    # --- NEW: Import functions for 10+ features ---
    get_voice_of_scientist_data, get_ai_briefing,
    get_ai_root_cause, get_vendor_scorecards,
    get_team_performance, get_global_kpis
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
# Helper Functions
# ==============================================================================
def create_wordcloud(text_data):
    """Generates and displays a word cloud from a dictionary of word frequencies."""
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(text_data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
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

# --- NEW: Data loading for 10+ features ---
vos_data = get_voice_of_scientist_data()
vendor_data = get_vendor_scorecards()
team_df, skills_gap = get_team_performance()
global_kpis_df = get_global_kpis()


# --- Tabbed Interface for Different Areas of Responsibility ---
# NEW: Added a 6th tab for Leadership & Global Alignment
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 **Executive Command Center**",
    "🎟️ **Lab Service Operations (ITIL)**",
    "💻 **GxP Asset & Vendor Lifecycle**",
    "🚀 **Strategic Initiatives & Innovation Pipeline**",
    "📋 **Compliance & GxP Posture**",
    "👥 **Leadership & Global Alignment**" # <-- NEW
])


# ==============================================================================
# TAB 1: EXECUTIVE COMMAND CENTER
# ==============================================================================
with tab1:
    st.header("Executive Summary: DTE Performance & Strategic Alignment")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lab System Uptime (West Coast)", "99.8%", help="Availability of critical GxP instrument and control systems this quarter.")
    col2.metric("P1/P2 Incident MTTR (Hours)", "3.8", delta="-0.5h", help="Mean Time to Resolution for high-priority incidents. Delta vs. last quarter.")
    col3.metric("Strategic Projects On-Time", "85%", delta="-5%", delta_color="inverse", help="Percentage of strategic initiatives on schedule.")
    col4.metric("Overdue GxP Validations", "1", delta="1", delta_color="inverse", help="Count of critical systems with pending or overdue periodic reviews.")
    
    st.divider()

    # --- NEW: Added AI Value Story & Briefing Generator ---
    st.subheader("DTE Strategic Value & Stakeholder Communication")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("**AI-Generated Value Story of the Month**")
        st.info(
            """
            🔬 **Value Story:** In May, the LE&W team successfully deployed the new automated liquid handlers for the San Diego Cell Therapy workflow. 
            **Impact:** This reduced manual sample prep time by an estimated **70%** (120 hours/month), directly accelerating candidate screening for the VT-101 program and improving data consistency.
            """, 
            icon="💡"
        )
    with c2:
        st.markdown("**AI Stakeholder Briefing Generator**")
        st.caption("Generate tailored updates for key stakeholders to lead engagement and representation of DTE.")
        audience = st.selectbox("Select Audience:", ["Site Leadership (SD)", "Global DTE Leadership", "Lab Scientists"])
        if st.button("Generate Briefing", use_container_width=True):
            briefing = get_ai_briefing(audience, {"uptime": "99.8%", "mttr": "3.8h", "projects_on_time": "85%"})
            st.text_area("Generated Draft:", briefing, height=150)

    st.divider()

    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("DTE Strategic Alignment to Site Goals")
        with st.expander("🔬 **Methodology & Significance**"):
            st.markdown("""
            This radar chart directly addresses the core responsibility to **partner with site leadership and align technology with site strategy**. It visualizes how DTE's efforts are balanced across key strategic pillars defined by the San Diego and Seattle site heads.
            - **Significance:** This is the primary communication tool for demonstrating value and alignment during site leadership meetings. It shows, at a glance, whether we are successfully supporting discovery speed, ensuring rock-solid compliance, enabling new modalities (e.g., cell & gene therapy), or driving operational efficiency. It allows for data-driven conversations about resource allocation and priorities.
            """)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=strategic_df['DTE Focus Score'], theta=strategic_df['Strategy Pillar'], fill='toself', name='DTE Effort Allocation'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), title="DTE Focus vs. Site Strategic Pillars")
        st.plotly_chart(fig_radar, use_container_width=True)

    with c2:
        st.subheader("Strategic Initiative Portfolio")
        with st.expander("🔬 **Methodology & Significance**"):
            st.markdown("""
            This bubble chart visualizes the entire portfolio of DTE projects, mapping them by **Impact on Science/Operations** and **Execution Effort**. This view is critical for resource planning and communicating priorities.
            - **Significance:** It allows the AD to answer key leadership questions: "What are our biggest bets?" (top-right quadrant) and "What are the quick wins?" (top-left quadrant). It also identifies low-impact, high-effort projects (bottom-right) that may need to be de-prioritized. The size of the bubble (budget) and color (strategic theme) add further layers for comprehensive portfolio management.
            """)
        fig_portfolio = px.scatter(portfolio_df, x="Effort (Person-Weeks)", y="Strategic Impact Score", size="Budget ($k)", color="Strategic Theme", hover_name="Project", size_max=60, title="DTE Strategic Projects: Impact vs. Effort")
        st.plotly_chart(fig_portfolio, use_container_width=True)


# ==============================================================================
# TAB 2: LAB SERVICE OPERATIONS (ITIL)
# ==============================================================================
with tab2:
    st.header("Lab Service Operations Dashboard (ITSM/ITIL Framework)")
    st.caption("Managing demand and delivery of lab computing services, aligned with Vertex DTE standards (e.g., ServiceNow).")

    p1_incidents = tickets_df[tickets_df['Priority'] == 'P1 - Critical'].shape[0]
    sla_met_pct = tickets_df[tickets_df['SLA Met'] == True].shape[0] / len(tickets_df) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active P1 Incidents", p1_incidents, help="Critical 'system down' incidents requiring immediate attention.")
    col2.metric("SLA Adherence (Last 30d)", f"{sla_met_pct:.1f}%")
    col3.metric("Avg. Resolution Time (MTTR, Last 30d)", f"{mttr_data.mean():.1f} hours")

    st.divider()

    # --- NEW: Added Voice of Scientist & AI Co-Pilot ---
    st.subheader("Proactive Problem Management & User Experience")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Voice of the Scientist (Analysis of Tickets & Surveys)**")
        st.caption("Identifies systemic frustrations before they escalate.")
        fig_wc = create_wordcloud(vos_data)
        st.pyplot(fig_wc)

    with c2:
        st.markdown("**AI Root Cause Co-Pilot**")
        st.caption("Leverages curiosity and expertise for rapid troubleshooting.")
        problem_description = st.text_input("Describe the issue:", "Multiple HPLCs in Lab 4C-SD are offline.")
        if st.button("Analyze for Root Cause", use_container_width=True):
            ai_analysis = get_ai_root_cause(problem_description)
            st.info(f"**AI Analysis:** {ai_analysis}")

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Ticket Volume & Resolution Time Trend")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=tickets_df['Date'], y=tickets_df['Ticket Count'], name='New Tickets'), secondary_y=False)
        fig.add_trace(go.Scatter(x=tickets_df['Date'], y=mttr_data, name='MTTR (Hours)', line=dict(color='red')), secondary_y=True)
        fig.update_yaxes(title_text="Ticket Volume", secondary_y=False)
        fig.update_yaxes(title_text="Avg. Resolution (Hours)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Top Incident Categories (Pareto)")
        incident_categories = tickets_df[tickets_df['Type'] == 'Incident']['Category'].value_counts().reset_index()
        fig_pareto = px.bar(incident_categories, x='Category', y='count', title="Incident Root Cause Categories")
        st.plotly_chart(fig_pareto, use_container_width=True)

    st.subheader("⚠️ High-Priority Incident Action Board")
    st.dataframe(tickets_df[tickets_df['Priority'].isin(['P1 - Critical', 'P2 - High'])], use_container_width=True, hide_index=True)


# ==============================================================================
# TAB 3: GXP ASSET & VENDOR LIFECYCLE
# ==============================================================================
# NEW: Title changed to include Vendors
with tab3:
    st.header("GxP Asset & Vendor Lifecycle Management")
    st.caption("Overseeing lab computing hardware, instrumentation, software, and key vendor partners.")

    total_assets = len(assets_df)
    unsupported_os = assets_df[assets_df['OS Support Status'] == 'Unsupported'].shape[0]
    pending_retirement = assets_df[assets_df['Lifecycle Status'] == 'Pending Retirement'].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Managed GxP Assets", total_assets)
    col2.metric("Assets on Unsupported OS", unsupported_os, delta=unsupported_os, delta_color="inverse", help="Security risk: e.g., Windows 7/10 older builds.")
    col3.metric("Assets Pending Decommission", pending_retirement, help="Requires formal retirement and data sanitization.")
    
    st.subheader("West Coast GxP Asset Inventory")
    st.caption("This live CMDB view enables management of security, compliance, and financial planning for all assets.")
    
    def style_assets(df):
        style = pd.DataFrame('', index=df.index, columns=df.columns)
        style.loc[df['Validation Status'] == 'Overdue', 'Validation Status'] = 'background-color: #D32F2F; color: white;'
        style.loc[df['Warranty Status'] == 'Expiring Soon', 'Warranty Status'] = 'background-color: #F57C00; color: white;'
        style.loc[df['OS Support Status'] == 'Unsupported', 'OS Support Status'] = 'background-color: #FFEE58;'
        return style

    st.dataframe(assets_df.style.apply(style_assets, axis=None), use_container_width=True, hide_index=True)

    st.divider()
    # --- NEW: Added Vendor Scorecards ---
    st.subheader("Key Vendor Performance Scorecards")
    st.caption("Manage vendor relationships with data-driven insights to ensure systems remain secure, scalable, and well-supported.")
    
    for vendor_name, data in vendor_data.items():
        st.markdown(f"**{vendor_name}**")
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        v_col1.metric("SLA Compliance", f"{data['sla_compliance']}%", delta=f"{data['sla_delta']}%")
        v_col2.metric("Avg. Support MTTR (h)", data['mttr'], delta=f"{data['mttr_delta']}h")
        v_col3.metric("Hardware Reliability (MTBF days)", data['mtbf'], help="Mean Time Between Failures")
        v_col4.metric("QBR Status", data['qbr_status'])


# ==============================================================================
# TAB 4: STRATEGIC INITIATIVES & INNOVATION PIPELINE
# ==============================================================================
with tab4:
    st.header("Strategic Initiatives & Technology Innovation")
    st.caption("Monitoring emerging lab technologies and overseeing process automation initiatives to drive future value.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Emerging Technology Radar")
        with st.expander("🔬 **Methodology & Significance**"):
            st.markdown("""
            This radar visualizes our stance on emerging technologies, adapted from the ThoughtWorks Tech Radar framework. It's a tool for strategic discussion and planning.
            - **Rings**: Represent the maturity of our adoption. **Adopt** are core technologies. **Trial** are promising techs we are actively piloting. **Assess** are ones to watch. **Hold** are technologies we are phasing out.
            - **Significance:** This provides a clear framework for managing innovation. It shows stakeholders that we are actively monitoring the landscape (e.g., **IoT Sensors, Lab Voice Assistants**) while methodically evaluating them (**AR/VR Lab Support**) before broad adoption. It ensures innovation is a managed process, not a series of random experiments.
            """)
        fig_radar_tech = px.scatter(tech_radar_df, x="theta", y="r", color="Quadrant", text="Technology", hover_name="Details", title="DTE Lab Technology Radar", polar=True)
        fig_radar_tech.update_layout(polar=dict(radialaxis=dict(showticklabels=False, ticks='', gridcolor='lightgrey'), angularaxis=dict(showticklabels=False, ticks='')))
        st.plotly_chart(fig_radar_tech, use_container_width=True)

    with col2:
        st.subheader("Process Automation Impact")
        with st.expander("🔬 **Methodology & Significance**"):
            st.markdown("""
            This chart quantifies the business value of our automation initiatives, a key responsibility for the AD. It tracks the cumulative lab staff hours saved per month by implementing automated scripts and workflows.
            - **Significance:** This is a direct, quantifiable measure of the DTE team's contribution to operational excellence. It translates technical work (e.g., writing a Python script for data transfer) into a business-centric metric ("We saved the QC team 40 hours this month"). This is essential for justifying budget and headcount for automation-focused roles.
            """)
        automation_data = pd.DataFrame({'Project': ['Automated HPLC Report Generation', 'NGS FASTQ File Transfer Script', 'LIMS Data Entry Bot'], 'Hours Saved / Month': [40, 25, 60]})
        fig_automation = px.bar(automation_data, x='Project', y='Hours Saved / Month', text='Hours Saved / Month', title='Impact of Lab Automation Initiatives')
        st.plotly_chart(fig_automation, use_container_width=True)


# ==============================================================================
# TAB 5: COMPLIANCE & GXP POSTURE
# ==============================================================================
with tab5:
    st.header("Compliance & GxP Posture Dashboard")
    st.caption("Centralized view of validation status, active deviations, and audit readiness for West Coast labs.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("GxP Systems in Validated State", "95%", help="Percentage of assets requiring validation that are currently in a validated state.")
    col2.metric("Open Quality Deviations", "3", help="Number of open deviations/non-conformances related to DTE systems.")
    col3.metric("21 CFR Part 11 Readiness", "98%", help="Estimated percentage of system controls meeting Part 11 requirements (audit trails, e-sigs, etc.).")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Validation Master Plan (VMP) Tracker")
        st.caption("Primary tool for planning and allocating validation resources and ensuring compliant, timely GxP system go-lives.")
        fig_vmp = px.timeline(vmp_df, x_start="Start", x_end="Finish", y="System/Instrument", color="Phase", hover_name="Validation Lead")
        st.plotly_chart(fig_vmp, use_container_width=True)
    
    with c2:
        st.subheader("Internal Audit Readiness Checklist")
        st.caption("Proactive self-assessment tool to demonstrate a mature, risk-based approach to quality management.")
        def style_audit_status(val):
            if val == 'Ready': return 'background-color: #2ca02c; color: white;'
            if val == 'Needs Review': return 'background-color: #ffc107; color: black;'
            if val == 'Gap Identified': return 'background-color: #d62728; color: white;'
            return ''
        st.dataframe(audit_df.style.map(style_audit_status, subset=['Status']), use_container_width=True, hide_index=True)


# ==============================================================================
# TAB 6: LEADERSHIP & GLOBAL ALIGNMENT (NEW)
# ==============================================================================
with tab6:
    st.header("Leadership: Team Performance & Global Alignment")
    st.caption("Fostering a culture of collaboration, innovation, and high performance through strategic talent management and matrix leadership.")

    st.subheader("Team Performance & Development Hub")
    st.markdown("Manage Vertex and partner team members at San Diego and Seattle.")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("**Team Skills & Training Matrix**")
        st.dataframe(team_df.style.applymap(lambda val: 'background-color: #FFEE58' if val == 'Beginner' else ''), use_container_width=True)
    with col2:
        st.markdown("**Identified Skill Gap & Training Need**")
        st.warning(f"**GAP:** {skills_gap['gap']}\n\n**Recommendation:** {skills_gap['recommendation']}")

    st.divider()

    st.subheader("Matrix Leadership: Global Alignment Dashboard")
    st.markdown("Deliver a globally aligned, locally enabled laboratory experience by benchmarking against global KPIs and sharing best practices.")
    
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
        st.markdown("**Global Best Practice Exchanger**")
        st.success(
            """
            **New Best Practice Identified (from Boston DTE):**
            - **Issue:** 'Lab Printer Offline' incidents.
            - **Boston's Solution:** Implemented a proactive script that pings all networked printers every 15 minutes. If a printer fails to respond twice, it auto-generates a low-priority ticket before a scientist reports it.
            - **Impact:** Reduced user-reported printer incidents by 90%.
            - **Recommendation:** Pilot this solution in the San Diego lab.
            """
        )
