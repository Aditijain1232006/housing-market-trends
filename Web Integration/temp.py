from pathlib import Path
import os
from flask import Flask, send_file

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR),
    static_folder=str(BASE_DIR / "assets"),
    static_url_path="/assets",
)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.after_request
def disable_cache(response):
    # Prevent stale page/assets in browser during local development.
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def index():
    return send_file(BASE_DIR / "index.html", mimetype="text/html")


@app.route("/__version")
def version():
    index_file = BASE_DIR / "index.html"
    return {
        "base_dir": str(BASE_DIR),
        "index_path": str(index_file),
        "index_last_modified": index_file.stat().st_mtime,
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5051"))
    app.run(debug=True, use_reloader=False, port=port)