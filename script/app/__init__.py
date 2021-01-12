from flask import Flask


from script.app.config import Config


navig = Flask(__name__)
navig.config.from_object(Config)

from script.app import routes

