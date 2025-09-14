# 🧠 GameBot Brainstorming - AI-Powered Game Discovery Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-4.44.0-orange.svg)](https://gradio.app)
[![Machine Learning](https://img.shields.io/badge/ML-Sentence%20Transformers-green.svg)](https://huggingface.co/sentence-transformers)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Project Overview

**GameBot Brainstorming** is an innovative AI-powered game recommendation system that helps users discover new gaming experiences through creative brainstorming and intelligent exploration. Built with advanced machine learning techniques, it transforms how users find games by understanding natural language queries and providing personalized, creative recommendations.

### 🎯 Key Features

- **🧠 Creative Brainstorming Interface**: Interactive design focused on discovery and exploration
- **🤖 Advanced NLP Understanding**: Processes free-form text to understand user intent, mood, and preferences
- **🎮 Intelligent Recommendations**: Uses sentence transformers and FAISS for semantic similarity search
- **💡 Dynamic Suggestions**: Clickable brainstorming prompts to inspire new gaming discoveries
- **🎨 Beautiful UI**: Modern, animated interface with gradient backgrounds and smooth transitions
- **📊 Comprehensive Data**: Built on a rich dataset of video game reviews and metadata

## 🚀 Tech Stack

### **Frontend & Interface**
- **Gradio 4.44.0** - Modern web interface framework
- **Custom CSS** - Animated, brainstorming-focused design
- **Responsive Layout** - Works on desktop and mobile devices

### **Machine Learning & NLP**
- **Sentence Transformers 3.1.1** - State-of-the-art text embeddings
- **FAISS 1.8.0** - Efficient similarity search and retrieval
- **spaCy 3.8.7** - Advanced natural language processing
- **scikit-learn 1.7.2** - Data preprocessing and scaling

### **Data Processing**
- **Pandas 2.3.2** - Data manipulation and analysis
- **NumPy 2.2.6** - Numerical computing
- **KaggleHub 0.2.4** - Dataset management

### **Development & Deployment**
- **Python 3.10+** - Core programming language
- **Jupyter Notebook** - ML model development and experimentation

## 📁 Project Structure

```
nlp_hack/
├── 📊 game_recommender.ipynb      # Main ML notebook with data processing and model training
├── 🧠 working_app.py              # Enhanced brainstorming web interface (MAIN APP)
├── 🔧 recommendation.py           # Core recommendation logic and NLP processing
├── 📦 notebook_integration.py     # Integration layer between notebook and web app
├── 🤖 game_recommender.py         # Extracted ML backend module
├── 📋 requirements.txt            # Python dependencies
├── 📖 README.md                   # This documentation
└── 🗂️ venv/                      # Virtual environment
```

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.10 or higher
- pip package manager
- Git (for cloning the repository)

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd nlp_hack
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Download Required Models**
The app will automatically download the required spaCy model on first run:
```bash
python -c "import spacy; spacy.cli.download('en_core_web_sm')"
```

## 🚀 Running the Application

### **Main Brainstorming App (Recommended)**
```bash
python working_app.py
```
**Access at:** `http://127.0.0.1:7862`

### **Alternative Apps**
```bash
# Interactive version
python interactive_app.py
# Access at: http://127.0.0.1:7863

# Basic brainstorming version
python brainstorming_app.py
# Access at: http://127.0.0.1:7864
```

## 🎮 How to Use

### **1. Creative Discovery**
- Enter your gaming curiosity in natural language
- Examples: "I want to discover games I've never heard of", "I'm looking for games that could inspire my creativity"

### **2. Mood Selection**
- Choose your creative mood: Excited, Curious, Creative, Bored, Stressed, or Adventurous
- This helps tailor the brainstorming approach

### **3. Brainstorming Prompts**
- Click on any of the suggested prompts to auto-fill your input
- Explore different angles: learning, creativity, relaxation, social gaming

### **4. Get Recommendations**
- Click "🧠 Brainstorm Ideas" to get personalized game suggestions
- Each response includes detailed explanations and follow-up prompts

## 🧠 How It Works

### **1. Data Processing**
- Downloads video game review dataset from Kaggle
- Preprocesses text using spaCy (lemmatization, stop word removal)
- Combines multiple features: game titles, genres, reviews, age groups, graphics quality

### **2. Machine Learning Pipeline**
- **Text Embeddings**: Uses Sentence Transformers to create semantic embeddings
- **Similarity Search**: FAISS index for fast nearest neighbor search
- **Intent Parsing**: Advanced NLP to understand user mood, preferences, and goals

### **3. Recommendation Engine**
- Analyzes user input for mood, time preferences, social needs, learning goals
- Generates contextualized queries combining user intent with game features
- Returns top-k similar games with confidence scores

### **4. Brainstorming Features**
- Dynamic suggestion generation based on user patterns
- Creative prompts to inspire new gaming directions
- Contextual follow-up questions to deepen exploration

## 🎯 Key Features Explained

### **Natural Language Understanding**
The system can understand complex queries like:
- "I'm feeling stressed and need something relaxing but engaging"
- "I want to learn Spanish through games"
- "I'm looking for games that could help me be more creative"
- "I want to find games that my friends and I could enjoy together"

### **Mood-Based Recommendations**
- **Excited**: High-energy, action-packed games
- **Curious**: Educational and exploration-focused games
- **Creative**: Art, design, and building games
- **Bored**: Unique, surprising, and unconventional games
- **Stressed**: Calming, meditative, and relaxing games
- **Adventurous**: Exploration, discovery, and adventure games

### **Brainstorming Interface**
- **Clickable Ideas**: Pre-written prompts to inspire exploration
- **Visual Feedback**: Hover effects and animations
- **Progressive Discovery**: Each response builds on previous interactions

## 📊 Dataset Information

- **Source**: Kaggle Video Game Reviews Dataset
- **Size**: Comprehensive collection of game reviews and metadata
- **Features**: Game titles, genres, user reviews, age groups, graphics quality, ratings
- **Processing**: Text preprocessing, feature engineering, embedding generation

## 🔧 Technical Architecture

### **Backend Components**
1. **Data Layer**: `notebook_integration.py` - Data loading and preprocessing
2. **ML Engine**: `game_recommender.py` - Core recommendation algorithms
3. **NLP Processing**: `recommendation.py` - Intent parsing and query processing
4. **API Layer**: Web interface integration

### **Frontend Components**
1. **UI Framework**: Gradio with custom CSS
2. **Interactive Elements**: Clickable prompts, mood selectors, dynamic suggestions
3. **Visual Design**: Animated gradients, floating elements, responsive layout

## 🎨 Design Philosophy

### **Brainstorming-First Approach**
- Encourages exploration over specific requests
- Promotes creative thinking and discovery
- Provides multiple pathways to gaming experiences

### **User Experience**
- Intuitive, conversational interface
- Visual feedback and animations
- Progressive disclosure of information

### **Accessibility**
- Clear typography and contrast
- Responsive design for all devices
- Keyboard navigation support

## 🚀 Future Enhancements

### **Planned Features**
- [ ] **Multi-language Support**: Expand to other languages
- [ ] **Advanced Filtering**: Price, platform, release date filters
- [ ] **Social Features**: Share recommendations, collaborative brainstorming
- [ ] **Learning Analytics**: Track user preferences and improvement over time
- [ ] **API Integration**: Connect to gaming platforms for real-time data

### **Technical Improvements**
- [ ] **Performance Optimization**: Caching and faster model loading
- [ ] **Mobile App**: Native mobile application
- [ ] **Advanced ML**: Fine-tuned models for specific gaming genres
- [ ] **Real-time Updates**: Live data synchronization

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Development**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Areas for Contribution**
- **UI/UX Improvements**: Better designs, animations, user experience
- **ML Enhancements**: Better models, new recommendation algorithms
- **Feature Development**: New brainstorming tools, filters, integrations
- **Documentation**: Better guides, tutorials, examples
- **Testing**: Unit tests, integration tests, user testing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team
### Farah Belgheith
### Rayhane Aissa
### Kabil daami
### Aya Gaha

## 🙏 Acknowledgments

- **Kaggle Community** for the comprehensive video game dataset
- **Hugging Face** for the sentence transformer models
- **Gradio Team** for the excellent web interface framework
- **spaCy Team** for the powerful NLP library
- **Open Source Community** for the amazing tools and libraries

## 🎮 Try It Now!

Ready to discover your next favorite game? Start brainstorming with GameBot!

```bash
python working_app.py
```

**Happy Gaming! 🎮✨**

---

*Built with ❤️ for the gaming community*
