from PySide6 import QtCore, QtWebSockets, QtNetwork, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu
from PySide6.QtCore import QUrl

class MyServer(QtCore.QObject):
    def __init__(self, parent):
        super().__init__()
        self.clients = []
        print(f"server name: {parent.serverName()}")
        self.server = QtWebSockets.QWebSocketServer(parent.serverName(), parent.secureMode(), parent)
        if self.server.listen(QtNetwork.QHostAddress.SpecialAddress.LocalHost):
            print(
                f'Listening: {self.server.serverName()}:{self.server.serverAddress().toString()}:{str(self.server.serverPort())}'
            )
        else:
            print('error')
        self.server.acceptError.connect(self.onAcceptError)
        self.server.newConnection.connect(self.onNewConnection)
        self.clientConnection = None
        print(self.server.isListening())
        self.onNewConnection()

    def onAcceptError(accept_error):
        print("Accept Error: {}".format(accept_error))

    def onNewConnection(self):
        print("onNewConnection")
        self.clientConnection = self.server.nextPendingConnection()
        self.clientConnection.textMessageReceived.connect(self.processTextMessage)

        self.clientConnection.textFrameReceived.connect(self.processTextFrame)

        self.clientConnection.binaryMessageReceived.connect(self.processBinaryMessage)
        self.clientConnection.disconnected.connect(self.socketDisconnected)

        print("newClient")
        self.clients.append(self.clientConnection)

    def processTextFrame(self, frame, is_last_frame):
        print("in processTextFrame")
        print(f"\tFrame: {frame} ; is_last_frame: {is_last_frame}")

    def processTextMessage(self, message):
        print(f"processTextMessage - message: {message}")
        if self.clientConnection:
            for client in self.clients:
                # if client!= self.clientConnection:
                client.sendTextMessage(message)
            # self.clientConnection.sendTextMessage(message)

    def processBinaryMessage(self, message):
        print("b:",message)
        if self.clientConnection:
            self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        print("socketDisconnected")
        if self.clientConnection:
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    serverObject = QtWebSockets.QWebSocketServer('ws://localhost:8000/ws/notifications/', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)
    serverObject.closed.connect(app.quit)
    app.exec()