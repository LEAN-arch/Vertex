# utils.py

import pandas as pd
import numpy as np
from datetime import date, timedelta

# ==============================================================================
# --- Base Data Simulation Functions ---
# ==============================================================================

def get_strategic_alignment_data():
    """Simulates data for the strategic alignment radar chart."""
    data = { 'Strategy Pillar': ['Accelerate Discovery (Speed)', 'Ensure GxP Compliance', 'Enable New Modalities (C>)', 'Drive Operational Efficiency', 'Enhance Data Integrity'], 'DTE Focus Score': [8, 9, 7, 8, 9.5] }
    return pd.DataFrame(data)

def get_project_portfolio_data():
    """Simulates the base data for the project portfolio."""
    data = {
        'Project': ['SD Lab Build-out Phase II', 'LIMS Upgrade', 'NGS Data Pipeline Automation', 'Cryo-EM Data Storage Expansion', 'Lab Computer Refresh Q3', 'AR/VR Support Pilot'],
        'Strategic Impact Score': [9.5, 8, 9, 8.5, 6, 7],
        'Effort (Person-Weeks)': [150, 80, 60, 120, 40, 25],
        'Budget ($k)': [2000, 750, 300, 1500, 500, 80],
        'Strategic Theme': ['New Modalities', 'Compliance', 'Efficiency', 'Discovery', 'Operations', 'Innovation'],
        'Status': ['On Track', 'At Risk', 'On Track', 'On Track', 'Completed', 'On Track'],
        'Planned Finish': pd.to_datetime(['2024-12-15', '2024-07-30', '2024-09-01', '2024-11-01', '2024-05-30', '2024-08-20'])
    }
    return pd.DataFrame(data)

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
    mttr_data = pd.Series(base_mttr, index=dates).reindex(tickets_df['Date'].unique(), method='pad')
    return tickets_df, mttr_data

def get_asset_inventory_data():
    """Simulates asset data from a Configuration Management Database (CMDB)."""
    return pd.DataFrame({'Asset ID': [f'VRTX-SD-HPLC-{i:03d}' for i in range(1, 11)] + [f'VRTX-SEA-NGS-{i:03d}' for i in range(1, 6)], 'Asset Name': [f'Agilent HPLC {i}' for i in range(1, 11)] + [f'Illumina NovaSeq {i}' for i in range(1, 6)], 'OS Support Status': ['Supported']*12 + ['Unsupported']*2 + ['Supported']*1, 'Warranty Status': ['Active']*10 + ['Expiring Soon']*3 + ['Expired']*2, 'Validation Status': ['Validated']*13 + ['Overdue']*1 + ['N/A']*1})

def get_tech_radar_data():
    """Simulates data for the technology radar."""
    return pd.DataFrame({'Technology': ['IoT Sensors', 'AI-driven Analytics', 'Cloud Collaboration', 'AR/VR Lab Support', 'Lab Voice Assistants', 'Robotic Process Automation (RPA)', 'Legacy LIMS'], 'Quadrant': ['Platforms', 'Techniques', 'Tools', 'Tools', 'Platforms', 'Techniques', 'Platforms'], 'r': [3.5, 2.5, 1.5, 2.8, 3.2, 1.8, 4.5], 'theta': [45, 120, 210, 300, 60, 150, 270], 'Details': ['Real-time monitoring of freezer temps and lab conditions.', 'Using ML models for predictive maintenance on instruments.', 'Using platforms like Benchling for cross-site experiment planning.', 'Using HoloLens for remote expert support during instrument repair.', 'Voice-to-text entry for ELNs to improve hands-free operation.', 'Automating routine data transfer between non-integrated systems.', 'Phasing out older, on-premise LIMS in favor of modern cloud solutions.']})

def get_vmp_tracker_data():
    """Simulates data for the Validation Master Plan Gantt chart."""
    return pd.DataFrame({'System/Instrument': [ 'New LIMS v2.0', 'New LIMS v2.0', 'New LIMS v2.0', 'SD HPLC #11', 'SD HPLC #11', 'SEA NGS #06', 'SEA NGS #06' ], 'Start': pd.to_datetime([ '2024-05-01', '2024-06-15', '2024-08-01', '2024-05-20', '2024-06-05', '2024-07-01', '2024-07-15' ]), 'Finish': pd.to_datetime([ '2024-06-14', '2024-07-30', '2024-08-15', '2024-06-04', '2024-06-15', '2024-07-14', '2024-08-01' ]), 'Phase': ['Validation Plan', 'IQ/OQ Execution', 'PQ & Go-Live', 'IQ', 'OQ', 'IQ', 'OQ/PQ'], 'Status': ['Completed', 'At Risk', 'On Track', 'Completed', 'Completed', 'On Track', 'On Track'], 'Validation Lead': ['J. Doe', 'J. Doe', 'J. Doe', 'A. Smith', 'A. Smith', 'L. Chen', 'L. Chen']})

def get_audit_readiness_data():
    """Simulates data for the audit readiness checklist."""
    return pd.DataFrame({'Audit Area': [ 'Change Control Procedures', 'System Access & Security Logs', '21 CFR Part 11 Controls', 'Data Backup and Recovery', 'Disaster Recovery Plan', 'Personnel Training Records', 'SOPs for GxP Systems' ], 'Status': ['Ready', 'Ready', 'Needs Review', 'Ready', 'Gap Identified', 'Ready', 'Ready'], 'Last Reviewed': [ date(2024, 4, 15), date(2024, 5, 1), date(2023, 11, 10), date(2024, 3, 22), date(2023, 1, 15), date(2024, 5, 5), date(2024, 4, 30) ], 'Owner': ['A. Smith', 'L. Chen', 'A. Smith', 'L. Chen', 'AD Lead', 'J. Doe', 'A. Smith']})

def get_voice_of_scientist_data():
    """Simulates word frequency data from analyzing ServiceNow tickets and user surveys."""
    return {"WIFI": 25, "SLOW": 22, "PRINTER": 20, "LOGIN": 18, "CONNECTIVITY": 15, "CRASH": 12, "DATA_TRANSFER": 10, "HPLC": 9, "ERROR": 8, "ACCESS": 7}

def get_ai_briefing(audience, kpis):
    """Simulates an LLM generating a tailored briefing."""
    if audience == "Site Leadership (SD)": return f"Team, this week DTE maintained exceptional lab system uptime of {kpis['uptime']}. Our key focus is supporting the new Cell Therapy lab build-out, which is currently on track. We are also addressing a minor increase in project delays (-5%) by reallocating resources to the LIMS upgrade project. Overall, the technology environment is stable and aligned with site goals."
    else: return f"Hi Team, just a quick update from DTE. We're happy to report that lab system stability remains high ({kpis['uptime']} uptime). We have a few new 'how-to' guides for the upgraded LIMS on the intranet, and we're planning a lunch-and-learn on advanced data analysis tools next month. As always, please continue to submit tickets for any issues you encounter."

def get_vendor_scorecards():
    """Simulates performance data for key technology vendors."""
    return {"Agilent Technologies (HPLCs)": {"sla_compliance": 98.5, "sla_delta": 1.5, "mttr": 8.2, "mttr_delta": -1.1, "mtbf": 120, "qbr_status": "Scheduled"}, "Illumina (Sequencers)": {"sla_compliance": 99.8, "sla_delta": 0.2, "mttr": 4.5, "mttr_delta": 0.3, "mtbf": 250, "qbr_status": "Completed"}, "Waters Corporation (Mass Spec)": {"sla_compliance": 95.2, "sla_delta": -2.8, "mttr": 12.1, "mttr_delta": 2.5, "mtbf": 85, "qbr_status": "Needs Scheduling"}}

def get_team_performance():
    """Simulates data for the team skills matrix and identified gaps."""
    team_data = {"Team Member": ["J. Doe (SD)", "A. Smith (SD)", "L. Chen (SEA)", "M. Patel (Partner)"], "Role": ["Sr. Specialist", "Specialist", "Sr. Specialist", "Support Tech"], "Core ITIL": ["Expert", "Advanced", "Expert", "Advanced"], "Windows GxP": ["Expert", "Advanced", "Advanced", "Intermediate"], "Linux/HPC": ["Intermediate", "Beginner", "Advanced", "Beginner"], "Network Troubleshooting": ["Advanced", "Intermediate", "Expert", "Intermediate"], "Automation (Python)": ["Intermediate", "Beginner", "Beginner", "Beginner"], "CSV/Validation": ["Advanced", "Intermediate", "Advanced", "Beginner"]}
    skills_gap = {"gap": "Team proficiency in Automation (Python/Scripting) is low.", "recommendation": "Identify 1-2 team members for advanced Python training to support lab automation goals."}
    return pd.DataFrame(team_data), skills_gap

def get_global_kpis():
    """Simulates benchmark data comparing West Coast to Global DTE performance."""
    return pd.DataFrame({"KPI": ["System Uptime", "P1 Incident MTTR (h)", "User Satisfaction (CSAT)"], "West Coast": [99.8, 3.8, 4.6], "Global Avg": [99.7, 4.5, 4.4], "unit": ["%", "", "/5"]})

def get_predictive_maintenance_data():
    """Simulates output from the Predictive Instrument Failure ML model, now with a prescriptive fix."""
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

# ==============================================================================
# --- NEW: Functions to power the "10++" Generative & Autonomous Features ---
# ==============================================================================

def generate_gxp_document(system_name, doc_type):
    """Simulates a GAMP 5-trained LLM generating a GxP document draft."""
    header = f"## Draft: {doc_type} for {system_name}\n**Document ID:** VP-DTE-WST-{doc_type.replace(' ', '')}-001\n**Status:** DRAFT\n**Author:** DTE Orchestration Engine\n\n"
    
    if doc_type == "Validation Plan (VP)":
        return header + """
### 1.0 Introduction
This document outlines the validation strategy for the {system_name} system to ensure it is fit for its intended use and complies with Vertex policies and 21 CFR Part 11.

### 2.0 Scope
The scope of this validation includes the qualification of the hardware, software, and procedures associated with the {system_name}.

### 3.0 Validation Approach (GAMP 5 Category 4)
A risk-based approach will be followed, including IQ, OQ, and PQ testing.

### 4.0 Test Strategy
Test cases will be developed to verify user requirements and functional specifications. All testing will be documented in approved protocols.
"""
    elif doc_type == "Installation Qualification (IQ)":
        return header + """
### 1.0 Purpose
To verify that the {system_name} and its components have been installed correctly according to vendor specifications and Vertex design documents.

### 2.0 Test Cases
| Step | Procedure | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|
| 1.1 | Verify physical installation and connections. | All components present and correctly connected. | | |
| 1.2 | Confirm software version matches specification. | Software version is 3.1.4. | | |
| 1.3 | Verify GxP security settings are enabled. | Access controls and audit trails are active. | | |
"""
    else:
        return header + f"Content for the {doc_type} will be generated here based on the system's User Requirement Specification and GAMP 5 category."

def generate_capex_proposal(asset_details):
    """Simulates a fine-tuned LLM generating a full CapEx proposal from model data."""
    return f"""
## Capital Expenditure Request: Replacement of {asset_details['Asset ID']}

**1. Executive Summary:**
This proposal requests ${asset_details['Total Cost of Ownership ($)'] * 1.5 / 1000:,.1f}k in capital funding to replace the existing {asset_details['Asset Age (Yrs)']}-year-old {asset_details['Asset Type']} ({asset_details['Asset ID']}). The current asset has a high Total Cost of Ownership (${asset_details['Total Cost of Ownership ($)']}) and is critical to our discovery pipeline (Scientific Need Score: {asset_details['Scientific Need Score']}/10). This investment will mitigate significant operational risk and directly support Vertex's strategic goals in [Relevant Scientific Area].

**2. Problem Statement & Risk Analysis:**
The current asset is experiencing escalating maintenance costs and reliability issues, leading to potential delays in critical GxP data generation. The risk of an unrecoverable, multi-week failure in the next 12 months is estimated at 40%. Failure would directly impact [Project A, Project B].

**3. Proposed Solution:**
We propose replacing the unit with the [New Vendor/Model], which offers a 3x increase in throughput and enhanced data integrity features compliant with 21 CFR Part 11.

**4. Financial Analysis:**
- Estimated Cost: ${asset_details['Total Cost of Ownership ($)'] * 1.5 / 1000:,.1f}k
- Estimated ROI (from increased efficiency & risk mitigation): 25% over 3 years.

**5. Strategic Alignment:**
This investment directly supports our strategic pillar of 'Accelerate Discovery' by providing a more robust and efficient platform for our scientists.
"""

def run_mitigation_simulation(scenario):
    """Simulates a Monte Carlo analysis for different project mitigation scenarios."""
    if "Engineer" in scenario:
        return {"new_finish_date": "2024-08-10", "budget_impact": 25, "success_prob": 75}
    elif "Overtime" in scenario:
        return {"new_finish_date": "2024-08-20", "budget_impact": 15, "success_prob": 60}
    else: # De-scope
        return {"new_finish_date": "2024-07-28", "budget_impact": 0, "success_prob": 95}
