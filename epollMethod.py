import select
import socket

def handle_recv(sock,recv_data):
    print("recv_data",recv_data)
    sock.send("I git it,I'm so sorry")


def main():

    # create listener socket
    listen_s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # bind port ip
    listen_s.bind(("192.168.30.198",8848))
    # setting listener total number
    listen_s.listen(20)

    # creat socket dictionary ,storage socket map to fileno
    socket_dict={}
    # put into listener socket and the fileno
    socket_dict[listen_s.fileno()]=listen_s
    # create epoll root
    epl = select.epoll()
    # add listener node into epoll tree
    # argument : need listener fileno , listener event
    epl.register(listen_s.fileno(),select.EPOLLIN)
    # loop
    while True:
        # obtain core returned fileno,socket
        client_list = epl.poll()
        # process everyone
        for client_sock,client_info in client_list:
            # if the socket is not existence ,then is new client connect,
            if socket_dict[client_sock.fileno()] == client_sock:
                # accept new connect and put into epoll root
                new_client_socket,new_client_info = listen_s.accept()
                socket_dict[new_client_socket.fileno()]=new_client_socket
                epl.register(new_client_socket.fileno(),select.EPOLLIN)
            else:
                # if the socket in old socket ,then recv data
                recv_data=client_sock.recv()
                if len(recv_data)>0:
                    # if have data, handle the data
                    handle_recv(client_sock,recv_data)
                else:
                    # if no have data,then is client close connect
                    # then delete the socket and epoll tree
                    epl.unregister(client_sock)
                    del socket_dict[client_sock.fileno]
                    client_sock.close()
    # close listener socket
    listen_s.close()

if __name__ == '__main__':
    main()