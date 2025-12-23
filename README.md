# Health & Fitness Monitor

A comprehensive health tracking application featuring a RESTful API backend and an interactive real-time dashboard.

## Project Description

The Health & Fitness Monitor is designed to help users track their daily health metrics such as steps, calories, and heart rate. It provides a robust backend for reliable data storage and retrieval, coupled with a visual dashboard for analyzing trends and setting fitness goals.

## Technology Stack

*   **Backend:** Python, FastAPI
*   **Database:** PostgreSQL, SQLAlchemy (ORM)
*   **Dashboard:** Dash (Plotly), HTML/CSS
*   **Authentication:** JWT (JSON Web Tokens), Passlib (Argon2 hashing)
*   **Visualization:** Plotly Express, Plotly Graph Objects

## Setup Instructions

### Prerequisites
*   Python 3.8+
*   PostgreSQL installed and running

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    *   Create a `.env` file in the root directory.
    *   You can use `.env.example` as a template.
    *   Set your `DATABASE_URL` (e.g., `postgresql://user:password@localhost/dbname`).
    *   Set `SECRET_KEY` and other configurations.

5.  **Run the Backend API:**
    ```bash
    python -m uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

6.  **Run the Dashboard:**
    ```bash
    python dashboard.py
    ```
    The dashboard will be available at `http://127.0.0.1:8050`.

## API Documentation

Once the backend is running, you can access the interactive API documentation (Swagger UI) at:

**`http://127.0.0.1:8000/docs`**

### Key Endpoints
*   **Authentication**
    *   `POST /token`: Login to get access token.
    *   `POST /users`: Register a new user.
    *   `GET /users/me`: Get current user profile.
*   **Metrics**
    *   `GET /metrics`: specific health metrics.
    *   `POST /metrics`: Log new health data.
    *   `DELETE /metrics/{id}`: Remove an entry.
*   **Goals**
    *   `POST /goals`: Set or update fitness goals.
    *   `GET /goals/progress`: View progress towards goals.
