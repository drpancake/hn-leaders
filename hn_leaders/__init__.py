from flask import Flask
from flask_caching import Cache
from .feed import get_feed

# config = {
#     "DEBUG": False,  # True,
#     "CACHE_TYPE": "SimpleCache",
#     "CACHE_DEFAULT_TIMEOUT": 300,
# }

config = {
    "DEBUG": False,
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": ".cache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route("/", methods=["GET"])
@cache.cached(timeout=3600)
def index():
    f = get_feed()
    return f
