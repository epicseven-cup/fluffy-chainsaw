from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

import emoji
import random
app = Flask("fluffy-chainsaw")
database = MongoClient("mongo")["fluffy-chainsaw"]
@app.route("/")
def main_page():
	return "main page"

@app.route("/url")
def url():
	# Creates the token
	all_emoji = list(emoji.EMOJI_DATA.keys())
	XSRF_LENGTH = 69
	emoji_token = random.choices(all_emoji, k=XSRF_LENGTH)
	print(emoji_token)
	emoji_token = "".join(emoji_token)
	print(emoji_token)
	# Save it to database
	xsrf_table = database["xsrf"]
	xsrf_table.insert_one({"token": emoji_token})
	# servers the forms
	return render_template("index.html", token=emoji_token)

@app.route("/post_route", methods=["POST"])
def storeURL():

	forum = request.form

	# Checks if the xrfs is in the database
	xsrf_token = forum.get("XSRF", "")
	xsrf_table = database["xsrf"]
	print("xsrf_token")
	search_result = xsrf_table.find_one({"token": xsrf_token})
	print("Search result")
	print(search_result)
	if search_result == None:
		# If it does not exist then return nothing
		return redirect("/404")
	# Stores it into the path
	url_table = database["url"]
	transform_url = forum.get("transform_url", "")
	orignal_url = forum.get("orignal_url", "")

	# Get the time
	limited_time = forum.get("time", "50")
	limited_time = int(limited_time)
	added_time = timedelta(minutes=limited_time)
	current_time = datetime.now()

	# expected to end
	expected_end = 	current_time + added_time

	# Checks for duplicate
	duplicate_query = {"transform": transform_url}

	duplicate_result = url_table.find_one(duplicate_query)

	if duplicate_result != None:
		print(duplicate_result)
		return redirect("/404")

	insert_data = {"orignal": orignal_url, "transform": transform_url, "time": expected_end}

	url_table.insert_one(insert_data)
	return redirect("/url")

@app.route("/url/<transform>")
def customRoute(transform):
	search_query = {"transform": transform}

	url_table = database["url"]

	result = url_table.find_one(search_query)

	# If the result does not exist exit
	if result == None:
		return redirect("/404")


	# Grab current time
	#NY = pytz.timezone("America/New_York")
	current_time = datetime.now()
	expected_time = result["time"]
	print(current_time)
	print(expected_time)
	if current_time > expected_time:
		return redirect("/404")
	else:
		redirect_url = result["orignal"]
		return redirect(redirect_url, code=302)
@app.route("/404")
def route404():
	return "404 Error"