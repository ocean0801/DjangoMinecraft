from mcipc.rcon.je import Biome, Client
import mcipc
try:
    with Client("127.0.0.1", 25575, passwd="minecraft") as client:
        re = client.run("tell","@p","test")
except mcipc.rcon.errors.NoPlayerFound:
    print("プレイヤーがーいなーいー")
