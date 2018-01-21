import praw
import time
import os
import requests

def botlogin():
	print ("Logging in...")
	r = praw.Reddit(username = "username",
	      password = "password",
	      client_id = "client_id",
	      client_secret = "client_secret",
	      user_agent = "user_agent")
	print("Logged in.")
	return r



def run_bot(r, comments_replied_to):
	n = 10
	movie = []
	print("Obtaining up to " + str(n) + " comments...")
	for comment in r.subreddit('CAS_Bot+test').comments(limit=n):
		if "!media " in comment.body and comment not in comments_replied_to and comment.author != r.user.me():
			print("String containing \"!media\" found!")

			###gets words after '!movie' and turns it into a usable format.
			keyphrase = comment.body[comment.body.find("!movie")+1:][6::]
			keyphrase = keyphrase.split()
			keyphrase = '+'.join(keyphrase)

			###checks if the movie requested exists. if it does, it gives the expected response.
			try:
				info = requests.get("http://www.omdbapi.com/?apikey=apikey=" + keyphrase).json()['Plot']
				comment_reply = "Here is a plot summary:\n\n"			
				comment_reply += ">" + info
				comment_reply += "\n\n*****"
				comment_reply += "\n\n" + " "
				comment_reply += "\n\n ^^Info ^^from ^^[omdbapi.com](https://omdbapi.com)." + " ^^I ^^am ^^a ^^bot ^^created ^^by ^^/u/81isnumber1. ^^Instructions ^^can ^^be ^^found ^^[here](https://github.com/orangeismyfavorite/CAS_Bot/blob/master/README.md"

				comment.reply(comment_reply)
				comments_replied_to.append(comment.id)

			except Exception:
				comments_replied_to.append(comment.id)
				print("That movie didn't exist! Just going to ignore that...")
				pass

			###puts the comment id into a text file so a check makes sure to not respond to
			###the same comment twice.
			with open("comments_replied_to.txt", "a") as f:
					f.write(comment.id + "\n")



	print("Sleeping for 10 seconds...")
	time.sleep(10)

###checks if file of comment ids exists. if it does, it puts the id there
###if not, it creates the file.
def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt.", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")

	return comments_replied_to


r = botlogin()
comments_replied_to = get_saved_comments()

###loops the program
while True:
	run_bot(r, comments_replied_to)
