from flask import Flask, render_template
from flask_caching import Cache
from .feed import get_feed

DEBUG = True

config = {
    "DEBUG": DEBUG,
    "TEMPLATES_AUTO_RELOAD": DEBUG,
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": ".cache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@cache.cached(timeout=1800)
def get_feed_cached():
    return get_feed()


@app.route("/", methods=["GET"])
def index():
    comments = get_feed_cached()
    return render_template("index.html", comments=comments)
