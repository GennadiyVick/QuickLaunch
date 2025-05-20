from threading import Thread
import socket
import select
import os
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import time


bufsize = 2048
accepttimeout = 5
readtimeout = 3
maxclients = 1


def strtodata(s):
    l = len(s)
    return l.to_bytes(2,'big') + s.encode('utf-8')


class StreamServer(QtCore.QObject):
    onFinish = QtCore.pyqtSignal(str)
    onRead = QtCore.pyqtSignal(str)

    def __init__(self, thread, port=51282):
        super().__init__()
        self.keep_running = False
        self.thread = thread
        self.childlist = []
        self.ipport = ('localhost', port)

    def childread(self, hdr):
        self.onRead.emit(hdr)

    def childFinish(self, receiver):
        self.childlist.remove(receiver)
        if (not self.keep_running) and (len(self.childlist) == 0):
            self.onFinish.emit('')
            if (self.thread != None):
                self.thread.quit()
                self.thread = None

    def newThread(self,client,addr):
        sock = client
        thread = QThread()
        receiver = Receiver(thread,sock, addr,self.onRead)
        receiver.onFinish.connect(self.childFinish)
        receiver.moveToThread(thread)
        thread.started.connect(receiver.run)
        self.childlist.append(receiver)
        thread.start()


    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(accepttimeout)
        try:
            self.sock.bind(self.ipport)
        except socket.error:
            print('can not open port',self.ipport)
            self.onFinish.emit('Ошибка открытия порта, возможно он уже занят')
            self.thread.quit()
            self.thread = None
            return
        except Exception as e:
            print('error',e)
        else:
            print('server listening:',self.ipport)
        self.sock.listen(maxclients)
        self.keep_running = True
        while self.keep_running:
            try:
                client, addr = self.sock.accept()
            except socket.timeout:
                time.sleep(0.5)
                #print('sleep')
            except socket.error as err:
                self.onFinish.emit(f'error accept: {err}')
                self.keep_running = False
                break;
            except Exception as e:
                print('error acception',e)
            else:
                print('client accepted:',addr)
                self.newThread(client,addr)

        self.sock.close()
        print('server stoped')
        if (len(self.childlist) == 0):
            self.onFinish.emit('')
            self.thread.quit()
            self.thread = None

class Receiver(QtCore.QObject):
    onFinish = QtCore.pyqtSignal(QtCore.QObject)
    #onRead = QtCore.pyqtSignal(DataHeader)

    def __init__(self, thread, sock, addr, onRead):
        super().__init__()
        sock.settimeout(readtimeout)
        self.sock = sock

        self.keep_running = True
        self.addr = addr
        self.thread = thread
        self.onRead = onRead


    def stop(self):
        self.keep_running = False

    def read(self,bs):
        try:
            data = self.sock.recv(bs)
        except socket.timeout:
            return None,2
        except socket.error as err:
            return None,0
        else:
            return data, 1

    def readstr(self, l):
        data, state = self.read(l)
        return (state, data.decode('utf-8')) if state == 1 else (state, '')

    def run(self):
        sleepcount = 0
        recvsize = 0
        self.keep_running = True
        while self.keep_running:
            data, state = self.read(2)
            if state == 2:
                time.sleep(0.5)
                sleepcount+=1
                if sleepcount > 5:
                    break
                else:
                    continue
            elif state == 0:
                break
            else:
                l = int.from_bytes(data,'big')
                r = self.readstr(l)
                if r[0] == 1:
                    self.onRead.emit(r[1])
                break
        self.sock.close()
        self.onFinish.emit(self)
        self.thread.quit()
        self.thread = None





def send(data, ipport=('localhost',51282)):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect(ipport)
        sock.settimeout(None)
        sock.sendall(strtodata(data))
        sock.close()
    except socket.timeout:
        print('sender error connection, time out')
        return False
    except socket.error:
        print('sender error connection')
        return False
    except Exception as e:
        print('Sender exception: %s' % e)
        return False
    else:
        return True


