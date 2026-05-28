"""
HYBRID RISK - Combine XGBoost and Isolation Forest
"""

class HybridRiskCalculator:
    def __init__(self, xgb_model, isolation_model):
        self.xgb = xgb_model
        self.isolation = isolation_model
    
    def calculate(self, X):
        """Calculate hybrid risk score"""
        
        xgb_risk = self.xgb.predict(X)
        anomaly_risk = self.isolation.detect(X)
        
        if xgb_risk is None or anomaly_risk is None:
            return None
        
        # Average of both scores
        hybrid = (xgb_risk + anomaly_risk) / 2
        
        return hybrid, xgb_risk, anomaly_risk