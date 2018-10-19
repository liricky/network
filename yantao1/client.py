import socket  # for sockets
import sys  # for exit
import struct
import time
import re
import webbrowser as web #对导入的库进行重命名

Get_str='''GET /index.html HTTP/1.1
Host: 127.0.0.1:8000
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
Accept: image/webp,image/apng,image/*,*/*;q=0.8
Referer: http://127.0.0.1:8000/index.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
'''
Post_str='''GET /reg.html HTTP/1.1
Host: 127.0.0.1:8000
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9

'''

Error_str='''GET /ind.html HTTP/1.1
Host: 127.0.0.1:8000
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
Accept: image/webp,image/apng,image/*,*/*;q=0.8
Referer: http://127.0.0.1:8000/index.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
'''

Error1_str='''GET /index.html HTTP/1.0
Host: 127.0.0.1:8000
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
Accept: image/webp,image/apng,image/*,*/*;q=0.8
Referer: http://127.0.0.1:8000/index.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
'''

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(("127.0.0.1",8000))
key=int(input("键入1/2/3/4 来选择 测试GET 或 测试POST 或 测试错误404 或 测试错误505："))
try:
    if key == 1:
        sock.sendall(Get_str.encode())
    elif key == 2:
        sock.sendall(Post_str.encode())
    elif key == 3:
        sock.sendall(Error_str.encode())
    elif key == 4:
        sock.sendall(Error1_str.encode())
except socket.error:
    print("Error sending data!")

buffer=[]
while True:
    d=sock.recv(1024)
    if d:
        buffer.append(d.decode('gbk'))
    else:
        break
if key == 1:
    data = ''.join(buffer)
    file = open('test1.html', 'w')
    file.write(data)
    file.close()
    web.open_new_tab('test1.html')
    sock.close()
elif key == 2:
    data = ''.join(buffer)
    print(data)
    file = open('test2.html', 'w')
    file.write(data)
    file.close()
    web.open_new_tab('test2.html')
    sock.close()
elif key == 3:
    data = ''.join(buffer)
    thing = re.search(r"<h1>(.*)+</h1>", data)
    print(thing)
    file=open('test3.html','w')
    file.write(thing.group(0))
    file.close()
    web.open_new_tab('test3.html')
    sock.close()
elif key == 4:
    data = ''.join(buffer)
    thing1 = re.search(r"<h1>(.*)+</h1>", data)
    print(thing1)
    file = open('test4.html', 'w')
    file.write(thing1.group(0))
    file.close()
    web.open_new_tab('test4.html')
    sock.close()

