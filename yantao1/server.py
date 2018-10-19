import socket
import re
import time
import os
import wx
from datetime import datetime, timedelta, timezone
import threading
global ADDR
global BUFSIZE
global path
global index_content
global reg_content
global status

def receive(clientSocket, server):
    status = 0
    path = "C:/Users/Ricky/Desktop/network_http/source"
    global index_content
    global reg_content

    index_content = ""

    file = open('C:/Users/Ricky/Desktop/network_http/source/index.html', 'r')
    index_content += file.read()
    file.close()

    reg_content = ""

    file = open('C:/Users/Ricky/Desktop/network_http/source/reg.html', 'r')
    reg_content += file.read()
    file.close()

    global BUFSIZE
    request = clientSocket.recv(BUFSIZE).decode()
    print("以下为客户端发来的请求报文：\n", request)

    method = request.split(" ")[0]
    url = request.split(" ")[1]
    agreement = request.split(" ")[2].split("\n")[0]
    thing = re.search(r'([a-z]+.[a-z]+)',url)
    struct_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime(time.time()))
    if method == "GET":
        content = ""
        if agreement != "HTTP/1.1":
            content = "HTTP/1.1" + " 505 HTTP Version Not Supported\r\n\n" + "<h1>505 HTTP Version Not Supported<br />非常抱歉,您的HTTP版本不受支持!</h1>"
        else:
            if url == "/index.html":
                content = index_content
            elif url == "/reg.html":
                content = reg_content
            elif re.match('^/\?.*$', url):
                entry = url.split('?')[1]

                content = agreement + " 200 OK\r\n" + "Content-Type: " + "test/html\r\n"

                content += entry
                content += '<br /><font color="blue" size="7">好好学习，天天向上!</p>'
            else:
                print(thing.group(0))
                if deeper_dir(thing.group(0), path) == 0:
                    content = agreement + " 404 Not Found\r\n\n" + "<h1>404 Not Found<br />非常抱歉,您当前访问的网页不存在</h1>"
    elif method == "POST":
        content = ""
        form = ""
        entry = ""
        form = request.split('\r\n')
        entry = form[-1]
        content = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n\r\n'
        content += entry
        content += '<br /><font color="red" size="7">好好学习，天天向上!</p>'
    clientSocket.send((content).encode("gbk"))
    clientSocket.close()

def getmethod():
    return method

def getclientSocket():
    return clientSocket

def find_cur(string, path):
    global status
    status = 0
    l = []
    for x in os.listdir(path):
        if os.path.isfile(path + '/' + x):
            if string in x:
                l.append(os.path.abspath(x))
    if not l:
        print(path, " 下不存在该文件！")
        status = 0
    else:
        print(l)
        status = 1

def deeper_dir(string, p): # '.'表示当前路径，'..'表示当前路径的父目录
    find_cur(string, p)
    for x in os.listdir(p):  # 关键，将父目录的路径保留下来，保证在完成子目录的查找之后能够返回继续遍历。
        pp = p
        if os.path.isdir(pp):
            pp = os.path.join(pp, x)
            if os.path.isdir(pp):
                deeper_dir(string, pp)
    if status == 0:
        return 0
    else:
        return 1

def main():
    HOST = "127.0.0.1"
    PORT = 8000
    global BUFSIZE
    BUFSIZE = 1024
    global ADDR
    ADDR = (HOST, PORT)

    server = "Microsoft-IIS/4.0"
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(ADDR)
    serverSocket.listen(10)
    print("服务器已启动，等待连接中......")
    while True:
        clientSocket, ADDR = serverSocket.accept()
        thread = threading.Thread(target = receive, args = (clientSocket, server))
        thread.start()

if __name__ == '__main__':
    main()