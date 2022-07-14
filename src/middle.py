import socket, threading
import random
from bitarray import bitarray

ENCODING = "utf8"


def randomLoss(data):
    a = bitarray()
    a.frombytes(data)
    spacing = "            "

    int_random = random.randint(1, 11)
    if(int_random > 3):
        return a.tobytes()

    slice_a = a[int(len(a) * 0.3):]
    print(spacing, "Hay perdida: ", int_random / 10 , "porcentaje " ,slice_a.tobytes())

    return slice_a.tobytes()

class Middle(threading.Thread):
    def run(self):
        # initialize necessary variables
        spacing = "            "
        clientHost = "127.0.0.1"
        clientPort = 12345
        clientAddress = (clientHost, clientPort)

        # open connection
        clientConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientConnection.bind(clientAddress)

        # initialize necessary variables
        serverHost = "127.0.0.1"
        serverPort = 12346
        serverAddress = (serverHost, serverPort)

        # open connection
        serverConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print(spacing, "open")

        while 1:
            # get request from client
            clientRequestData, clientAddress = clientConnection.recvfrom(1024)
            print(spacing, "get:", clientRequestData.decode(ENCODING))

            serverRequestData = randomLoss(clientRequestData).decode(ENCODING)

            # print(randomLoss(clientRequestData))

            # send request to server
            print(spacing, "put:", serverRequestData)
            serverConnection.sendto(serverRequestData.encode(ENCODING), serverAddress)

            # get response from server
            serverResponseData, serverAddress = serverConnection.recvfrom(1024)
            print(spacing, "get:", serverResponseData.decode(ENCODING))

            # modify response (if desired)
            clientResponseData = serverResponseData.decode(ENCODING)

            # send response to client
            print(spacing, "put:", clientResponseData)
            clientConnection.sendto(clientResponseData.encode(ENCODING), clientAddress)

            if serverResponseData.decode(ENCODING) == "done":
                break

        # close connection
        serverConnection.close()
        clientConnection.close()
        print(spacing, "close")

# create all threads
middle = Middle()

# start all threads
middle.start()

# join all threads
middle.join()
