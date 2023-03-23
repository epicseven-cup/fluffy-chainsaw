from flask import Flask
from pymongo import MongoClient

import emoji
import random
app = Flask("fluffy-chainsaw")
database = MongoClient("mongo")
@app.route("/")
def main_page():
	return "main page"

@app.route("url")
def url():
	# Creates the token
	all_emoji = list(emoji.EMOJI_DATA.keys())
	XSRF_LENGTH = 42069
	emoji_token = random.choices(all_emoji, k=XSRF_LENGTH)
	# Save it to database
	xsrf_table = database["xsrf"]
	xsrf_table.insert_one({"token": emoji_token})
	# servers the forms
	return render_template("url/index.html", token=emoji_token)

@app.route("post_route")
def storeURL():
	return

