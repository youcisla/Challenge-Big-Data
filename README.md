# Olympic Games Data Analytics 🏅

A Python-based web application to explore, visualize, and predict Olympic Games historical data (Athens 1896 - Beijing 2022).

## Features
- **Data Exploration**: Interactive visualizations of medal counts and participation trends.
- **Predictions**: AI/ML integration to predict future outcomes (Paris 2024).
- **Clustering**: Analysis of country performance clusters.
- **Database**: Robust PostgreSQL storage via Supabase.

## Prerequisites
- **Python**: Version **3.10, 3.11, or 3.12** is required.
  > ⚠️ **Note**: Python 3.14 is currently **not supported** due to dependency compatibility issues.
- **PostgreSQL Database**: A Supabase instance (or local Postgres) with the required schema.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/youcisla/Challenge-Big-Data.git
    cd ChallengeBigData
    ```

2.  **Install dependencies**:
    We have provided a helper script for Windows:
    ```powershell
    .\make install
    ```
    *(If you are on Linux/Mac, use `make install` or run `pip install -r requirements.txt`)*

## Configuration

1.  **Environment Variables**:
    Copy `.env.example` to `.env`:
    ```powershell
    copy .env.example .env
    ```

2.  **Edit `.env`**:
    Open the `.env` file and fill in your Supabase **Connection Pooling** credentials. You can find these in the Supabase Dashboard under `Project Settings > Database > Connection Pooling`.

    ```ini
    user=postgres.your_project_ref
    password=your_database_password
    host=aws-0-eu-central-1.pooler.supabase.com
    port=6543
    dbname=postgres
    ```

3.  **Database Setup**:
    The database schema is defined in `db.sql`.
    - If your database is empty, execute the contents of `db.sql` in your Supabase SQL Editor.
    - Import the datasets (Hosts, Athletes, Results, Medals) if available.

## Running the App

To launch the Streamlit dashboard:

```powershell
.\make run
```

The application will open in your browser at `http://localhost:8501`.

## Troubleshooting

-   **"pip not recognized"**: Ensure Python is added to your PATH. Use `.\make install` which uses `python -m pip` to avoid this.
-   **Build Errors**: If you see errors about `meson-python` or `pyroaring`, check your Python version (`python --version`). You must use Python 3.12 or lower.
