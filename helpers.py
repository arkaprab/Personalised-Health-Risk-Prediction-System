"""
HELPER FUNCTIONS - Utilities
"""

import pandas as pd

def get_sample_format():
    """Return sample CSV format"""
    return pd.DataFrame({
        'date': ['2026-04-10', '2026-04-11', '2026-04-12'],
        'heart_rate': [72, 75, 80],
        'sleep_hours': [7.5, 7.0, 6.5],
        'activity': [8000, 7500, 6000],
    })

def format_percentage(value):
    return f"{value * 100:.1f}%"

def get_risk_color(risk):
    if risk > 0.6:
        return "#e74c3c"  # Red
    elif risk > 0.4:
        return "#f39c12"  # Orange
    else:
        return "#2ecc71"  # Green
