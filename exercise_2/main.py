from flask import Flask, jsonify
import sqlite3
import os
import config
import db
import sys
from api_controller import urls_blueprint
import api_controller

# input args
if (len(sys.argv) == 2 and sys.argv[1] == 'reset'):
    print("Cleaning database...")
    db.reset_db(config.DATABASE_PATH)

# database
conn = db.connect(config.DATABASE_PATH)
db.load_schema(config.SCHEMA_PATH, conn)
api_controller.DB_CONN = conn

# Init flask app
app = Flask(__name__)
app.register_blueprint(urls_blueprint)
app.run(debug=False, threaded=True, port=config.PORT)


print("finish")