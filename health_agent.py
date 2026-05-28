"""
HEALTH AGENT - Main intelligent decision maker
"""

from Alertdecision import AlertDecider
from Explanations import ExplanationGenerator

class HealthAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.alert_decider = AlertDecider(user_id)
        self.explanation_gen = ExplanationGenerator()
        self.consecutive_high = 0
    
    def decide(self, risk_score, deviations, current_data):
        """Main decision function"""
        
        # Update consecutive counter
        if risk_score > 0.6:
            self.consecutive_high += 1
        else:
            self.consecutive_high = 0
        
        # Get alert level
        alert_level = self.alert_decider.get_level(risk_score)
        
        # Get action
        action = self.alert_decider.get_action(risk_score, self.consecutive_high)
        
        # Get explanation
        explanation = self.explanation_gen.generate(risk_score, deviations)
        
        return {
            'alert_level': alert_level,
            'explanation': explanation,
            'action': action,
            'consecutive_days': self.consecutive_high
        }