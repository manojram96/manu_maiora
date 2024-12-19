
# Joke API Fetcher

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/joke-api-fetcher.git
   cd joke-api-fetcher
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your PostgreSQL database (e.g., `jokeapi_db`), and update the database connection string in `models.py` (`DATABASE_URL` variable).

4. Run the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

5. Visit `http://127.0.0.1:8000/jokes` to see the fetched jokes stored in your database.

6. Optionally, you can check the logs to verify that the jokes are being fetched and stored correctly.
