"""
EXPLANATION GENERATOR - Human readable explanations
"""

class ExplanationGenerator:
    def generate(self, risk_score, deviations):
        """Generate explanation for user"""
        
        reasons = []

        if deviations:
            hr_dev = deviations.get('deviation_hr', 0)
            if hr_dev > 10:
                reasons.append(f"Heart rate is {hr_dev:.0f} bpm ABOVE your normal")
            elif hr_dev < -10:
                reasons.append(f"Heart rate is {abs(hr_dev):.0f} bpm BELOW your normal")
            
            sleep_dev = deviations.get('deviation_sleep', 0)
            if sleep_dev < -1.5:
                reasons.append(f"Sleep reduced by {abs(sleep_dev):.1f} hours")
            
            activity_dev = deviations.get('deviation_activity', 0)
            if activity_dev < -2000:
                reasons.append(f"Activity dropped by {abs(activity_dev):.0f} steps")
        
        if risk_score > 0.6:
            reasons.append("Multiple abnormal patterns detected")
        
        if not reasons:
            return "All health metrics are within your normal range"
        
        return " • " + "\n • ".join(reasons)