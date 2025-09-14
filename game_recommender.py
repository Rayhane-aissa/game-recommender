"""
Advanced Game Recommendation Engine
Extracted from Jupyter notebook and optimized for production use.
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import torch
import os
import faiss
import re
import spacy
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class GameRecommender:
    def __init__(self, model_name='all-mpnet-base-v2', device=None, embedding_dir="embeddings"):
        """
        Game recommender using combined embeddings.
        """
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)
        self.embedding_dir = embedding_dir
        os.makedirs(self.embedding_dir, exist_ok=True)
        self.game_embeddings = None
        self.game_names = None
        self.index = None
        self.df = None
        self.scaler = MinMaxScaler()
        
        # Initialize spaCy for text preprocessing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None

    def load_and_preprocess_data(self, csv_path=None):
        """
        Load and preprocess the game dataset.
        """
        if csv_path and os.path.exists(csv_path):
            print(f"Loading data from {csv_path}")
            self.df = pd.read_csv(csv_path)
        else:
            print("No data file found. Using sample data...")
            self.df = self._create_sample_data()
        
        print(f"Loaded {len(self.df)} game records")
        return self._preprocess_data()

    def _create_sample_data(self):
        """Create sample data for testing when no CSV is available."""
        return pd.DataFrame({
            'Game Title': [
                'The Legend of Zelda: Breath of the Wild',
                'Animal Crossing: New Horizons', 
                'Hollow Knight',
                'Celeste',
                'Stardew Valley',
                'Journey',
                'Ori and the Blind Forest',
                'Subnautica',
                'Spiritfarer',
                'What Remains of Edith Finch'
            ],
            'Genre': [
                'Adventure', 'Simulation', 'Metroidvania', 'Platformer',
                'Farming', 'Adventure', 'Platformer', 'Survival',
                'Management', 'Adventure'
            ],
            'User Review Text': [
                'amazing open world adventure exploration puzzle solving',
                'relaxing life simulation cute animals peaceful',
                'challenging metroidvania beautiful art platformer',
                'emotional platformer personal struggle challenging',
                'charming farming simulation social elements relaxing',
                'meditative adventure beautiful landscapes peaceful',
                'emotional platformer stunning visuals adventure',
                'underwater survival exploration adventure',
                'beautiful game goodbye peace emotional',
                'narrative exploration family stories emotional'
            ],
            'Age Group Targeted': [
                'Teen', 'Everyone', 'Teen', 'Teen', 'Everyone',
                'Everyone', 'Teen', 'Teen', 'Teen', 'Mature'
            ],
            'Graphics Quality': [
                'High', 'High', 'High', 'High', 'Medium',
                'High', 'High', 'High', 'High', 'High'
            ],
            'User Rating': [9.5, 9.0, 9.2, 8.8, 9.2, 9.1, 9.0, 8.7, 9.0, 8.9],
            'Price': [59.99, 59.99, 14.99, 19.99, 14.99, 14.99, 19.99, 29.99, 29.99, 19.99]
        })

    def _preprocess_data(self):
        """
        Preprocess the game data for ML pipeline.
        """
        print("Preprocessing data...")
        
        # Clean text data
        if 'User Review Text' in self.df.columns:
            self.df['User Review Text'] = self.df['User Review Text'].fillna('')
            self.df['User Review Text'] = self.df['User Review Text'].str.lower()
            self.df['User Review Text'] = self.df['User Review Text'].apply(
                lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x))
            )
            
            # Apply spaCy preprocessing if available
            if self.nlp:
                self.df['User Review Text'] = self.df['User Review Text'].apply(
                    lambda doc: " ".join([token.lemma_ for token in self.nlp(doc) if not token.is_stop])
                )
        
        # Fill missing values
        self.df = self.df.fillna('Unknown')
        
        print("Data preprocessing completed")
        return self.df

    def prepare_text(self, df):
        """
        Combine all textual features into a single string per game.
        """
        combined = (
            df['Game Title'].astype(str) + " | " +
            df['Genre'].astype(str) + " | " +
            df['User Review Text'].astype(str) + " | " +
            "Age: " + df['Age Group Targeted'].astype(str) + " | " +
            "Graphics: " + df['Graphics Quality'].astype(str)
        )
        return combined

    def encode_games(self, df=None):
        """
        Encode all games and save/load embeddings.
        """
        if df is None:
            df = self.df
        
        self.game_names = df['Game Title'].tolist()
        embedding_path = os.path.join(self.embedding_dir, "game_embeddings.npy")

        if os.path.exists(embedding_path):
            print(f"Loading game embeddings from {embedding_path}")
            self.game_embeddings = np.load(embedding_path)
        else:
            print("Encoding game embeddings...")
            combined_texts = self.prepare_text(df).tolist()
            self.game_embeddings = self.model.encode(
                combined_texts,
                convert_to_tensor=False,
                batch_size=64,
                show_progress_bar=True
            )
            # Normalize embeddings
            self.game_embeddings = normalize(self.game_embeddings)
            np.save(embedding_path, self.game_embeddings)
            print(f"Saved embeddings to {embedding_path}")

        # Build FAISS index
        dim = self.game_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # inner product on normalized = cosine similarity
        self.index.add(self.game_embeddings.astype('float32'))
        print("FAISS index built.")

    def query(self, user_input, top_k=5):
        """
        Find top-k games based on a user query.
        """
        if self.index is None:
            raise ValueError("Model not initialized. Call encode_games() first.")
            
        user_emb = self.model.encode([user_input], convert_to_tensor=False)
        user_emb = normalize(user_emb)
        D, I = self.index.search(user_emb.astype('float32'), k=top_k)
        results = [(self.game_names[idx], float(score)) for idx, score in zip(I[0], D[0])]
        return results

    def get_game_details(self, game_name):
        """
        Get detailed information about a specific game.
        """
        if self.df is None:
            return None
            
        game_info = self.df[self.df['Game Title'] == game_name]
        if len(game_info) > 0:
            return game_info.iloc[0].to_dict()
        return None

    def initialize_model(self, csv_path=None):
        """
        Complete initialization: load data, preprocess, and encode games.
        """
        print("Initializing Game Recommender...")
        self.load_and_preprocess_data(csv_path)
        self.encode_games()
        print("Game Recommender ready!")

# Global recommender instance
_recommender = None

def get_recommender():
    """Get or create the global recommender instance."""
    global _recommender
    if _recommender is None:
        _recommender = GameRecommender(device='cpu')
        # Try to load from Kaggle dataset if available
        try:
            import kagglehub
            path = kagglehub.dataset_download("jahnavipaliwal/video-game-reviews-and-ratings")
            csv_path = os.path.join(path, "video_game_reviews.csv")
            _recommender.initialize_model(csv_path)
        except Exception as e:
            print(f"Could not load Kaggle dataset: {e}")
            print("Using sample data instead...")
            _recommender.initialize_model()
    return _recommender

def get_recommendations(user_input, mood=None, top_k=5):
    """
    Get game recommendations for a user query.
    
    Args:
        user_input: User's query string
        mood: Optional mood filter (not used in current implementation)
        top_k: Number of recommendations to return
    
    Returns:
        List of tuples (game_name, similarity_score)
    """
    recommender = get_recommender()
    return recommender.query(user_input, top_k=top_k)

def get_game_info(game_name):
    """Get detailed information about a specific game."""
    recommender = get_recommender()
    return recommender.get_game_details(game_name)
