"""
Player Clustering Model
Groups players based on their choice patterns
"""
import logging
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib

from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class PlayerClusteringModel:
    """
    K-Means clustering to identify player archetypes
    
    Features:
    - Choice diversity score
    - Average playtime per episode
    - Completion rate
    - Major choice patterns
    
    Output:
    - Player cluster/archetype (e.g., "Story-focused", "Explorer", "Speed-runner")
    """
    
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.model = None
        self.scaler = StandardScaler()
        self.pca = None
        self.feature_columns = []
        self.cluster_labels = {}
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate player-level features
        
        Args:
            df: Dataframe with player and choice data
            
        Returns:
            pd.DataFrame: Player-level features
        """
        # Aggregate by player
        player_features = df.groupby('player_id').agg({
            'episode': 'nunique',  # Unique episodes played
            'choice_id': 'count',  # Total choices made
            'timestamp_in_game': 'mean',  # Average playtime
        }).reset_index()
        
        player_features.columns = [
            'player_id',
            'unique_episodes',
            'total_choices',
            'avg_playtime'
        ]
        
        # Calculate derived features
        player_features['choices_per_episode'] = (
            player_features['total_choices'] / player_features['unique_episodes']
        )
        
        player_features['completion_rate'] = (
            player_features['unique_episodes'] / 5.0  # Max 5 episodes
        )
        
        # Convert playtime to hours
        player_features['avg_hours_played'] = player_features['avg_playtime'] / 3600
        
        return player_features
    
    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train K-Means clustering model
        
        Args:
            df: Dataframe with player choice data
            
        Returns:
            dict: Clustering metrics
        """
        logger.info(f"Training player clustering model with {self.n_clusters} clusters")
        
        # Prepare features
        features = self.prepare_features(df)
        
        # Select numeric features for clustering
        feature_cols = [
            'unique_episodes',
            'total_choices',
            'choices_per_episode',
            'completion_rate',
            'avg_hours_played'
        ]
        
        X = features[feature_cols]
        self.feature_columns = feature_cols
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply PCA for dimensionality reduction (optional)
        self.pca = PCA(n_components=3)
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Train K-Means
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10
        )
        
        clusters = self.model.fit_predict(X_scaled)
        features['cluster'] = clusters
        
        # Analyze clusters
        cluster_summary = features.groupby('cluster')[feature_cols].mean()
        
        # Assign interpretable labels (simplified heuristic)
        self.cluster_labels = self._assign_cluster_labels(cluster_summary)
        
        logger.info("Clustering complete")
        logger.info(f"Cluster labels: {self.cluster_labels}")
        
        return {
            'n_clusters': self.n_clusters,
            'cluster_summary': cluster_summary.to_dict(),
            'cluster_labels': self.cluster_labels,
            'inertia': self.model.inertia_,
            'pca_variance_explained': self.pca.explained_variance_ratio_.tolist()
        }
    
    def _assign_cluster_labels(self, cluster_summary: pd.DataFrame) -> Dict[int, str]:
        """
        Assign interpretable labels to clusters based on characteristics
        
        Args:
            cluster_summary: Summary statistics per cluster
            
        Returns:
            dict: Mapping of cluster ID to label
        """
        labels = {}
        
        for cluster_id in cluster_summary.index:
            stats = cluster_summary.loc[cluster_id]
            
            # Simple heuristics for labeling
            if stats['completion_rate'] >= 0.8 and stats['avg_hours_played'] >= 10:
                labels[cluster_id] = "Completionist"
            elif stats['choices_per_episode'] >= 15:
                labels[cluster_id] = "Explorer"
            elif stats['avg_hours_played'] <= 5 and stats['completion_rate'] >= 0.6:
                labels[cluster_id] = "Speed Runner"
            elif stats['unique_episodes'] <= 2:
                labels[cluster_id] = "Casual Player"
            else:
                labels[cluster_id] = "Average Player"
        
        return labels
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predict cluster for new players
        
        Args:
            df: Dataframe with player choice data
            
        Returns:
            np.ndarray: Cluster assignments
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        features = self.prepare_features(df)
        X = features[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        clusters = self.model.predict(X_scaled)
        return clusters
    
    def get_cluster_label(self, cluster_id: int) -> str:
        """Get interpretable label for cluster"""
        return self.cluster_labels.get(cluster_id, f"Cluster {cluster_id}")
    
    def save_model(self, path: str):
        """Save trained model to disk"""
        if self.model is None:
            raise ValueError("No model to save")
        
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'pca': self.pca,
            'feature_columns': self.feature_columns,
            'cluster_labels': self.cluster_labels
        }, path)
        
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model from disk"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.pca = data['pca']
        self.feature_columns = data['feature_columns']
        self.cluster_labels = data['cluster_labels']
        
        logger.info(f"Model loaded from {path}")
