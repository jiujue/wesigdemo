import threading
import socket
import dynamic.miniFrame as mini_frame
import sys
import re

class ServerbyTHreading():

    def __init__(self,ip="127.0.0.1",port=80,srcdir="./templates"):
        """
        :param ip: default 127.0.0.1
        :param port: default 80
        :param srcdir: source path
        """

        self.ip=ip
        self.port=port
        self.srcdir=srcdir
        self.ser=socket.socket(socket.AF_INET,
                socket.SOCK_STREAM)
        self.ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ser.bind((self.ip,self.port))
        self.ser.listen(127)

    def getFileType(self,filename):
        if filename.endswith(".html"):
            return "text/html; charset=utf-8"
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            return "image/jpeg"
        if filename.endswith(".gif"):
            return "image/gif"
        if filename.endswith(".png"):
            return "image/png"
        if filename.endswith(".css"):
            return "text/css"
        if filename.endswith(".au"):
            return "audio/basic"
        if filename.endswith(".wav"):
            return "audio/wav"
        if filename.endswith(".avi"):
            return "video/x-msvideo"
        if filename.endswith(".mov") or filename.endswith(".qt"):
            return "video/quicktime"
        if filename.endswith(".mpeg") or filename.endswith(".mpe"):
            return "video/mpeg"
        if filename.endswith(".vrml") or filename.endswith(".wrl"):
            return "model/vrml"
        if filename.endswith(".midi") or filename.endswith(".mid"):
            return "audio/midi"
        if filename.endswith(".mp3"):
            return "audio/mpeg"
        if filename.endswith(".ogg"):
            return "application/ogg"
        if filename.endswith(".pac"):
            return "application/x-ns-proxy-autoconfig"
        if filename.endswith(".ico"):
            return "image/x-icon"
        return "text/plain; charset=utf-8"

    def setResponds_hand(self,stat_code,stat_info,content_type,Length=-1):
        self.respond_hand = \
        """HTTP/1.1 {code} {info}\r\nServer: jiujue_ser\r\nContent-Type: {type}; charset=utf-8\r\nContent-Language: zh-CN\r\n\r\n""".\
            format(code=stat_code, info=stat_info,
                   type=content_type, Length=Length)

    def run(self):
        print("Start listen on {ip}:{port} for http protocol".format(ip=self.ip,port=self.port))
        while True:
            cli,add=self.ser.accept()
            print("Have new client connect , it's it info:",add)
            threading.Thread(target=self.handleRequest,args=(cli,add)).start()


    def handleRequest(self,cli,add):
        recv=cli.recv(1024).decode("utf-8")
        print(recv)
        method,path,protocol=recv.split("\r\n")[0].split(" ")


        if path=='/':
            path="/index.html"

        if path.endswith(".html"):
            env=dict()
            filepath=self.srcdir+path
            env["abspath"]=filepath
            env["srcdir"]=self.srcdir
            env["path"]=path
            env["cli"]=cli
            env["add"]=add
            respond_body=mini_frame.application(env, self.setResponds_hand)
            if not respond_body == 404:
                cli.send(self.respond_hand.encode("utf-8"))
                print("------------>sent hand >>\n", self.respond_hand)
                cli.send(respond_body.encode("utf-8"))
                print("------------>sent body >>\n", respond_body)
                cli.close()
            else:
                self.sendNotFound(cli)
        else:
            try:
                filepath=self.srcdir+path
                print("reqeuest path: >>",filepath)
                with open(filepath,"rb") as f:
                    ftype=self.getFileType(path)
                    self.setResponds_hand(200,"OK",ftype)
                    cli.send(self.respond_hand.encode("utf-8"))
                    print("------------>sent hand >>\n",self.respond_hand)
                    content=f.read()
                    cli.send(content)
                    if not ftype == "image/x-icon":
                        print("------------>sent body >>\n",content.decode("utf-8"))
                        pass
                    else:
                        print("------------>sent ico >>\n", )
                        pass
            except FileNotFoundError as e:
                self.sendNotFound( cli)
            finally:
                cli.close()

    def sendNotFound(self,cli):
        path = "/404.html"
        print("srcdir", self.srcdir, "path", path)
        filepath = self.srcdir + path
        print("File not found , auto transfer path to 404 : >>", filepath)
        print(filepath)
        with open(filepath, "rb") as f:
            self.setResponds_hand(404, "not found", self.getFileType(path))
            cli.send(self.respond_hand.encode("utf-8"))
            print("------------>sent hand >>\n", self.respond_hand)
            content = f.read()
            cli.send(content)
            print("------------>sent body >>\n", content.decode("utf-8"))


if __name__ == '__main__':
    
    if len(sys.argv) == 2 :
        temp = str(sys.argv[1])
        if None == re.match(r'^(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]?)\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]?)\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]):([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5]?)$',temp):
            print('argument is enough')
            print('eg: ./server.py ip:port')
            exit()
    else:
            print('argument is enough')
            print('eg: ./server.py ip:port')
            exit()

    temp = str(sys.argv[1]).split(':')
    IP = temp[0]
    PORT = int(temp[1])
    print('start http service on',IP,PORT)
    
    srcdir = "./templates"
    ser=ServerbyTHreading(ip=IP,port=PORT,srcdir=srcdir)
    ser.run()



