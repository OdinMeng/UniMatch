# FinalDeliveryTemplate

This repository serves as a **template** for the final project, providing a pre-structured framework to streamline development. The structure includes placeholders for key modules, assets, and utilities required for a fully functional chatbot integrated with Streamlit and LangChain.

## Purpose

- Offer a **starting point** for building custom chatbot applications.
- Include reusable components for **retrieval-augmented generation (RAG)**, intent routing, and database interactions.
- Facilitate modular design for **scalability** and **ease of customization**.

### Guidelines

Students are expected to **follow this structure as closely as possible** when developing their projects.

- The predefined organization will help ensure that all required components (e.g., chatbot logic, data processing, database interactions, and Streamlit pages) are implemented systematically.
- Teams are encouraged to adapt and expand the template for their specific use cases, but significant deviations should be justified in the final project documentation.

This structure is not only a foundation but also a tool to ensure **best practices** in project design and implementation. By adhering to it, students can focus more on innovation and less on reorganization. Feel free to adapt this template to meet your specific project requirements by replacing placeholder content (e.g., `company_name/`) and adding new functionality where needed.

## Repository Structure

```plaintext
root/
├── app.py                # Main Streamlit application script.
├── requirements.txt      # Python dependencies.
├── .gitignore            # Standard .gitignore file.
├── README.md             # Comprehensive project documentation.
├── company_name/         # Replace "company_name" with your company name.
│   ├──  __init__.py      # Package initialization, expose bot and dev_bot.
│   ├── chatbot/          # Chatbot modules and assets.
│   │   ├── bot.py        # Core chatbot logic.
│   │   ├── memory.py     # Chatbot memory.
│   │   ├── chains/       # Custom LangChain chains.
│   │   │   └── *.py      # Chain modules.
│   │   ├── rag/          # RAG-related modules for retrieval-augmented generation.
│   │   │   └── *.py      # Scripts for retrieval, embedding, ranking, QA pipelines, and utilities.
│   │   ├── router/       # Intent router.
│   │   │   └── *.py      # Intent router developement.
│   │   │   └── *.ipynb   # Intent routing training and evaluation. And to create synthetic data.
│   ├── pages/            # Streamlit app pages.
│   │   └── *.py          # Page modules.
│   ├── data/             # Data and scripts.
│   │   │── loader.py     # Functions to load data.
│   │   ├── database/     # Database files/scripts.
│   │   │   ├── *.db      # SQLite databases.
│   │   │   ├── *.ipynb   # Scripts for database creation.
│   │   ├── pdfs/         # PDFs and embedding scripts.
│   │   │   ├── *.pdf     # PDF files.
│   │   │   └── *.ipynb   # PDF processing scripts.
```

## Directory and File Details

#### Root Directory

- **`app.py`**: Main Streamlit application script that handles the frontend interface and user interactions.
- **`requirements.txt`**: List of Python dependencies.
- **`.gitignore`**: Specifies files and directories to be excluded from version control.
- **`README.md`**: Documentation explaining the project, setup, and usage.

#### `company_name/` (Replace with your company name)

- **`__init__.py`**: Package initialization file that exposes the chatbot and development chatbot for external use.

- **`chatbot/`**: Contains chatbot backend functionalities:

  - **`bot.py`**: Core chatbot logic.
  - **`memory.py`**: Implements chatbot memory for retaining context.
  - **`chains/`**: Custom LangChain chains:
    - **`*.py`**: Pipelines for querying databases, processing PDFs, or RAG.
  - **`rag/`**: Modules for Retrieval-Augmented Generation (RAG):
    - **`*.py`**: Scripts for embedding, ranking, and integrating context.
  - **`router/`**: Handles user intent routing:
    - **`*.py`**: Intent detection and routing scripts.
    - **`*.ipynb`**: Training and evaluating intent routing models.

- **`pages/`**: Streamlit app pages:

  - **`*.py`**: Modules representing different pages (e.g., chatbot interface, home page).

- **`data/`**: Manages project data:
  - **`loader.py`**: Functions for loading data.
  - **`database/`**: Database files and scripts:
    - **`*.db`**: SQLite databases for structured data storage.
    - **`*.ipynb`**: Jupyter notebooks for database creation and management.
  - **`pdfs/`**: PDF documents and processing scripts:
    - **`*.pdf`**: Source PDFs.
    - **`*.ipynb`**: Scripts for extracting text, embeddings, and integration.
