import os
import httpx
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

load_dotenv()  # take environment variables from .env.
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') 
# TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_BOTCHAT_ID')

app = FastAPI() # Create a FastAPI instance

subscriptions = [] # Store the subscriptions in memory for now

class Subscription(BaseModel): # Define a Pydantic model for the subscription
    repo: str
    chat_id: str

async def send_telegram_message(chat_id: str, message: str):
    """
    Sends a message to a Telegram chat.

    Args:
        chat_id (str): The ID of the chat to send the message to.
        message (str): The message to send.

    Returns:
        None
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=data)

async def get_initial_commit_sha(repo: str):
    """
    Retrieves the SHA of the initial commit for a given repository.

    Args:
        repo (str): The name of the repository in the format "owner/repo".

    Returns:
        str: The SHA of the initial commit.

    Raises:
        httpx.HTTPStatusError: If a 4XX or 5XX HTTP status code is returned.
        httpx.RequestError: If an error occurs during the request.

    """
    url = f"https://api.github.com/repos/{repo}/commits/main" # URL for the GitHub API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url) # Send a GET request to the GitHub API
            response.raise_for_status()  # Raises exception for 4XX/5XX responses
            data = response.json() # Parse the JSON response
            return data['sha'] # Return the SHA of the initial commit
    except httpx.HTTPStatusError as e: 
        print(f"HTTP error occurred: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    return None  # TODO Consider what to do in case of failure to retrieve the SHA

@app.post("/subscribe/")
async def subscribe(subscription: Subscription):
    initial_commit_sha = await get_initial_commit_sha(subscription.repo)
    new_subscription = {
        'repo': subscription.repo,
        'chat_id': subscription.chat_id,
        'last_commit': initial_commit_sha
    }
    subscriptions.append(new_subscription)
    return {"message": "Subscribed successfully with initial commit SHA fetched!"}

async def check_repository_updates():
    async with httpx.AsyncClient() as client:
        for subscription in subscriptions:
            response = await client.get(f"https://api.github.com/repos/{subscription['repo']}/commits")
            json_response = response.json()
            if isinstance(json_response, list) and json_response:
                latest_commit = json_response[0]['sha']
                if latest_commit != subscription['last_commit']:
                    subscription['last_commit'] = latest_commit
                    message = f"New update in {subscription['repo']}: {latest_commit}"
                    print(message)
                    await send_telegram_message(subscription['chat_id'], message)
            else:
                print(f"Error with repo {subscription['repo']}: {json_response}")

def run_check_repository_updates():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(check_repository_updates())
    finally:
        loop.close()

scheduler = BackgroundScheduler()
scheduler.add_job(run_check_repository_updates, IntervalTrigger(seconds=30))
scheduler.start()
