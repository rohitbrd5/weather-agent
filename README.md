# 🌤️ Weather Agent powered by Langchain & Langgraph

This project implements an AI-powered weather agent using Langchain and Langgraph, integrated with a FastAPI backend and a simple HTML/CSS/JavaScript frontend. The agent can fetch real-time weather information for specified locations using the OpenWeatherMap API.

## ✨ Features

*   **Intelligent Agent:** Built with Langchain and Langgraph to understand natural language queries about weather.
*   **Real-time Weather Data:** Integrates with the OpenWeatherMap API to provide current weather conditions.
*   **FastAPI Backend:** Exposes a RESTful API for communication between the frontend and the agent.
*   **Interactive UI:** A simple, modern web interface for users to chat with the weather agent.
*   **Modular Project Structure:** Organized into standard production-grade folders (`src/nodes`, `src/state`, `src/graph`, `src/tools`, `src/llm`).
*   **Environment Variable Management:** Secure handling of API keys using `.env` and `.env.example`.

## 🛠️ Technologies Used

*   **Python 3.x**
*   **uv** (Package Manager)
*   **FastAPI** (Web Framework)
*   **Langchain** (LLM Orchestration)
*   **Langgraph** (Agentic Workflow)
*   **Groq** (LLM Provider - `qwen-qw-32b` model)
*   **OpenWeatherMap API** (Weather Data)
*   **HTML, CSS, JavaScript** (Frontend)

## 🚀 Getting Started

###  prerequisites

*   Python 3.x installed
*   `uv` package manager installed (`pip install uv`)
*   API keys for [Groq](https://console.groq.com/keys) and [OpenWeatherMap](https://openweathermap.org/api)

### 1. Clone the repository

```bash
git clone https://github.com/rishav-learnerml/weather-agent.git
cd weather-agent
```

### 2. Set up your virtual environment and install dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the root of your project based on `.env.example` and add your API keys:

```dotenv
GROQ_API_KEY="your_groq_api_key"
LANGCHAIN_PROJECT="BlogGeneratorAgent" # Or your desired project name
LANGCHAIN_API_KEY="your_langchain_api_key"
UNSPLASH_ACCESS_KEY="your_unsplash_access_key" # Not directly used in weather agent, but kept for consistency
OPENWEATHER_API_KEY="your_openweathermap_api_key"
```

Replace the placeholder values with your actual API keys. You can get them from:
*   [Groq Console](https://console.groq.com/keys)
*   [OpenWeatherMap API](https://openweathermap.org/api)

### 4. Run the Backend

Ensure your virtual environment is activated:

```bash
source .venv/bin/activate
python main.py
```

The FastAPI application will run on `http://127.0.0.1:8000`.

### 5. Run the Frontend

Open the `ui/index.html` file in your web browser. For local development, it's recommended to use a simple HTTP server (e.g., VS Code Live Server extension or `python -m http.server 5500` in the `ui` directory).

The frontend will typically run on `http://127.0.0.1:5500` (or similar, depending on your local server setup).

## 🧑‍💻 Project Structure

```
.env               # Environment variables (ignored by Git)
.env.example       # Template for .env
.gitignore         # Git ignore file
main.py            # FastAPI application entry point
pyproject.toml     # Project metadata (for uv)
requirements.txt   # Python dependencies

src/
├── graph/         # Langgraph definitions
│   └── graph.py
├── llm/           # LLM configurations
│   └── llm.py
├── nodes/         # Langgraph nodes (functions/steps in the agent workflow)
│   └── nodes.py
├── state/         # Langgraph state definition
│   └── state.py
└── tools/         # Langchain tools for the agent
    └── tools.py

ui/
├── index.html     # Frontend HTML structure
├── script.js      # Frontend JavaScript for chat interaction
└── style.css      # Frontend CSS for styling
```
