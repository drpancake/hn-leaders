from flask import Flask

# from flask_caching import Cache

# config = {
#     "DEBUG": True,          # some Flask specific configs
#     "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
#     "CACHE_DEFAULT_TIMEOUT": 300
# }
app = Flask(__name__)
# app.config.from_mapping(config)
# cache = Cache(app)


@app.route("/", methods=["GET"])
def index():
    return "lololol"
