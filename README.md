# Python AI Agent

This guide provides step-by-step instructions to set up and run the Python AI Agent project.

---

## Prerequisites

Before you begin, ensure the following tools are installed on your system:

- **pyenv**: For managing Python versions.
- **API Keys**: Set up the API keys for OpenAI and Google:
  - `OPENAI_API_KEY`
  - `GOOGLE_API_KEY`

---

## Step 1: Install Python 3.11 Using `pyenv`

1. Install Python 3.11:
   ```bash
   pyenv install 3.11
   ```

2. Set Python 3.11 as the local version:
   ```bash
   pyenv local 3.11
   ```

3. Verify the active Python version:
   ```bash
   python --version
   ```
   or
   ```bash
   pyenv which python
   ```

---

## Step 2: Set Up a Virtual Environment

1. Create a virtual environment:
   ```bash
   python3 -m venv ai-agents
   ```

2. Activate the virtual environment:
   ```bash
   source ai-agents/bin/activate
   ```

---

## Step 3: Install Dependencies

1. Install the required dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

---

## Step 4: Run the Project

You can run the project using one of the following options:

1. **Run the main Python script**:
   ```bash
   python main.py
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

---

## Notes

- Ensure your API keys are properly configured in your environment before running the project.
- For additional details or troubleshooting, refer to the project documentation.