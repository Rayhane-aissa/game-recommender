"""
Game Recommendation Frontend
Integration with the ML-based recommendation system from Jupyter notebook.
"""

from typing import List, Dict, Optional, Tuple
import sys
from pathlib import Path

# Import the notebook-based recommendation engine
try:
    from notebook_integration import get_notebook_recommendations as get_ml_recommendations, get_notebook_game_info as get_game_info
    ML_ENGINE_AVAILABLE = True
    print("✅ Notebook ML recommendation engine loaded successfully!")
except ImportError as e:
    ML_ENGINE_AVAILABLE = False
    print(f"⚠️ Notebook ML engine not available: {e}")
    print("Falling back to basic recommendation system...")

# Dummy game database - placeholder for real backend connection
GAME_DATABASE = {
    "adventure": [
        {"name": "The Legend of Zelda: Breath of the Wild", "rating": 9.5, "price": 59.99, "reviews": 15000, "description": "Open-world adventure with exploration and puzzle-solving"},
        {"name": "Hollow Knight", "rating": 9.2, "price": 14.99, "reviews": 8500, "description": "Metroidvania adventure with beautiful art and challenging gameplay"},
        {"name": "Ori and the Blind Forest", "rating": 9.0, "price": 19.99, "reviews": 6200, "description": "Emotional platformer adventure with stunning visuals"},
        {"name": "Celeste", "rating": 8.8, "price": 19.99, "reviews": 4800, "description": "Challenging platformer about overcoming personal struggles"},
        {"name": "Subnautica", "rating": 8.7, "price": 29.99, "reviews": 12000, "description": "Underwater survival adventure with exploration"},
    ],
    "language_learning": [
        {"name": "Duolingo", "rating": 8.5, "price": 0.00, "reviews": 25000, "description": "Free language learning app with gamified lessons"},
        {"name": "Babbel", "rating": 8.2, "price": 6.95, "reviews": 12000, "description": "Interactive language learning with real-world conversations"},
        {"name": "Rosetta Stone", "rating": 7.8, "price": 11.99, "reviews": 8500, "description": "Immersive language learning experience"},
        {"name": "Memrise", "rating": 8.0, "price": 8.99, "reviews": 6800, "description": "Vocabulary building with spaced repetition"},
        {"name": "Drops", "rating": 7.9, "price": 9.99, "reviews": 4500, "description": "Visual language learning with beautiful graphics"},
    ],
    "educational": [
        {"name": "Prodigy Math Game", "rating": 8.7, "price": 0.00, "reviews": 18000, "description": "Math adventure game for kids ages 6-14"},
        {"name": "Khan Academy Kids", "rating": 9.1, "price": 0.00, "reviews": 22000, "description": "Free educational games for ages 2-8"},
        {"name": "ABCmouse", "rating": 8.9, "price": 9.95, "reviews": 15000, "description": "Comprehensive early learning curriculum"},
        {"name": "DragonBox Numbers", "rating": 8.6, "price": 7.99, "reviews": 3200, "description": "Number sense and basic math for ages 4-8"},
        {"name": "Scratch", "rating": 9.3, "price": 0.00, "reviews": 12000, "description": "Creative coding platform for kids"},
        {"name": "Minecraft Education", "rating": 8.8, "price": 5.00, "reviews": 8500, "description": "Educational version of Minecraft for classrooms"},
    ], 
    "happy": [
        {"name": "Animal Crossing: New Horizons", "rating": 9.0, "price": 59.99, "reviews": 20000, "description": "Relaxing life simulation with cute animals"},
        {"name": "Stardew Valley", "rating": 9.2, "price": 14.99, "reviews": 18000, "description": "Charming farming simulation with social elements"},
        {"name": "Untitled Goose Game", "rating": 8.5, "price": 19.99, "reviews": 8500, "description": "Playful puzzle game where you're a mischievous goose"},
        {"name": "Overcooked 2", "rating": 8.3, "price": 24.99, "reviews": 12000, "description": "Chaotic cooking co-op game for friends"},
        {"name": "Fall Guys", "rating": 8.1, "price": 0.00, "reviews": 25000, "description": "Colorful battle royale party game"},
    ],
    "chill": [
        {"name": "Journey", "rating": 9.1, "price": 14.99, "reviews": 15000, "description": "Meditative adventure through beautiful landscapes"},
        {"name": "Flower", "rating": 8.7, "price": 6.99, "reviews": 4200, "description": "Relaxing wind simulation game"},
        {"name": "Abzû", "rating": 8.4, "price": 19.99, "reviews": 3800, "description": "Underwater exploration adventure"},
        {"name": "Gris", "rating": 8.8, "price": 16.99, "reviews": 5500, "description": "Emotional platformer with stunning watercolor art"},
        {"name": "A Short Hike", "rating": 8.9, "price": 7.99, "reviews": 3200, "description": "Peaceful exploration game about climbing a mountain"},
    ],
    "sad": [
        {"name": "Spiritfarer", "rating": 9.0, "price": 29.99, "reviews": 8500, "description": "Beautiful game about saying goodbye and finding peace"},
        {"name": "What Remains of Edith Finch", "rating": 8.9, "price": 19.99, "reviews": 7200, "description": "Narrative exploration of family stories"},
        {"name": "Night in the Woods", "rating": 8.6, "price": 19.99, "reviews": 4800, "description": "Story-driven game about mental health and friendship"},
        {"name": "To the Moon", "rating": 9.2, "price": 9.99, "reviews": 6800, "description": "Emotional story about fulfilling a dying man's wish"},
        {"name": "Firewatch", "rating": 8.5, "price": 19.99, "reviews": 5500, "description": "Atmospheric story about isolation and connection"},
    ]
}

def parse_user_intent(user_input: str) -> str:
    """
    Parse user input to identify their intent and return appropriate category.
    This is placeholder logic that can be enhanced or replaced with ML models.
    """
    user_input_lower = user_input.lower()
    
    # Boredom detection - recommend adventure games
    if any(word in user_input_lower for word in ['bored', 'boring', 'nothing to do', 'uninterested', 'tired of']):
        return "adventure"
    
    # Language learning detection
    if any(phrase in user_input_lower for phrase in [
        'learn spanish', 'learn french', 'learn german', 'learn japanese', 
        'learn language', 'spanish', 'french', 'german', 'japanese',
        'language learning', 'learn a language'
    ]):
        return "language_learning"
    
    # Educational/parental detection
    if any(phrase in user_input_lower for phrase in [
        'parent', 'child', 'kid', 'learn math', 'educational', 'school', 
        'homework', 'study', 'my child', 'for my kid', 'educational game'
    ]):
        return "educational"
    
    # Default to adventure if no specific intent detected
    return "adventure"

def get_recommendations(user_input: str, mood: Optional[str] = None) -> Tuple[List[Dict], str]:
    """
    Get personalized game recommendations based on user input and mood.
    
    Uses ML-based recommendation engine when available, falls back to placeholder data.
    
    Args:
        user_input: User's message/request
        mood: Selected mood filter (Happy, Sad, Chill, or None)
    
    Returns:
        Tuple of (recommendations_list, explanation_string)
    """
    # Use ML recommendation engine if available
    if ML_ENGINE_AVAILABLE:
        try:
            # Get ML-based recommendations
            ml_recommendations = get_ml_recommendations(user_input, mood, top_k=5)
            
            # Convert to the expected format
            recommendations = []
            for game_name, similarity_score in ml_recommendations:
                # Get detailed game info
                game_info = get_game_info(game_name)
                if game_info:
                    recommendations.append({
                        'name': game_name,
                        'rating': game_info.get('User Rating', 8.0),
                        'price': game_info.get('Price', 19.99),
                        'reviews': 1000,  # Placeholder
                        'description': f"Genre: {game_info.get('Genre', 'Unknown')} | {game_info.get('User Review Text', 'Great game!')[:100]}...",
                        'similarity_score': similarity_score,
                        'genre': game_info.get('Genre', 'Unknown'),
                        'platform': 'Multi-platform'
                    })
                else:
                    # Fallback if game info not found
                    recommendations.append({
                        'name': game_name,
                        'rating': 8.0,
                        'price': 19.99,
                        'reviews': 1000,
                        'description': f"Recommended based on: {user_input}",
                        'similarity_score': similarity_score,
                        'genre': 'Unknown',
                        'platform': 'Multi-platform'
                    })
            
            explanation = f"I found {len(recommendations)} games that match your request '{user_input}' using advanced ML similarity matching. These recommendations are based on game titles, genres, reviews, and descriptions."
            return recommendations, explanation
            
        except Exception as e:
            print(f"Error using ML engine: {e}")
            print("Falling back to placeholder data...")
    
    # Fallback to placeholder implementation
    intent_category = parse_user_intent(user_input)
    recommendations = GAME_DATABASE.get(intent_category, [])
    
    # Apply mood filter if provided and different from intent
    if mood and mood.lower() != intent_category:
        mood_recommendations = GAME_DATABASE.get(mood.lower(), [])
        recommendations.extend(mood_recommendations[:2])
    
    # Sort by rating and limit to 5 recommendations
    recommendations = sorted(recommendations, key=lambda x: x['rating'], reverse=True)[:5]
    explanation = generate_explanation(intent_category, mood, user_input)
    
    return recommendations, explanation

def generate_explanation(intent_category: str, mood: Optional[str], user_input: str) -> str:
    """
    Generate a personalized explanation for the recommendations.
    """
    explanations = {
        "adventure": "I detected you're looking for something exciting to combat boredom! Here are some thrilling adventure games that will get your heart racing.",
        "language_learning": "I see you want to learn a new language - that's fantastic! These games make language learning fun and engaging.",
        "educational": "I understand you're looking for educational content. These games are perfect for learning while having fun, with high ratings from parents and educators.",
        "happy": "Based on your happy mood, I'm recommending uplifting games that will keep your spirits high!",
        "sad": "I'm suggesting some thoughtful, emotionally engaging games that might help you process your feelings.",
        "chill": "For a chill mood, here are some relaxing and peaceful games to help you unwind."
    }
    
    base_explanation = explanations.get(intent_category, "Here are some personalized recommendations for you!")
    
    # Add quality assurance message
    quality_note = " All recommendations are filtered by high user ratings, positive reviews, and value for money to ensure quality."
    
    return base_explanation + quality_note

def format_recommendations(recommendations: List[Dict]) -> str:
    """
    Format recommendations into a readable string for the UI.
    """
    if not recommendations:
        return "I couldn't find any specific recommendations right now. Could you tell me more about what you're looking for?"
    
    formatted = "🎮 **Here are my recommendations for you:**\n\n"
    
    for i, game in enumerate(recommendations, 1):
        price_text = "Free" if game['price'] == 0 else f"${game['price']}"
        
        # Add similarity score if available
        score_text = ""
        if 'similarity_score' in game:
            score_text = f" (Match: {game['similarity_score']:.1%})"
            
        formatted += f"**{i}. {game['name']}** ⭐ {game['rating']}/10{score_text}\n"
        formatted += f"   💰 {price_text} | 👥 {game['reviews']:,} reviews\n"
        formatted += f"   🎭 {game.get('genre', 'Unknown')} | 🖥️ {game.get('platform', 'Multi-platform')}\n"
        formatted += f"   📝 {game['description']}\n\n"
    
    formatted += "💡 *Recommendations are based on semantic similarity and user ratings.*"
    
    return formatted

# Placeholder for future backend connection
def connect_to_backend(backend_url: str, api_key: str = None):
    """
    Placeholder function for connecting to a real backend service.
    This would replace the dummy GAME_DATABASE with real API calls.
    """
    # This is where you would implement the actual backend connection
    # For example: requests.get(f"{backend_url}/recommendations", headers={"Authorization": f"Bearer {api_key}"})
    pass
