"""
Working Game Recommendation App
Fixed Gradio chatbot format issues.
"""

import gradio as gr
from recommendation import get_recommendations, format_recommendations
import json

# Custom CSS for a brainstorming-focused design
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
    position: relative;
    overflow: hidden;
    color: #333;
}

.brainstorm-container h3 {
    color: #1a237e;
    font-weight: 700;
    margin-bottom: 20px;
    font-size: 1.4em;
}

.brainstorm-container p {
    color: #424242;
    line-height: 1.6;
    margin-bottom: 15px;
}

.brainstorm-container strong {
    color: #0d47a1;
    font-weight: 600;
}

.brainstorm-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
    animation: float 8s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-15px) rotate(180deg); }
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
    color: #495057;
}

.input-section label {
    color: #343a40;
    font-weight: 600;
    font-size: 1.1em;
}

.input-section .gr-textbox {
    color: #212529;
}

.input-section .gr-textbox::placeholder {
    color: #6c757d;
    font-style: italic;
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
    color: #333;
}

.output-section label {
    color: #495057;
    font-weight: 600;
    font-size: 1.1em;
}

.brainstorm-ideas {
    background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    border-left: 5px solid #2196f3;
    position: relative;
    color: #1565c0;
}

.brainstorm-ideas h4 {
    color: #0d47a1;
    font-weight: 700;
    margin-bottom: 15px;
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
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
    color: #333;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.idea-item:hover {
    background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
    transform: translateX(10px) scale(1.02);
    border-color: #667eea;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    color: #1a237e;
}

.idea-item::before {
    content: '✨';
    margin-right: 10px;
    font-size: 1.1em;
}

.exploration-prompt {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    border-left: 5px solid #ff9800;
    font-style: italic;
    color: #e65100;
    font-weight: 500;
}

.exploration-prompt::before {
    content: '🔍';
    margin-right: 10px;
    font-size: 1.2em;
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
"""

def create_welcome_message():
    """Create a brainstorming-focused welcome message."""
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
                    <h1>🧠 GameBot Brainstorming</h1>
                    <p>Creative Gaming Discovery & Exploration</p>
                    <p>Where Every Question Leads to New Possibilities</p>
                </div>
                """)
        
        # Mood selector
        with gr.Row():
            with gr.Column():
                gr.HTML('<div class="input-section">')
                mood_selector = gr.Dropdown(
                    choices=["Any", "Excited", "Curious", "Creative", "Bored", "Stressed", "Adventurous"],
                    value="Any",
                    label="🎭 What's your creative mood today?",
                    info="This helps me tailor my brainstorming approach to your energy!"
                )
                gr.HTML('</div>')
        
        # Chat interface
        with gr.Row():
            with gr.Column(scale=2):
                gr.HTML('<div class="input-section">')
                
                # Main input
                msg = gr.Textbox(
                    placeholder="Tell me what you're curious about! For example: 'I want to discover games I've never heard of' or 'I'm looking for games that could inspire my creativity' or 'I want to explore genres I've never tried'",
                    label="💭 What are you curious about?",
                    lines=3,
                    max_lines=5
                )
                
                # Action buttons
                with gr.Row():
                    send_btn = gr.Button("🧠 Brainstorm Ideas", variant="primary", elem_classes=["btn-primary"])
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary", elem_classes=["btn-secondary"])
                
                gr.HTML('</div>')
                
                # Brainstorming ideas box
                gr.HTML('<div class="brainstorm-ideas">')
                gr.HTML('<h4>💡 Try these brainstorming prompts:</h4>')
                suggestions_html = """
                <div class='idea-item' onclick='document.querySelector("textarea").value=this.textContent; document.querySelector("textarea").dispatchEvent(new Event("input"));'>I want to discover games I've never heard of</div>
                <div class='idea-item' onclick='document.querySelector("textarea").value=this.textContent; document.querySelector("textarea").dispatchEvent(new Event("input"));'>I'm curious about games that could teach me something</div>
                <div class='idea-item' onclick='document.querySelector("textarea").value=this.textContent; document.querySelector("textarea").dispatchEvent(new Event("input"));'>I want to explore genres I've never tried</div>
                <div class='idea-item' onclick='document.querySelector("textarea").value=this.textContent; document.querySelector("textarea").dispatchEvent(new Event("input"));'>I'm looking for games that could inspire my creativity</div>
                <div class='idea-item' onclick='document.querySelector("textarea").value=this.textContent; document.querySelector("textarea").dispatchEvent(new Event("input"));'>I want to find games that could surprise me</div>
                <div class='idea-item' onclick='document.querySelector("textarea").value=this.textContent; document.querySelector("textarea").dispatchEvent(new Event("input"));'>I'm interested in games that could help me relax in a unique way</div>
                """
                gr.HTML(suggestions_html)
                gr.HTML('</div>')
            
            with gr.Column(scale=3):
                gr.HTML('<div class="output-section">')
                
                # Output display
                output_text = gr.Textbox(
                    value=create_welcome_message(),
                    label="🧠 GameBot's Creative Response",
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
