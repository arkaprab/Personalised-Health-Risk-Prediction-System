"""
ALERT DECISION - Determine alert level and action
"""

from constants import RISK_CRITICAL, RISK_HIGH, RISK_MODERATE

class AlertDecider:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_level(self, risk_score):
        """Get alert level from risk score"""
        
        if risk_score > RISK_CRITICAL:
            return "🔴 CRITICAL"
        elif risk_score > RISK_HIGH:
            return "🟠 HIGH"
        elif risk_score > RISK_MODERATE:
            return "🟡 MODERATE"
        else:
            return "🟢 LOW"
    
    def get_action(self, risk_score, consecutive_days):
        """Get recommended action"""
        
        if risk_score > 0.7 and consecutive_days >= 2:
            return "🚨 IMMEDIATE: Seek medical attention"
        elif risk_score > 0.6:
            return "⚠️ HIGH RISK: Rest and monitor closely"
        elif risk_score > 0.4:
            return "📊 MODERATE: Improve sleep and activity"
        else:
            return "💚 NORMAL: Continue healthy habits"
    
    