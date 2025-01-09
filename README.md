# MVD.AI

**MVD.AI**  is a personal AI management hub that connects a variety of AI services, such as OpenAI, GoogleAI, ClaudeAI, and Stable Diffusion, through an easy-to-use web interface. Built to function as both a standalone tool and an API for integration with other projects, MVD.AI is ideal for developers and hobbyists looking to explore AI capabilities. As this is a personal project, some features may be experimental, and occasional bugs should be expected.

---

## **Features**

### **AI Modules**
- **OpenAI Integration**: Chat-based AI functionality for OpenAI models.
- **GoogleAI Integration**: Connects with Google's Generative AI services.
- **ClaudeAI Integration**: Support for Anthropic Claude models.
- **Stable Diffusion**: Generate AI-based images directly from prompts.

### **Core Functionalities**
- **Text-to-Speech (TTS)**: Natural speech synthesis using Azure Cognitive Services.
- **Speech-to-Text (STT)**: Integration for voice transcription (e.g., OpenAI Whisper).
- **Live Object Detection**: Computer vision via YOLO for real-time object detection.
- **Chat Management**: Respond to queries from multiple AI models simultaneously.
- **System Monitoring**: Track system metrics like CPU, GPU, and memory usage.
- **Activity Tracker**: Context-aware tracking for personalized AI interactions.

### **User Interface**
- Web-based interface with multiple tabs for:
  - AI Requests
  - Live Object Detection
  - Azure TTS
  - Stable Diffusion
  - System Monitoring
  - Logs

---

## **Installation**

### **Prerequisites**
1. **Python 3.10+**
2. **Node.js** (optional for additional frontend features)
3. API keys for the following services:
   - OpenAI
   - Google Cloud
   - Azure Cognitive Services (for TTS/STT)
   - Anthropic (ClaudeAI)

# For CUDA 12.4 support, install torch as per: https://pytorch.org/get-started/locally/
torch==2.5.1+cu124

### **Clone the Repository**
```bash
git clone https://github.com/yourusername/MVD.AI.git
cd MVD.AI
```

### **Environment Setup**
1. Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLEAI_API_KEY=your_googleai_api_key
   AZURE_API_KEY=your_azure_api_key
   AZURE_REGION=your_azure_region
   CLAUDE_API_KEY=your_claude_api_key
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Optional: Set up Stable Diffusion locally by following the [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) instructions.


---

## **Usage**

### **Run the Application**
1. Start the MVD.AI server:
   ```bash
   python app_server.py
   ```
2. Access the web interface at:
   ```
   http://127.0.0.1:5000
   ```

---

## **Directory Structure**
```
MVD.AI/
├── app_server.py         # Main server script
├── .env                  # Environment variables
├── modules/              # Modular AI service implementations
│   ├── openai.py         # OpenAI integration
│   ├── googleai.py       # GoogleAI integration
│   ├── claude.py         # ClaudeAI integration
│   ├── stable_diffusion.py # Stable Diffusion API
│   ├── live_object_detection.py # YOLO-based object detection
│   ├── filter_manager.py # Content filtering
│   ├── activity_tracker.py # Activity tracking
│   ├── system_monitor.py # System metrics tracking
│   └── log_manager.py    # Log management
├── static/               # Frontend assets
│   ├── css/
│   │   └── styles.css    # Main stylesheet
│   ├── js/
│   │   └── scripts.js    # Main JavaScript
│   └── audio/            # Generated audio files
├── templates/            # HTML templates
│   └── index.html        # Main UI template
├── README.md             # Documentation
└── requirements.txt      # Python dependencies
```

---

## **Contributing**
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.