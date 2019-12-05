import serial
import pymysql
import time
import socket
from threading import Thread, Lock
from conf import *
from pdu import *
import datetime

DEVICE_LAST_TIME = dict.fromkeys(DEVICE_INTERVAL.keys(), 0)
BLACKLIST = set()


def serial_read(port, mutex=Lock()):

    while SERIAL_READ:
        table_name = TB_NAME
        attributes = []
        values = []

        pdu = PDU_DEFAULT['attribute']
        size = PDU_DEFAULT['size']
        payload = PDU_DEFAULT['payload']

        address = ""

        insert = True
        i = 0
        mutex.acquire()
        while i < len(pdu):

            read = port.read(size[i])

            if pdu[i] == 'pdu':
                try:
                    pdu_type = PDU_TYPE[read]
                except:
                    insert = False
                    break

                size = pdu_type['size']
                pdu = pdu_type['attribute']
                payload = pdu_type['payload']
                i = 0
                continue

            if pdu[i] in payload:
                if pdu[i] == 'endereco':
                    read = read.hex().upper()
                    address = read
                else:
                    read = read.decode('utf-8')

                attributes.append('data')
                values.append(datetime.datetime.today())
                attributes.append(pdu[i])  # tag
                values.append(read)
            i += 1
        mutex.release()
        if insert:
            insert_database(table_name, attributes, values)
            print(values)


def insert_database(table_name, attributes, values):
    placeholders = ', '.join(['%s'] * len(attributes))
    attributes = ', '.join(attributes)
    values = tuple(values)
    print(values)

    connection = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME
    )
    try:
        with connection.cursor() as cursor:
            query = " INSERT INTO %s ( %s ) VALUES ( %s ) " % (
                table_name, attributes, placeholders
            )
            print(query, table_name, attributes, placeholders)
            cursor.execute(query, values)
        connection.commit()

    finally:
        connection.close()


def device_control(address):
    try:
        time_in = DEVICE_LAST_TIME[address]
        time_fn = time.time()
        interval = time_fn - time_in
        if interval < DEVICE_INTERVAL[address]:
            BLACKLIST.add(address)
        DEVICE_LAST_TIME[address] = time.time()
    except:
        BLACKLIST.add(address)

    return address not in BLACKLIST


def server(port, mutex):
    server_socket = socket.socket()
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    while True:
        conn = server_socket.accept()[0]
        data = conn.recv(4096).decode('utf-8')
        if 'A' in data:
            mutex.acquire()
            port.write(b'1')
            mutex.release()
        elif 'D' in data:
            mutex.acquire()
            port.write(b'0')
            mutex.release()

        conn.close()
    server_socket.close()


if __name__ == "__main__":
    port = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE)
    mutex = Lock()

    serial_thread = Thread(target=serial_read, args=(port, mutex))
    serial_thread.start()
    #server_thread = Thread(target=server, args=(port, mutex))
    #server_thread.start()

    serial_thread.join()
    #server_thread.join()
