from utils.index import *
import socket, threading

ENCODING = "utf8"
KEY = "1001"

class Client(threading.Thread):
    def run(self):
        # initialize necessary variables
        spacing = ""
        clientHost = "127.0.0.1"
        clientPort = 12345
        clientAddress = (clientHost, clientPort)

        # open connection
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # connection.settimeout(2)

        print(spacing, "open")

        requestData = ["h", "e", "r", "n", "a", "n", "."]
        
        for datum in requestData:
            # send request to server
            print(spacing, "put:", datum)
            connection.sendto(encode_data(datum, KEY).encode(ENCODING), clientAddress)

            # get response from server
            responseData, clientAddress = connection.recvfrom(1024)

            if "error" in responseData.decode(ENCODING):
                print(spacing, "get:", responseData.decode(ENCODING))
                while 1:
                    connection.sendto(encode_data(datum, KEY).encode(ENCODING), clientAddress)
                    responseData, clientAddress = connection.recvfrom(1024)

                    if "error" not in responseData.decode(ENCODING):
                        print(spacing, "get:", responseData.decode(ENCODING))
                        break
            else: 
                print(spacing, "get:", responseData.decode(ENCODING))

        # close connection
        connection.close()
        print(spacing, "close")


client = Client()

client.start()

client.join()