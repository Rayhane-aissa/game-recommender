"""
Working Game Recommendation App
Fixed Gradio chatbot format issues.
"""

import gradio as gr
from recommendation import get_recommendations, format_recommendations
import json

# Custom CSS for a clean design
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.chat-container {
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    padding: 20px;
    margin: 20px;
}

.header {
    text-align: center;
    background: white;
    padding: 30px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.header h1 {
    color: #667eea;
    margin: 0;
    font-size: 2.5em;
    font-weight: 300;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    padding: 12px 25px;
    border-radius: 25px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}
"""

def create_welcome_message():
    """Create a welcoming initial message from the bot."""
    return """🤖 **Welcome to GameBot!** 👋

I'm your personal game recommendation assistant, here to help you discover amazing games tailored just for you! 

**How I work:**
✨ **Smart Analysis**: I analyze your requests to understand what you're looking for
🎯 **Personalized**: Recommendations based on your specific needs and mood
⭐ **Quality Focused**: High ratings, positive reviews, and great value
🎮 **Diverse Selection**: From adventure to educational games

**Try saying things like:**
• "I'm bored and want something exciting"
• "I want to learn Spanish through games"
• "I'm a parent looking for math games for my 8-year-old"
• "I'm feeling sad and need something comforting"

What can I help you find today? 🎮"""

def get_game_recommendations(message, mood):
    """Get game recommendations and format the response."""
    try:
        recommendations, explanation = get_recommendations(message, mood)
        
        if recommendations:
            formatted_recs = format_recommendations(recommendations)
            response = f"🤖 **GameBot:** {explanation}\n\n{formatted_recs}"
        else:
            response = f"🤖 **GameBot:** {explanation}\n\nI'd love to help you find the perfect game! Could you tell me more about what you're looking for?"
        
        return response
    except Exception as e:
        return f"🤖 **GameBot:** Sorry, I encountered an error: {str(e)}\n\nPlease try again with a different request."

def main():
    """Create and launch the Gradio interface."""
    
    with gr.Blocks(css=custom_css, title="GameBot - AI Game Recommendations") as demo:
        
        # Header section
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="header">
                    <h1>🎮 GameBot</h1>
                    <p>AI-Powered Game Recommendation Assistant</p>
                    <p>Powered by Machine Learning from Jupyter Notebook</p>
                </div>
                """)
        
        # Mood selector
        with gr.Row():
            with gr.Column():
                mood_selector = gr.Dropdown(
                    choices=["Happy", "Sad", "Chill", "Any"],
                    value="Any",
                    label="🎭 How are you feeling today? (Optional)",
                    info="This helps me personalize recommendations even better!"
                )
        
        # Chat interface
        with gr.Row():
            with gr.Column(scale=3):
                gr.HTML('<div class="chat-container">')
                
                # Use a simple textbox for output instead of chatbot
                output_text = gr.Textbox(
                    value=create_welcome_message(),
                    label="💬 GameBot Response",
                    lines=15,
                    max_lines=20,
                    interactive=False,
                    show_copy_button=True
                )
                
                msg = gr.Textbox(
                    placeholder="Tell me what you're looking for... (e.g., 'I'm bored', 'I want to learn Spanish', 'I need games for my child')",
                    label="Your message",
                    lines=2,
                    max_lines=4
                )
                
                with gr.Row():
                    send_btn = gr.Button("Get Recommendations", variant="primary", elem_classes=["btn-primary"])
                    clear_btn = gr.Button("Clear", variant="secondary")
                gr.HTML('</div>')
        
        # Information panel
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="chat-container">
                    <h3>🔍 How GameBot Works</h3>
                    <p><strong>Smart Analysis:</strong> I analyze your messages to understand what you really want - whether it's adventure, learning, or relaxation.</p>
                    <p><strong>Quality Assurance:</strong> All recommendations are filtered by user ratings, review quality, and value for money.</p>
                    <p><strong>Personal Touch:</strong> Your mood and goals are considered together for the most relevant suggestions.</p>
                    <p><strong>ML-Powered:</strong> Uses advanced machine learning from the Jupyter notebook for intelligent recommendations.</p>
                </div>
                """)
        
        # Event handlers
        def process_message(message, mood):
            if not message.strip():
                return create_welcome_message()
            return get_game_recommendations(message, mood)
        
        def clear_conversation():
            return create_welcome_message()
        
        # Connect the interface
        send_btn.click(
            process_message, 
            inputs=[msg, mood_selector], 
            outputs=output_text
        )
        
        msg.submit(
            process_message, 
            inputs=[msg, mood_selector], 
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
        server_port=7862,
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
