import berserk
import beeminderpy.beeminderpy as beem
import time
import json

LICHESS_USER = ''
LICHESS_API_TOKEN = ''
BEEMINDER_USER = ''
BEEMINDER_API_TOKEN = ''

BEEMINDER_CHESS_GOAL = ''

session = berserk.TokenSession(LICHESS_API_TOKEN)
lichess = berserk.Client(session)
bmndr = beem.Beeminder(BEEMINDER_API_TOKEN)

dpts = bmndr.get_datapoints(BEEMINDER_USER, BEEMINDER_CHESS_GOAL).decode()
d = json.loads(dpts)
lastData = d[0]["value"]

NOW = time.time()
t = time.strftime("%H:%M:%S",time.localtime())

bmndr.create_datapoint(BEEMINDER_USER, BEEMINDER_CHESS_GOAL, NOW, lastData, 
	comment=f"restarted app at {t} with last datapoint {lastData}")


while True:
	myData = lichess.users.get_public_data(LICHESS_USER)
	games = myData['count']['rated']
	if lastData !=  games:
		NOW = int(time.time())
		bmndr.create_datapoint(BEEMINDER_USER, BEEMINDER_CHESS_GOAL, NOW, games)
		lastData = games
	if time.localtime().tm_hour < 23:
		time.sleep(60*60)
	else:
		time.sleep(60*5)
