from scapy.all import *
import re
import wx

global load_packet
global load_raw
global has_raw
global status
global summary
global dpkt


def manage(object, ip, protocol, num):
    # object = "src"
    # ip = "192.168.1.103"
    # protocol = "tcp"
    filter = "ip %s %s and %s" % (object, ip, protocol)
    # num = 5
    global load_packet
    global load_raw
    global has_raw
    load_packet = []
    load_raw = []
    has_raw = 0
    global dpkt
    dpkt = sniff(filter=filter, prn=lambda x: x.summary(), count=num)
    for i in dpkt:
        IP(i).show()
        load_packet.append(repr(i))
        try:
            rawr = i[Raw].load
            print(rawr)
            print(repr(rawr))
            load_raw.append(repr(rawr))
            has_raw = 1
        except:
            has_raw = 0
            pass

    for i in load_packet:
        print(i)
        print("数据链路层报头")
        Ether_dst = re.search(r'(<Ether  dst=)(.*?)(\s)', i)
        Ether_src = re.search(r'(src=)(.*?)(\s)', i)
        Ether_type = re.search(r'(type=)(.*?)(\s)', i)
        print("IPv4 数据报头格式")
        VERSION = re.search(r'(version=)(.*?)(\s)', i)
        print("Version:" + VERSION.group(2))
        IHL = re.search(r'(ihl=)(.*?)(\s)', i)
        print("IP Header Length:" + IHL.group(2))
        TOS = re.search(r'(tos=)(.*?)(\s)', i)
        print("Type-of-Service:" + TOS.group(2))
        LEN = re.search(r'(len=)(.*?)(\s)', i)
        print("Total Length:" + LEN.group(2))
        ID = re.search(r'(id=)(.*?)(\s)', i)
        print("Identification:" + ID.group(2))
        FLAGS = re.search(r'(flags=)(.*?)(\s)', i)
        print("Flags:" + FLAGS.group(2))
        FRAG = re.search(r'(frag=)(.*?)(\s)', i)
        print("Fragment Offset:" + FRAG.group(2))
        TTL = re.search(r'(ttl=)(.*?)(\s)', i)
        print("Time-To-Live:" + TTL.group(2))
        PROTO = re.search(r'(proto=)(.*?)(\s)', i)
        print("Protocol:" + PROTO.group(2))
        CHKSUM = re.search(r'(chksum=)(.*?)(\s)', i)
        print("Header Checksum:" + CHKSUM.group(2))
        SRC = re.search(r'(<IP)(.*?)(src=)(.*?)(\s)', i)
        print("Source Address:" + SRC.group(4))
        DST = re.search(r'(<IP)(.*?)(dst=)(.*?)(\s)', i)
        print("Destination Adress:" + DST.group(4))
        OPTIONS = re.search(r'(options=)(.*?)(\s)', i)
        print("Options:" + OPTIONS.group(2))

    for i in load_raw:
        print(i)


class ipFrame(wx.Frame):
    def __init__(self, superior):
        frame = wx.Frame.__init__(self, title="抓包分析", parent=superior, size=(1080, 800))
        panel = wx.Panel(self, -1)
        self.title1 = wx.StaticText(parent=panel, label="数据链路层：", pos=(500, 20))
        self.eth_dst = wx.TextCtrl(parent=panel, pos=(50, 50), size=(360, -1), style=wx.TE_CENTER)
        self.eth_src = wx.TextCtrl(parent=panel, pos=(410, 50), size=(360, -1), style=wx.TE_CENTER)
        self.eth_type = wx.TextCtrl(parent=panel, pos=(770, 50), size=(240, -1), style=wx.TE_CENTER)
        self.title2 = wx.StaticText(parent=panel, label="IP层：", pos=(520, 80))
        self.version = wx.TextCtrl(parent=panel, pos=(50, 110), size=(120, -1), style=wx.TE_CENTER)
        self.ihl = wx.TextCtrl(parent=panel, pos=(170, 110), size=(120, -1), style=wx.TE_CENTER)
        self.tos = wx.TextCtrl(parent=panel, pos=(290, 110), size=(240, -1), style=wx.TE_CENTER)
        self.len = wx.TextCtrl(parent=panel, pos=(530, 110), size=(480, -1), style=wx.TE_CENTER)
        self.id = wx.TextCtrl(parent=panel, pos=(50, 140), size=(480, -1), style=wx.TE_CENTER)
        self.flags = wx.TextCtrl(parent=panel, pos=(530, 140), size=(90, -1), style=wx.TE_CENTER)
        self.frag = wx.TextCtrl(parent=panel, pos=(620, 140), size=(390, -1), style=wx.TE_CENTER)
        self.tol = wx.TextCtrl(parent=panel, pos=(50, 170), size=(240, -1), style=wx.TE_CENTER)
        self.pro = wx.TextCtrl(parent=panel, pos=(290, 170), size=(240, -1), style=wx.TE_CENTER)
        self.chksum = wx.TextCtrl(parent=panel, pos=(530, 170), size=(480, -1), style=wx.TE_CENTER)
        self.src = wx.TextCtrl(parent=panel, pos=(50, 200), size=(960, -1), style=wx.TE_CENTER)
        self.dst = wx.TextCtrl(parent=panel, pos=(50, 230), size=(960, -1), style=wx.TE_CENTER)
        self.options = wx.TextCtrl(parent=panel, pos=(50, 260), size=(960, -1), style=wx.TE_CENTER)
        self.title3 = wx.StaticText(parent=panel, label="TCP层：", pos=(515, 290))
        self.tcp_sport = wx.TextCtrl(parent=panel, pos=(50, 320), size=(240, -1), style=wx.TE_CENTER)
        self.tcp_dport = wx.TextCtrl(parent=panel, pos=(290, 320), size=(240, -1), style=wx.TE_CENTER)
        self.tcp_seq = wx.TextCtrl(parent=panel, pos=(530, 320), size=(480, -1), style=wx.TE_CENTER)
        self.tcp_ack = wx.TextCtrl(parent=panel, pos=(50, 350), size=(480, -1), style=wx.TE_CENTER)
        self.tcp_dataofs = wx.TextCtrl(parent=panel, pos=(530, 350), size=(160, -1), style=wx.TE_CENTER)
        self.tcp_reserved = wx.TextCtrl(parent=panel, pos=(690, 350), size=(160, -1), style=wx.TE_CENTER)
        self.tcp_flags = wx.TextCtrl(parent=panel, pos=(850, 350), size=(160, -1), style=wx.TE_CENTER)
        self.tcp_window = wx.TextCtrl(parent=panel, pos=(50, 380), size=(320, -1), style=wx.TE_CENTER)
        self.tcp_chksum = wx.TextCtrl(parent=panel, pos=(370, 380), size=(320, -1), style=wx.TE_CENTER)
        self.tcp_urgptr = wx.TextCtrl(parent=panel, pos=(690, 380), size=(160, -1), style=wx.TE_CENTER)
        self.tcp_options = wx.TextCtrl(parent=panel, pos=(850, 380), size=(160, -1), style=wx.TE_CENTER)
        self.title4 = wx.StaticText(parent=panel, label="UDP层：", pos=(515, 410))
        self.udp_sport = wx.TextCtrl(parent=panel, pos=(50, 430), size=(240, -1), style=wx.TE_CENTER)
        self.udp_dport = wx.TextCtrl(parent=panel, pos=(290, 430), size=(240, -1), style=wx.TE_CENTER)
        self.udp_len = wx.TextCtrl(parent=panel, pos=(530, 430), size=(160, -1), style=wx.TE_CENTER)
        self.udp_chksum = wx.TextCtrl(parent=panel, pos=(690, 430), size=(320, -1), style=wx.TE_CENTER)
        self.title5 = wx.StaticText(parent=panel, label="Raw：", pos=(520, 460))
        self.raw = wx.TextCtrl(parent=panel, pos=(50, 480), size=(960, 50), style=wx.TE_LEFT | wx.TE_MULTILINE)
        self.object = wx.TextCtrl(parent=panel, pos=(50, 550), size=(240, -1), style=wx.TE_CENTER)
        self.ip = wx.TextCtrl(parent=panel, pos=(290, 550), size=(240, -1), style=wx.TE_CENTER)
        self.protocal = wx.TextCtrl(parent=panel, pos=(530, 550), size=(240, -1), style=wx.TE_CENTER)
        self.num = wx.TextCtrl(parent=panel, pos=(770, 550), size=(240, -1), style=wx.TE_CENTER)
        self.num_catch = wx.TextCtrl(parent=panel, pos=(50, 600), size=(60, -1), style=wx.TE_CENTER)
        self.startbutton = wx.Button(parent=panel, label="开始抓包", pos=(300, 600))
        self.readbutton = wx.Button(parent=panel, label="读包", pos=(480, 600))
        self.clearbutton = wx.Button(parent=panel, label="清空", pos=(650, 600))

        self.createbutton = wx.Button(parent=panel, label="生成数据包", pos=(820, 600))

        self.summary = wx.TextCtrl(parent=panel, pos=(50, 650), size=(960, -1), style=wx.TE_LEFT | wx.TE_MULTILINE)
        self.Bind(wx.EVT_BUTTON, self.OnStartButtonClick, self.startbutton)
        self.Bind(wx.EVT_BUTTON, self.OnClearButtonClick, self.clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnReadButtonClick, self.readbutton)

        self.Bind(wx.EVT_BUTTON, self.OnCreateButtonClick, self.createbutton)

        self.eth_dst.SetValue("Ether dst")
        self.eth_src.SetValue("Ether src")
        self.eth_type.SetValue("Ether type")
        self.version.SetValue("Version")
        self.ihl.SetValue("IHL")
        self.tos.SetValue("Type of Service")
        self.len.SetValue("Total Length")
        self.id.SetValue("Identification")
        self.flags.SetValue("Flags")
        self.frag.SetValue("Fragment Offset")
        self.tol.SetValue("Time To Live")
        self.pro.SetValue("Protocol")
        self.chksum.SetValue("Header Checksum")
        self.src.SetValue("Source IP Address")
        self.dst.SetValue("Destination IP Address")
        self.options.SetValue("Options(最多四十字节）")
        self.object.SetValue("src|dst")
        self.ip.SetValue("ip address")
        self.protocal.SetValue("tcp|udp")
        self.tcp_sport.SetValue("tcp_sport")
        self.tcp_dport.SetValue("tcp_dport")
        self.tcp_seq.SetValue("tcp_seq")
        self.tcp_ack.SetValue("tcp_ack")
        self.tcp_dataofs.SetValue("tcp_dataofs")
        self.tcp_reserved.SetValue("tcp_reserved")
        self.tcp_flags.SetValue("tcp_flags")
        self.tcp_window.SetValue("tcp_window")
        self.tcp_chksum.SetValue("tcp_chksum")
        self.tcp_urgptr.SetValue("tcp_urgptr")
        self.tcp_options.SetValue("tcp_options")
        self.udp_sport.SetValue("udp_sport")
        self.udp_dport.SetValue("udp_dport")
        self.udp_chksum.SetValue("udp_chksum")
        self.udp_len.SetValue("udp_len")
        self.raw.SetValue("")
        self.num.SetValue("抓包数量")
        self.num_catch.SetValue("读包序号")
        self.summary.SetValue("")

    def OnStartButtonClick(self, event):
        global status
        status = 1
        object = self.object.GetValue()
        if (object != "src" and object != "dst"):
            self.object.SetValue("错误的内容填写")
            status = 0
        ip = self.ip.GetValue()
        protocol = self.protocal.GetValue()
        if (protocol != "tcp" and protocol != "udp"):
            self.protocal.SetValue("错误的内容填写")
            status = 0
        num = self.num.GetValue()
        if (status == 1):
            manage(object, ip, protocol, int(num))
        global dpkt
        # print(dpkt)
        # print(type(dpkt))
        t = 1
        for i in dpkt:
            self.summary.AppendText(str(t))
            self.summary.AppendText(": ")
            self.summary.AppendText(i.summary())
            self.summary.AppendText("\n")
            t = t + 1

    def OnReadButtonClick(self, event):
        global status
        if (status == 1):
            global load_packet
            global load_raw
            global has_raw
            i = self.num_catch.GetValue()
            i = int(i)
            i = i - 1
            # print(i)
            # print(type(i))
            protocol = self.protocal.GetValue()
            Ether_dst = re.search(r'(<Ether  dst=)(.*?)(\s)', load_packet[i])
            self.eth_dst.SetValue(Ether_dst.group(2))
            Ether_src = re.search(r'(src=)(.*?)(\s)', load_packet[i])
            self.eth_src.SetValue(Ether_src.group(2))
            Ether_type = re.search(r'(type=)(.*?)(\s)', load_packet[i])
            self.eth_type.SetValue(Ether_type.group(2))
            VERSION = re.search(r'(version=)(.*?)(\s)', load_packet[i])
            self.version.SetValue(VERSION.group(2))
            IHL = re.search(r'(ihl=)(.*?)(\s)', load_packet[i])
            self.ihl.SetValue(IHL.group(2))
            TOS = re.search(r'(tos=)(.*?)(\s)', load_packet[i])
            self.tos.SetValue(TOS.group(2))
            LEN = re.search(r'(len=)(.*?)(\s)', load_packet[i])
            self.len.SetValue(LEN.group(2))
            ID = re.search(r'(id=)(.*?)(\s)', load_packet[i])
            self.id.SetValue(ID.group(2))
            FLAGS = re.search(r'(flags=)(.*?)(\s)', load_packet[i])
            self.flags.SetValue(FLAGS.group(2))
            FRAG = re.search(r'(frag=)(.*?)(\s)', load_packet[i])
            self.frag.SetValue(FRAG.group(2))
            TTL = re.search(r'(ttl=)(.*?)(\s)', load_packet[i])
            self.tol.SetValue(TTL.group(2))
            PROTO = re.search(r'(proto=)(.*?)(\s)', load_packet[i])
            self.pro.SetValue(PROTO.group(2))
            CHKSUM = re.search(r'(chksum=)(.*?)(\s)', load_packet[i])
            self.chksum.SetValue(CHKSUM.group(2))
            SRC = re.search(r'(<IP)(.*?)(src=)(.*?)(\s)', load_packet[i])
            self.src.SetValue(SRC.group(4))
            DST = re.search(r'(<IP)(.*?)(dst=)(.*?)(\s)', load_packet[i])
            self.dst.SetValue(DST.group(4))
            OPTIONS = re.search(r'(options=)(.*?)(\s)', load_packet[i])
            self.options.SetValue(OPTIONS.group(2))
            if (protocol == "tcp"):
                TCP_SPORT = re.search(r'(<TCP  sport=)(.*?)(\s)', load_packet[i])
                self.tcp_sport.SetValue(TCP_SPORT.group(2))
                TCP_DPORT = re.search(r'(dport=)(.*?)(\s)', load_packet[i])
                self.tcp_dport.SetValue(TCP_DPORT.group(2))
                TCP_SEQ = re.search(r'(seq=)(.*?)(\s)', load_packet[i])
                self.tcp_seq.SetValue(TCP_SEQ.group(2))
                TCP_ACK = re.search(r'(ack=)(.*?)(\s)', load_packet[i])
                self.tcp_ack.SetValue(TCP_ACK.group(2))
                TCP_DATAOFS = re.search(r'(dataofs=)(.*?)(\s)', load_packet[i])
                self.tcp_dataofs.SetValue(TCP_DATAOFS.group(2))
                TCP_RESERVED = re.search(r'(reserved=)(.*?)(\s)', load_packet[i])
                self.tcp_reserved.SetValue(TCP_RESERVED.group(2))
                TCP_FLAGS = re.search(r'(flags=)(.*?)(\s)', load_packet[i])
                self.tcp_flags.SetValue(TCP_FLAGS.group(2))
                TCP_WINDOW = re.search(r'(window=)(.*?)(\s)', load_packet[i])
                self.tcp_window.SetValue(TCP_WINDOW.group(2))
                TCP_CHKSUM = re.search(r'(chksum=)(.*?)(\s)', load_packet[i])
                self.tcp_chksum.SetValue(TCP_CHKSUM.group(2))
                TCP_URGPTR = re.search(r'(urgptr=)(.*?)(\s)', load_packet[i])
                self.tcp_urgptr.SetValue(TCP_URGPTR.group(2))
                TCP_OPTIONS = re.search(r'(options=)(.*?)(\s)', load_packet[i])
                self.tcp_options.SetValue(TCP_OPTIONS.group(2))
                self.udp_sport.SetValue("udp_sport")
                self.udp_dport.SetValue("udp_dport")
                self.udp_chksum.SetValue("udp_chksum")
                self.udp_len.SetValue("udp_len")
            elif (protocol == "udp"):
                UDP_SPORT = re.search(r'(sport=)(.*?)(\s)', load_packet[i])
                self.udp_sport.SetValue(UDP_SPORT.group(2))
                UDP_DPORT = re.search(r'(dport=)(.*?)(\s)', load_packet[i])
                self.udp_dport.SetValue(UDP_DPORT.group(2))
                UDP_LEN = re.search(r'(len=)(.*?)(\s)', load_packet[i])
                self.udp_len.SetValue(UDP_LEN.group(2))
                UDP_CHKSUM = re.search(r'(chksum=)(.*?)(\s)', load_packet[i])
                self.udp_chksum.SetValue(UDP_CHKSUM.group(2))
                self.tcp_sport.SetValue("tcp_sport")
                self.tcp_dport.SetValue("tcp_dport")
                self.tcp_seq.SetValue("tcp_seq")
                self.tcp_ack.SetValue("tcp_ack")
                self.tcp_dataofs.SetValue("tcp_dataofs")
                self.tcp_reserved.SetValue("tcp_reserved")
                self.tcp_flags.SetValue("tcp_flags")
                self.tcp_window.SetValue("tcp_window")
                self.tcp_chksum.SetValue("tcp_chksum")
                self.tcp_urgptr.SetValue("tcp_urgptr")
                self.tcp_options.SetValue("tcp_options")
            if (has_raw == 1):
                self.raw.SetValue(load_raw[i])
            elif (has_raw == 0):
                self.raw.SetValue("")
        else:
            self.eth_dst.SetValue("Ether dst")
            self.eth_src.SetValue("Ether src")
            self.eth_type.SetValue("Ether type")
            self.version.SetValue("Version")
            self.ihl.SetValue("IHL")
            self.tos.SetValue("Type of Service")
            self.len.SetValue("Total Length")
            self.id.SetValue("Identification")
            self.flags.SetValue("Flags")
            self.frag.SetValue("Fragment Offset")
            self.tol.SetValue("Time To Live")
            self.pro.SetValue("Protocol")
            self.chksum.SetValue("Header Checksum")
            self.src.SetValue("Source IP Address")
            self.dst.SetValue("Destination IP Address")
            self.options.SetValue("Options(最多四十字节）")
            self.object.SetValue("src|dst")
            self.ip.SetValue("ip address")
            self.protocal.SetValue("tcp|udp")
            self.tcp_sport.SetValue("tcp_sport")
            self.tcp_dport.SetValue("tcp_dport")
            self.tcp_seq.SetValue("tcp_seq")
            self.tcp_ack.SetValue("tcp_ack")
            self.tcp_dataofs.SetValue("tcp_dataofs")
            self.tcp_reserved.SetValue("tcp_reserved")
            self.tcp_flags.SetValue("tcp_flags")
            self.tcp_window.SetValue("tcp_window")
            self.tcp_chksum.SetValue("tcp_chksum")
            self.tcp_urgptr.SetValue("tcp_urgptr")
            self.tcp_options.SetValue("tcp_options")
            self.udp_sport.SetValue("udp_sport")
            self.udp_dport.SetValue("udp_dport")
            self.udp_chksum.SetValue("udp_chksum")
            self.udp_len.SetValue("udp_len")
            self.raw.SetValue("")
            self.num.SetValue("抓包数量")
            self.num_catch.SetValue("读包序号")

    def OnClearButtonClick(self, event):
        self.eth_dst.SetValue("Ether dst")
        self.eth_src.SetValue("Ether src")
        self.eth_type.SetValue("Ether type")
        self.version.SetValue("Version")
        self.ihl.SetValue("IHL")
        self.tos.SetValue("Type of Service")
        self.len.SetValue("Total Length")
        self.id.SetValue("Identification")
        self.flags.SetValue("Flags")
        self.frag.SetValue("Fragment Offset")
        self.tol.SetValue("Time To Live")
        self.pro.SetValue("Protocol")
        self.chksum.SetValue("Header Checksum")
        self.src.SetValue("Source IP Address")
        self.dst.SetValue("Destination IP Address")
        self.options.SetValue("Options(最多四十字节）")
        self.object.SetValue("src|dst")
        self.ip.SetValue("ip address")
        self.protocal.SetValue("tcp|udp")
        self.tcp_sport.SetValue("tcp_sport")
        self.tcp_dport.SetValue("tcp_dport")
        self.tcp_seq.SetValue("tcp_seq")
        self.tcp_ack.SetValue("tcp_ack")
        self.tcp_dataofs.SetValue("tcp_dataofs")
        self.tcp_reserved.SetValue("tcp_reserved")
        self.tcp_flags.SetValue("tcp_flags")
        self.tcp_window.SetValue("tcp_window")
        self.tcp_chksum.SetValue("tcp_chksum")
        self.tcp_urgptr.SetValue("tcp_urgptr")
        self.tcp_options.SetValue("tcp_options")
        self.udp_sport.SetValue("udp_sport")
        self.udp_dport.SetValue("udp_dport")
        self.udp_chksum.SetValue("udp_chksum")
        self.udp_len.SetValue("udp_len")
        self.raw.SetValue("")
        self.num.SetValue("抓包数量")
        self.num_catch.SetValue("读包序号")
        self.summary.SetValue("")

    def OnCreateButtonClick(self, event):
        print("\n\n")
        data = "try create package"
        ip = IP(src="10.95.13.159", dst="10.95.11.179") / UDP(sport=12345, dport=5555) / data
        self.summary.AppendText(repr(ip))
        self.summary.AppendText("\n")
        send(ip, inter=1, count=1)


if __name__ == '__main__':
    app = wx.App()
    frame = ipFrame(None)
    frame.Show()
    app.MainLoop()
