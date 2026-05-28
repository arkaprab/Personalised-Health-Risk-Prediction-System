"""
ISOLATION FOREST - Anomaly detection
"""

from sklearn.ensemble import IsolationForest
class IsolationForestModel:
    def __init__(self):
        self.model = None
    
    def train(self, X):
        """Train Isolation Forest"""
        
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        
        self.model.fit(X)
        return True
    
    def detect(self, X):
        """Detect anomalies (higher score = more anomalous)"""
        if self.model is None:
            return None
        
        raw_scores = -self.model.score_samples(X)
        
        # Normalize to 0-1
        min_score = raw_scores.min()
        max_score = raw_scores.max()
        normalized = (raw_scores - min_score) / (max_score - min_score + 0.00001)
        
        return normalized