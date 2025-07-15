# utils.py

import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime

# ==============================================================================
# --- Base Data Simulation Functions ---
# ==============================================================================

def get_strategic_alignment_data():
    """Simulates data for the strategic alignment radar chart."""
    return pd.DataFrame({ 'Strategy Pillar': ['Accelerate Discovery (Speed)', 'Ensure GxP Compliance', 'Enable New Modalities (C>)', 'Drive Operational Efficiency', 'Enhance Data Integrity'], 'DTE Focus Score': [8, 9, 7, 8, 9.5] })

def get_project_portfolio_data():
    """Simulates the base data for the project portfolio."""
    return pd.DataFrame({
        'Project': ['SD Lab Build-out Phase II', 'LIMS Upgrade', 'NGS Data Pipeline Automation', 'Cryo-EM Data Storage Expansion', 'Lab Computer Refresh Q3', 'AR/VR Support Pilot'],
        'Strategic Impact Score': [9.5, 8, 9, 8.5, 6, 7],
        'Effort (Person-Weeks)': [150, 80, 60, 120, 40, 25],
        'Budget ($k)': [2000, 750, 300, 1500, 500, 80],
        'Strategic Theme': ['New Modalities', 'Compliance', 'Efficiency', 'Discovery', 'Operations', 'Innovation'],
        'Status': ['On Track', 'At Risk', 'On Track', 'On Track', 'Completed', 'On Track'],
        'Planned Finish': pd.to_datetime(['2024-12-15', '2024-07-30', '2024-09-01', '2024-11-01', '2024-05-30', '2024-08-20'])
    })

def get_itsm_ticket_data():
    """Simulates ITSM ticket data from a system like ServiceNow."""
    today = date.today()
    dates = pd.to_datetime([today - timedelta(days=i) for i in range(30)])
    dates = sorted(dates)
    data = {'Ticket ID': [f'INC{12345+i}' for i in range(50)] + [f'REQ{54321+i}' for i in range(50)], 'Date': np.random.choice(dates, 100), 'Category': np.random.choice(['Instrument Connectivity', 'Software Login', 'Data Access', 'Printer Issue', 'New Software Request', 'Performance Lag', 'Hardware Failure'], 100, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.1, 0.05]), 'Priority': np.random.choice(['P1 - Critical', 'P2 - High', 'P3 - Medium', 'P4 - Low'], 100, p=[0.05, 0.15, 0.5, 0.3]), 'SLA Met': np.random.choice([True, False], 100, p=[0.9, 0.1]), 'Type': ['Incident']*50 + ['Request']*50}
    tickets_df = pd.DataFrame(data).sort_values(by='Date')
    base_mttr = np.random.uniform(2, 6, size=len(dates))
    spike_indices = np.random.choice(len(dates), 2, replace=False)
    base_mttr[spike_indices] = [9.2, 9.5]
    mttr_data = pd.Series(base_mttr, index=dates).reindex(pd.to_datetime(tickets_df['Date'].unique()), method='pad')
    return tickets_df, mttr_data

def get_asset_inventory_data():
    """Simulates asset data from a Configuration Management Database (CMDB)."""
    return pd.DataFrame({'Asset ID': [f'VRTX-SD-HPLC-{i:03d}' for i in range(1, 11)] + [f'VRTX-SEA-NGS-{i:03d}' for i in range(1, 6)], 'Asset Name': [f'Agilent HPLC {i}' for i in range(1, 11)] + [f'Illumina NovaSeq {i}' for i in range(1, 6)], 'OS Support Status': ['Supported']*12 + ['Unsupported']*2 + ['Supported']*1, 'Warranty Status': ['Active']*10 + ['Expiring Soon']*3 + ['Expired']*2, 'Validation Status': ['Validated']*13 + ['Overdue']*1 + ['N/A']*1})

def get_tech_radar_data():
    """Simulates data for the technology radar."""
    return pd.DataFrame({'Technology': ['IoT Sensors', 'AI-driven Analytics', 'Cloud Collaboration', 'AR/VR Lab Support', 'Lab Voice Assistants', 'Robotic Process Automation (RPA)', 'Legacy LIMS'], 'Quadrant': ['Platforms', 'Techniques', 'Tools', 'Tools', 'Platforms', 'Techniques', 'Platforms'], 'r': [3.5, 2.5, 1.5, 2.8, 3.2, 1.8, 4.5], 'theta': [45, 120, 210, 300, 60, 150, 270], 'Details': ['...'] * 7})

def get_vmp_tracker_data():
    """Simulates data for the Validation Master Plan Gantt chart."""
    return pd.DataFrame({'System/Instrument': [ 'New LIMS v2.0', 'SD HPLC #11', 'SEA NGS #06' ], 'Start': pd.to_datetime([ '2024-05-01', '2024-05-20', '2024-07-01' ]), 'Finish': pd.to_datetime([ '2024-08-15', '2024-06-15', '2024-08-01' ]), 'Phase': ['Validation Lifecycle', 'Qualification', 'Qualification'], 'Status': ['At Risk', 'Completed', 'On Track'], 'Validation Lead': ['J. Doe', 'A. Smith', 'L. Chen']})

def get_audit_readiness_data():
    """Simulates data for the audit readiness checklist."""
    return pd.DataFrame({'Audit Area': [ 'Change Control Procedures', 'System Access & Security Logs', '21 CFR Part 11 Controls', 'Data Backup and Recovery', 'Disaster Recovery Plan', 'Personnel Training Records', 'SOPs for GxP Systems' ], 'Status': ['Ready', 'Ready', 'Needs Review', 'Ready', 'Gap Identified', 'Ready', 'Ready'], 'Last Reviewed': [ date(2024, 4, 15), date(2024, 5, 1), date(2023, 11, 10), date(2024, 3, 22), date(2023, 1, 15), date(2024, 5, 5), date(2024, 4, 30) ], 'Owner': ['A. Smith', 'L. Chen', 'A. Smith', 'L. Chen', 'AD Lead', 'J. Doe', 'A. Smith']})

def get_voice_of_scientist_data():
    """Simulates word frequency data from analyzing ServiceNow tickets and user surveys."""
    return {"WIFI": 25, "SLOW": 22, "PRINTER": 20, "LOGIN": 18, "CONNECTIVITY": 15, "CRASH": 12, "DATA_TRANSFER": 10, "HPLC": 9, "ERROR": 8, "ACCESS": 7}

def get_ai_briefing(audience, kpis):
    """Simulates an LLM generating a tailored briefing."""
    if audience == "Site Leadership (SD)": return f"Team, DTE maintained exceptional lab system uptime of {kpis['uptime']}..."
    else: return f"Hi Team, just a quick update from DTE. We're happy to report that lab system stability remains high..."

def get_ai_root_cause(problem_description):
    """Simulates an AI co-pilot diagnosing an issue by correlating data from different systems."""
    return "Correlated data shows a network switch (SW-4C-01) in Lab 4C-SD is reporting high packet loss. This is the most likely root cause..."
    
def get_vendor_scorecards():
    """Simulates performance data for key technology vendors."""
    return {
        "Agilent Technologies": {"annual_spend_k": 850, "performance_score": 88, "incidents": 12},
        "Illumina": {"annual_spend_k": 1200, "performance_score": 95, "incidents": 5},
        "Hamilton": {"annual_spend_k": 400, "performance_score": 92, "incidents": 8}
    }

def get_team_performance():
    """Simulates data for the team skills matrix and identified gaps."""
    team_data = {"Team Member": ["J. Doe (SD)", "A. Smith (SD)", "L. Chen (SEA)", "M. Patel (Partner)"], "Role": ["Sr. Specialist", "Specialist", "Sr. Specialist", "Support Tech"], "Core ITIL": ["Expert", "Advanced", "Expert", "Advanced"], "Windows GxP": ["Expert", "Advanced", "Advanced", "Intermediate"], "Linux/HPC": ["Intermediate", "Beginner", "Advanced", "Beginner"], "Automation (Python)": ["Intermediate", "Beginner", "Beginner", "Beginner"], "CSV/Validation": ["Advanced", "Intermediate", "Advanced", "Beginner"]}
    skills_gap = {"gap": "Team proficiency in Automation (Python/Scripting) is low.", "recommendation": "Identify 1-2 team members for advanced Python training to support lab automation goals."}
    return pd.DataFrame(team_data), skills_gap

def get_global_kpis():
    """Simulates benchmark data comparing West Coast to Global DTE performance."""
    return pd.DataFrame({"KPI": ["System Uptime", "P1 Incident MTTR (h)", "User Satisfaction (CSAT)"], "West Coast": [99.8, 3.8, 4.6], "Global Avg": [99.7, 4.5, 4.4], "unit": ["%", "", "/5"]})

def get_predictive_maintenance_data():
    """Simulates output from the Predictive Instrument Failure ML model."""
    return pd.DataFrame({'Asset ID': ['VRTX-SD-HPLC-007', 'VRTX-SEA-NGS-002', 'VRTX-SD-MS-001'], 'Instrument Type': ['Agilent HPLC', 'Illumina NovaSeq', 'Waters Mass Spec'], 'Predicted Failure Risk (%)': [85, 45, 20], 'Predicted Failure Type': ['Pump Seal Failure', 'Laser Power Degradation', 'Normal Wear'], 'Prescribed Fix': ['Replace pump seal (P/N 5063-6589)', 'Re-calibrate laser power output', 'Continue standard monitoring']})

def get_capital_asset_model_data():
    """Simulates output from the Intelligent Capital Asset Refresh ML model."""
    return pd.DataFrame({'Asset ID': ['VRTX-SEA-NGS-001', 'VRTX-SD-HPLC-002', 'VRTX-SD-ROBO-004', 'VRTX-SEA-MS-003'], 'Asset Type': ['NGS Sequencer', 'HPLC', 'Liquid Handler', 'Mass Spectrometer'], 'Asset Age (Yrs)': [7, 8, 2, 5], 'Total Cost of Ownership ($)': [180000, 95000, 15000, 120000], 'Scientific Need Score': [9.8, 6.5, 8.0, 9.2]})

def get_project_forecast_data(portfolio_df):
    """Simulates output from the Project Risk & Timeline Forecaster ML model."""
    health_scores = [95, 45, 88, 75, 100, 90]
    predicted_finishes = [pd.to_datetime('2024-12-20'), pd.to_datetime('2024-09-15'), pd.to_datetime('2024-09-05'), pd.to_datetime('2024-11-10'), pd.to_datetime('2024-05-30'), pd.to_datetime('2024-08-22')]
    portfolio_df['Health Score (%)'] = health_scores
    portfolio_df['Predicted Finish'] = predicted_finishes
    return portfolio_df

def generate_gxp_document(system_name, doc_type):
    """Simulates a GAMP 5-trained LLM generating a GxP document draft."""
    return f"## Draft: {doc_type} for {system_name}\nThis document outlines the validation strategy..."

def generate_capex_proposal(asset_details):
    """Simulates a fine-tuned LLM generating a full CapEx proposal from model data."""
    return f"## Capital Expenditure Request: Replacement of {asset_details['Asset ID']}\n\n**1. Executive Summary:**..."

def run_mitigation_simulation(scenario):
    """Simulates a Monte Carlo analysis for different project mitigation scenarios."""
    if "Engineer" in scenario: return {"new_finish_date": "2024-08-10", "budget_impact": 25, "success_prob": 75}
    else: return {"new_finish_date": "2024-07-28", "budget_impact": 0, "success_prob": 95}

def get_self_healing_log():
    """Simulates the real-time log from the autonomous reliability module."""
    now = datetime.now()
    return pd.DataFrame({'Timestamp': [now - timedelta(minutes=5), now - timedelta(hours=2), now - timedelta(hours=6)], 'System': ['LIMS Production DB', 'SD-HPLC-007', 'Scientific Data Archive'], 'Event Detected': ['High query latency detected (>3s)', 'Anomalous pressure signature detected', 'Data backup job failed'], 'Autonomous Diagnosis (RCA)': ['Orphaned SQL query from user `jdoe`', 'Precursor signature for pump seal failure', 'Network timeout to secondary storage'], 'Autonomous Resolution': ['Killed orphaned query, latency restored', 'Prescribed Fix, workflow initiated', 'Re-initiated backup job, completed'], 'Status': ['Resolved', 'Action Pending Approval', 'Resolved']})

def run_strategic_financial_model(query):
    """Simulates the output of the complex financial and strategic modeler."""
    return {"capex_impact": 55.3, "headcount_growth": 45, "npv": 127.5, "narrative": "Accelerating the C> program by 30% will require a significant upfront investment of $55.3M over 5 years..."}

def get_autonomous_resource_recommendation():
    """Simulates the output of the autonomous resource orchestrator when a project is at risk."""
    return {"project": "LIMS Upgrade", "health_score": 45, "recommended_resource": "P. Sharma", "resource_location": "Boston", "skills_needed": "CSV, LIMS Integration, SQL", "duration": "3 Weeks (50% Allocation)", "confidence": 90, "source_impact": "4-day delay to non-critical 'Boston Reporting' project"}

def get_living_system_file_log():
    """Simulates a query against the 'Living System Lifecycle File' (LSLF)."""
    now = datetime.now()
    return pd.DataFrame({'Event Timestamp': [now - timedelta(minutes=15), now - timedelta(hours=1, minutes=2), now - timedelta(hours=4, minutes=30)], 'Event Type': ['User Action', 'System Change', 'Data Entry'], 'User/Process': ['davis_c', 'System Patch Manager', 'HPLC #11'], 'Description': ['User davis_c logged into the system.', 'Security patch KB5011487 applied successfully.', 'New result set for Batch #VTX-45A-003 saved.'], 'Cryptographic Hash': [f'0x{np.random.randint(1e15, 1e16-1):x}', f'0x{np.random.randint(1e15, 1e16-1):x}', f'0x{np.random.randint(1e15, 1e16-1):x}']})

def get_tco_data():
    """Simulates data for the Total Cost of Ownership treemap."""
    return pd.DataFrame({'Asset ID': ['VRTX-SEA-NGS-001', 'VRTX-SD-HPLC-002', 'VRTX-SD-ROBO-004', 'VRTX-SEA-MS-003'], 'Asset Type': ['NGS Sequencer', 'HPLC', 'Liquid Handler', 'Mass Spectrometer'], 'TCO ($k)': [250, 120, 45, 180], 'Uptime (%)': [98.5, 99.8, 99.9, 99.1], 'Maintenance Costs ($k)': [70, 25, 10, 60]})

def get_automation_roi_data():
    """Simulates data for the cumulative ROI chart."""
    return pd.DataFrame({'Month': range(1, 13), 'Cumulative Value ($k)': [-50, -40, -30, -15, 5, 25, 45, 65, 85, 105, 125, 145]})
    
def get_risk_adjusted_vmp_data():
    """Simulates data for the risk-based validation scheduling chart."""
    return pd.DataFrame({'System/Instrument': [ 'New LIMS v2.0', 'Research HPLC #15', 'QC Plate Reader #3', 'Empower Upgrade' ], 'Days Until Due': [45, 120, 15, 90], 'System Criticality': [10, 3, 8, 9], 'Validation Effort (Hours)': [400, 80, 120, 300], 'Status': ['On Track', 'On Track', 'At Risk', 'On Track']})

def run_what_if_scenario(query):
    """Simulates the output of the what-if scenario planner."""
    if "Hamilton-01" in query:
        return "IMPACT: Delaying Hamilton-01 validation by 2 weeks will directly delay the start of the 'Cologuard Lib Prep Validation' project by 10 business days, creating a high risk of missing the Q3 go-live target."
    return "No critical project dependencies found for this scenario."

# --- CORRECTED FUNCTION ---
def get_assay_impact_data():
    """Simulates data for the instrument-to-assay Sankey diagram."""
    # This dictionary now has lists of equal length.
    data_dict = {
        'source': [0, 1, 1, 2, 3, 4, 5],
        'target': [3, 4, 5, 6, 6, 7, 7],
        'value':  [10, 5, 5, 8, 10, 5, 8],
        'label': ["HPLC-007 (OK)", "NGS-002 (OOS)", "MassSpec-001 (OK)", "Assay A", "Assay B", "Assay C", "Project 'VT-101'", "Project 'VT-205'"],
        'color': ["green", "red", "green", "blue", "blue", "blue", "purple", "purple"]
    }
    # To use Sankey, we need a flat list of all unique sources and targets for the labels.
    # The length of source, target, and value must be equal.
    sankey_data = {
        'source': data_dict['source'],
        'target': data_dict['target'],
        'value': data_dict['value'],
    }
    
    # We will pass the full labels and colors, but the plotting logic will use them based on node indices.
    # It's better to pass the labels/colors separately to the plotting function.
    # For this simulation, we will combine them into one DataFrame. The app.py will need to handle this.
    # A simplified approach for the simulation:
    return pd.DataFrame({
        'label': data_dict['label'],
        'color': data_dict['color'],
        'source': data_dict['source'] + [0], # Pad to match length
        'target': data_dict['target'] + [0], # Pad to match length
        'value': data_dict['value'] + [0] # Pad to match length
    })

def get_reagent_genealogy_data():
    """Returns a path to a pre-made image for the genealogy graph."""
    return "https://i.imgur.com/U3v5G2d.png"

def get_clinical_sample_journey():
    """Simulates the journey of a single clinical sample."""
    return pd.DataFrame({'Step': [1, 2, 3, 4, 5], 'Action': ['Sample Received', 'Prep & Aliquoting', 'PCR Amplification', 'Data Analysis', 'Result Certified'], 'System/Instrument': ['LIMS Entry Station', 'Hamilton-03', 'QuantStudio-08', 'Pipeline Server v2.1', 'LIMS Reporting Module'], 'Timestamp': pd.to_datetime(['2024-05-20 09:00', '2024-05-20 11:30', '2024-05-20 14:00', '2024-05-20 18:00', '2024-05-21 10:00']), 'Status': ['OK', 'OK', 'OK', 'OK', 'OK']})
    
def get_qms_query_result(query):
    """Simulates an LLM-powered query against a QMS."""
    if "CAPA" in query and "software" in query:
        return pd.DataFrame({'CAPA ID': ['CAPA-0123', 'CAPA-0145'], 'Product': ['Cologuard', 'Oncotype DX'], 'Issue': ['Software bug caused incorrect data parsing', 'UI freeze during result entry'], 'Status': ['Closed', 'Open']})
    return pd.DataFrame({'Result': ['No matching records found for your query.']})
    
def get_systemic_risk_insight():
    """Simulates an AI agent finding a hidden, systemic risk."""
    return {"title": "Systemic Vendor Risk Detected: ACME Reagents", "insight": "AI analysis of QMS, LIMS, and ITSM data reveals that 'ACME Reagents' is linked to 3 open CAPAs and 2 lots currently on hold. Furthermore, the MTTR for incidents related to their reagents is 40% higher than the lab average.", "recommendation": "Initiate a strategic business review of this vendor relationship and evaluate alternative suppliers."}
