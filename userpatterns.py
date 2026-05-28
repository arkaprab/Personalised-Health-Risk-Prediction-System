"""
BASELINE ENGINE - Learn user's normal patterns
"""

class BaselineEngine:
    def __init__(self):
        self.baselines = {}
    
    def compute_baseline(self, user_data, user_id):
        """Compute baseline from first 5 days"""
        
        if len(user_data) >= 3:
            baseline = {
                'heart_rate': user_data['heart_rate'].mean(),
                'sleep': user_data['sleep_hours'].mean(),
                'activity': user_data['steps'].mean()
            }
            self.baselines[user_id] = baseline
            return baseline
        
        return None
    
    def get_baseline(self, user_id):
        return self.baselines.get(user_id, None)
    
    def save_to_db(self, user_id, baseline, db_save_func):
        db_save_func(user_id, baseline['heart_rate'], baseline['sleep'], baseline['activity'])