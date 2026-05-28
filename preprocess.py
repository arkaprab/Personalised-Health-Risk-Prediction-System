
import pandas as pd

class DataPreprocessor:
    def __init__(self, daily_df, sleep_df, heart_df):
        self.daily_df = daily_df.copy() if daily_df is not None else pd.DataFrame()
        self.sleep_df = sleep_df.copy() if sleep_df is not None else pd.DataFrame()
        self.heart_df = heart_df.copy() if heart_df is not None else pd.DataFrame()

    def preprocess(self):

        # --- Daily Activity ---
        daily = self.daily_df.copy()
        daily.columns = daily.columns.str.strip()

        # Standardise user id column
        if 'Id' in daily.columns:
            daily = daily.rename(columns={'Id': 'user_id'})

        # Standardise date column
        if 'ActivityDate' in daily.columns:
            daily['date'] = pd.to_datetime(daily['ActivityDate'], errors='coerce')
        elif 'date' in daily.columns:
            daily['date'] = pd.to_datetime(daily['date'], errors='coerce')

        # Rename activity columns to standard names
        rename_map = {
            'TotalSteps': 'steps',
            'Calories': 'calories',
            'VeryActiveMinutes': 'very_active',
            'FairlyActiveMinutes': 'fairly_active',
            'SedentaryMinutes': 'sedentary',
        }
        daily = daily.rename(columns={k: v for k, v in rename_map.items() if k in daily.columns})

        daily = daily.dropna(subset=['date'])

        # --- Sleep Data (minuteSleep) - aggregate to daily sleep_hours ---
        sleep_daily = None
        if not self.sleep_df.empty:
            sleep = self.sleep_df.copy()
            sleep.columns = sleep.columns.str.strip()

            if 'Id' in sleep.columns:
                sleep = sleep.rename(columns={'Id': 'user_id'})

            # Parse datetime column
            date_col = None
            for c in ['date', 'Date', 'SleepDay', 'sleep_day']:
                if c in sleep.columns:
                    date_col = c
                    break
            if date_col:
                sleep['date'] = pd.to_datetime(sleep[date_col], errors='coerce').dt.date
                sleep['date'] = pd.to_datetime(sleep['date'])
                # Each row is one minute; count minutes per user per day → convert to hours
                sleep_daily = (
                    sleep.groupby(['user_id', 'date'])
                    .size()
                    .reset_index(name='sleep_minutes')
                )
                sleep_daily['sleep_hours'] = sleep_daily['sleep_minutes'] / 60.0
                sleep_daily = sleep_daily[['user_id', 'date', 'sleep_hours']]

        # --- Heart Rate (second-level) - aggregate to daily mean ---
        hr_daily = None
        if not self.heart_df.empty:
            hr = self.heart_df.copy()
            hr.columns = hr.columns.str.strip()

            if 'Id' in hr.columns:
                hr = hr.rename(columns={'Id': 'user_id'})

            date_col = None
            for c in ['Time', 'time', 'date', 'Date']:
                if c in hr.columns:
                    date_col = c
                    break

            value_col = None
            for c in ['Value', 'value', 'heart_rate']:
                if c in hr.columns:
                    value_col = c
                    break

            if date_col and value_col:
                hr['date'] = pd.to_datetime(hr[date_col], errors='coerce').dt.date
                hr['date'] = pd.to_datetime(hr['date'])
                hr_daily = (
                    hr.groupby(['user_id', 'date'])[value_col]
                    .mean()
                    .reset_index()
                    .rename(columns={value_col: 'heart_rate'})
                )

        # --- Merge all on user_id + date ---
        merged = daily[['user_id', 'date'] + [c for c in ['steps', 'calories', 'very_active', 'fairly_active', 'sedentary'] if c in daily.columns]].copy()

        if sleep_daily is not None:
            merged = pd.merge(merged, sleep_daily, on=['user_id', 'date'], how='left')
        else:
            merged['sleep_hours'] = 7.0  # default fallback

        if hr_daily is not None:
            merged = pd.merge(merged, hr_daily, on=['user_id', 'date'], how='left')
        else:
            merged['heart_rate'] = 70.0  # default fallback

        # Fill remaining NaNs with sensible defaults
        defaults = {
            'heart_rate': 70,
            'sleep_hours': 7,
            'steps': 5000,
            'calories': 2000,
            'very_active': 30,
            'fairly_active': 20,
            'sedentary': 600,
        }
        for col, val in defaults.items():
            if col not in merged.columns:
                merged[col] = val
            else:
                merged[col] = merged[col].fillna(val)

        merged = merged.dropna(subset=['user_id', 'date'])
        merged = merged.reset_index(drop=True)

        return merged
