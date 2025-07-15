# utils.py

import pandas as pd
import numpy as np
from datetime import date, timedelta

# --- Existing Functions for Original Dashboard ---

def get_strategic_alignment_data():
    """Simulates data for the strategic alignment radar chart."""
    data = {
        'Strategy Pillar': [
            'Accelerate Discovery (Speed)', 'Ensure GxP Compliance', 
            'Enable New Modalities (C>)', 'Drive Operational Efficiency', 
            'Enhance Data Integrity'
        ],
        'DTE Focus Score': [8, 9, 7, 8, 9.5]
    }
    return pd.DataFrame(data)

def get_project_portfolio_data():
    """Simulates data for the project portfolio bubble chart."""
    data = {
        'Project': [
            'SD Lab Build-out Phase II', 'LIMS Upgrade', 'NGS Data Pipeline Automation',
            'Cryo-EM Data Storage Expansion', 'Lab Computer Refresh Q3', 'AR/VR Support Pilot'
        ],
        'Strategic Impact Score': [9, 8, 9, 8, 6, 7],
        'Effort (Person-Weeks)': [150, 80, 60, 120, 40, 25],
        'Budget ($k)': [2000, 750, 300, 1500, 500, 80],
        'Strategic Theme': ['New Modalities', 'Compliance', 'Efficiency', 'Discovery', 'Operations', 'Innovation']
    }
    return pd.DataFrame(data)

def get_itsm_ticket_data():
    """Simulates ITSM ticket data from a system like ServiceNow."""
    today = date.today()
    dates = [today - timedelta(days=i) for i in range(30)]
    dates.reverse()
    
    data = {
        'Ticket ID': [f'INC{12345+i}' for i in range(50)] + [f'REQ{54321+i}' for i in range(50)],
        'Date': np.random.choice(dates, 100),
        'Site': np.random.choice(['San Diego', 'Seattle'], 100),
        'Category': np.random.choice([
            'Instrument Connectivity', 'Software Login', 'Data Access', 'Printer Issue',
            'New Software Request', 'Performance Lag', 'Hardware Failure'
        ], 100, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.1, 0.05]),
        'Priority': np.random.choice(['P1 - Critical', 'P2 - High', 'P3 - Medium', 'P4 - Low'], 100, p=[0.05, 0.15, 0.5, 0.3]),
        'Status': np.random.choice(['Open', 'Closed', 'In Progress'], 100, p=[0.1, 0.8, 0.1]),
        'SLA Met': np.random.choice([True, False], 100, p=[0.9, 0.1]),
        'Type': ['Incident']*50 + ['Request']*50
    }
    tickets_df = pd.DataFrame(data).sort_values(by='Date')
    
    # Simulate ticket counts and MTTR for the trend chart
    ticket_counts = tickets_df.groupby('Date').size().reset_index(name='Ticket Count')
    mttr_data = pd.Series(np.random.uniform(2, 8, size=len(ticket_counts)), name="MTTR")
    
    return tickets_df, mttr_data


def get_asset_inventory_data():
    """Simulates asset data from a Configuration Management Database (CMDB)."""
    data = {
        'Asset ID': [f'VRTX-SD-HPLC-{i:03d}' for i in range(1, 11)] + [f'VRTX-SEA-NGS-{i:03d}' for i in range(1, 6)],
        'Asset Name': [f'Agilent HPLC {i}' for i in range(1, 11)] + [f'Illumina NovaSeq {i}' for i in range(1, 6)],
        'Site': ['San Diego']*10 + ['Seattle']*5,
        'Lab': [f'Lab {np.random.choice(["1A", "2B", "3C"])}' for _ in range(15)],
        'OS': ['Windows 10']*12 + ['Windows 7']*2 + ['Linux']*1,
        'OS Support Status': ['Supported']*12 + ['Unsupported']*2 + ['Supported']*1,
        'Warranty Status': ['Active']*10 + ['Expiring Soon']*3 + ['Expired']*2,
        'Validation Status': ['Validated']*13 + ['Overdue']*1 + ['N/A']*1,
        'Lifecycle Status': ['In Production']*14 + ['Pending Retirement']*1,
        'Last User': [f'user{np.random.randint(1,20)}' for _ in range(15)]
    }
    return pd.DataFrame(data)

def get_tech_radar_data():
    """Simulates data for the technology radar."""
    data = {
        'Technology': ['IoT Sensors', 'AI-driven Analytics', 'Cloud Collaboration', 'AR/VR Lab Support', 'Lab Voice Assistants', 'Robotic Process Automation (RPA)', 'Legacy LIMS'],
        'Quadrant': ['Platforms', 'Techniques', 'Tools', 'Tools', 'Platforms', 'Techniques', 'Platforms'],
        'r': [3.5, 2.5, 1.5, 2.8, 3.2, 1.8, 4.5], # Distance from center (1=Adopt, 2=Trial, 3=Assess, 4=Hold)
        'theta': [45, 120, 210, 300, 60, 150, 270],
        'Details': [
            'Real-time monitoring of freezer temps and lab conditions.',
            'Using ML models for predictive maintenance on instruments.',
            'Using platforms like Benchling for cross-site experiment planning.',
            'Using HoloLens for remote expert support during instrument repair.',
            'Voice-to-text entry for ELNs to improve hands-free operation.',
            'Automating routine data transfer between non-integrated systems.',
            'Phasing out older, on-premise LIMS in favor of modern cloud solutions.'
        ]
    }
    return pd.DataFrame(data)

def get_vmp_tracker_data():
    """Simulates data for the Validation Master Plan Gantt chart."""
    data = {
        'System/Instrument': [
            'New LIMS v2.0', 'New LIMS v2.0', 'New LIMS v2.0',
            'SD HPLC #11', 'SD HPLC #11', 'SEA NGS #06', 'SEA NGS #06'
        ],
        'Start': [
            date(2024, 5, 1), date(2024, 6, 15), date(2024, 8, 1),
            date(2024, 5, 20), date(2024, 6, 5), date(2024, 7, 1), date(2024, 7, 15)
        ],
        'Finish': [
            date(2024, 6, 14), date(2024, 7, 30), date(2024, 8, 15),
            date(2024, 6, 4), date(2024, 6, 15), date(2024, 7, 14), date(2024, 8, 1)
        ],
        'Phase': ['Validation Plan', 'IQ/OQ Execution', 'PQ & Go-Live', 'IQ', 'OQ', 'IQ', 'OQ/PQ'],
        'Validation Lead': ['J. Doe', 'J. Doe', 'J. Doe', 'A. Smith', 'A. Smith', 'L. Chen', 'L. Chen']
    }
    return pd.DataFrame(data)

def get_audit_readiness_data():
    """Simulates data for the audit readiness checklist."""
    data = {
        'Audit Area': [
            'Change Control Procedures', 'System Access & Security Logs', '21 CFR Part 11 Controls',
            'Data Backup and Recovery', 'Disaster Recovery Plan', 'Personnel Training Records', 'SOPs for GxP Systems'
        ],
        'Status': ['Ready', 'Ready', 'Needs Review', 'Ready', 'Gap Identified', 'Ready', 'Ready'],
        'Last Reviewed': [
            date(2024, 4, 15), date(2024, 5, 1), date(2023, 11, 10),
            date(2024, 3, 22), date(2023, 1, 15), date(2024, 5, 5), date(2024, 4, 30)
        ],
        'Owner': ['A. Smith', 'L. Chen', 'A. Smith', 'L. Chen', 'AD Lead', 'J. Doe', 'A. Smith']
    }
    return pd.DataFrame(data)

# ==============================================================================
# --- NEW: Functions to support the "10+" extended features ---
# ==============================================================================

def get_voice_of_scientist_data():
    """Simulates word frequency data from analyzing ServiceNow tickets and user surveys."""
    # In a real scenario, this would be the output of an NLP model.
    return {
        "WIFI": 25, "SLOW": 22, "PRINTER": 20, "LOGIN": 18, "CONNECTIVITY": 15,
        "CRASH": 12, "DATA_TRANSFER": 10, "HPLC": 9, "ERROR": 8, "ACCESS": 7
    }

def get_ai_briefing(audience, kpis):
    """Simulates an LLM generating a tailored briefing."""
    if audience == "Site Leadership (SD)":
        return f"Team, this week DTE maintained exceptional lab system uptime of {kpis['uptime']}. Our key focus is supporting the new Cell Therapy lab build-out, which is currently on track. We are also addressing a minor increase in project delays (-5%) by reallocating resources to the LIMS upgrade project. Overall, the technology environment is stable and aligned with site goals."
    elif audience == "Global DTE Leadership":
        return f"Update from West Coast: Operational KPIs are strong with uptime at {kpis['uptime']} and P1 MTTR at {kpis['mttr']}. We are seeing a slight dip in project schedule adherence (85%), primarily due to vendor delays on the LIMS project. We are tracking one overdue GxP validation which is scheduled for remediation next week. All core services are meeting global standards."
    else: # Lab Scientists
        return f"Hi Team, just a quick update from DTE. We're happy to report that lab system stability remains high ({kpis['uptime']} uptime). We have a few new 'how-to' guides for the upgraded LIMS on the intranet, and we're planning a lunch-and-learn on advanced data analysis tools next month. As always, please continue to submit tickets for any issues you encounter."

def get_ai_root_cause(problem_description):
    """Simulates an AI co-pilot diagnosing an issue by correlating data from different systems."""
    if "hplc" in problem_description.lower() and "offline" in problem_description.lower():
        return "Correlated data shows a network switch (SW-4C-01) in Lab 4C-SD is reporting high packet loss. This is the most likely root cause. Recommend dispatching network engineer to investigate the switch before troubleshooting individual HPLCs."
    return "No obvious correlations found in system logs. Recommend standard troubleshooting starting with checking physical connections and restarting the affected instrument."
    
def get_vendor_scorecards():
    """Simulates performance data for key technology vendors."""
    return {
        "Agilent Technologies (HPLCs)": {
            "sla_compliance": 98.5, "sla_delta": 1.5,
            "mttr": 8.2, "mttr_delta": -1.1,
            "mtbf": 120, "qbr_status": "Scheduled"
        },
        "Illumina (Sequencers)": {
            "sla_compliance": 99.8, "sla_delta": 0.2,
            "mttr": 4.5, "mttr_delta": 0.3,
            "mtbf": 250, "qbr_status": "Completed"
        },
        "Waters Corporation (Mass Spec)": {
            "sla_compliance": 95.2, "sla_delta": -2.8,
            "mttr": 12.1, "mttr_delta": 2.5,
            "mtbf": 85, "qbr_status": "Needs Scheduling"
        }
    }

def get_team_performance():
    """Simulates data for the team skills matrix and identified gaps."""
    team_data = {
        "Team Member": ["J. Doe (SD)", "A. Smith (SD)", "L. Chen (SEA)", "M. Patel (Partner)"],
        "Role": ["Sr. Specialist", "Specialist", "Sr. Specialist", "Support Tech"],
        "Core ITIL": ["Expert", "Advanced", "Expert", "Advanced"],
        "Windows GxP": ["Expert", "Advanced", "Advanced", "Intermediate"],
        "Linux/HPC": ["Intermediate", "Beginner", "Advanced", "Beginner"],
        "Network Troubleshooting": ["Advanced", "Intermediate", "Expert", "Intermediate"],
        "Automation (Python)": ["Intermediate", "Beginner", "Beginner", "Beginner"],
        "CSV/Validation": ["Advanced", "Intermediate", "Advanced", "Beginner"]
    }
    team_df = pd.DataFrame(team_data)
    
    skills_gap = {
        "gap": "Team proficiency in Automation (Python/Scripting) is low.",
        "recommendation": "Identify 1-2 team members for advanced Python training to support lab automation goals."
    }
    return team_df, skills_gap

def get_global_kpis():
    """Simulates benchmark data comparing West Coast to Global DTE performance."""
    data = {
        "KPI": ["System Uptime", "P1 Incident MTTR (h)", "User Satisfaction (CSAT)"],
        "West Coast": [99.8, 3.8, 4.6],
        "Global Avg": [99.7, 4.5, 4.4],
        "unit": ["%", "", "/5"]
    }
    return pd.DataFrame(data)
