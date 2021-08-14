from mcipc.rcon.je import Biome, Client
with Client('127.0.0.1', 25575, passwd='minecraft') as client:
        client.effect.give('@p','speed')
