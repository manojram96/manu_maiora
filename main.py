import httpx
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import SessionLocal, Joke

app = FastAPI()

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any"

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fetch jokes from JokeAPI
async def fetch_jokes_from_api():
    async with httpx.AsyncClient() as client:
        response = await client.get(JOKE_API_URL, params={"amount": 100})
        response.raise_for_status()  # Will raise an exception for non-200 responses
        return response.json()

# Process jokes and store in the database
async def process_and_store_jokes(db: Session):
    jokes = await fetch_jokes_from_api()
    for joke_data in jokes.get("jokes", []):
        # Process joke
        category = joke_data["category"]
        type_ = joke_data["type"]
        nsfw = joke_data.get("flags", {}).get("nsfw", False)
        political = joke_data.get("flags", {}).get("political", False)
        sexist = joke_data.get("flags", {}).get("sexist", False)
        safe = joke_data.get("safe", True)
        lang = joke_data["lang"]

        # If the joke is of "single" type
        if type_ == "single":
            joke_text = joke_data.get("joke")
            setup = None
            delivery = None
        else:
            # For "twopart" type
            joke_text = None
            setup = joke_data.get("setup")
            delivery = joke_data.get("delivery")
        
        # Store in database
        joke_entry = Joke(
            category=category,
            type=type_,
            joke=joke_text,
            setup=setup,
            delivery=delivery,
            nsfw=nsfw,
            political=political,
            sexist=sexist,
            safe=safe,
            lang=lang
        )
        db.add(joke_entry)
    db.commit()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    await process_and_store_jokes(db)

@app.get("/jokes")
async def get_jokes(db: Session = Depends(get_db)):
    jokes = db.query(Joke).all()
    return jokes