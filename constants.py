"""
CONSTANTS FILE - All global variables
"""
# Risk thresholds
RISK_CRITICAL = 0.8
RISK_HIGH = 0.6
RISK_MODERATE = 0.4
RISK_LOW = 0.2

# Health thresholds
NORMAL_HR_MAX = 90
NORMAL_SLEEP_MIN = 5
NORMAL_STEPS_MIN = 3000
SEDENTARY_LIMIT = 800

# ML parameters
XGBOOST_ESTIMATORS = 100
XGBOOST_MAX_DEPTH = 4
ISOLATION_FOREST_CONTAMINATION = 0.1

# Feature columns
FEATURE_COLUMNS = [
    'heart_rate', 'sleep_hours', 'steps',
    'hr_rolling_3', 'sleep_rolling_3', 'steps_rolling_3',
    'hr_daily_change', 'sleep_daily_change', 'steps_daily_change',
    'hr_variability_3', 'active_ratio', 'sedentary', 'calories'
]

# Database path
DATABASE_PATH = "health_ai.db"
DATA_FOLDER = "data/"
