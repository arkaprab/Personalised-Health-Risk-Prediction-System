"""
DEVIATION CALCULATOR - Compare current values with baseline
"""

class DeviationCalculator:
    def __init__(self, baseline_engine):
        self.baseline_engine = baseline_engine
    
    def calculate(self, user_id, heart_rate, sleep, activity):
        """Calculate deviations from personal baseline"""
        
        baseline = self.baseline_engine.get_baseline(user_id)
        
        if baseline is None:
            return None
        
        deviations = {
            'deviation_hr': heart_rate - baseline['heart_rate'],
            'deviation_sleep': sleep - baseline['sleep'],
            'deviation_activity': activity - baseline['activity']
        }
        
        return deviations
    
    def is_significant(self, deviations):
        """Check if deviations are significant"""
        
        if deviations is None:
            return False
        
        hr_sig = abs(deviations.get('deviation_hr', 0)) > 10
        sleep_sig = deviations.get('deviation_sleep', 0) < -1.5
        activity_sig = deviations.get('deviation_activity', 0) < -2000
        
        return hr_sig or sleep_sig or activity_sig