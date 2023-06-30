import socket
import threading

# Данные соединения
host = '172.20.10.4'  # "Вводим наш IP" - запускаем внутри hosta
port = 55102

# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем socket
server.bind((host, port)) # привязываем socket к host'у и port'у 
server.listen() # переводим socket в состояние прослушивания
# Создаем списки клиентов и имен
clients = []
nicknames = []
# Отправка сообщения для всех подключенных клиентов 
def broadcast(message): # принимаем сообщение от клиента
    for client in clients: # и
        client.send(message) # отправляем это сообщение всем клиентам
        
# Функция обработки сообщений от клиентов
def handle(client):
    while True:
        try:
            # Рассылка сообщений
            message = client.recv(1024) # Если принимаем сообщение
            broadcast(message) # то рассылаем его всем клиентам 
        except: # если приосходит что-то не так:
            # Удаление и закрытие клиентов
            index = clients.index(client) # запоминем индекс клиента
            clients.remove(client) # удаляем клиента из списка клиентов
            client.close() # закрываем socket клиента
            nickname = nicknames[index] # берем никнейм удаленного клиента
            broadcast("{} left!".format(nickname).encode("ascii")) # сообщаем всем об удалениии клиента
            nicknames.remove(nickname) # удаляем никнейм из списка никнеймов
            break
        
# Функции отправки и прослушивания
def receive():
    while True:
        # Фиксация соединения
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        # запрос и запись никнейма
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        # Печать и рассылка никнейма
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode("ascii"))
        client.send("Connected to server!".encode("ascii"))
        # Запуск потока обработки сообщений для клиентов
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
print("Server if listening...")
receive()