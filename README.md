# 🏥 Hospital Chatbot with Streamlit Interface

A sophisticated hospital chatbot built with LangChain, LangGraph, and Streamlit that provides intelligent responses to hospital-related queries using RAG (Retrieval-Augmented Generation) technology.

![image](https://github.com/user-attachments/assets/4ad776d3-f59f-4d5e-afb0-10e84db2b29e)


## 🌟 Features

- **🗣️ Conversational Interface**: Modern chat interface built with Streamlit
- **🧠 RAG Technology**: Retrieval-Augmented Generation for accurate, context-aware responses
- **💭 Memory Management**: Remembers conversation context for personalized interactions
- **📚 Multi-Source Knowledge**: Combines hospital FAQ data with a comprehensive knowledge base
- **✅ Quality Assurance**: Built-in response grading and hallucination detection
- **🚨 Emergency Detection**: Automatic emergency situation recognition
- **👍 Feedback System**: User feedback collection with satisfaction metrics
- **📱 Responsive Design**: Mobile-friendly interface with hospital-themed styling
- **🐳 Production Ready**: Dockerized deployment with health checks

## 🏗️ Architecture

The chatbot uses a sophisticated graph-based architecture `(Agentic RAG Workflow)` mainly from my last project [here](https://github.com/mahmoud-mohsen97/Chat_Agents):

```
User Query →
    Route Question →
        [RAG Pipeline | Simulated Generation] →
            Grade Documents →
                Generate Response →
                    Grade Response →
                        Final Answer
```

### Core Components

- **LangGraph**: Orchestrates the conversation flow
- **ChromaDB**: Vector database for hospital knowledge
- **OpenAI GPT-4**: Language model for response generation
- **Simulated Generation**: Intelligent responses for queries outside the knowledge base
- **Streamlit**: Web interface and user experience

## 🚀 Quick Start (5 minutes)

### Prerequisites

- Python 3.12+
- Docker (for containerized deployment)
- OpenAI API key

### 1. Set Up Environment

```bash
# Clone the repository
git clone <repository-url>
cd hospital_chatbot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
TEMPERATURE=0
MAX_TOKENS=1000
```

### 2. Test the Integration

```bash
python test_integration.py
```

### 3. Deploy

**Option A: Local Development**
```bash
streamlit run streamlit_app.py
```

**Option B: Docker (Recommended)**
```bash
# Quick deployment
./src/scripts/deploy.sh

# Or manually:
docker-compose up --build -d
```

### 4. Access Your Chatbot

- **Local**: http://localhost:8501
- **Docker**: http://localhost:8501

## 📊 Project Structure

```
hospital_chatbot/
├── .streamlit/
│   └── config.toml                    # Streamlit configuration
├── config/
│   ├── __init__.py                    # Configuration module
│   └── settings.py                    # Centralized settings and constants
├── data/
│   ├── hospital_faq.csv               # FAQ data for UI responses
│   └── hospital_knowledge_base.csv    # Comprehensive hospital knowledge base
├── src/
│   ├── chains/                        # LangChain components
│   ├── nodes/                         # Graph processing nodes
│   ├── utils/                         # Utility functions
│   │   └── ui_components.py           # Reusable UI components
│   ├── scripts/                       # Automation scripts
│   │   ├── clean.sh                   # Cleanup script
│   │   └── deploy.sh                  # Deployment script
│   ├── graph.py                       # Main conversation graph
│   ├── state.py                       # State management
│   └── ingestion.py                   # Data ingestion utilities
├── __init__.py                        # Configuration module
├── streamlit_app.py                   # Main Streamlit application
├── test_integration.py                # Integration testing
├── Dockerfile                         # Docker configuration
├── docker-compose.yml                 # Docker Compose setup
├── pyproject.toml                     # Python dependencies
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 💻 Usage & Features

### Basic Chat

1. Open the application in your browser
2. Type your question in the chat input
3. Receive intelligent responses from the hospital assistant

### Key Features Demo

1. **Hospital Questions**: "What are your visiting hours?", "How can I book an appointment?"
2. **Emergency Detection**: "This is an emergency!" - Automatic emergency response
3. **Sidebar FAQs**: Click preset questions for quick answers
4. **Feedback System**: Rate responses with 👍/👎 buttons
5. **Statistics**: View conversation metrics in sidebar
6. **Memory Test**: Say "My name is John" then ask "What's my name?"

### Sample Questions

- "How can I book an appointment?"
- "What are your visiting hours?"
- "Do you have a pharmacy?"
- "What insurance do you accept?"
- "Where is the hospital located?"
- "What are the available clinics?"
- "I want to request an ambulance"

## 🏥 Hospital Information

The chatbot provides comprehensive information about:

- **🏥 Services**: Emergency care, laboratory, radiology, pediatrics, maternity
- **🏢 Facilities**: Pharmacy, cafeteria, gift shop, parking
- **📋 Policies**: Visiting hours, insurance, appointments, medical records
- **📞 Contact**: Location, phone numbers, emergency procedures
- **👨‍⚕️ Clinics**: Cardiology, orthopedics, gynecology, ENT, and more
- **💰 Pricing**: Surgery costs, consultation fees, insurance coverage

## 🔧 Configuration & Customization

### Environment Variables

Configure the application through `.env`:

```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional Configurations
OPENAI_MODEL=gpt-4.1-mini
TEMPERATURE=0
MAX_TOKENS=500
```

### Hospital Information

Update hospital details in `config/settings.py`:

```python
HOSPITAL_INFO = {
    "name": "🏥 Hospital Assistant",
    "location": "Your Location",
    "emergency_number": "123",
    "phone": "Your Phone",
    "email": "your@email.com",
    # ... more settings
}
```

### Add New Content

1. **Hospital Information**: Edit `data/hospital_knowledge_base.csv`
2. **FAQ Responses**: Update `data/hospital_faq.csv`
3. **UI Styling**: Modify CSS in `src/utils/ui_components.py`

## 🐳 Production Deployment

### Docker Deployment

```bash
# Build and deploy
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Health Monitoring

The application includes health checks:
```bash
# Check health
curl http://localhost:8501/_stcore/health

# Restart services
docker-compose restart
```

### Production Checklist

- [ ] Environment variables configured
- [ ] API keys added to `.env`
- [ ] Integration tests pass (`python test_integration.py`)
- [ ] Docker deployment works
- [ ] Health checks respond
- [ ] Hospital information updated
- [ ] FAQ data is current
- [ ] Security settings reviewed

## 🔒 Security & Privacy

- Environment variables for sensitive API keys
- Non-root Docker user for security
- No persistent storage of conversation data
- HIPAA-aware design (does not store patient information)
- Comprehensive `.gitignore` for sensitive files

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Import Errors** | Run `python test_integration.py` to check setup |
| **API Key Issues** | Verify `.env` file has correct keys |
| **Docker Issues** | Check `docker-compose logs` |
| **Port Conflicts** | Change port in `docker-compose.yml` |

### Debug Commands

```bash
# View Docker logs
docker-compose logs -f

# Check application health
curl http://localhost:8501/_stcore/health

# Run integration tests
python test_integration.py

# Clean up cache files
./src/scripts/clean.sh
```

## 🎯 Technical Details

### What's Working

- ✅ RAG-powered responses from hospital knowledge base
- ✅ Quality grading and hallucination detection
- ✅ Memory retention across conversations
- ✅ Professional hospital-themed UI
- ✅ Docker containerization with health checks
- ✅ Error handling and fallbacks
- ✅ Centralized configuration management

### Architecture Benefits

1. **Modularity**: Centralized configuration, clear separation of concerns
2. **Maintainability**: Single source of truth for settings, easy updates
3. **Production Readiness**: Proper directory structure, Docker deployment
4. **Developer Experience**: Clear project structure, comprehensive documentation

---

🎉 **Your hospital chatbot is ready to help patients and visitors with intelligent, context-aware responses!**
