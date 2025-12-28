# Crypto Automation Dashboard

A Python automation project that **regularly collects cryptocurrency data**, stores it in a spreadsheet, generates charts, and creates **PDF reports**.  
The project is designed to run **automatically (via Task Scheduler)** and is easy to extend and maintain.

---

## What the project does

During a single run, the project performs the following steps:

1. Sends HTTP requests to cryptocurrency web pages
2. Collects:
   - cryptocurrency name
   - current price
   - date of retrieval
3. Writes data into a **Google Spreadsheet** (existing or newly created)  
   > ⚠ Make sure you are logged into the **same Google account** where the spreadsheet will be created.
4. Calculates price change compared to the previous value (if available)
5. Generates:
   - **line charts** (price history)
   - **bar charts** (cryptocurrency comparison)
6. Creates a **PDF report**:
   - overview page with summary table
   - separate page for each cryptocurrency (if chart data is available)
7. Logs all steps (info / warning / error)
8. Supports **automatic execution** using Windows Task Scheduler

---

## Key features

- ✅ Modular architecture (each responsibility in a separate file)
- ✅ Robust error handling using `try / except`
- ✅ Logging to file
- ✅ Automatic creation of missing files
- ✅ Easy adding/removing cryptocurrencies via config
- ✅ Designed for long-term automated execution

---

## Project structure

- `program_01_main.py` – Main entry point  
- `program_02_request.py` – Data fetching from web  
- `program_03_spreadsheet.py` – Spreadsheet operations  
- `program_04_line_chart.py` – Line chart generation  
- `program_05_bar_chart.py` – Bar chart generation  
- `program_06_pdf.py` – PDF report generation  
- `program_07_task_scheduler.py` – Automatic scheduling  

- `s_program_01_config.py` – Project configuration  
- `s_program_02_utils.py` – Utility functions  
- `s_program_03_access_token.py` – Token handling  
- `s_program_04_logger.py` – Logging



> 📌 Generated files (charts, PDFs, logs, data files) are **not included** in the repository and are ignored using `.gitignore`.

---

## Requirements

- Python **3.10+**
- Install required libraries using:

```bash
pip install -r requirements.txt
```

Libraries included:

- `requests` – HTTP requests handling  
- `matplotlib` – Plotting and chart generation  
- `reportlab` – PDF report creation  
- `PyPDF2` – PDF manipulation and merging  
- `google-api-python-client` – Access Google APIs (Sheets, Drive)  
- `google-auth` – Google authentication  
- `google-auth-oauthlib` – OAuth 2.0 support for Google APIs


## Google API – Client Secret Setup

This project uses **Google Sheets API** and **Google Drive API**.  
To allow access, you must create an **OAuth client secret file**.

---

### 1️⃣ Create a Google Cloud project

1. Go to **Google Cloud Console**:  
   [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Create a **new project** (or select an existing one).

---

### 2️⃣ Enable required APIs

1. Navigate to: **APIs & Services → Library**
2. Enable the following APIs:
   - **Google Sheets API**
   - **Google Drive API**

---

### 3️⃣ Start OAuth client creation

1. Go to: **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. If OAuth is not configured yet, Google will redirect you to the **OAuth Overview** page.
4. Click **Configure consent screen**

---

### 4️⃣ Configure OAuth consent screen

**App information:**

- **App name**: `Crypto Automation Dashboard`
- **User support email**: your email

Click **Next**  

**App audience:**

- Select **External**  
- Click **Next**  

**Contact information:**

- Enter your email  
- Click **Finish**  
- Click **Agree** if prompted  

> ℹ️ Publishing the app is **not required**. Test mode is sufficient for personal automation projects.

---

### 5️⃣ Create OAuth client ID

1. After finishing the consent screen, you will be redirected to **OAuth Overview**
2. You will see the message:  
   > *You haven't configured any OAuth clients for this project yet*
3. Click **Create OAuth client**
4. Select **Application type**: `Desktop app`
5. Enter a name (e.g., `Crypto Dashboard Desktop`)
6. Click **Create**
7. **Download the credentials JSON file** (contains your client ID and client secret)

---

### 6️⃣ Prepare client secret file

1. Rename the downloaded file to:

```text
j_client_secret.json
```

### Place the client secret file

Place the downloaded JSON file in the project directory  
(as expected by `s_program_03_access_token.py`).

---

### 🔐 Security note

This JSON file contains **sensitive credentials** and must **never** be committed to GitHub.  
It is excluded via `.gitignore`.

---

### 7️⃣ First run authorization (token creation) 

Run the project for the first time:

```bash
python program_01_main.py
```

A browser window will automatically open.

Google will ask you to authorize access using the client secret.  
**Grant all requested permissions.**

This process will:

- Create an OAuth token from the client secret
- Allow the program to access Google Sheets
- Enable future spreadsheet operations without re-authentication

The generated token file is stored locally and reused on subsequent runs.

> ⚠ **Important:** Run the program as **Administrator** at least once to allow Task Scheduler to create the scheduled task.

---

### 8️⃣ Configure project paths

Before running the project, open `s_program_01_config.py` and update the following paths:

```python
# Path to Python executable – replace with your own path
PYTHON_PATH = "C:/Path/To/Python/python.exe"

# Path to main script – replace with your own path
SCRIPT_PATH = "C:/Path/To/Project/main.py"

# Path to client secret – replace with your own path
CLIENT_SECRET_PATH = "j_client_secret.json"
```

⚠ **Make sure all paths are correct**; otherwise Task Scheduler or the program may fail.

---

### ✔ Why this step matters

Without this authorization and proper permissions:

- Spreadsheets **cannot** be created or updated
- Task Scheduler **cannot** register the automatic execution of the program





