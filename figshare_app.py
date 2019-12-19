import os
from flask import Flask, redirect, url_for

from .figshare_blueprint import make_figshare_blueprint, figshare


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["FIGSHARE_OAUTH_CLIENT_KEY"] = os.environ.get("FIGSHARE_OAUTH_CLIENT_KEY")
app.config["FIGSHARE_OAUTH_CLIENT_SECRET"] = os.environ.get("FIGSHARE_OAUTH_CLIENT_SECRET")
figshare_bp = make_figshare_blueprint()
app.register_blueprint(figshare_bp, url_prefix="/login")


@app.route("/")
def index():
    if not figshare.authorized:
        return redirect(url_for("figshare.login"))
    resp = figshare.get("account/verify_credentials.json")
    assert resp.ok
    return resp

