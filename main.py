import datetime
import random
import os
from termcolor import colored

name = "Minh Duc"
dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, "data")

current_time = datetime.datetime.now()
if current_time.hour > 6 and current_time.hour < 12:
    phrase = "Good morning"
elif current_time.hour < 18:
    phrase = "Good afternoon"
else:
    phrase = "Good evening"
phrase = colored(phrase, color='blue')

random_topic = random.choice(os.listdir(data_dir))
topic_dir = os.path.join(data_dir, random_topic)
quote_file = os.path.join(topic_dir, random.choice(os.listdir(topic_dir)))
with open(quote_file, "r") as f:
    content = f.read().rpartition("-")
    quote = content[0]
    author = colored(content[2], 'magenta', attrs=["bold"])

name = colored(name, 'cyan', attrs=["bold"])
print(phrase + " " + name + "!", end="\n\n")
print(f'{quote}-{author}')
