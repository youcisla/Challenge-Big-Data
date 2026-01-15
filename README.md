# Oracle Paris 2024 - Olympic Games Analytics

An advanced **Django** web application designed to explore historical Olympic data, debunk myths, and predict the outcomes of the Paris 2024 Olympic Games using **Machine Learning (XGBoost)**.

![Dashboard Preview](docs/dashboard_preview.png)

## Features

### 1. Interactive Dashboard & Explorer
-   **High-Level KPIs**: Real-time stats on Medals, Athletes, and Games.
-   **Interactive Charts**: 
    -   Global Choropleth Map (Plotly) showing medal distribution.
    -   Host Country Analysis (Top organizers).
    -   Country-specific deep dives (France focus: Medal evolution, seasonal performance).

### 2. AI Predictions (Oracle Paris 2024)
-   **Algorithmic Forecasting**: Uses an **XGBoost Regressor** trained on 120 years of history to predict medal counts for Paris 2024.
-   **Feature Engineering**: Accounts for "Host Country Advantage", delegation size, and historical performance.
-   **Visualizations**:
    -   **Podium**: Dynamic "Glassmorphism" cards for the Top 3 favorites.
    -   **Leaderboard**: Complete predicted rankings with search and filtering.
    -   **Golden Card**: Specific focus on France's predicted performance (+Comparisons).

### 3. Myths & Fact-Checking
-   Interactive cards verifying common Olympic myths (e.g., "Did women participate in 1900?").
-   Data-backed verdicts (True/False) with historical insights.

### 4. Real vs AI Comparison
-   **Simulation Mode**: A dedicated page comparing AI predictions against "Official" (simulated) results.
-   **Performance Metrics**: Visual indicators of AI accuracy (Precision, Under/Over-performance).

---

## Technology Stack

-   **Backend**: Python 3.10+, Django 5.x
-   **Database**: PostgreSQL (via Supabase)
-   **Data Science**: Pandas, NumPy, XGBoost, Scikit-Learn
-   **Frontend**: HTML5, Bootstrap 5, Dark Mode Aesthetic
-   **Visualization**: Plotly.js (Client-side rendering for interactivity)

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/youcisla/Challenge-Big-Data.git
cd Challenge-Big-Data
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory with your database credentials:
```ini
user=postgres.your_project_ref
password=your_database_password
host=aws-0-eu-central-1.pooler.supabase.com
port=6543
dbname=postgres
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 4. Database Setup
Run the import script to populate the `olympic_stats` table from the CSV dataset:
```powershell
python import_data.py
```

### 5. Run the Application
You can use the helper script (Windows):
```powershell
./make run
```
Or the standard Django command:
```powershell
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000** to access the Oracle.

---

## Project Structure

-   `config/`: Main Django settings and URL routing.
-   `core/`: Application logic.
    -   `views.py`: Controls data flow and rendering.
    -   `models.py`: Database schema definition.
    -   `ml_service.py`: Singleton service managing the XGBoost model and predictions.
-   `ml_models/`: Stores the trained `.pkl` models.
-   `templates/`: HTML templates with Bootstrap styling.
-   `static/`: CSS (Dashboard themes), Images, and JS.
-   `data/`: Raw CSV datasets.

---

## Contributors
-   **Project Team**: Y. Chehboub & Team
-   **Context**: Big Data Challenge / Hackathon
