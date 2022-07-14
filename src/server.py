import socket, threading
from utils.index import *
import time, random

ENCODING = "utf8"
KEY = "1001"

def random_retard():
    limit = [500, 3000]
    random_limit = random.randint(limit[0], limit[1] + 1)
    print('Retard: ', random_limit)
    return random_limit/1000

class Server(threading.Thread):
    def run(self):
        # initialize necessary variables
        count = 0
        spacing = "\t\t\t"
        serverHost = "127.0.0.1"
        serverPort = 12346
        serverAddress = (serverHost, serverPort)

        # open connection
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection.bind(serverAddress)

        print(spacing, "open")

        while 1:
            # get request from client
            requestData, clientAddress = connection.recvfrom(1024)
            responseDataWithCode = decode_data(requestData, KEY)

            print(spacing, "get:", requestData) #[:-1 * len(responseDataWithCode)]

            # process request
            count += 1

            # random retard 500-3000 miliseconds
            time.sleep(random_retard())

            if (responseDataWithCode == "0" * (len(KEY) - 1)):
                if requestData.decode(ENCODING) == ".":
                    responseData = "done"
                else:
                    responseData = "ok [" + str(count) + "]"
            else:
                responseData = "error [" + str(count) + "]"

            # send response to client
            print(spacing, "put:", responseData)
            connection.sendto(responseData.encode(ENCODING), clientAddress)

            # close connection
            if requestData.decode(ENCODING) == ".":
                break

        connection.close()
        print(spacing, "close")


server = Server()

server.start()

server.join()
