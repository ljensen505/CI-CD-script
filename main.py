from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import hmac
import hashlib
import os
from starlette.responses import Response
import subprocess

BRANCH = "main"  # the branch you wish to deploy
PIP = "/path/to/your/venv/bin/pip"  # virtual environment's pip binary
SERVICE = "your-app.service"  # the systemd service used to run the app


load_dotenv()
app = FastAPI()


def update_and_restart():
    # Change the directory to the appropriate one
    os.chdir("/path/to/your/app")

    # Run the git commands to update the code
    subprocess.run(["git", "switch", BRANCH])
    subprocess.run(["git", "fetch"])
    subprocess.run(["git", "reset", "--hard", f"origin/{BRANCH}"])
    subprocess.run(["git", "merge", f"origin/{BRANCH}"])

    # install dependencies
    subprocess.run([PIP, "install", "-r", "requirements.txt"])

    # Restart app
    subprocess.run(["sudo", "systemctl", "restart", SERVICE])


@app.post("/")
async def root(request: Request) -> Response:
    # Get the webhook secret from your configuration
    webhook_secret = os.getenv("SECRET")

    if webhook_secret is None:
        raise HTTPException(
            status_code=400, detail=f"Error reading webhook_secret env variable"
        )

    try:
        # Get the X-Hub-Signature header from the request
        signature = request.headers.get("X-Hub-Signature")

        # Compute the expected hash of the request body and webhook secret
        expected_signature = (
            "sha1="
            + hmac.new(
                webhook_secret.encode("utf-8"), await request.body(), hashlib.sha1
            ).hexdigest()
        )

        # Compare the computed hash with the received signature
        if not hmac.compare_digest(signature, expected_signature):  # type: ignore
            raise HTTPException(status_code=400, detail="Invalid signature")

        response = Response(content="", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad request: {e}")

    update_and_restart()  # Assuming you have the implementation for this function
    return response
