
"""
FEATURE ENGINEERING - Create time-series features
"""

import pandas as pd

class FeatureEngine:
    def __init__(self, dataframe):
        self.df = dataframe
        self.feature_cols = None
    
    def create_features(self):
        """Create all time-series features"""

        df = self.df.copy()

        df.columns = df.columns.str.strip()

        # Ensure user_id exists
        if 'user_id' not in df.columns:
            df['user_id'] = 1

        # Ensure date exists
        if 'date' not in df.columns:

            possible_date_cols = [
                'SleepDay',
                'sleep_day',
                'ActivityDate',
                'Date'
            ]

            found = False

            for col in possible_date_cols:
                if col in df.columns:
                    df['date'] = pd.to_datetime(df[col])
                    found = True
                    break

            if not found:
                df['date'] = pd.date_range(
                    start='2024-01-01',
                    periods=len(df),
                    freq='D'
                )

        # Ensure required columns exist
        required_cols = {
            'heart_rate': 70,
            'sleep_hours': 7,
            'steps': 5000,
            'very_active': 30,
            'fairly_active': 20,
            'sedentary': 600,
            'calories': 2000
        }

        for col, default in required_cols.items():
            if col not in df.columns:
                df[col] = default

        df = df.sort_values(['user_id', 'date']).copy()

        processed = []

        for user_id in df['user_id'].unique():

            user_data = df[df['user_id'] == user_id].copy()

            # Rolling averages
            user_data['hr_rolling_3'] = (
                user_data['heart_rate']
                .rolling(3, min_periods=1)
                .mean()
            )

            user_data['sleep_rolling_3'] = (
                user_data['sleep_hours']
                .rolling(3, min_periods=1)
                .mean()
            )

            user_data['steps_rolling_3'] = (
                user_data['steps']
                .rolling(3, min_periods=1)
                .mean()
            )

            # Daily changes
            user_data['hr_daily_change'] = (
                user_data['heart_rate']
                .diff()
                .fillna(0)
            )

            user_data['sleep_daily_change'] = (
                user_data['sleep_hours']
                .diff()
                .fillna(0)
            )

            user_data['steps_daily_change'] = (
                user_data['steps']
                .diff()
                .fillna(0)
            )

            # HR variability
            user_data['hr_variability_3'] = (
                user_data['heart_rate']
                .rolling(3, min_periods=1)
                .std()
                .fillna(0)
            )

            # Activity ratio
            user_data['active_ratio'] = (
                user_data['very_active'] +
                user_data['fairly_active']
            ) / (user_data['sedentary'] + 1)

            processed.append(user_data)

        result = pd.concat(processed, ignore_index=True)

        self.feature_cols = [
            'heart_rate',
            'sleep_hours',
            'steps',
            'hr_rolling_3',
            'sleep_rolling_3',
            'steps_rolling_3',
            'hr_daily_change',
            'sleep_daily_change',
            'steps_daily_change',
            'hr_variability_3',
            'active_ratio',
            'sedentary',
            'calories'
        ]

        return result

    def get_feature_columns(self):
        return self.feature_cols
