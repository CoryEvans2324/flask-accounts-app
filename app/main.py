from app import create_app

app = create_app()

@app.after_request
def atfer_request(resp):
    resp.cache_control.max_age = 0
    return resp