from flask import Flask, render_template
from flask_caching import Cache
from .feed import get_feed

# config = {
#     "DEBUG": False,  # True,
#     "CACHE_TYPE": "SimpleCache",
#     "CACHE_DEFAULT_TIMEOUT": 300,
# }

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


@cache.cached(timeout=3600)
def get_feed_cached():
    return get_feed()


@app.route("/", methods=["GET"])
def index():
    comments = get_feed_cached()
    # return comments
    return render_template("index.html", comments=comments)
