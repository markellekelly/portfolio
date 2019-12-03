import praw
from subprocess import run,Popen, PIPE, STDOUT

bot = praw.Reddit(user_agent='stacia5000',
                  client_id='62Jk2dZKv5-Wqg',
                  client_secret='fO8MgmqsWSM9P9Wx9EYsjNxvzZY',
                  username=USER_NAME,
                  password=SECRET_KEY)

subreddit = bot.subreddit('CSC466')
comments = subreddit.stream.comments()
for comment in comments:
   text = comment.body
   print(text)
   if 'hey stacia?' in text.lower():
      message = "Hey, don't be so shy! I'm glad to help answer your questions about CSC Instructors and their research areas. Just type 'hey stacia!' followed by your question\n\n"
      message += "Don't know what to ask? Try one of the following:\n\n"
      message += "What senior projects has Dekhtyar advised?\n\n"
      message += "What is Phillip Nico's polyrating?\n\n"
      message += "What journals are Zoe Wood published in?\n\n"
      comment.reply(message) # Send message
   if 'hey stacia!' in text.lower():
      if len(text) < 100:
        query = text.lower().split('hey stacia!')
        p = run(['python3','staciareddit.py'],stdout=PIPE, input=query[1], universal_newlines=True, encoding='utf8')
        print(p.stdout.replace("\n","\n\n"))
        comment.reply(p.stdout.replace("\n","\n\n"))
