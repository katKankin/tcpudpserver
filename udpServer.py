# -----------------------------------------------------------------
# Tecnológico de Costa Rica
# Curso: Redes
# TCP / UDP Sockets Connection
# Katherine Tuz Carrillo
# 2019
# -----------------------------------------------------------------
import socket
from _thread import *
import threading
import os

print_lock = threading.Lock()
# path defined to list files
path = 'c:\\Users\\kathetuz\\Desktop\\myserver\\files'

def udpserver():
    host = socket.gethostbyname(socket.gethostname())
    port = 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print("Welcome. The server UDP is listening")
    while 1:
        d = s.recvfrom(1024)
        data= d[0]
        addr = d[1]
        # -----------------------------------------------------------------
        # List
        # -----------------------------------------------------------------
        if ( (str(data.decode('ascii'))) == '-l'):
            files = []
            # r=root, d=directories, f = files
            for r, d, f in os.walk(path):
                for file in f:
                    files.append(os.path.join(r, file))
            #sending list to client
            for f in files:
                s.sendto(bytes(f, "utf8"), addr)
            s.sendto(bytes(" Finish", "utf8"), addr)
        # -----------------------------------------------------------------
        # Download
        # -----------------------------------------------------------------
        elif ((str(data.decode('ascii'))) == '-d'):
            filer = s.recvfrom(1024)
            filerData = filer[0]
            # addr = filer[1]
            fileParsed = str(filerData.decode('ascii'))
            mylist = os.listdir('./files')
            getSize = str(os.path.getsize('.\\files\\' + fileParsed))
            s.sendto(bytes(getSize, "utf8"), addr)
            if mylist.count(fileParsed) > 0:
                with open('.\\files\\' + filerData.decode('ascii'), 'rb') as f:
                    sendBytes = f.read(1024)
                    s.sendto(sendBytes, addr)
                    while sendBytes != "":
                        sendBytes = f.read(1024)
                        s.sendto(sendBytes, addr)
            else:
                s.sendto(bytes("not", "utf8"), addr)
            s.close()
        # -----------------------------------------------------------------
        # Upload
        # -----------------------------------------------------------------
        else:
            try:
                filer = s.recvfrom(1024)
                filerData = filer[0]
                addr = filer[1]
                parsing = str(filerData.decode('ascii'))
                if parsing == "Error":
                    print('There is an error')
                else:
                    s.sendto(bytes("Starting", "utf8"), addr)
                    sizeF = s.recvfrom(1024)
                    sizeFData = sizeF[0]
                    addr = sizeF[1]
                    convertsize = int((str(sizeFData.decode('ascii'))))
                    f = open(".\\files\\" + parsing, 'wb')
                    obtain = s.recvfrom(1024)
                    obtainData = obtain[0]
                    addr = obtain[1]
                    limit = len(obtainData)
                    f.write(obtainData)
                    while limit < convertsize:
                        s.sendto(bytes("Continue", "utf8"), addr)
                        obtain = s.recvfrom(1024)
                        obtainData = obtain[0]
                        addr = obtain[1]
                        limit += len(obtainData)
                        f.write(obtainData)
                        s.sendto(bytes("Finish", "utf8"), addr)
                    return('Process finished')
                s.close()
            except error:
                print('Error exception')


    s.close()

if __name__ == '__main__':
    udpserver()