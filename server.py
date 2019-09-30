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

def tcpserver():
    host = socket.gethostbyname(socket.gethostname())
    port = 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    print('Welcome. The server TCP is listening')

    while True:
        c, addr = s.accept()
        data = c.recv(1024)
        # -----------------------------------------------------------------
        # List
        # -----------------------------------------------------------------
        if ( (str(data.decode('ascii'))) == '-l'):
            files = []
            # r=root, d=directories, f = files
            for r, d, f in os.walk(path):
                for file in f:
                    files.append(os.path.join(r, file))
            for f in files:
                c.send(bytes(f, "utf8"))
            c.send(bytes(" Finish", "utf8"))
        # -----------------------------------------------------------------
        # Download
        # -----------------------------------------------------------------
        elif( (str(data.decode('ascii'))) == '-d'):
            filer = c.recv(1024)
            fileParsed = str(filer.decode('ascii'))
            mylist = os.listdir('./files')
            getSize = str(os.path.getsize('.\\files\\' + fileParsed))
            c.send(bytes(getSize, "utf8"))
            if mylist.count(fileParsed) > 0:
                with open('.\\files\\' + filer.decode('ascii'), 'rb') as f:
                    sendBytes = f.read(1024)
                    c.send(sendBytes)
                    while sendBytes != "":
                        sendBytes = f.read(1024)
                        c.send(sendBytes)
            else:
                c.send("not")
            c.close()
        # -----------------------------------------------------------------
        # Upload
        # -----------------------------------------------------------------
        else:
            try:
                filer = c.recv(1024)
                parsing = str(filer.decode('ascii'))
                if parsing == "Error":
                    print('There is an error')
                else:
                    c.send(bytes("Starting", "utf8"))
                    sizeF = c.recv(1024)
                    convertsize = int((str(sizeF.decode('ascii'))))
                    f = open(".\\files\\" + parsing, 'wb')
                    obtain = c.recv(1024)
                    limit = len(obtain)
                    f.write(obtain)
                    while limit < convertsize:
                        c.send(bytes("Continue", "utf8"))
                        obtain = c.recv(1024)
                        limit += len(obtain)
                        f.write(obtain)
                        c.send(bytes("Finish", "utf8"))
                    print('Process finished')
                c.close()
            except error:
                print('Error exception')

    s.close()


if __name__ == '__main__':
    tcpserver()