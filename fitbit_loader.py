```python
import pandas as pd
import os

class FitbitLoader:

    def __init__(self, data_path):

        self.data_path = data_path

        self.daily = None
        self.sleep = None
        self.heart_rate = None

    def load_all(self):

        try:

            daily_path = os.path.join(
                self.data_path,
                "dailyActivity_merged.csv"
            )

            sleep_path = os.path.join(
                self.data_path,
                "minuteSleep_merged.csv"
            )

            hr_path = os.path.join(
                self.data_path,
                "heartrate_seconds_merged.csv"
            )

            self.daily = pd.read_csv(
                daily_path,
                encoding_errors="ignore"
            )

            self.sleep = pd.read_csv(
                sleep_path,
                encoding_errors="ignore"
            )

            self.heart_rate = pd.read_csv(
                hr_path,
                encoding_errors="ignore"
            )

            return True

        except Exception as e:

            import streamlit as st

            st.error(f"REAL ERROR: {e}")

            return False

    def get_daily(self):

        return self.daily

    def get_sleep(self):

        return self.sleep

    def get_heart_rate(self):

        return self.heart_rate
```
