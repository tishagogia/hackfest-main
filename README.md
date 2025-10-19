

# TruthGuard AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25-orange)](https://streamlit.io/)

TruthGuard AI is a multi-modal, real-time misinformation detection platform leveraging **Snowflake Cortex APIs** and multiple AI models (Mistral, Claude, Llama) for enterprise-grade fact verification and content safety.

---

## Table of Contents

- [Inspiration](#inspiration)  
- [What it Does](#what-it-does)  
- [Features](#features)  
- [Architecture](#architecture)  
- [Getting Started](#getting-started)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)  

---

## Inspiration

With the explosion of AI-generated content, deepfakes, and misinformation on social media, organizations struggle to verify content in real-time. TruthGuard AI was inspired by the need for **automated, verifiable, and auditable misinformation detection** to protect elections, public health, and scientific integrity.

---

## What it Does

TruthGuard AI processes text, images, and video to detect misinformation across **six critical domains**:

1. News  
2. Elections  
3. Climate  
4. Health & Viral Content  
5. Deepfakes  
6. Mental Health  

It runs **three state-of-the-art AI models in parallel** to provide a consensus-based verdict with **real-time logging, audit trails, and exportable reports**.

---

## Features

- Multi-model consensus verification (Mistral, Claude, Llama)  
- Real-time streaming API with instant results  
- Categorized analysis for domain-specific accuracy  
- JSON/CSV output and visualization ready  
- Full audit trail stored in Snowflake  
- Production-ready REST API  

---

## Architecture

```mermaid
flowchart TD

subgraph UI[User Interface]
  UI1["Streamlit Frontend - Glassmorphism UI"]
  UI2["Real-time Input - Text, Image, Video"]
end

subgraph BE[Backend Services]
  B1["Python API Service"]
  B2["Consensus Engine - Weighted Multi-Model Scoring"]
  B3["Result Formatter - JSON, CSV, Visualization"]
end

subgraph AI[Snowflake Cortex APIs]
  C1["Mistral-Large2"]
  C2["Claude-3.5-Sonnet"]
  C3["Llama3.1-70B"]
end

subgraph SF[Snowflake Data Infrastructure]
  D1["Log Table - Queries, Responses, Scores"]
  D2["Audit Trail - Timestamped Records"]
  D3["Dashboard Analytics - SQL + Visualization"]
end

UI1 -->|User enters content| UI2
UI2 -->|POST /analyze| B1
B1 -->|REST API call| C1
B1 -->|REST API call| C2
B1 -->|REST API call| C3
C1 -->|Responses| B2
C2 -->|Responses| B2
C3 -->|Responses| B2
B2 -->|Aggregated verdict| B3
B3 -->|Formatted Output| UI1
B1 -->|Store logs| D1
B2 -->|Store consensus data| D2
D1 --> D3
D2 --> D3
D3 -->|Analytics feedback| UI1
````

---

## Getting Started

### Prerequisites

* Python 3.11+
* Streamlit
* Requests / HTTP client
* Snowflake account with **Cortex API access**

### Installation

```bash
git clone https://github.com/yourusername/truthguard-ai.git
cd truthguard-ai
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. Set your **Snowflake credentials** in `.env`:

```env
SNOWFLAKE_ACCOUNT=<account_name>
SNOWFLAKE_USER=<user>
SNOWFLAKE_PASSWORD=<password>
SNOWFLAKE_WAREHOUSE=<warehouse>
```

2. Update API keys for **Mistral, Claude, Llama** if needed.

---

## Usage

Run the app locally:

```bash
streamlit run streamlit_app.py
```

* Open [http://localhost:8501](http://localhost:8501)
* Enter content (text, image, video)
* Select the category (News, Election, Climate, etc.)
* View real-time consensus verdict and audit logs

---

## Contributing

We welcome contributions!

1. Fork the repo
2. Create a new branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please follow the **code of conduct** and ensure all new features are tested.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* [Snowflake Cortex](https://www.snowflake.com/cortex/)
* OpenAI Models: Mistral, Claude, Llama
* [Streamlit](https://streamlit.io)
* MLH Hackathon & organizers

```

