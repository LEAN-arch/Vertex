import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import graphviz

# ==============================================================================
# --- Enhanced Data Simulation Functions (Now Site-Aware) ---
# The original data functions have been refactored to include a 'Site' column
# to support the West Coast Associate Director's role.
# ==============================================================================

def get_project_portfolio_data():
    """Simulates site-aware project portfolio data."""
    return pd.DataFrame({
        'Project': ['SD Lab Build-out Phase II', 'LIMS Upgrade', 'NGS Data Pipeline Automation', 'Cryo-EM Data Storage Expansion', 'SEA Lab Computer Refresh Q3', 'AR/VR Support Pilot'],
        'Site': ['San Diego', 'San Diego', 'Seattle', 'San Diego', 'Seattle', 'San Diego'],
        'Strategic Impact Score': [9.5, 8, 9, 8.5, 6, 7],
        'Budget ($k)': [2000, 750, 300, 1500, 500, 80],
        'Status': ['On Track', 'At Risk', 'On Track', 'On Track', 'Completed', 'On Track'],
        'Planned Finish': pd.to_datetime(['2024-12-15', '2024-07-30', '2024-09-01', '2024-11-01', '2024-05-30', '2024-08-20'])
    })

def get_itsm_ticket_data():
    """Simulates site-aware ITSM ticket data (e.g., from ServiceNow)."""
    today = date.today()
    dates = pd.to_datetime([today - timedelta(days=i) for i in range(60)])
    dates = sorted(dates)
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

def get_vmp_tracker_data():
    """Simulates a site-aware Validation Master Plan."""
    return pd.DataFrame({
        'System/Instrument': [ 'New LIMS v2.0 (SD)', 'SD HPLC #11', 'SEA NGS #06' ],
        'Site': ['San Diego', 'San Diego', 'Seattle'],
        'Start': pd.to_datetime([ '2024-05-01', '2024-05-20', '2024-07-01' ]),
        'Finish': pd.to_datetime([ '2024-08-15', '2024-06-15', '2024-08-01' ]),
        'Status': ['At Risk', 'Completed', 'On Track']})

def get_tco_data():
    """Simulates site-aware data for Total Cost of Ownership."""
    return pd.DataFrame({
        'Asset ID': ['VRTX-SD-NGS-001', 'VRTX-SD-HPLC-002', 'VRTX-SEA-ROBO-004', 'VRTX-SEA-MS-003'],
        'Site': ['San Diego', 'San Diego', 'Seattle', 'Seattle'],
        'Asset Type': ['NGS Sequencer', 'HPLC', 'Liquid Handler', 'Mass Spectrometer'],
        'TCO ($k)': [250, 120, 45, 180],
        'Uptime (%)': [98.5, 99.8, 99.9, 99.1],
        'Maintenance Costs ($k)': [70, 25, 10, 60]})

def get_risk_adjusted_vmp_data():
    """Simulates site-aware data for risk-based validation scheduling."""
    return pd.DataFrame({
        'System/Instrument': [ 'New LIMS v2.0', 'Research HPLC #15', 'QC Plate Reader #3', 'Empower Upgrade' ],
        'Site': ['San Diego', 'San Diego', 'Seattle', 'Seattle'],
        'Days Until Due': [45, 120, 15, 90],
        'System Criticality': [10, 3, 8, 9],
        'Validation Effort (Hours)': [400, 80, 120, 300],
        'Status': ['On Track', 'On Track', 'At Risk', 'On Track']})

def get_team_performance():
    """Simulates site-aware data for the team skills matrix."""
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
    """Simulates benchmark data comparing West Coast sites to Global DTE performance."""
    return pd.DataFrame({
        "KPI": ["System Uptime", "P1 Incident MTTR (h)", "User Satisfaction (CSAT)"],
        "San Diego": [99.6, 4.1, 4.5],
        "Seattle": [99.9, 3.5, 4.7],
        "Global Avg": [99.7, 4.5, 4.4],
        "unit": ["%", "", "/5"]})

def get_predictive_maintenance_data():
    """Simulates site-aware output from the Predictive Instrument Failure ML model."""
    return pd.DataFrame({
        'Asset ID': ['VRTX-SD-HPLC-007', 'VRTX-SEA-NGS-002', 'VRTX-SD-MS-001'],
        'Site': ['San Diego', 'Seattle', 'San Diego'],
        'Instrument Type': ['Agilent HPLC', 'Illumina NovaSeq', 'Waters Mass Spec'],
        'Predicted Failure Risk (%)': [85, 45, 20],
        'Predicted Failure Type': ['Pump Seal Failure', 'Laser Power Degradation', 'Normal Wear']})

def get_self_healing_log():
    """Simulates a site-aware log from the autonomous reliability module."""
    now = datetime.now()
    return pd.DataFrame({
        'Timestamp': [now - timedelta(minutes=5), now - timedelta(hours=2), now - timedelta(hours=6)],
        'System': ['LIMS Production DB', 'SD-HPLC-007', 'SEA-DATA-ARCHIVE'],
        'Site': ['San Diego', 'San Diego', 'Seattle'],
        'Autonomous Diagnosis (RCA)': ['Orphaned SQL query from user `jdoe`', 'Precursor signature for pump seal failure', 'Network timeout to secondary storage'],
        'Autonomous Resolution': ['Killed orphaned query, latency restored', 'Prescribed Fix, workflow initiated', 'Re-initiated backup job, completed']})

def get_living_system_file_log():
    """Simulates a query against the 'Living System Lifecycle File' (21 CFR Part 11)."""
    now = datetime.now()
    return pd.DataFrame({
        'Event Timestamp': [now - timedelta(minutes=15), now - timedelta(hours=1, minutes=2), now - timedelta(hours=4, minutes=30)],
        'System': ['LIMS-PROD', 'LIMS-PROD', 'HPLC-SD-011'],
        'User/Process': ['davis_c', 'System Patch Manager', 'hplc_instrument_svc'],
        'Description': ['User davis_c logged into the system.', 'Security patch KB5011487 applied successfully.', 'New result set for Batch #VTX-45A-003 saved.'],
        'Cryptographic Hash': [f'0x{np.random.randint(1e15, 1e16-1):x}', f'0x{np.random.randint(1e15, 1e16-1):x}', f'0x{np.random.randint(1e15, 1e16-1):x}']})

def get_autonomous_resource_recommendation():
    """Simulates the output of the autonomous resource orchestrator for a West Coast project."""
    return {"project": "LIMS Upgrade", "site": "San Diego", "health_score": 45, "recommended_resource": "P. Sharma", "resource_location": "Boston (Global Team)", "skills_needed": "CSV, LIMS Integration, SQL", "duration": "3 Weeks (50% Allocation)", "confidence": 90}

def get_qms_query_result(query):
    """Simulates an LLM-powered query against a QMS."""
    if "CAPA" in query and "software" in query:
        site_filter = "San Diego" if "San Diego" in query else "Seattle" if "Seattle" in query else None
        df = pd.DataFrame({'CAPA ID': ['CAPA-0123', 'CAPA-0145'], 'Site':['San Diego', 'Seattle'], 'Product': ['Cologuard', 'Oncotype DX'], 'Issue': ['Software bug caused incorrect data parsing', 'UI freeze during result entry'], 'Status': ['Closed', 'Open']})
        if site_filter:
            return df[df['Site'] == site_filter]
        return df # Return all for "West Coast (Overall)"
    return pd.DataFrame({'Result': ['No matching records found for your query.']})

def get_systemic_risk_insight():
    """Simulates an AI agent finding a hidden, systemic risk relevant to the West Coast."""
    return {"title": "Systemic Vendor Risk Detected: ACME Reagents (Impacting San Diego)", "insight": "AI analysis of QMS, LIMS, and ITSM data reveals that 'ACME Reagents' is linked to 2 open CAPAs at the San Diego site. Furthermore, the MTTR for incidents related to their reagents is 40% higher than the lab average at that site.", "recommendation": "Initiate a strategic business review of this vendor relationship and evaluate alternative suppliers for the San Diego labs."}

# --- UNCHANGED OR MINIMALLY CHANGED FUNCTIONS ---

def get_project_forecast_data(portfolio_df):
    """Simulates output from the Project Risk & Timeline Forecaster ML model."""
    health_scores = [95, 45, 88, 75, 100, 90]
    predicted_finishes = [pd.to_datetime('2024-12-20'), pd.to_datetime('2024-09-15'), pd.to_datetime('2024-09-05'), pd.to_datetime('2024-11-10'), pd.to_datetime('2024-05-30'), pd.to_datetime('2024-08-22')]
    portfolio_df['Health Score (%)'] = health_scores
    portfolio_df['Predicted Finish'] = predicted_finishes
    return portfolio_df

def get_automation_roi_data():
    """Simulates data for the cumulative ROI chart."""
    return pd.DataFrame({'Month': range(1, 13), 'Cumulative Value ($k)': [-50, -40, -30, -15, 5, 25, 45, 65, 85, 105, 125, 145]})

def get_vendor_scorecards():
    """Simulates performance data for key technology vendors."""
    return {"Agilent Technologies": {"annual_spend_k": 850, "performance_score": 88, "incidents": 12}, "Illumina": {"annual_spend_k": 1200, "performance_score": 95, "incidents": 5}, "Hamilton": {"annual_spend_k": 400, "performance_score": 92, "incidents": 8}}

# --- CORRECTED FUNCTION (Bug fix maintained) ---
def get_assay_impact_data():
    """Simulates data for the instrument-to-assay Sankey diagram."""
    return {
        'sources': [0, 1, 1, 2, 3, 4, 5, 6],
        'targets': [3, 4, 5, 6, 6, 7, 7, 7],
        'values':  [10, 5, 5, 8, 10, 5, 8, 2],
        'labels': ["HPLC-007 (OK)", "NGS-002 (OOS)", "MassSpec-001 (OK)", "Assay A", "Assay B", "Assay C", "Project 'VT-101'", "Project 'VT-205'"],
        'colors': ["green", "red", "green", "blue", "blue", "blue", "purple", "purple"]
    }

def get_reagent_genealogy_data(reagent_lot_id):
    """Generates a Graphviz chart object for the reagent genealogy."""
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
    """Simulates the journey of a single clinical sample."""
    return pd.DataFrame({'Step': [1, 2, 3, 4, 5], 'Action': ['Sample Received', 'Prep & Aliquoting', 'PCR Amplification', 'Data Analysis', 'Result Certified'], 'System/Instrument': ['LIMS Entry Station', 'Hamilton-03 (SD)', 'QuantStudio-08 (SD)', 'Pipeline Server v2.1', 'LIMS Reporting Module'], 'Timestamp': pd.to_datetime(['2024-05-20 09:00', '2024-05-20 11:30', '2024-05-20 14:00', '2024-05-20 18:00', '2024-05-21 10:00']), 'Status': ['OK', 'OK', 'OK', 'OK', 'OK']})

# These functions are placeholders for completeness, not actively used in the refined UI
def get_strategic_alignment_data(): return pd.DataFrame()
def get_asset_inventory_data(): return pd.DataFrame()
def get_tech_radar_data(): return pd.DataFrame()
def get_audit_readiness_data(): return pd.DataFrame()
def get_voice_of_scientist_data(): return {}
def get_ai_briefing(a, k): return ""
def get_ai_root_cause(p): return ""
def get_capital_asset_model_data(): return pd.DataFrame()
def generate_gxp_document(s, d): return ""
def generate_capex_proposal(a): return ""
def run_mitigation_simulation(s): return {}
def run_strategic_financial_model(q): return {}
def run_what_if_scenario(q): return "No critical project dependencies found for this scenario."
