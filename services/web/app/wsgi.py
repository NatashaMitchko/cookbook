from app import create_app

app = create_app()

# PROD ONLY ROUTES

@app.route("/healthcheck")
def healthcheck():
    return {"ping": "pong"}