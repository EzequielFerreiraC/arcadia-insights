"""
Choice Prediction Model
Predicts player choices based on historical data
"""
import logging
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class ChoicePredictionModel:
    """
    Random Forest model to predict player choices
    
    Features:
    - Player country
    - Platform
    - Previous choices in episode
    - Time spent in game
    
    Target:
    - Choice option selected
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.feature_columns = []
        self.label_encoder = {}
        self.model_path = model_path
        
        if model_path:
            self.load_model(model_path)
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for training/prediction
        
        Args:
            df: Raw dataframe with choice data
            
        Returns:
            pd.DataFrame: Processed features
        """
        # Create a copy to avoid modifying original
        features = df.copy()
        
        # One-hot encode categorical variables
        features = pd.get_dummies(
            features,
            columns=['player_country', 'player_platform'],
            prefix=['country', 'platform']
        )
        
        # Extract time-based features
        if 'timestamp_in_game' in features.columns:
            features['hours_played'] = features['timestamp_in_game'] / 3600
            features['minutes_played'] = features['timestamp_in_game'] / 60
        
        # Episode and chapter as numeric
        features['episode'] = features['episode'].astype(int)
        features['chapter'] = features['chapter'].astype(int)
        
        return features
    
    def train(
        self,
        df: pd.DataFrame,
        target_column: str = 'option_selected',
        test_size: float = 0.2
    ) -> Dict[str, Any]:
        """
        Train the choice prediction model
        
        Args:
            df: Training dataframe
            target_column: Name of target column
            test_size: Proportion of test set
            
        Returns:
            dict: Training metrics
        """
        logger.info(f"Training choice prediction model on {len(df)} samples")
        
        # Prepare features
        X = self.prepare_features(df)
        y = df[target_column]
        
        # Store feature columns
        self.feature_columns = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Model trained with accuracy: {accuracy:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'feature_importance': feature_importance.head(10).to_dict('records')
        }
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predict choice options
        
        Args:
            df: Dataframe with features
            
        Returns:
            np.ndarray: Predicted choice options
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X = self.prepare_features(df)
        
        # Ensure same features as training
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0
        
        X = X[self.feature_columns]
        
        predictions = self.model.predict(X)
        return predictions
    
    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predict choice probabilities
        
        Args:
            df: Dataframe with features
            
        Returns:
            np.ndarray: Predicted probabilities for each class
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X = self.prepare_features(df)
        
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0
        
        X = X[self.feature_columns]
        
        probabilities = self.model.predict_proba(X)
        return probabilities
    
    def save_model(self, path: str):
        """Save trained model to disk"""
        if self.model is None:
            raise ValueError("No model to save")
        
        joblib.dump({
            'model': self.model,
            'feature_columns': self.feature_columns,
            'label_encoder': self.label_encoder
        }, path)
        
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model from disk"""
        data = joblib.load(path)
        self.model = data['model']
        self.feature_columns = data['feature_columns']
        self.label_encoder = data['label_encoder']
        
        logger.info(f"Model loaded from {path}")
