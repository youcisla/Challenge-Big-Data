# Olympic Games Analytics 🏅

A robust **Django** web application to explore, visualize, and predict Olympic Games historical data (Athens 1896 - Beijing 2022).

## Features
- **Dashboard**: Professional Bootstrap 5 interface with high-level KPIs.
- **Data Exploration**: Visualization of medal counts and participation trends.
- **Predictions**: AI/ML integration to predict future outcomes (Paris 2024).
- **Database**: PostgreSQL storage (Supabase).
- **Architecture**: Scalable Django MVT (Model-View-Template) structure.

## Prerequisites
- **Python**: Version 3.10+
- **PostgreSQL Database**: A Supabase instance with the `olympic_stats` table populated.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/youcisla/Challenge-Big-Data.git
    cd Challenge-Big-Data
    ```

2.  **Install dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

## Configuration

1.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in your Supabase credentials:
    ```ini
    user=postgres.your_project_ref
    password=your_database_password
    host=aws-0-eu-central-1.pooler.supabase.com
    port=6543
    dbname=postgres
    ```

## Running the App

You can use the helper script (Windows):
```powershell
.\make run
```
Or run the standard Django command:
```powershell
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000`.

## Project Structure
-   `config/`: Main Django project settings and URLs.
-   `core/`: Main application logic (Models, Views).
-   `templates/`: HTML templates using Bootstrap 5.
-   `static/`: CSS and JavaScript files.
-   `import_data.py`: Script to populate the database from CSV.
