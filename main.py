from flask import Flask
from pymongo import MongoClient

import emoji
import random
app = Flask("fluffy-chainsaw")
database = MongoClient("mongo")
@app.route("/")
def main_page():
	return "main page"

@app.route("/url")
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

@app.route("/post_route", method=["POST"])
def storeURL():

	forum = request.form

	# Checks if the xrfs is in the database
	xsrf_token = forum.get("XSRF", "")
	xsrf_table = database["xsrf"]
	search_result = xsrf_table.find_one({"token": xsrf_token})
	if search_result == None:
		# If it does not exist then return nothing
		return ""
	# Stores it into the path
	url_table = database["url"]
	transform_url = forum.get("transform_url", "")
	orignal_url = forum.get("orignal_url", "")


	# Checks for duplicate
	duplicate_query = {"transform": transform_url}

	duplicate_result = url_table.find_one(duplicate_query)

	if duplicate_result != None:
		return ""

	insert_data = {"orignal": orignal_url, "transform": transform_url}

	url_table.insert_one(insert_data)
	return

	@app.route("url/<transform>")
	def customRoute(transform):
		search_query = {"transform": transform}

		url_table = database["url"]

		result = url_table.find_one(search_query)

		# If the result does not exist exit
		if result == None:
			return ""
		

		return ""