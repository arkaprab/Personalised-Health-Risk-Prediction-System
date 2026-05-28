"""
FITBIT DATA LOADER - Loads CSV files
"""

import pandas as pd
import os


class FitbitLoader:
    def __init__(self, data_path="data/"):
        self.data_path = data_path
        self.daily = None
        self.sleep = None
        self.heart_rate = None
    
    def load_all(self):
        """Load all Fitbit CSV files"""
        
        print("📊 Loading Fitbit data...")
        
        # Load daily activity
        daily_path = os.path.join(self.data_path, "dailyActivity_merged.csv")
        if os.path.exists(daily_path):
            self.daily = pd.read_csv(daily_path)
            print(f"✅ Daily activity: {len(self.daily)} records")
        else:
            print(f"❌ File not found: {daily_path}")
            return False
        
        
        # Load sleep
        sleep_path = os.path.join(self.data_path, "minuteSleep_merged.csv")
        if os.path.exists(sleep_path):
            self.sleep = pd.read_csv(sleep_path)
            print(f"✅ Sleep data: {len(self.sleep)} records")
        
        # Load heart rate
        hr_path = os.path.join(self.data_path, "heartrate_seconds_merged.csv")
        if os.path.exists(hr_path):
            self.heart_rate = pd.read_csv(hr_path)
            print(f"✅ Heart rate: {len(self.heart_rate)} records")
        
        return True
    
    def get_daily(self):
        return self.daily
    
    def get_sleep(self):
        return self.sleep
    
    def get_heart_rate(self):
        return self.heart_rate