import socket

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"[*] Received: {request}")
    client_socket.send("ACK!".encode())
    client_socket.close()
   
def start_server(client_address):
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建socket对象，走tcp通道
    tcp_server.bind(client_address) # 绑定地址
    tcp_server.listen(5) # 设置最大连接数，超过后排队
    print("[*] Listening on: %s:%d" % client_address)
    
    while True:
        client_socket, addr = tcp_server.accept() # 建立客户端连接
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        handle_client(client_socket) # 处理客户端请求 

client_host = socket.gethostname() # 获取本地主机名
client_port = 25566 # 端口号
client_address = (client_host, client_port)

start_server(client_address)