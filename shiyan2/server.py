import socket
import threading
import wx
from time import ctime
from wx.lib.pubsub import pub

global status
global ADDR
global client_form
global client_information

global tcpServerSocket1

class TestThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def run(self):
        servermain()

def serverconnect(client_info):
    print("test1")

    HOST = "localhost"
    PORT = 1619
    global ADDR
    ADDR = (HOST, PORT)

    global tcpServerSocket1

    tcpServerSocket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcpServerSocket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServerSocket1.bind(ADDR)

    frame.serverstatusbox.AppendText("来自 " + client_info + " 客户端的连接。\n")

    while True:
        print("test2")
        data, ADDR = tcpServerSocket1.recvfrom(1024)
        data = data.decode()
        if data == "_quit":
            print("test3")
            frame.serverstatusbox.AppendText("来自  " + client_info + " 客户端的连接已中断（客户端操作）。\n")

            print("来自  " + client_info + " 客户端的连接已中断（客户端操作）。")
            tcpServerSocket1.close()
            break
        else:
            print("test4")
            frame.serverstatusbox.AppendText("从客户端 " + client_info + " 接收到的数据：" + data + "\n")

            print("从客户端 " + client_info + " 接收到的数据：" + data)
            tcpServerSocket1.sendto(("服务器已验收！ [%s] 传输的信息为：%s" % (ctime(), data)).encode(), ADDR)

def servermain():
    HOST = "localhost"
    PORT = 1619
    global ADDR
    ADDR = (HOST, PORT)
    global client_form
    client_form = [["user1", "123456"], ["user2", "234567"]]
    global status
    status = 0
    tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServerSocket.bind(ADDR)
    tcpServerSocket.listen(50)

    frame.serverstatusbox.AppendText("等待连接中！\n")

    print("等待连接中")
    while True:
        tcpClientSocket, ADDR = tcpServerSocket.accept()
        thread = threading.Thread(target=serverservice, args=(tcpClientSocket, ADDR))
        thread.start()
    #
    # tcpClientSocket, ADDR = tcpServerSocket.accept()
    # serverservice(tcpClientSocket, ADDR)

def serverservice(tcpClientSocket, ADDR):
    global status
    status = 0
    client_info1 = ""
    client_info2 = ""
    while status == 0:
        client_info1 = tcpClientSocket.recv(1024).decode()
        tcpClientSocket.send(("true").encode())
        client_info2 = tcpClientSocket.recv(1024).decode()
        client_info = [client_info1, client_info2]
        global client_form
        for i in range(len(client_form)):
            if client_info == client_form[i]:
                tcpClientSocket.send(("true").encode())
                status = 1
                # thing = client_info[0]
                break
        if status == 0:

            frame.serverstatusbox.AppendText("非法用户！")

            print("非法用户！")
            tcpClientSocket.send(("false").encode())
        elif status == 1:

            frame.serverstatusbox.AppendText("来自 " + client_info[0] + " 客户端的连接。")

            print("来自 " + client_info[0] + " 客户端的连接。")
    tcpClientSocket.close()
    if status == 1:
        serverconnect(client_info[0])

class serverFrame(wx.Frame):
    def __init__(self, superior):
        frame = wx.Frame.__init__(self, title="通讯小软件（服务器端）界面", parent=superior, size=(650, 550))
        panel = wx.Panel(self, -1)
        self.serverstatus = wx.StaticText(parent=panel, label="服务器状态：", pos=(100, 50))
        self.clientstatus = wx.StaticText(parent=panel, label="用户登陆信息：", pos=(100, 100))
        self.clientstatusbox = wx.TextCtrl(parent=panel, pos=(200, 50), size=(330, -1), style=wx.TE_READONLY)
        self.serverstatusbox = wx.TextCtrl(parent=panel, pos=(100, 150), size=(430, 200), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.startbutton = wx.ToggleButton(parent=panel, label="开关", pos=(100, 450))
        self.breakbutton = wx.Button(parent=panel, label="中断", pos=(450, 400))
        # self.breakobject = wx.StaticText(parent=panel, label="中断对象：", pos=(100, 400))
        # self.inputbreak = wx.TextCtrl(parent=panel, pos=(200, 400), size=(200, -1), style=wx.TE_LEFT)
        self.breakhint = wx.StaticText(parent=panel, label="中断提示：", pos=(100, 400))
        self.inputbreakhint = wx.TextCtrl(parent=panel, pos=(200, 400), size=(200, -1), style=wx.TE_READONLY)
        self.quitbutton = wx.Button(parent=panel, label="退出", pos=(450, 450))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnStartButtonClick, self.startbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBreakButtonClick, self.breakbutton)
        self.Bind(wx.EVT_BUTTON, self.OnQuitButtonClick, self.quitbutton)
        self.clientstatusbox.SetValue("服务器界面开启！")

    def OnStartButtonClick(self, event):
        if self.startbutton.GetValue() == False:
            print("False")
        else:
            TestThread()
            self.clientstatusbox.SetValue("服务器已开启！")

            # event.GetEventObject().Disable()

            # servermain()

    def OnBreakButtonClick(self, event):
        global tcpServerSocket1
        self.clientstatusbox.SetValue("服务器已中断！")
        self.inputbreakhint.SetValue("已从服务器断开连接！")
        self.startbutton.SetValue(True)
        self.serverstatusbox.SetValue("")
        tcpServerSocket1.close()

    def OnQuitButtonClick(self, event):
        self.Close()

if __name__ == '__main__':

    app = wx.App()
    frame = serverFrame(None)
    frame.Show()
    app.MainLoop()