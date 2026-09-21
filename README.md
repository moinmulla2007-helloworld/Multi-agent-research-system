# 🤖 Multi-Agent Research System

An interactive **Multi-Agent AI Research System** that uses specialized AI agents to research topics, gather information from the web, analyze the collected data, and generate a structured response.

The project is built using **Google Gemini, LangChain, LangGraph, Tavily, BeautifulSoup, and Streamlit**.

---

## 🚀 Overview

Traditional research often requires manually searching multiple websites, reading different sources, extracting useful information, and combining the findings into a final answer.

This project automates that workflow using a **multi-agent architecture**.

Instead of relying on a single AI call, different agents and tools can perform specialized tasks such as:

* 🔍 Researching a given topic
* 🌐 Searching the web for relevant information
* 📄 Extracting information from web pages
* 🧠 Processing and analyzing collected information
* ✍️ Generating a structured final response
* 🔄 Coordinating multiple stages through an agentic workflow

The application provides an easy-to-use **Streamlit interface** for interacting with the research system.

---

## ✨ Key Features

### 🤖 Multi-Agent Architecture

The system uses specialized agents to divide the research workflow into separate tasks.

This makes the application easier to extend and allows different parts of the research process to have dedicated responsibilities.

### 🔎 Web Search

The system integrates **Tavily** for web-based information retrieval.

This allows the agents to search for relevant and current information instead of relying only on the model's existing knowledge.

### 🌐 Web Scraping

**BeautifulSoup** is used to extract useful content from web pages returned during the research process.

### 🧠 Google Gemini

Google Gemini provides the underlying large language model capabilities used by the agents.

The project integrates Gemini through:

`langchain-google-genai`

### 🔗 LangChain & LangGraph

**LangChain** provides the framework for working with LLMs and tools, while **LangGraph** is used to organize the agent workflow and execution flow.

### 🖥️ Streamlit Interface

A Streamlit-based interface allows users to interact with the research system without needing to use the command line.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    │  Research Query  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Agent Workflow │
                    │    LangGraph     │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
      ┌───────────────┐             ┌───────────────┐
      │ Research Agent│             │ Supporting     │
      │               │             │ Agents/Tasks   │
      └───────┬───────┘             └───────┬───────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    ┌──────────────────┐
                    │   Web Search     │
                    │     Tavily       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Web Scraping   │
                    │   BeautifulSoup  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Gemini / LLM    │
                    │ Analysis &       │
                    │ Generation       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Final Research │
                    │     Response     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Streamlit     │
                    │       UI         │
                    └──────────────────┘
```

---

## 📁 Project Structure

```text
Multi-agent-research-system/
│
├── agents.py
│   └── Defines the AI agents and their responsibilities
│
├── pipeline.py
│   └── Coordinates the overall agent workflow
│
├── tools.py
│   └── Contains research and web-related tools
│
├── ui.py
│   └── Streamlit user interface
│
├── requirements.txt
│   └── Python dependencies
│
└── .gitignore
    └── Files excluded from version control
```

---

## 🛠️ Tech Stack

| Technology        | Purpose                             |
| ----------------- | ----------------------------------- |
| **Python**        | Core programming language           |
| **Google Gemini** | Large Language Model                |
| **LangChain**     | LLM and tool integration            |
| **LangGraph**     | Agent workflow orchestration        |
| **Tavily**        | Web search                          |
| **BeautifulSoup** | Web scraping and content extraction |
| **Streamlit**     | User interface                      |

The repository's GitHub description identifies this stack as Gemini + LangChain/LangGraph, Tavily, BeautifulSoup, and Streamlit.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/moinmulla2007-helloworld/Multi-agent-research-system.git
```

### 2. Navigate to the project

```bash
cd Multi-agent-research-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys

The application requires API credentials for the external AI and search services used by the project.

Create a `.env` file in the project directory and add your credentials:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

> **Important:** Never upload your API keys or `.env` file to GitHub.

Make sure `.env` is included in `.gitignore`.

---

## ▶️ Running the Application

Start the Streamlit application with:

```bash
streamlit run ui.py
```

After starting the application, Streamlit will provide a local URL in the terminal.

Open that URL in your browser to use the research system.

---

## 🔄 How the System Works

### Step 1 — User Query

The user enters a research question or topic through the Streamlit interface.

### Step 2 — Agent Processing

The query is passed into the agent workflow managed using LangGraph.

### Step 3 — Information Retrieval

The system can use web-search functionality to locate relevant information.

### Step 4 — Web Content Extraction

Relevant web pages can be processed using BeautifulSoup to extract useful textual information.

### Step 5 — AI Analysis

The collected information is processed using Google Gemini.

### Step 6 — Response Generation

The agents combine the gathered information and generate a structured research response.

### Step 7 — Display

The final result is presented through the Streamlit interface.

---

## 💡 Example Queries

You can use the system for questions such as:

```text
What are the latest applications of artificial intelligence in healthcare?
```

```text
Explain the impact of renewable energy on modern power systems.
```

```text
Compare different approaches to autonomous vehicles.
```

```text
What are the major developments in generative AI?
```

---

## 🎯 Use Cases

The system can be useful for:

* 📚 Academic research
* 📝 Research report preparation
* 🔍 Topic exploration
* 🧠 Information gathering
* 🌐 Web-based research
* 📊 Technology analysis
* 💡 Project research
* 🤖 Experimenting with multi-agent AI architectures

---

## 🔮 Future Improvements

Possible improvements include:

* [ ] Add more specialized research agents
* [ ] Add source citation and reference management
* [ ] Add PDF/document research
* [ ] Add persistent research memory
* [ ] Add research history
* [ ] Add export to PDF/Markdown
* [ ] Add configurable research depth
* [ ] Add source-quality verification
* [ ] Add parallel agent execution
* [ ] Add conversation-based follow-up questions
* [ ] Add automated fact checking
* [ ] Add deployment configuration

---

## ⚠️ Disclaimer

> **Disclaimer:** This project is an AI-assisted research tool intended for educational and informational purposes. The generated responses may contain inaccuracies, incomplete information, or errors in interpretation. Always verify important information using reliable primary or authoritative sources before relying on it.

---

## 👨‍💻 Author

**Moin Mulla**

GitHub:
https://github.com/moinmulla2007-helloworld

---

## ⭐ Acknowledgements

This project uses several open-source technologies and services, including:

* Google Gemini
* LangChain
* LangGraph
* Tavily
* BeautifulSoup
* Streamlit

---

## 📌 Project Status

**Active Development**

This project is intended as an evolving implementation of a multi-agent AI research workflow. Features and architecture may change as the system is further developed.
