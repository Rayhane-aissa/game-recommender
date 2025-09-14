"""
Interactive Game Recommendation App
Enhanced with natural language understanding and conversational AI.
"""

import gradio as gr
from recommendation import get_recommendations, format_recommendations
import re
import random

# Custom CSS for a modern, interactive design
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.chat-container {
    background: white;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    padding: 25px;
    margin: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}

.header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.header h1 {
    margin: 0;
    font-size: 3em;
    font-weight: 300;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.header p {
    margin: 10px 0 0 0;
    font-size: 1.2em;
    opacity: 0.9;
}

.input-section {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    border: 2px solid #e9ecef;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    padding: 15px 30px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
    background: #6c757d;
    border: none;
    color: white;
    padding: 12px 25px;
    border-radius: 25px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-secondary:hover {
    background: #5a6268;
    transform: translateY(-2px);
}

.output-section {
    background: white;
    border-radius: 15px;
    padding: 20px;
    border: 2px solid #e9ecef;
    min-height: 400px;
}

.suggestion-box {
    background: #e3f2fd;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    border-left: 4px solid #2196f3;
}

.suggestion-box h4 {
    margin: 0 0 10px 0;
    color: #1976d2;
}

.suggestion-item {
    background: white;
    padding: 8px 12px;
    margin: 5px 0;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid #e0e0e0;
}

.suggestion-item:hover {
    background: #f0f0f0;
    transform: translateX(5px);
}

.mood-indicator {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 500;
    margin: 5px;
}

.mood-happy { background: #d4edda; color: #155724; }
.mood-sad { background: #f8d7da; color: #721c24; }
.mood-chill { background: #d1ecf1; color: #0c5460; }
.mood-any { background: #e2e3e5; color: #383d41; }
"""

def create_welcome_message():
    """Create an engaging welcome message with suggestions."""
    return """🤖 **Welcome to GameBot!** 👋

I'm your intelligent game recommendation assistant! I can understand natural language and help you find the perfect games based on your mood, interests, and preferences.

**💡 Try asking me anything like:**
• "I'm feeling stressed and need something relaxing"
• "I want to play something with my friends tonight"
• "I'm in the mood for a good story-driven game"
• "I have 30 minutes to kill, what should I play?"
• "I want to learn something new through gaming"
• "I'm looking for a challenging puzzle game"
• "I need something to cheer me up"

**🎮 I understand:**
✨ **Moods & Emotions** - Happy, sad, stressed, excited, bored
🎯 **Time Constraints** - Quick games, long sessions, casual play
👥 **Social Preferences** - Solo, multiplayer, co-op, competitive
📚 **Learning Goals** - Educational, skill-building, creative
🎨 **Genres & Styles** - Any game type you can think of!

**Just type naturally and I'll understand what you're looking for!** 🚀"""

def analyze_user_intent(text):
    """Analyze user input to understand their intent and extract key information."""
    text_lower = text.lower()
    
    # Extract mood indicators
    mood_indicators = {
        'happy': ['happy', 'cheerful', 'excited', 'joyful', 'upbeat', 'positive', 'good mood'],
        'sad': ['sad', 'depressed', 'down', 'blue', 'melancholy', 'gloomy', 'feeling low'],
        'stressed': ['stressed', 'anxious', 'overwhelmed', 'tense', 'worried', 'pressure'],
        'chill': ['chill', 'relaxed', 'calm', 'peaceful', 'zen', 'mellow', 'laid back'],
        'bored': ['bored', 'boring', 'nothing to do', 'uninterested', 'tired of', 'stuck'],
        'excited': ['excited', 'pumped', 'thrilled', 'energetic', 'hyped', 'ready for action']
    }
    
    detected_mood = 'any'
    for mood, keywords in mood_indicators.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_mood = mood
            break
    
    # Extract time constraints
    time_indicators = {
        'quick': ['quick', 'fast', 'short', '30 minutes', '15 minutes', 'brief', 'casual'],
        'long': ['long', 'extended', 'hours', 'all day', 'marathon', 'deep dive'],
        'any': ['any time', 'flexible', 'whenever']
    }
    
    time_preference = 'any'
    for time_type, keywords in time_indicators.items():
        if any(keyword in text_lower for keyword in keywords):
            time_preference = time_type
            break
    
    # Extract social preferences
    social_indicators = {
        'solo': ['alone', 'solo', 'by myself', 'single player', 'personal'],
        'multiplayer': ['friends', 'multiplayer', 'together', 'co-op', 'social', 'with others'],
        'competitive': ['competitive', 'vs', 'against', 'challenge', 'battle', 'fight']
    }
    
    social_preference = 'any'
    for social_type, keywords in social_indicators.items():
        if any(keyword in text_lower for keyword in keywords):
            social_preference = social_type
            break
    
    # Extract learning goals
    learning_indicators = ['learn', 'education', 'skill', 'practice', 'improve', 'study', 'knowledge']
    wants_learning = any(indicator in text_lower for indicator in learning_indicators)
    
    # Extract genre preferences
    genre_indicators = {
        'adventure': ['adventure', 'explore', 'journey', 'quest', 'discovery'],
        'puzzle': ['puzzle', 'brain', 'think', 'logic', 'challenge', 'problem solving'],
        'action': ['action', 'fast', 'intense', 'thrilling', 'exciting', 'adrenaline'],
        'strategy': ['strategy', 'planning', 'tactical', 'thinking', 'management'],
        'creative': ['creative', 'build', 'design', 'art', 'craft', 'create'],
        'story': ['story', 'narrative', 'plot', 'characters', 'drama', 'cinematic']
    }
    
    detected_genres = []
    for genre, keywords in genre_indicators.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_genres.append(genre)
    
    return {
        'mood': detected_mood,
        'time': time_preference,
        'social': social_preference,
        'learning': wants_learning,
        'genres': detected_genres,
        'original_text': text
    }

def generate_personalized_response(intent_analysis, recommendations, explanation):
    """Generate a personalized, conversational response based on user intent."""
    mood = intent_analysis['mood']
    time_pref = intent_analysis['time']
    social_pref = intent_analysis['social']
    learning = intent_analysis['learning']
    genres = intent_analysis['genres']
    
    # Create mood-based greeting
    mood_greetings = {
        'happy': "😊 I can see you're in a great mood!",
        'sad': "💙 I understand you're feeling down. Let me help you find something uplifting.",
        'stressed': "🧘 I can tell you're feeling stressed. Let's find something to help you unwind.",
        'chill': "😌 Perfect! You're looking for something relaxing.",
        'bored': "😴 I hear you're feeling bored. Let's find something exciting!",
        'excited': "🎉 I love your energy! Let's find something that matches your excitement!",
        'any': "🎮 Great! Let me help you find the perfect game."
    }
    
    greeting = mood_greetings.get(mood, mood_greetings['any'])
    
    # Add context about their preferences
    context_parts = []
    
    if time_pref == 'quick':
        context_parts.append("I'll focus on games you can enjoy in short sessions")
    elif time_pref == 'long':
        context_parts.append("I'll recommend games perfect for longer gaming sessions")
    
    if social_pref == 'solo':
        context_parts.append("I'll suggest great single-player experiences")
    elif social_pref == 'multiplayer':
        context_parts.append("I'll find games perfect for playing with friends")
    elif social_pref == 'competitive':
        context_parts.append("I'll recommend competitive games to challenge yourself")
    
    if learning:
        context_parts.append("I'll include educational and skill-building games")
    
    if genres:
        genre_text = ", ".join(genres)
        context_parts.append(f"I'll focus on {genre_text} games")
    
    context = ". ".join(context_parts) + "." if context_parts else ""
    
    # Generate the full response
    response = f"{greeting}\n\n"
    if context:
        response += f"**Based on what you told me:** {context}\n\n"
    
    response += f"**Here are my recommendations:**\n\n{format_recommendations(recommendations)}"
    
    # Add personalized closing
    closings = [
        "Hope you find something you love! 🎮",
        "Let me know if you'd like more suggestions! ✨",
        "Enjoy your gaming! 🚀",
        "Happy gaming! 🎯",
        "Have fun exploring these games! 🌟"
    ]
    
    response += f"\n\n{random.choice(closings)}"
    
    return response

def get_smart_recommendations(user_input, mood):
    """Get intelligent recommendations based on natural language understanding."""
    # Analyze the user's intent
    intent_analysis = analyze_user_intent(user_input)
    
    # Get recommendations using the analyzed intent
    recommendations, explanation = get_recommendations(user_input, mood)
    
    # Generate personalized response
    if recommendations:
        response = generate_personalized_response(intent_analysis, recommendations, explanation)
    else:
        response = f"🤖 **GameBot:** I understand you're looking for something, but I need a bit more information to give you the best recommendations.\n\n**Could you tell me more about:**\n• What kind of experience you're seeking?\n• How much time you have?\n• Whether you want to play alone or with others?\n• Any specific genres or styles you prefer?\n\n**Or try asking me something like:**\n• \"I want something relaxing for 30 minutes\"\n• \"I need an exciting game to play with friends\"\n• \"I'm looking for a challenging puzzle game\""
    
    return response

def get_conversation_suggestions():
    """Generate dynamic conversation suggestions based on common patterns."""
    suggestions = [
        "I'm bored and want something exciting",
        "I need something relaxing after work",
        "I want to play with my friends tonight",
        "I have 30 minutes to kill",
        "I'm feeling sad and need cheering up",
        "I want to learn something new",
        "I'm looking for a good story game",
        "I need a challenging puzzle game",
        "I want something creative to build",
        "I'm stressed and need to unwind"
    ]
    return random.sample(suggestions, 5)

def main():
    """Create and launch the interactive Gradio interface."""
    
    with gr.Blocks(css=custom_css, title="GameBot - Interactive AI Game Recommendations") as demo:
        
        # Header section
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="header">
                    <h1>🎮 GameBot</h1>
                    <p>Interactive AI Game Recommendation Assistant</p>
                    <p>Powered by Natural Language Understanding & Machine Learning</p>
                </div>
                """)
        
        # Main interface
        with gr.Row():
            with gr.Column(scale=2):
                gr.HTML('<div class="input-section">')
                
                # Mood selector
                mood_selector = gr.Dropdown(
                    choices=["Any", "Happy", "Sad", "Chill", "Stressed", "Bored", "Excited"],
                    value="Any",
                    label="🎭 How are you feeling? (Optional - I'll also detect your mood from your message!)",
                    info="This helps me personalize recommendations even better!"
                )
                
                # Main input
                user_input = gr.Textbox(
                    placeholder="Tell me anything! For example: 'I'm stressed and need something relaxing' or 'I want to play with friends tonight' or 'I have 30 minutes and want something exciting'",
                    label="💬 What are you looking for?",
                    lines=3,
                    max_lines=5
                )
                
                # Action buttons
                with gr.Row():
                    get_recs_btn = gr.Button("🎯 Get Recommendations", variant="primary", elem_classes=["btn-primary"])
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary", elem_classes=["btn-secondary"])
                
                gr.HTML('</div>')
                
                # Suggestions box
                gr.HTML('<div class="suggestion-box">')
                gr.HTML('<h4>💡 Try asking me:</h4>')
                suggestions_html = "<div class='suggestion-item' onclick='document.querySelector(\"textarea\").value=this.textContent; document.querySelector(\"textarea\").dispatchEvent(new Event(\"input\"));'>I'm bored and want something exciting</div>"
                for suggestion in get_conversation_suggestions()[1:]:
                    suggestions_html += f"<div class='suggestion-item' onclick='document.querySelector(\"textarea\").value=this.textContent; document.querySelector(\"textarea\").dispatchEvent(new Event(\"input\"));'>{suggestion}</div>"
                gr.HTML(suggestions_html)
                gr.HTML('</div>')
            
            with gr.Column(scale=3):
                gr.HTML('<div class="output-section">')
                
                # Output display
                output_text = gr.Textbox(
                    value=create_welcome_message(),
                    label="🤖 GameBot's Response",
                    lines=20,
                    max_lines=25,
                    interactive=False,
                    show_copy_button=True,
                    elem_classes=["output-section"]
                )
                
                gr.HTML('</div>')
        
        # Information panel
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="chat-container">
                    <h3>🧠 How GameBot Understands You</h3>
                    <p><strong>Natural Language Processing:</strong> I analyze your messages to understand your mood, preferences, time constraints, and social needs.</p>
                    <p><strong>Context Awareness:</strong> I consider multiple factors like whether you want to learn, relax, compete, or just have fun.</p>
                    <p><strong>Personalized Responses:</strong> Every recommendation is tailored to your specific situation and preferences.</p>
                    <p><strong>Conversational AI:</strong> I understand free-form text - no need to use specific phrases or keywords!</p>
                    <p><strong>Smart Suggestions:</strong> I provide dynamic conversation starters based on common gaming needs.</p>
                </div>
                """)
        
        # Event handlers
        def process_request(input_text, mood):
            if not input_text.strip():
                return create_welcome_message()
            return get_smart_recommendations(input_text, mood)
        
        def clear_conversation():
            return create_welcome_message()
        
        # Connect the interface
        get_recs_btn.click(
            process_request, 
            inputs=[user_input, mood_selector], 
            outputs=output_text
        )
        
        user_input.submit(
            process_request, 
            inputs=[user_input, mood_selector], 
            outputs=output_text
        )
        
        clear_btn.click(
            clear_conversation, 
            inputs=None, 
            outputs=output_text
        )
    
    # Launch the interface
    demo.launch(
        server_name="127.0.0.1",
        server_port=7863,
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
