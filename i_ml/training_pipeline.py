"""
ML Training Pipeline
Orchestrates model training and evaluation
"""
import logging
from pathlib import Path
from typing import Dict, Any
import pandas as pd

from i_ml.models.choice_predictor import ChoicePredictionModel
from i_ml.models.player_clustering import PlayerClusteringModel
from i_ml.features.feature_engineering import create_player_features, create_choice_features
from g_storage.parquet_reader import ParquetReader
from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class MLTrainingPipeline:
    """
    End-to-end ML training pipeline
    """
    
    def __init__(self, data_source: str = 'silver'):
        self.data_source = data_source
        self.reader = ParquetReader()
        self.models_dir = Path('i_ml/trained_models')
        self.models_dir.mkdir(exist_ok=True, parents=True)
    
    def load_data(self) -> pd.DataFrame:
        """
        Load training data from Silver layer
        
        Returns:
            pd.DataFrame: Combined training data
        """
        logger.info(f"Loading data from {self.data_source} layer")
        
        # Load choices from Silver layer
        choices_df = self.reader.read_from_silver('choices')
        
        if choices_df.empty:
            raise ValueError("No training data available in Silver layer")
        
        logger.info(f"Loaded {len(choices_df)} choice records")
        return choices_df
    
    def train_choice_predictor(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train choice prediction model
        
        Args:
            df: Training dataframe
            
        Returns:
            dict: Training results
        """
        logger.info("Training Choice Prediction Model")
        
        # Prepare features
        features_df = create_choice_features(df)
        
        # Initialize and train model
        model = ChoicePredictionModel()
        metrics = model.train(features_df, target_column='option_selected')
        
        # Save model
        model_path = self.models_dir / 'choice_predictor.joblib'
        model.save_model(str(model_path))
        
        logger.info(f"Choice predictor saved to {model_path}")
        return metrics
    
    def train_player_clustering(self, df: pd.DataFrame, n_clusters: int = 5) -> Dict[str, Any]:
        """
        Train player clustering model
        
        Args:
            df: Training dataframe
            n_clusters: Number of player clusters
            
        Returns:
            dict: Training results
        """
        logger.info("Training Player Clustering Model")
        
        # Initialize and train model
        model = PlayerClusteringModel(n_clusters=n_clusters)
        metrics = model.train(df)
        
        # Save model
        model_path = self.models_dir / 'player_clustering.joblib'
        model.save_model(str(model_path))
        
        logger.info(f"Player clustering model saved to {model_path}")
        return metrics
    
    def run_pipeline(self) -> Dict[str, Any]:
        """
        Run complete training pipeline
        
        Returns:
            dict: Results from all models
        """
        logger.info("Starting ML training pipeline")
        
        # Load data
        df = self.load_data()
        
        results = {}
        
        # Train choice predictor
        try:
            choice_metrics = self.train_choice_predictor(df)
            results['choice_predictor'] = choice_metrics
        except Exception as e:
            logger.error(f"Failed to train choice predictor: {e}")
            results['choice_predictor'] = {'error': str(e)}
        
        # Train player clustering
        try:
            cluster_metrics = self.train_player_clustering(df)
            results['player_clustering'] = cluster_metrics
        except Exception as e:
            logger.error(f"Failed to train player clustering: {e}")
            results['player_clustering'] = {'error': str(e)}
        
        logger.info("ML training pipeline complete")
        return results


if __name__ == "__main__":
    # Example usage
    pipeline = MLTrainingPipeline()
    results = pipeline.run_pipeline()
    
    print("\nTraining Results:")
    print("=" * 50)
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print(metrics)
