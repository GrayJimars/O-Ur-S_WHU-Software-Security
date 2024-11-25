import socket

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"[*] Received: {request}")
    client_socket.send("ACK!".encode())
    client_socket.close()
   
def start_server(client_address):
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ����socket������tcpͨ��
    tcp_server.bind(client_address) # �󶨵�ַ
    tcp_server.listen(5) # ����������������������Ŷ�
    print("[*] Listening on: %s:%d" % client_address)
    
    while True:
        client_socket, addr = tcp_server.accept() # �����ͻ�������
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        handle_client(client_socket) # ����ͻ������� 

client_host = socket.gethostname() # ��ȡ����������
client_port = 25566 # �˿ں�
client_address = (client_host, client_port)

start_server(client_address)