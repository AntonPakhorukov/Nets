import socket
import threading
# Ввод имени
nickname = input("Choose your nickname: ") # Запрос на ввод nickname
# Подключение к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет Ipv4 и TCP
client.connect(("172.20.10.4", 55102)) # Коннектимся к адресу сервера
# Слушать сервер и отправлять сообщения
def receive(): # функция, с помощью которой пробуем посылать/получать сообщения на севрер
    while True:
        try: # Получать сообщения с сервера и отправить Никнейм если он есть
            message = client.recv(1024).decode("ascii") # Получаем пакета размера 1024 на латинице 
            if message == "NICK": # если полученное сообщение содержит "NICK"
                client.send(nickname.encode("ascii")) # то отправляем свой ник на латинице
            else:
                print(message) # иначе просто печатаем сообщение
        except: # Если возникла ошибка
            # Закрываем соединение при возникновении ошибки
            print("An error occured!") # Сообщаем об ошибке
            client.close() # закрываем клиента
            break # Прерываем функцию
        
def write(): # Функция на запись сообщения
    while True:
        message = "{}: {}".format(nickname, input("")) # input - принимает ввод с клавиатуры
        # Первая часть {} = nickname, вторая {} = вводу с клавиатуры
        client.send(message.encode("ascii")) # отправляем сообщение в socket в формате латиницы
        
# Запуск потока для прослушивания и записи
receive_thread = threading.Thread(target=receive) # Создаем поток на прослушивания сервера
receive_thread.start() # запускаем поток

write_thread = threading.Thread(target=write) # Создаем поток на отправку сообщений
write_thread.start() # запускаем поток