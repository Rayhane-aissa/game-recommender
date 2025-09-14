"""
Brainstorming Game Recommendation App
Interactive AI that helps users discover and explore new gaming possibilities.
"""

import gradio as gr
from recommendation import get_recommendations, format_recommendations
import re
import random

# Custom CSS for a creative, brainstorming-focused design
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.brainstorm-container {
    background: white;
    border-radius: 25px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    padding: 30px;
    margin: 20px;
    border: 2px solid rgba(255,255,255,0.3);
}

.header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 50px;
    border-radius: 25px;
    margin-bottom: 30px;
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

.header h1 {
    margin: 0;
    font-size: 3.5em;
    font-weight: 300;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}

.header p {
    margin: 15px 0 0 0;
    font-size: 1.3em;
    opacity: 0.9;
    position: relative;
    z-index: 1;
}

.input-section {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
    border: 3px solid #dee2e6;
    position: relative;
}

.input-section::before {
    content: '💡';
    position: absolute;
    top: -15px;
    left: 20px;
    background: white;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 1.2em;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    padding: 18px 35px;
    border-radius: 35px;
    font-weight: 700;
    font-size: 18px;
    transition: all 0.4s ease;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.btn-primary:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
    background: #6c757d;
    border: none;
    color: white;
    padding: 15px 30px;
    border-radius: 30px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-secondary:hover {
    background: #5a6268;
    transform: translateY(-2px);
}

.output-section {
    background: white;
    border-radius: 20px;
    padding: 25px;
    border: 3px solid #e9ecef;
    min-height: 500px;
    position: relative;
}

.brainstorm-ideas {
    background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    border-left: 5px solid #2196f3;
    position: relative;
}

.brainstorm-ideas::before {
    content: '🧠';
    position: absolute;
    top: -10px;
    left: 20px;
    background: white;
    padding: 5px 10px;
    border-radius: 10px;
    font-size: 1.1em;
}

.idea-item {
    background: white;
    padding: 12px 18px;
    margin: 8px 0;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid #e0e0e0;
    font-weight: 500;
    position: relative;
}

.idea-item:hover {
    background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
    transform: translateX(10px) scale(1.02);
    border-color: #667eea;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
}

.idea-item::before {
    content: '✨';
    margin-right: 10px;
    font-size: 1.1em;
}

.mood-indicator {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 25px;
    font-size: 0.95em;
    font-weight: 600;
    margin: 5px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.mood-happy { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); color: #155724; }
.mood-sad { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); color: #721c24; }
.mood-chill { background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); color: #0c5460; }
.mood-excited { background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); color: #856404; }
.mood-creative { background: linear-gradient(135deg, #e2e3e5 0%, #d6d8db 100%); color: #383d41; }
.mood-any { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); color: #495057; }

.exploration-prompt {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    border-left: 5px solid #ff9800;
    font-style: italic;
    color: #e65100;
}

.exploration-prompt::before {
    content: '🔍';
    margin-right: 10px;
    font-size: 1.2em;
}
"""

def create_brainstorming_welcome():
    """Create an engaging brainstorming-focused welcome message."""
    return """🧠 **Welcome to GameBot Brainstorming!** 🚀

I'm your creative gaming companion, here to help you **discover**, **explore**, and **brainstorm** amazing gaming possibilities you never knew existed!

**🎯 Let's Brainstorm Together!**

**💭 Tell me what's on your mind:**
• "I'm curious about games that could teach me something new"
• "I want to explore genres I've never tried before"
• "I'm looking for games that could help me relax in a unique way"
• "I want to discover games that my friends and I could enjoy together"
• "I'm interested in games that could challenge my creativity"
• "I want to find games that could transport me to different worlds"

**🌟 Brainstorming Features:**
✨ **Creative Discovery** - Find games you never knew you wanted
🎨 **Genre Exploration** - Venture into uncharted gaming territories
🤝 **Social Brainstorming** - Discover multiplayer experiences
🧩 **Problem-Solving** - Find games that match your specific needs
🎪 **Adventure Mapping** - Plan your next gaming journey
💡 **Idea Generation** - Get inspired by unexpected recommendations

**Ready to explore the infinite possibilities of gaming? Let's brainstorm!** 🎮✨"""

def analyze_creative_intent(text):
    """Analyze user input for creative brainstorming opportunities."""
    text_lower = text.lower()
    
    # Creative exploration indicators
    creative_indicators = {
        'discovery': ['discover', 'explore', 'new', 'never tried', 'unfamiliar', 'unknown', 'curious', 'wonder'],
        'learning': ['learn', 'teach', 'education', 'skill', 'improve', 'develop', 'master', 'understand'],
        'social': ['friends', 'together', 'social', 'multiplayer', 'co-op', 'party', 'group', 'team'],
        'creative': ['creative', 'build', 'design', 'art', 'craft', 'create', 'imagine', 'invent'],
        'challenge': ['challenge', 'difficult', 'hard', 'complex', 'advanced', 'expert', 'master'],
        'relaxation': ['relax', 'calm', 'peaceful', 'zen', 'meditation', 'stress', 'unwind', 'chill'],
        'adventure': ['adventure', 'explore', 'journey', 'quest', 'discover', 'world', 'travel'],
        'story': ['story', 'narrative', 'plot', 'characters', 'drama', 'cinematic', 'emotional'],
        'puzzle': ['puzzle', 'brain', 'think', 'logic', 'problem', 'solve', 'mystery'],
        'action': ['action', 'fast', 'intense', 'thrilling', 'exciting', 'adrenaline', 'rush']
    }
    
    detected_themes = []
    for theme, keywords in creative_indicators.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_themes.append(theme)
    
    # Mood analysis
    mood_indicators = {
        'excited': ['excited', 'pumped', 'thrilled', 'energetic', 'hyped', 'ready'],
        'curious': ['curious', 'wonder', 'interested', 'intrigued', 'fascinated'],
        'bored': ['bored', 'tired', 'stuck', 'uninspired', 'routine'],
        'stressed': ['stressed', 'overwhelmed', 'anxious', 'tense', 'pressure'],
        'creative': ['creative', 'inspired', 'artistic', 'imaginative', 'innovative'],
        'adventurous': ['adventurous', 'bold', 'daring', 'brave', 'explorer']
    }
    
    detected_mood = 'any'
    for mood, keywords in mood_indicators.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_mood = mood
            break
    
    return {
        'themes': detected_themes,
        'mood': detected_mood,
        'original_text': text,
        'is_exploratory': any(word in text_lower for word in ['explore', 'discover', 'new', 'try', 'brainstorm', 'ideas'])
    }

def generate_brainstorming_prompts(intent_analysis):
    """Generate creative brainstorming prompts based on user intent."""
    themes = intent_analysis['themes']
    mood = intent_analysis['mood']
    
    prompts = []
    
    # Theme-based prompts
    if 'discovery' in themes:
        prompts.extend([
            "What if we explored games from completely different cultures?",
            "How about games that combine genres in unexpected ways?",
            "What about indie games that big studios don't make?"
        ])
    
    if 'learning' in themes:
        prompts.extend([
            "What if gaming could teach you a real-world skill?",
            "How about games that make learning feel like play?",
            "What about games that challenge your assumptions?"
        ])
    
    if 'social' in themes:
        prompts.extend([
            "What if we found games that bring people together in new ways?",
            "How about games that create shared experiences?",
            "What about games that build communities?"
        ])
    
    if 'creative' in themes:
        prompts.extend([
            "What if we found games that let you express yourself?",
            "How about games that inspire your creativity?",
            "What about games that are works of art themselves?"
        ])
    
    # Mood-based prompts
    if mood == 'excited':
        prompts.extend([
            "What if we found games that match your energy level?",
            "How about games that get your heart racing?",
            "What about games that make you feel alive?"
        ])
    
    if mood == 'curious':
        prompts.extend([
            "What if we explored games that answer your questions?",
            "How about games that satisfy your curiosity?",
            "What about games that make you wonder?"
        ])
    
    if mood == 'bored':
        prompts.extend([
            "What if we found games that break your routine?",
            "How about games that surprise you?",
            "What about games that shake things up?"
        ])
    
    # Default creative prompts
    if not prompts:
        prompts = [
            "What if we explored games you've never heard of?",
            "How about games that challenge your expectations?",
            "What about games that tell stories in new ways?",
            "What if we found games that match your personality?",
            "How about games that create new experiences?"
        ]
    
    return random.sample(prompts, min(3, len(prompts)))

def generate_brainstorming_response(intent_analysis, recommendations, explanation):
    """Generate a creative, brainstorming-focused response."""
    themes = intent_analysis['themes']
    mood = intent_analysis['mood']
    is_exploratory = intent_analysis['is_exploratory']
    
    # Creative greeting based on analysis
    if is_exploratory:
        greeting = "🧠 **Great! Let's dive into some creative exploration!**"
    elif mood == 'curious':
        greeting = "🔍 **I love your curiosity! Let me show you some fascinating possibilities!**"
    elif mood == 'creative':
        greeting = "🎨 **Perfect! Let's brainstorm some creative gaming adventures!**"
    else:
        greeting = "💡 **Excellent! Let me help you discover some amazing gaming possibilities!**"
    
    # Generate brainstorming prompts
    prompts = generate_brainstorming_prompts(intent_analysis)
    
    # Build the response
    response = f"{greeting}\n\n"
    
    # Add theme-based context
    if themes:
        theme_text = ", ".join(themes)
        response += f"**I can see you're interested in:** {theme_text.title()}\n\n"
    
    # Add the recommendations
    response += f"**Here are some games that might spark your imagination:**\n\n{format_recommendations(recommendations)}"
    
    # Add brainstorming prompts
    if prompts:
        response += f"\n\n**🧠 Let's brainstorm further:**\n"
        for i, prompt in enumerate(prompts, 1):
            response += f"\n**{i}.** {prompt}"
    
    # Add creative closing
    closings = [
        "Keep exploring and let your curiosity guide you! 🌟",
        "The gaming world is full of surprises - keep discovering! 🚀",
        "Every game is a new adventure waiting to happen! 🎮",
        "Let your imagination run wild with these possibilities! ✨",
        "The best games are often the ones you least expect! 🎯"
    ]
    
    response += f"\n\n{random.choice(closings)}"
    
    return response

def get_brainstorming_recommendations(user_input, mood):
    """Get creative, brainstorming-focused recommendations."""
    # Analyze the user's creative intent
    intent_analysis = analyze_creative_intent(user_input)
    
    # Get recommendations
    recommendations, explanation = get_recommendations(user_input, mood)
    
    # Generate brainstorming response
    if recommendations:
        response = generate_brainstorming_response(intent_analysis, recommendations, explanation)
    else:
        response = f"🧠 **Let's brainstorm together!**\n\nI can see you're looking for something, but I need a bit more to spark some creative ideas!\n\n**💭 Try asking me things like:**\n• \"I want to discover games I've never heard of\"\n• \"I'm curious about games that could teach me something\"\n• \"I want to explore genres I've never tried\"\n• \"I'm looking for games that could inspire my creativity\"\n• \"I want to find games that could surprise me\"\n\n**🎯 The more specific you are about what you're curious about, the better I can help you brainstorm!**"
    
    return response

def get_brainstorming_suggestions():
    """Generate dynamic brainstorming conversation starters."""
    suggestions = [
        "I want to discover games I've never heard of",
        "I'm curious about games that could teach me something",
        "I want to explore genres I've never tried",
        "I'm looking for games that could inspire my creativity",
        "I want to find games that could surprise me",
        "I'm interested in games that could help me relax in a unique way",
        "I want to discover games that my friends and I could enjoy together",
        "I'm looking for games that could challenge my creativity",
        "I want to find games that could transport me to different worlds",
        "I'm curious about games that combine different genres",
        "I want to explore indie games that big studios don't make",
        "I'm interested in games that could build communities"
    ]
    return random.sample(suggestions, 6)

def main():
    """Create and launch the brainstorming Gradio interface."""
    
    with gr.Blocks(css=custom_css, title="GameBot Brainstorming - Creative Gaming Discovery") as demo:
        
        # Header section
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="header">
                    <h1>🧠 GameBot Brainstorming</h1>
                    <p>Creative Gaming Discovery & Exploration</p>
                    <p>Where Every Question Leads to New Possibilities</p>
                </div>
                """)
        
        # Main interface
        with gr.Row():
            with gr.Column(scale=2):
                gr.HTML('<div class="input-section">')
                
                # Mood selector
                mood_selector = gr.Dropdown(
                    choices=["Any", "Excited", "Curious", "Creative", "Bored", "Stressed", "Adventurous"],
                    value="Any",
                    label="🎭 What's your creative mood today?",
                    info="This helps me tailor my brainstorming approach to your energy!"
                )
                
                # Main input
                user_input = gr.Textbox(
                    placeholder="Tell me what you're curious about! For example: 'I want to discover games I've never heard of' or 'I'm looking for games that could inspire my creativity' or 'I want to explore genres I've never tried'",
                    label="💭 What are you curious about?",
                    lines=4,
                    max_lines=6
                )
                
                # Action buttons
                with gr.Row():
                    brainstorm_btn = gr.Button("🧠 Brainstorm Ideas", variant="primary", elem_classes=["btn-primary"])
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary", elem_classes=["btn-secondary"])
                
                gr.HTML('</div>')
                
                # Brainstorming ideas box
                gr.HTML('<div class="brainstorm-ideas">')
                gr.HTML('<h4>💡 Try these brainstorming prompts:</h4>')
                suggestions_html = ""
                for suggestion in get_brainstorming_suggestions():
                    suggestions_html += f"<div class='idea-item' onclick='document.querySelector(\"textarea\").value=this.textContent; document.querySelector(\"textarea\").dispatchEvent(new Event(\"input\"));'>{suggestion}</div>"
                gr.HTML(suggestions_html)
                gr.HTML('</div>')
            
            with gr.Column(scale=3):
                gr.HTML('<div class="output-section">')
                
                # Output display
                output_text = gr.Textbox(
                    value=create_brainstorming_welcome(),
                    label="🧠 GameBot's Creative Response",
                    lines=25,
                    max_lines=30,
                    interactive=False,
                    show_copy_button=True,
                    elem_classes=["output-section"]
                )
                
                gr.HTML('</div>')
        
        # Information panel
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="brainstorm-container">
                    <h3>🧠 How Brainstorming Works</h3>
                    <p><strong>Creative Discovery:</strong> I help you explore gaming possibilities you never knew existed, sparking new interests and curiosities.</p>
                    <p><strong>Theme Exploration:</strong> We dive deep into different gaming themes - from learning and creativity to social connection and adventure.</p>
                    <p><strong>Idea Generation:</strong> Every response includes brainstorming prompts to keep your creative juices flowing and inspire further exploration.</p>
                    <p><strong>Unexpected Connections:</strong> I help you discover games that connect to your interests in surprising and delightful ways.</p>
                    <p><strong>Continuous Learning:</strong> The more you explore, the better I understand your creative preferences and can suggest even more targeted discoveries.</p>
                </div>
                """)
        
        # Event handlers
        def process_brainstorming_request(input_text, mood):
            if not input_text.strip():
                return create_brainstorming_welcome()
            return get_brainstorming_recommendations(input_text, mood)
        
        def clear_conversation():
            return create_brainstorming_welcome()
        
        # Connect the interface
        brainstorm_btn.click(
            process_brainstorming_request, 
            inputs=[user_input, mood_selector], 
            outputs=output_text
        )
        
        user_input.submit(
            process_brainstorming_request, 
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
        server_port=7864,
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
