import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import graphviz
from docx import Document

# ==============================================================================
# --- "10+" ENHANCEMENT DATA FUNCTIONS ---
# ==============================================================================

# Enhancement #1: Action Center
def get_action_center_items(pred_maint_df):
    """Aggregates all items needing approval."""
    actions = []
    # Autonomous Resource Recommendation
    actions.append({'id': 'res_rec_01', 'type': 'Resource Allocation', 'description': "Approve allocation of P. Sharma to 'LIMS Upgrade' project.", 'status': 'Pending'})
    # Predictive Maintenance
    for _, row in pred_maint_df[pred_maint_df['Status'] == 'Approval Pending'].iterrows():
        actions.append({'id': f"pm_{row['Asset ID']}", 'type': 'Predictive Maintenance', 'description': f"Approve PM Work Order for {row['Asset ID']} (Risk: {row['Predicted Failure Risk (%)']}%).", 'status': 'Pending'})
    # GxP Access Request
    actions.append({'id': 'access_01', 'type': 'GxP Access Request', 'description': "Approve elevated privileges for 'davis_c' on LIMS-PROD for data migration.", 'status': 'Pending'})
    return actions

# Enhancement #2: AI Weekly Briefing
def generate_weekly_briefing_text(site, data):
    """Generates a markdown report summarizing the week."""
    portfolio_df = data['portfolio_df']
    at_risk_projects = portfolio_df[portfolio_df['Status'] == 'At Risk'].shape[0]
    accomplishments = "- **Project Advancement:** 'LIMS Upgrade' project health score improved from 45% to 65% after resource allocation.\n- **Operational Stability:** Maintained 99.8% uptime across all critical lab systems."
    risks = f"- **Systemic Vendor Risk:** Continue to monitor 'ACME Reagents' performance as per active QMS insight.\n- **Project Risk:** {at_risk_projects} project(s) currently classified as 'At Risk'. See portfolio for details."
    
    kpi_summary = "KPI Data Not Available"
    if site in data['global_kpis'].columns:
        kpi_summary = f"- **System Uptime:** {data['global_kpis'].loc[0, site]:.1f}% (Global: {data['global_kpis'].loc[0, 'Global Avg']}%)\n- **MTTR (P1 Incidents):** {data['global_kpis'].loc[1, site]:.1f}h (Global: {data['global_kpis'].loc[1, 'Global Avg']}h)"


    return f"""
# DTE West Coast - Weekly Leadership Briefing
**Site:** {site}
**Date:** {date.today().strftime('%Y-%m-%d')}

---

### 1. Executive Summary
This week, the DTE team focused on mitigating risks for the 'LIMS Upgrade' project while maintaining exceptional operational stability. Proactive measures in predictive maintenance have prevented potential downtime, and we continue to track key vendor performance closely.

### 2. Key Accomplishments
{accomplishments}

### 3. Risks & Mitigations
{risks}

### 4. KPI Benchmark
{kpi_summary}
"""

# Enhancement #4: CapEx Proposal Generator
def generate_capex_proposal_text(asset_details):
    """Generates a full CapEx proposal draft."""
    return f"""
# Capital Expenditure Request: Replacement of {asset_details['Asset ID']}
**Date:** {date.today().strftime('%Y-%m-%d')}
**Requesting Dept:** DTE West Coast

---

### 1. Executive Summary
This proposal requests capital funds for the replacement of asset **{asset_details['Asset ID']} ({asset_details['Asset Type']})**. The existing asset has become a significant operational and financial drain, with an uptime of only **{asset_details['Uptime (%)']:.1f}%**, a high Total Cost of Ownership of **${asset_details['TCO ($k)']}k**, and **{asset_details['Incident Count (L12M)']}** incidents in the last 12 months. Replacement is critical to ensure scientific continuity and reduce operational risk.

### 2. Business Justification
The current asset's poor reliability directly impacts scientific workflows that depend on it. The high frequency of incidents consumes valuable DTE support hours and delays research. A modern replacement will offer higher throughput, greater reliability, and lower maintenance overhead.

### 3. Financial Analysis
- **Current TCO (Annualized):** ${asset_details['TCO ($k)']}k
- **Estimated New Asset Cost:** $150k (Quote from Vendor XYZ)
- **Projected New Asset TCO:** $30k
- **Payback Period:** Approx. 18 months

### 4. Proposed Solution
We recommend the purchase of the 'VendorXYZ Model 2.0', which is the current industry standard and compatible with our existing infrastructure.

### 5. Appendix
- Incident History Log for {asset_details['Asset ID']}
- Quote from VendorXYZ
"""

# Enhancement #5: FinOps / Cloud Cost Data
def get_finops_data():
    """Simulates cloud cost data."""
    dates = pd.to_datetime([date.today() - timedelta(days=i) for i in range(90)])
    df = pd.DataFrame({
        'Date': np.random.choice(dates, 200),
        'Cost ($)': np.random.rand(200) * 50 + np.linspace(10, 50, 200),
        'Project': np.random.choice(['NGS Pipeline', 'Cryo-EM Analysis', 'AI Drug Discovery', 'Shared Infrastructure'], 200, p=[0.4, 0.3, 0.2, 0.1]),
        'Service': np.random.choice(['EC2 (Compute)', 'S3 (Storage)', 'SageMaker (AI/ML)', 'Data Transfer'], 200, p=[0.5, 0.2, 0.2, 0.1])
    })
    return df.sort_values('Date')

# Enhancement #6: Instrument Utilization Data
def get_instrument_utilization_data():
    """Simulates live instrument utilization."""
    return pd.DataFrame({
        'Instrument': ['SD-HPLC-001', 'SD-HPLC-002', 'SD-MS-001', 'SEA-NGS-001', 'SEA-NGS-002', 'SEA-ROBO-004'],
        'Site': ['San Diego', 'San Diego', 'San Diego', 'Seattle', 'Seattle', 'Seattle'],
        'Status': np.random.choice(['In Use', 'Idle', 'Maintenance'], 6, p=[0.5, 0.4, 0.1]),
        'Utilization (Last 7 Days %)': np.random.randint(10, 95, 6)
    })

# Enhancement #8: Digital Twin Simulation
def run_digital_twin_simulation(change_description):
    """Simulates running a change in a digital twin environment."""
    if "patch" in change_description.lower():
        risk = "Low"
        impact = "No performance degradation detected. All connectivity tests passed."
    elif "update" in change_description.lower():
        risk = "Medium"
        impact = "Minor (5%) increase in query latency detected. Recommended to proceed with monitoring."
    else:
        risk = "High"
        impact = "Critical API failure detected. 'get_sample_data' endpoint unresponsive. DO NOT DEPLOY."
    return {"risk": risk, "impact": impact}

# Enhancement #9: Interactive Audit Trail Search
def search_audit_log(log_df, query):
    """Simulates a simple natural language search on the audit log."""
    query = query.lower()
    filtered_df = log_df.copy()
    if "user" in query:
        try:
            user = query.split("user")[-1].split("'")[1].strip()
            filtered_df = filtered_df[filtered_df['User/Process'].str.contains(user, case=False)]
        except IndexError:
            pass # Handle cases where query format is unexpected
    if "system" in query:
        try:
            system = query.split("system")[-1].strip().upper().split(" ")[0]
            filtered_df = filtered_df[filtered_df['System'].str.contains(system, case=False)]
        except IndexError:
            pass
    return filtered_df

# Enhancement #10: Resource Allocation Heatmap
def get_resource_allocation_data(portfolio_df):
    """Generates resource allocation data for the heatmap."""
    members = portfolio_df['Assigned_To'].unique()
    months = pd.to_datetime([date.today() + timedelta(days=30*i) for i in range(6)]).strftime('%Y-%m')
    heatmap_data = pd.DataFrame(np.random.randint(40, 111, size=(len(members), 6)), index=members, columns=months)
    return heatmap_data

# ==============================================================================
# --- Fully Integrated & Enhanced Base Data Simulation Functions ---
# ==============================================================================

def get_strategic_alignment_data():
    return pd.DataFrame({'Strategy Pillar': ['Accelerate Discovery', 'Ensure GxP Compliance', 'Enable New Modalities', 'Drive Efficiency', 'Enhance Data Integrity'], 'DTE Focus Score': [8, 9, 7, 8, 9.5]})

def get_project_portfolio_data():
    return pd.DataFrame({
        'Task': ['SD Lab Build-out Phase II', 'LIMS Upgrade', 'LIMS User Training', 'NGS Data Pipeline Automation', 'Cryo-EM Data Storage Expansion', 'SEA Lab Computer Refresh Q3', 'AR/VR Support Pilot'],
        'Site': ['San Diego', 'San Diego', 'San Diego', 'Seattle', 'San Diego', 'Seattle', 'San Diego'],
        'Start': pd.to_datetime(['2024-10-01', '2024-07-01', '2024-09-16', '2024-07-15', '2024-08-01', '2024-09-01', '2024-09-15']),
        'Finish': pd.to_datetime(['2025-02-15', '2024-09-15', '2024-10-15', '2024-11-30', '2024-12-01', '2024-11-30', '2024-12-15']),
        'Status': ['On Track', 'At Risk', 'Not Started', 'On Track', 'On Track', 'On Track', 'On Track'],
        'Dependencies': [None, None, 'LIMS Upgrade', None, None, None, None],
        'Assigned_To': ['J. Doe', 'A. Smith', 'A. Smith', 'L. Chen', 'J. Doe', 'L. Chen', 'M. Patel (Partner)']
    })

def get_itsm_ticket_data():
    today = date.today()
    dates = pd.to_datetime([today - timedelta(days=i) for i in range(60)])
    data = {'Ticket ID': [f'INC{12345+i}' for i in range(100)] + [f'REQ{54321+i}' for i in range(100)],
            'Date': np.random.choice(dates, 200),
            'Site': np.random.choice(['San Diego', 'Seattle'], 200, p=[0.6, 0.4]),
            'Category': np.random.choice(['Instrument Connectivity', 'Software Login', 'Data Access', 'Printer Issue', 'New Software Request', 'Performance Lag', 'Hardware Failure'], 200, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.1, 0.05]),
            'Priority': np.random.choice(['P1 - Critical', 'P2 - High', 'P3 - Medium', 'P4 - Low'], 200, p=[0.05, 0.15, 0.5, 0.3]),
            'Type': ['Incident']*100 + ['Request']*100}
    tickets_df = pd.DataFrame(data).sort_values(by='Date')
    base_mttr = np.random.uniform(2, 6, size=len(dates))
    spike_indices = np.random.choice(len(dates), 4, replace=False)
    base_mttr[spike_indices] = [9.2, 9.5, 10.1, 8.9]
    mttr_data = pd.Series(base_mttr, index=dates).reindex(pd.to_datetime(tickets_df['Date'].unique()), method='pad')
    return tickets_df, mttr_data

def get_asset_inventory_data():
    return pd.DataFrame({'Asset ID': [f'VRTX-SD-HPLC-{i:03d}' for i in range(1, 11)] + [f'VRTX-SEA-NGS-{i:03d}' for i in range(1, 6)], 'Asset Name': [f'Agilent HPLC {i}' for i in range(1, 11)] + [f'Illumina NovaSeq {i}' for i in range(1, 6)], 'OS Support Status': ['Supported']*12 + ['Unsupported']*2 + ['Supported']*1, 'Warranty Status': ['Active']*10 + ['Expiring Soon']*3 + ['Expired']*2, 'Validation Status': ['Validated']*13 + ['Overdue']*1 + ['N/A']*1})

def get_tech_radar_data():
    return pd.DataFrame({'Technology': ['IoT Sensors', 'AI-driven Analytics', 'Cloud Collaboration', 'AR/VR Lab Support', 'Lab Voice Assistants', 'Robotic Process Automation (RPA)', 'Legacy LIMS'], 'Quadrant': ['Platforms', 'Techniques', 'Tools', 'Tools', 'Platforms', 'Techniques', 'Platforms'], 'r': [3.5, 2.5, 1.5, 2.8, 3.2, 1.8, 4.5], 'theta': [45, 120, 210, 300, 60, 150, 270], 'Details': ['...'] * 7})

def get_vmp_tracker_data():
    return pd.DataFrame({'System/Instrument': ['New LIMS v2.0 (SD)', 'SD HPLC #11', 'SEA NGS #06'], 'Site': ['San Diego', 'San Diego', 'Seattle'], 'Start': pd.to_datetime(['2024-05-01', '2024-05-20', '2024-07-01']), 'Finish': pd.to_datetime(['2024-08-15', '2024-06-15', '2024-08-01']), 'Status': ['At Risk', 'Completed', 'On Track']})

def get_audit_readiness_data():
    return pd.DataFrame({'Audit Area': ['Change Control Procedures', 'System Access & Security Logs', '21 CFR Part 11 Controls', 'Data Backup and Recovery', 'Disaster Recovery Plan', 'Personnel Training Records', 'SOPs for GxP Systems'], 'Status': ['Ready', 'Ready', 'Needs Review', 'Ready', 'Gap Identified', 'Ready', 'Ready'], 'Last Reviewed': [date(2024, 4, 15), date(2024, 5, 1), date(2023, 11, 10), date(2024, 3, 22), date(2023, 1, 15), date(2024, 5, 5), date(2024, 4, 30)], 'Owner': ['A. Smith', 'L. Chen', 'A. Smith', 'L. Chen', 'AD Lead', 'J. Doe', 'A. Smith']})

def get_voice_of_scientist_data():
    return {"WIFI": 25, "SLOW": 22, "PRINTER": 20, "LOGIN": 18, "CONNECTIVITY": 15, "CRASH": 12}

def get_ai_briefing(audience, kpis):
    if audience == "Site Leadership (SD)": return f"Team, DTE maintained exceptional lab system uptime of {kpis['uptime']}..."
    else: return f"Hi Team, just a quick update from DTE. We're happy to report that lab system stability remains high..."

def get_ai_root_cause(problem_description):
    return "Correlated data shows a network switch (SW-4C-01) in Lab 4C-SD is reporting high packet loss. This is the most likely root cause..."

def get_vendor_scorecards():
    return {"Agilent Technologies": {"annual_spend_k": 850, "performance_score": 88, "incidents": 12}, "Illumina": {"annual_spend_k": 1200, "performance_score": 95, "incidents": 5}, "Hamilton": {"annual_spend_k": 400, "performance_score": 92, "incidents": 8}}

def get_team_performance():
    team_data = {
        "Team Member": ["J. Doe", "A. Smith", "L. Chen", "M. Patel (Partner)"],
        "Site": ["San Diego", "San Diego", "Seattle", "San Diego"],
        "Role": ["Sr. Specialist", "Specialist", "Sr. Specialist", "Support Tech"],
        "Core ITIL": ["Expert", "Advanced", "Expert", "Advanced"],
        "Windows GxP": ["Expert", "Advanced", "Advanced", "Intermediate"],
        "Automation (Python)": ["Intermediate", "Beginner", "Beginner", "Beginner"],
        "CSV/Validation": ["Advanced", "Intermediate", "Advanced", "Beginner"]}
    skills_gap = {"gap": "Team proficiency in Automation (Python/Scripting) is low across the West Coast.", "recommendation": "Identify 1-2 team members for advanced Python training to support lab automation goals."}
    return pd.DataFrame(team_data), skills_gap

def get_global_kpis():
    return pd.DataFrame({"KPI": ["System Uptime", "P1 Incident MTTR (h)", "User Satisfaction (CSAT)"], "San Diego": [99.6, 4.1, 4.5], "Seattle": [99.9, 3.5, 4.7], "Global Avg": [99.7, 4.5, 4.4], "unit": ["%", "", "/5"]})

def get_predictive_maintenance_data():
    return pd.DataFrame({'Asset ID': ['VRTX-SD-HPLC-007', 'VRTX-SEA-NGS-002', 'VRTX-SD-MS-001'], 'Site': ['San Diego', 'Seattle', 'San Diego'], 'Instrument Type': ['Agilent HPLC', 'Illumina NovaSeq', 'Waters Mass Spec'], 'Predicted Failure Risk (%)': [85, 45, 20], 'Predicted Failure Type': ['Pump Seal Failure', 'Laser Power Degradation', 'Normal Wear'], 'Status': ['Approval Pending', 'Tracked', 'Tracked']})

def get_capital_asset_model_data():
    return pd.DataFrame({'Asset ID': ['VRTX-SEA-NGS-001', 'VRTX-SD-HPLC-002', 'VRTX-SD-ROBO-004', 'VRTX-SEA-MS-003'], 'Asset Type': ['NGS Sequencer', 'HPLC', 'Liquid Handler', 'Mass Spectrometer'], 'Asset Age (Yrs)': [7, 8, 2, 5], 'Total Cost of Ownership ($)': [180000, 95000, 15000, 120000], 'Scientific Need Score': [9.8, 6.5, 8.0, 9.2]})

def get_project_forecast_data(portfolio_df):
    portfolio_df['Health Score (%)'] = np.random.randint(40, 101, size=len(portfolio_df))
    return portfolio_df

def generate_gxp_document(system_name, doc_type):
    return f"## Draft: {doc_type} for {system_name}\nThis document outlines the validation strategy..."

def generate_capex_proposal(asset_details):
    return f"## Capital Expenditure Request: Replacement of {asset_details['Asset ID']}\n\n**1. Executive Summary:**..."

def run_mitigation_simulation(scenario):
    if "Engineer" in scenario: return {"new_finish_date": "2024-08-10", "budget_impact": 25, "success_prob": 75}
    else: return {"new_finish_date": "2024-07-28", "budget_impact": 0, "success_prob": 95}

def get_self_healing_log():
    now = datetime.now()
    return pd.DataFrame({'Timestamp': [now - timedelta(minutes=5), now - timedelta(hours=2), now - timedelta(hours=6)], 'System': ['LIMS Production DB', 'SD-HPLC-007', 'SEA-DATA-ARCHIVE'], 'Site': ['San Diego', 'San Diego', 'Seattle'], 'Autonomous Diagnosis (RCA)': ['Orphaned SQL query from user `jdoe`', 'Precursor signature for pump seal failure', 'Network timeout to secondary storage'], 'Autonomous Resolution': ['Killed orphaned query, latency restored', 'Prescribed Fix, workflow initiated', 'Re-initiated backup job, completed']})

def run_strategic_financial_model(query):
    return {"capex_impact": 55.3, "headcount_growth": 45, "npv": 127.5, "narrative": "Accelerating the C> program by 30% will require a significant upfront investment of $55.3M over 5 years..."}

def get_autonomous_resource_recommendation():
    return {"project": "LIMS Upgrade", "site": "San Diego", "health_score": 45, "recommended_resource": "P. Sharma", "resource_location": "Boston (Global Team)", "skills_needed": "CSV, LIMS Integration, SQL", "duration": "3 Weeks (50% Allocation)", "confidence": 90}

def get_living_system_file_log():
    now = datetime.now()
    return pd.DataFrame({'Event Timestamp': [now - timedelta(minutes=15), now - timedelta(hours=1, minutes=2), now - timedelta(hours=4, minutes=30), now - timedelta(days=1)], 'System': ['LIMS-PROD', 'LIMS-PROD', 'HPLC-SD-011', 'LIMS-PROD'], 'User/Process': ['davis_c', 'System Patch Manager', 'hplc_instrument_svc', 'davis_c'], 'Description': ['User davis_c logged into the system.', 'Security patch KB5011487 applied successfully.', 'New result set for Batch #VTX-45A-003 saved.', 'User davis_c changed sample status.'], 'Cryptographic Hash': [f'0x{np.random.randint(1e15, 1e16-1):x}', f'0x{np.random.randint(1e15, 1e16-1):x}', f'0x{np.random.randint(1e15, 1e16-1):x}', f'0x{np.random.randint(1e15, 1e16-1):x}']})

def get_tco_data():
    return pd.DataFrame({'Asset ID': ['VRTX-SD-NGS-001', 'VRTX-SD-HPLC-002', 'VRTX-SEA-ROBO-004', 'VRTX-SEA-MS-003'], 'Site': ['San Diego', 'San Diego', 'Seattle', 'Seattle'], 'Asset Type': ['NGS Sequencer', 'HPLC', 'Liquid Handler', 'Mass Spectrometer'], 'TCO ($k)': [250, 120, 45, 180], 'Uptime (%)': [98.5, 90.1, 99.9, 99.1], 'Maintenance Costs ($k)': [70, 45, 10, 60], 'Incident Count (L12M)': [5, 22, 2, 8]})

def get_automation_roi_data():
    return pd.DataFrame({'Month': range(1, 13), 'Cumulative Value ($k)': [-50, -40, -30, -15, 5, 25, 45, 65, 85, 105, 125, 145]})

def get_risk_adjusted_vmp_data():
    return pd.DataFrame({'System/Instrument': ['New LIMS v2.0', 'Research HPLC #15', 'QC Plate Reader #3', 'Empower Upgrade'], 'Site': ['San Diego', 'San Diego', 'Seattle', 'Seattle'], 'Days Until Due': [45, 120, 15, 90], 'System Criticality': [10, 3, 8, 9], 'Validation Effort (Hours)': [400, 80, 120, 300], 'Status': ['On Track', 'On Track', 'At Risk', 'On Track']})

def run_what_if_scenario(query):
    if "Hamilton-01" in query:
        return "IMPACT: Delaying Hamilton-01 validation by 2 weeks will directly delay the start of the 'Cologuard Lib Prep Validation' project by 10 business days, creating a high risk of missing the Q3 go-live target."
    return "No critical project dependencies found for this scenario."

def get_assay_impact_data():
    return {'sources': [0, 1, 1, 2, 3, 4, 5, 6], 'targets': [3, 4, 5, 6, 6, 7, 7, 7], 'values': [10, 5, 5, 8, 10, 5, 8, 2], 'labels': ["HPLC-007 (OK)", "NGS-002 (OOS)", "MassSpec-001 (OK)", "Assay A", "Assay B", "Assay C", "Project 'VT-101'", "Project 'VT-205'"], 'colors': ["green", "red", "green", "blue", "blue", "blue", "purple", "purple"]}

def get_reagent_genealogy_data(reagent_lot_id):
    dot = graphviz.Digraph(comment='Reagent Lot Genealogy')
    dot.attr('node', shape='box', style='rounded,filled')
    dot.node('lot', f'Problem Lot\n{reagent_lot_id}', fillcolor='red', fontcolor='white')
    dot.node('run1', 'NGS Run 240510-A'); dot.node('run2', 'HTS Run 240511-C')
    dot.edge('lot', 'run1'); dot.edge('lot', 'run2')
    dot.node('plate1', 'Plate P123'); dot.node('plate2', 'Plate P124'); dot.node('plate3', 'Plate P201')
    dot.edge('run1', 'plate1'); dot.edge('run1', 'plate2'); dot.edge('run2', 'plate3')
    dot.node('proj1', "Project 'VT-101'", fillcolor='purple', fontcolor='white')
    dot.node('proj2', "Project 'VT-315'", fillcolor='purple', fontcolor='white')
    dot.edge('plate1', 'proj1'); dot.edge('plate2', 'proj1'); dot.edge('plate3', 'proj2')
    return dot

def get_clinical_sample_journey():
    return pd.DataFrame({'Step': [1, 2, 3, 4, 5], 'Action': ['Sample Received', 'Prep & Aliquoting', 'PCR Amplification', 'Data Analysis', 'Result Certified'], 'System/Instrument': ['LIMS Entry Station', 'Hamilton-03 (SD)', 'QuantStudio-08 (SD)', 'Pipeline Server v2.1', 'LIMS Reporting Module'], 'Timestamp': pd.to_datetime(['2024-05-20 09:00', '2024-05-20 11:30', '2024-05-20 14:00', '2024-05-20 18:00', '2024-05-21 10:00']), 'Status': ['OK', 'OK', 'OK', 'OK', 'OK']})

def get_qms_query_result(query):
    if "CAPA" in query and "software" in query:
        site_filter = "San Diego" if "San Diego" in query else "Seattle" if "Seattle" in query else None
        df = pd.DataFrame({'CAPA ID': ['CAPA-0123', 'CAPA-0145'], 'Site': ['San Diego', 'Seattle'], 'Product': ['Cologuard', 'Oncotype DX'], 'Issue': ['Software bug caused incorrect data parsing', 'UI freeze during result entry'], 'Status': ['Closed', 'Open']})
        if site_filter: return df[df['Site'] == site_filter]
        return df
    return pd.DataFrame({'Result': ['No matching records found for your query.']})

def get_systemic_risk_insight():
    return {"title": "Systemic Vendor Risk Detected: ACME Reagents (Impacting San Diego)", "insight": "AI analysis of QMS, LIMS, and ITSM data reveals that 'ACME Reagents' is linked to 2 open CAPAs at the San Diego site. Furthermore, the MTTR for incidents related to their reagents is 40% higher than the lab average at that site.", "recommendation": "Initiate a strategic business review of this vendor relationship and evaluate alternative suppliers for the San Diego labs."}
