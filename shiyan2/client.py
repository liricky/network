import socket
import getpass
import wx


class Client:
    def __init__(self):
        HOST = "localhost"
        PORT = 1619
        self.__BUFSIZE = 1024
        self.__ADDR = (HOST, PORT)
        self.__t = 0
        self.__tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tcpClientSocket.connect(self.__ADDR)

    def login(self, user_name, password):
        self.__client_inform = [user_name, password]

    def check(self):
        status = "false"
        if self.__t == 0:
            self.__tcpClientSocket.send(self.__client_inform[0].encode())
            status = self.__tcpClientSocket.recv(self.__BUFSIZE).decode()
            if status == "true":
                self.__tcpClientSocket.send(self.__client_inform[1].encode())
            self.__permission = self.__tcpClientSocket.recv(self.__BUFSIZE).decode()
            if self.__permission != "true":
                print("验证错误，无法登录！")
                # self.__tcpClientSocket.close()
            else:
                print("登录成功！")
                self.__t = 1
        else:
            print("已经登陆，退出来登陆其他账号！")

    def gett(self):
        return self.__t

    def sett(self, t):
        self.__t = t

    # def quit1(self):
    #     self.__tcpClientSocket.close()
    #     print("已退出！")
    #     self.__tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.__tcpClientSocket.connect(self.__ADDR)
    #     self.__t = 0
    #     self.__permission == "false"

    # def quit(self):
    #     self.__tcpClientSocket.send(("_quit").encode())
    #     self.__t = 0
    #     self.__permission == "false"
    #     #
    #     # self.__tcpClientSocket.recv(1024).decode()
    #     #
    #     self.__tcpClientSocket.close()
    #     print("已退出！")
    #     # self.__tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # self.__tcpClientSocket.connect(self.__ADDR)

    def close(self):
        self.__tcpClientSocket.close()

    def run(self, data):
        if self.__permission == "true":
            try:
                self.__tcpClientSocket.send(data.encode())
                self.__data1 = self.__tcpClientSocket.recv(self.__BUFSIZE).decode()
                print("从服务器得到的信息：", self.__data1)
            except Exception as e:
                print("错误：", e)
        else:
            print("连接中断!")

    def data_server(self):
        return self.__data1

    def getpermission(self):
        return self.__permission


class loginFrame(wx.Frame):
    def __init__(self, superior):
        self.client = Client()
        # print(self.client)
        frame1 = wx.Frame.__init__(self, title="通讯小软件（客户端）登陆界面", parent=superior, size=(450, 280))
        panel = wx.Panel(self, -1)
        self.username = wx.StaticText(parent=panel, label="用户名：", pos=(50, 50))
        self.password = wx.StaticText(parent=panel, label="口令：", pos=(50, 100))
        self.inputusername = wx.TextCtrl(parent=panel, pos=(100, 50), size=(150, -1), style=wx.TE_LEFT)
        self.inputpassword = wx.TextCtrl(parent=panel, pos=(100, 100), size=(150, -1), style=wx.TE_PASSWORD)
        self.connectbutton = wx.Button(parent=panel, label="登录", pos=(300, 70))
        self.note = wx.StaticText(parent=panel, label="提示：", pos=(50, 150))
        self.inputnote = wx.TextCtrl(parent=panel, pos=(100, 150), size=(300, -1), style=wx.TE_READONLY)
        self.Bind(wx.EVT_BUTTON, self.OnConnectButtonClick, self.connectbutton)
        self.inputnote.SetValue("请输入用户名和口令以登陆！")

    def OnConnectButtonClick(self, event):
        if self.inputusername.GetValue() == "" or self.inputpassword.GetValue() == "":
            self.inputnote.SetValue("用户名及口令不能为空！")
        else:
            if self.client.gett() == 0:
                self.client.login(self.inputusername.GetValue(), self.inputpassword.GetValue())
                self.client.check()
                if self.client.getpermission() == "true":
                    # self.inputnote.SetValue("登陆成功——请输入要传送的信息：")
                    self.client.sett(1)
                    self.client.close()
                    frame1 = contentFrame(None)
                    frame1.Show()
                    self.Close()
                else:
                    self.inputnote.SetValue("验证错误")


class contentFrame(wx.Frame):
    def __init__(self, superior):
        # self.__client = frame.client
        self.__rem = ""
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__client.connect(("localhost",1619))
        frame1 = wx.Frame.__init__(self, title="通讯小软件（客户端）登陆界面", parent=superior, size=(700, 500))
        panel = wx.Panel(self, -1)
        # panel.SetBackgroundColour("white")
        self.sendmessage = wx.StaticText(parent=panel, label="发送信息：", pos=(50, 100))
        self.sendbutton = wx.Button(parent=panel, label="发送", pos=(550, 100))
        self.quitbutton = wx.Button(parent=panel, label="退出", pos=(550, 50))
        self.inputmessage = wx.TextCtrl(parent=panel, pos=(130, 100), size=(400, -1), style=wx.TE_LEFT)
        self.note = wx.StaticText(parent=panel, label="提示：", pos=(50, 50))
        self.inputnote = wx.TextCtrl(parent=panel, pos=(130, 50), size=(400, -1), style=wx.TE_READONLY)
        self.serverdata = wx.StaticText(parent=panel, label="返回信息：", pos=(50, 150))
        self.inputdata = wx.TextCtrl(parent=panel, pos=(130, 150), size=(400, 280), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.Bind(wx.EVT_BUTTON, self.OnSendButtonClick, self.sendbutton)
        self.Bind(wx.EVT_BUTTON, self.OnQuitButtonClick, self.quitbutton)
        self.inputnote.SetValue("登陆成功——请输入要传送的信息：")

    # def OnConnectButtonClick(self, event):
    #     if self.inputusername.GetValue() == "" or self.inputpassword.GetValue() == "":
    #         self.inputnote.SetValue("用户名及口令不能为空！")
    #     else:
    #         if self.client.gett() == 0:
    #             self.client.login(self.inputusername.GetValue(), self.inputpassword.GetValue())
    #             self.client.build_connect()
    #             self.client.check()
    #             if self.client.getpermission() == "true":
    #                 self.inputnote.SetValue("登陆成功——请输入要传送的信息：")
    #             else:
    #                 self.inputnote.SetValue("验证错误")
    #         else:
    #             self.inputnote.SetValue("已经登陆，退出来登陆其他账号！")

    def OnSendButtonClick(self, event):
        # if self.__client.gett() == 1:
        #     if self.__client.getpermission() == "true":
        #         if self.inputmessage.GetValue() != "":
        #             self.__client.run(self.inputmessage.GetValue())
        #             self.inputdata.SetValue(self.__client.data_server())
        #         else:
        #             self.inputnote.SetValue("发送的信息不能为空！")
        #     else:
        #         self.inputnote.SetValue("连接中断")
        # else:
        #     self.inputnote.SetValue("尚未登陆！")
        try:
            if self.inputmessage.GetValue() == "":
                self.inputnote.SetValue("发送的信息不能为空！")
            else:
                self.__client.sendall(self.inputmessage.GetValue().encode())
                data = self.__client.recv(1024).decode()
                self.inputdata.AppendText("从服务器端返回信息：" + data + "\n")
        except Exception as e:
            wx.MessageBox(message="您已被服务器踢出连接！", caption="警告！", style=wx.OK)
            self.Close()

    def OnQuitButtonClick(self, event):
        # if self.__client.gett() == 1:
        #     if self.__client.getpermission() == "true":
        #         self.inputnote.SetValue("已退出")
        #         self.inputdata.SetValue("")
        #         self.inputmessage.SetValue("")
        #         self.__client.sett(0)
        #         # frame = loginFrame(None)
        #         # frame.Show()
        #         self.Close()
        #         self.__client.quit()
        #     else:
        #         self.inputnote.SetValue("连接中断")
        # else:
        #     self.inputnote.SetValue("尚未登陆！")
        try:
            self.__rem = ""
            self.__client.send(("_quit").encode())
            self.__client.close()
            self.Close()
        except Exception as e:
            wx.MessageBox(message="您已被服务器踢出连接！", caption="警告！", style=wx.OK)
            self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = loginFrame(None)
    frame.Show()
    app.MainLoop()
