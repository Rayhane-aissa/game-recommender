"""
Direct integration of Jupyter notebook code with the web interface.
This module extracts and adapts the working code from game_recommender.ipynb
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
import warnings
warnings.filterwarnings('ignore')

class NotebookGameRecommender:
    """
    Direct implementation of the GameRecommender from the Jupyter notebook.
    """
    def __init__(self, model_name='all-mpnet-base-v2', device=None, embedding_dir="embeddings"):
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)
        self.embedding_dir = embedding_dir
        os.makedirs(self.embedding_dir, exist_ok=True)
        self.game_embeddings = None
        self.game_names = None
        self.index = None
        self.df = None
        
        # Initialize spaCy for text preprocessing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Text preprocessing will be basic.")
            self.nlp = None

    def load_kaggle_data(self):
        """Load data from Kaggle dataset as in the notebook."""
        try:
            import kagglehub
            print("Downloading Kaggle dataset...")
            path = kagglehub.dataset_download("jahnavipaliwal/video-game-reviews-and-ratings")
            csv_path = os.path.join(path, "video_game_reviews.csv")
            self.df = pd.read_csv(csv_path)
            print(f"Loaded {len(self.df)} records from Kaggle dataset")
            return self.df
        except Exception as e:
            print(f"Could not load Kaggle dataset: {e}")
            return self._create_sample_data()

    def _create_sample_data(self):
        """Create sample data based on the notebook's structure."""
        print("Creating sample data...")
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
                'What Remains of Edith Finch',
                'Sid Meier\'s Civilization VI',
                '1000-Piece Puzzle',
                'The Witcher 3: Wild Hunt',
                'Minecraft',
                'Portal 2'
            ],
            'Genre': [
                'Adventure', 'Simulation', 'Metroidvania', 'Platformer',
                'Farming', 'Adventure', 'Platformer', 'Survival',
                'Management', 'Adventure', 'Strategy', 'Puzzle',
                'RPG', 'Sandbox', 'Puzzle'
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
                'narrative exploration family stories emotional',
                'strategy civilization building historical',
                'relaxing puzzle piece assembly calm',
                'epic fantasy rpg adventure story',
                'creative building sandbox exploration',
                'puzzle portal physics challenging'
            ],
            'Age Group Targeted': [
                'Teen', 'Everyone', 'Teen', 'Teen', 'Everyone',
                'Everyone', 'Teen', 'Teen', 'Teen', 'Mature',
                'Teen', 'Everyone', 'Mature', 'Everyone', 'Teen'
            ],
            'Graphics Quality': [
                'High', 'High', 'High', 'High', 'Medium',
                'High', 'High', 'High', 'High', 'High',
                'High', 'Medium', 'High', 'Medium', 'High'
            ],
            'User Rating': [9.5, 9.0, 9.2, 8.8, 9.2, 9.1, 9.0, 8.7, 9.0, 8.9, 8.6, 7.5, 9.3, 8.8, 9.0],
            'Price': [59.99, 59.99, 14.99, 19.99, 14.99, 14.99, 19.99, 29.99, 29.99, 19.99, 59.99, 4.99, 39.99, 26.95, 9.99]
        })

    def preprocess_data(self, df):
        """Preprocess data exactly as in the notebook."""
        print("Preprocessing data...")
        
        # Clean text data
        if 'User Review Text' in df.columns:
            df['User Review Text'] = df['User Review Text'].fillna('')
            df['User Review Text'] = df['User Review Text'].str.lower()
            df['User Review Text'] = df['User Review Text'].apply(
                lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x))
            )
            
            # Apply spaCy preprocessing if available
            if self.nlp:
                df['User Review Text'] = df['User Review Text'].apply(
                    lambda doc: " ".join([token.lemma_ for token in self.nlp(doc) if not token.is_stop])
                )
        
        # Fill missing values
        df = df.fillna('Unknown')
        
        print("Data preprocessing completed")
        return df

    def prepare_text(self, df):
        """Combine all textual features into a single string per game."""
        combined = (
            df['Game Title'].astype(str) + " | " +
            df['Genre'].astype(str) + " | " +
            df['User Review Text'].astype(str) + " | " +
            "Age: " + df['Age Group Targeted'].astype(str) + " | " +
            "Graphics: " + df['Graphics Quality'].astype(str)
        )
        return combined

    def encode_games(self, df):
        """Encode all games and save/load embeddings."""
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
        """Find top-k games based on a user query."""
        if self.index is None:
            raise ValueError("Model not initialized. Call encode_games() first.")
            
        user_emb = self.model.encode([user_input], convert_to_tensor=False)
        user_emb = normalize(user_emb)
        D, I = self.index.search(user_emb.astype('float32'), k=top_k)
        results = [(self.game_names[idx], float(score)) for idx, score in zip(I[0], D[0])]
        return results

    def get_game_details(self, game_name):
        """Get detailed information about a specific game."""
        if self.df is None:
            return None
            
        game_info = self.df[self.df['Game Title'] == game_name]
        if len(game_info) > 0:
            return game_info.iloc[0].to_dict()
        return None

    def initialize(self):
        """Complete initialization: load data, preprocess, and encode games."""
        print("Initializing Notebook Game Recommender...")
        
        # Load data
        self.df = self.load_kaggle_data()
        
        # Preprocess data
        self.df = self.preprocess_data(self.df)
        
        # Encode games
        self.encode_games(self.df)
        
        print("Notebook Game Recommender ready!")

# Global recommender instance
_notebook_recommender = None

def get_notebook_recommender():
    """Get or create the global notebook recommender instance."""
    global _notebook_recommender
    if _notebook_recommender is None:
        _notebook_recommender = NotebookGameRecommender(device='cpu')
        _notebook_recommender.initialize()
    return _notebook_recommender

def get_notebook_recommendations(user_input, mood=None, top_k=5):
    """
    Get game recommendations using the notebook's ML model.
    
    Args:
        user_input: User's query string
        mood: Optional mood filter (not used in current implementation)
        top_k: Number of recommendations to return
    
    Returns:
        List of tuples (game_name, similarity_score)
    """
    recommender = get_notebook_recommender()
    return recommender.query(user_input, top_k=top_k)

def get_notebook_game_info(game_name):
    """Get detailed information about a specific game."""
    recommender = get_notebook_recommender()
    return recommender.get_game_details(game_name)
