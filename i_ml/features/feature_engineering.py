"""
Feature Engineering for ML Models
"""
import pandas as pd
import numpy as np
from typing import List, Dict


def create_player_features(choices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create player-level features from choice data
    
    Args:
        choices_df: Dataframe with player choices
        
    Returns:
        pd.DataFrame: Player-level features
    """
    player_features = choices_df.groupby('player_id').agg({
        'episode': ['nunique', 'max'],
        'chapter': 'count',
        'choice_id': 'nunique',
        'timestamp_in_game': ['mean', 'max', 'std'],
    })
    
    # Flatten column names
    player_features.columns = [
        'unique_episodes',
        'max_episode',
        'total_choices',
        'unique_choice_types',
        'avg_playtime',
        'max_playtime',
        'playtime_std'
    ]
    
    # Derived features
    player_features['completion_rate'] = player_features['max_episode'] / 5.0
    player_features['choices_per_episode'] = (
        player_features['total_choices'] / player_features['unique_episodes']
    )
    
    return player_features.reset_index()


def create_choice_features(choices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create choice-level features for prediction
    
    Args:
        choices_df: Dataframe with choices
        
    Returns:
        pd.DataFrame: Enhanced choice features
    """
    features = choices_df.copy()
    
    # Time-based features
    features['hours_into_game'] = features['timestamp_in_game'] / 3600
    features['is_early_game'] = (features['episode'] <= 2).astype(int)
    features['is_late_game'] = (features['episode'] >= 4).astype(int)
    
    # Episode progress
    features['episode_progress'] = features['episode'] / 5.0
    
    # Choice context
    features['is_major_choice'] = features['choice_id'].str.contains(
        'sacrifice|save|kill', case=False, na=False
    ).astype(int)
    
    return features


def create_temporal_features(df: pd.DataFrame, timestamp_col: str = 'created_at') -> pd.DataFrame:
    """
    Extract temporal features from timestamp
    
    Args:
        df: Dataframe with timestamp column
        timestamp_col: Name of timestamp column
        
    Returns:
        pd.DataFrame: Dataframe with temporal features
    """
    df = df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    df['hour'] = df[timestamp_col].dt.hour
    df['day_of_week'] = df[timestamp_col].dt.dayofweek
    df['month'] = df[timestamp_col].dt.month
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_night'] = ((df['hour'] >= 20) | (df['hour'] <= 6)).astype(int)
    
    return df


def encode_categorical_features(
    df: pd.DataFrame,
    columns: List[str],
    method: str = 'onehot'
) -> pd.DataFrame:
    """
    Encode categorical features
    
    Args:
        df: Dataframe
        columns: List of categorical columns
        method: 'onehot' or 'label'
        
    Returns:
        pd.DataFrame: Encoded dataframe
    """
    df = df.copy()
    
    if method == 'onehot':
        df = pd.get_dummies(df, columns=columns, prefix=columns)
    elif method == 'label':
        from sklearn.preprocessing import LabelEncoder
        for col in columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    
    return df


def create_choice_sequences(choices_df: pd.DataFrame, max_length: int = 10) -> Dict:
    """
    Create choice sequences for sequence-based models (LSTM, etc.)
    
    Args:
        choices_df: Dataframe with choices sorted by player and time
        max_length: Maximum sequence length
        
    Returns:
        dict: Sequences and labels
    """
    sequences = []
    labels = []
    
    for player_id in choices_df['player_id'].unique():
        player_choices = choices_df[choices_df['player_id'] == player_id].sort_values(
            'timestamp_in_game'
        )
        
        choice_sequence = player_choices['choice_id'].tolist()
        
        # Create sliding windows
        for i in range(len(choice_sequence) - 1):
            seq = choice_sequence[max(0, i - max_length + 1):i + 1]
            label = choice_sequence[i + 1]
            
            # Pad sequence if needed
            if len(seq) < max_length:
                seq = ['<PAD>'] * (max_length - len(seq)) + seq
            
            sequences.append(seq)
            labels.append(label)
    
    return {
        'sequences': sequences,
        'labels': labels
    }
