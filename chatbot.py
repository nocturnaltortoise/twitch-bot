from config import Config
from time import sleep
import socket
import re

cfg = Config()

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))


def chat(skt, msg):
    print("test")
    skt.send((("PRIVMSG #{} :{}".format(cfg.CHAN, msg)).encode("utf-8")))
    # skt.send(("PRIVMSG #{" + cfg.CHAN + "}" + " " + ":{" + msg + "}").encode("utf-8"))

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

while True:

    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)
        message = CHAT_MSG.sub("", response)

        print(username + ": " + message)

        if "hello, server!\r\n" in response:
            print("test")
            chat(s, "hello\r\n")

    sleep(1 / cfg.RATE)
