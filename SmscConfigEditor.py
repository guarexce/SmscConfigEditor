#!/usr/bin/env python

from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
import mysql.connector
from mysql.connector import Error

start_page_html = """
<html>
    <head>
        <title>Настройки подключения к базе данных</title>
    </head>
    <body>
        <form method="get" action="">
            <table align="center">
                <tr></<tr>
                <tr>
                    <td><p>Название соединения: </p></td>
                    <td><input align="left" type="text" name="connection_name" value="%(connection_name)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Адрес хоста: </p></td>
                    <td><input align="left" type="text" name="host_address" value="%(host_address)s"></td>
                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Имя базы данных: </p></td>
                    <td><input align="left" type="text" name="database_name" value="%(database_name)s"></td>
                </tr>
                <tr></<tr>
                <tr>
                    <td><p align="left">Пользователь: </p></td>
                    <td><input align="left" type="text" name="username" value="%(username)s"></td>
                </tr>
                <tr></<tr>
                <tr>
                    <td><p align="left">Пароль: </p></td>
                    <td><input align="left" type="text" name="password" value="%(password)s"></td>
                </tr>
                <tr></<tr>
                <tr>
                    <td><input align="left" type="submit" value="По умолчанию" name="ByDefault"></td>
                    <td><input align="left" type="submit" value="Сохранить" name="Save"></td>
                </tr>
            </table>
        </form>
    </body>
</html>
"""

next_page_html = """
<html>
    <head>
        <title>Редактор конфигурации СМС-Центра</title>
    </head>
    <body>
        <form method="get" action="">
            <table align="center">
                <tr></<tr>
                <tr>
                    <td><p>IP-адрес телекоммуникационного оборудования: </p></td>
                    <td><input type="text" name="telecomm_hardware_ip" value="%(telecomm_hardware_ip)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Порт телекоммуникационного оборудования: </p></td>
                    <td><input type="text" name="telecomm_hardware_port" value="%(telecomm_hardware_port)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>IP-адрес базы данных: </p></td>
                    <td><input type="text" name="database_ip" value="%(database_ip)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Порт базы данных: </p></td>
                    <td><input type="text" name="database_port" value="%(database_port)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Имя пользователя к базе данных: </p></td>
                    <td><input type="text" name="database_username" value="%(database_username)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Пароль к базе данных: </p></td>
                    <td><input type="text" name="database_password" value="%(database_password)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Наименование схемы базы данных: </p></td>
                    <td><input type="text" name="database_schema" value="%(database_schema)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Ограничение принимаемых и отправляемых сообщений: </p></td>
                    <td><input type="text" name="queue_limit" value="%(queue_limit)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Прослушиваемый IP-адрес для SMPP подключений: </p></td>
                    <td><input type="text" name="smpp_listen_ip" value="%(smpp_listen_ip)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><p>Прослушиваемый порт для SMPP подключений: </p></td>
                    <td><input type="text" name="smpp_listen_port" value="%(smpp_listen_port)s"></td>                    
                </tr>
                <tr></<tr>
                <tr>
                    <td><input type="submit" value="Настройки подключения" name="ConnectionSettings"></td>
                    <td><input type="submit" value="Записать" name="Write"></td>
                </tr>
            </table>
        </form>
    </body>
</html>
"""

connection_name_by_default = 'CONNECTION'
host_address_by_default = '10.0.0.22'
database_name_by_default = 'smsc_db'
username_by_default = 'config_editor'
password_by_default = ''

def start_page(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])

    connection_name = d.get('connection_name', [''])[0]
    host_address = d.get('host_address', [''])[0]
    database_name = d.get('database_name', [''])[0]
    username = d.get('username', [''])[0]
    password = d.get('password', [''])[0]

    connection_name = escape(connection_name)
    host_address = escape(host_address)
    database_name = escape(database_name)
    username = escape(username)
    password = escape(password)

    response_body = start_page_html % {
        'connection_name': connection_name or connection_name_by_default,
        'host_address': host_address or host_address_by_default,
        'database_name': database_name or database_name_by_default,
        'username': username or username_by_default,
        'password': password or password_by_default
    }

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode()]

def start_by_default_page(environ, start_response):
    response_body = start_page_html % {
        'connection_name': connection_name_by_default,
        'host_address': host_address_by_default,
        'database_name': database_name_by_default,
        'username': username_by_default,
        'password': password_by_default
    }

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode()]

connection = None
cursor = None

def next_page(environ, start_response):
    request_body = environ['QUERY_STRING']
    d = parse_qs(request_body)

    connection_name = d.get('connection_name', [''])[0]
    host_address = d.get('host_address', [''])[0]
    database_name = d.get('database_name', [''])[0]
    username = d.get('username', [''])[0]
    password = d.get('password', [''])[0]

    connection_name = escape(connection_name)
    host_address = escape(host_address)
    database_name = escape(database_name)
    username = escape(username)
    password = escape(password)

    telecomm_hardware_ip = ''
    telecomm_hardware_port = ''
    database_ip = ''
    database_port = ''
    database_username = ''
    database_password = ''
    database_schema = ''
    queue_limit = ''
    smpp_listen_ip = ''
    smpp_listen_port = ''

    global connection
    global cursor

    if connection == None:
        connection = mysql.connector.connect(
            host='localhost',
            database='smsc_db',
            user='admin',
            password='Admin_12345'
        )

        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")

            statement = """
                SELECT telecomm_hardware_ip, telecomm_hardware_port, database_ip,
                database_port, database_username, database_password,
                database_schema, queue_limit, smpp_listen_ip, smpp_listen_port
                FROM new_settings_list;
            """
            cursor.execute(statement)

            record = cursor.fetchone()
                
            telecomm_hardware_ip = record[0]
            telecomm_hardware_port = record[1]
            database_ip = record[2]
            database_port = record[3]
            database_username = record[4]
            database_password = record[5]
            database_schema = record[6]
            queue_limit = record[7]
            smpp_listen_ip = record[8]
            smpp_listen_port = record[9]
    else:
        telecomm_hardware_ip = d.get('telecomm_hardware_ip', [''])[0]
        telecomm_hardware_port = d.get('telecomm_hardware_port', [''])[0]
        database_ip = d.get('database_ip', [''])[0]
        database_port = d.get('database_port', [''])[0]
        database_username = d.get('database_username', [''])[0]
        database_password = d.get('database_password', [''])[0]
        database_schema = d.get('database_schema', [''])[0]
        queue_limit = d.get('queue_limit', [''])[0]
        smpp_listen_ip = d.get('smpp_listen_ip', [''])[0]
        smpp_listen_port = d.get('smpp_listen_port', [''])[0]
        
        telecomm_hardware_ip = escape(telecomm_hardware_ip)
        telecomm_hardware_port = escape(telecomm_hardware_port)
        database_ip = escape(database_ip)
        database_port = escape(database_port)
        database_username = escape(database_username)
        database_password = escape(database_password)
        database_schema = escape(database_schema)
        queue_limit = escape(queue_limit)
        smpp_listen_ip = escape(smpp_listen_ip)
        smpp_listen_port = escape(smpp_listen_port)

        if connection.is_connected():
            values = (
                telecomm_hardware_ip,
                telecomm_hardware_port,
                database_ip,
                database_port,
                database_username,
                database_password,
                database_schema,
                queue_limit,
                smpp_listen_ip,
                smpp_listen_port
            )
            
            statement = """
                UPDATE new_settings_list SET
                telecomm_hardware_ip = %s,
                telecomm_hardware_port = %s,
                database_ip = %s,
                database_port = %s,
                database_username = %s,
                database_password = %s,
                database_schema = %s,
                queue_limit = %s,
                smpp_listen_ip = %s,
                smpp_listen_port = %s;
            """

            cursor.execute(statement, values)
            connection.commit()

    response_body = next_page_html % { # Fill the above html template in
        'telecomm_hardware_ip': telecomm_hardware_ip or '',
        'telecomm_hardware_port': telecomm_hardware_port or '',
        'database_ip': database_ip or '',
        'database_port': database_port or '',
        'database_username': database_username or '',
        'database_password': database_password or '',
        'database_schema': database_schema or '',
        'queue_limit': queue_limit or '',
        'smpp_listen_ip': smpp_listen_ip or '',
        'smpp_listen_port': smpp_listen_port or ''
    }

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode()]

def choice_page(environ, start_response):
    request_body = environ['QUERY_STRING']
    d = parse_qs(request_body)

    by_default = d.get('ByDefault', [''])[0]
    save = d.get('Save', [''])[0]
    connection_settings = d.get('ConnectionSettings', [''])[0]
    write = d.get('Write', [''])[0]

    global connection
    global cursor

    if by_default:
        return start_by_default_page(environ, start_response)
    elif save:
        return next_page(environ, start_response)
    elif connection_settings:
        if connection != None:
            connection.shutdown()

        connection = None
        cursor = None
        
        return start_page(environ, start_response)
    elif write:
        return next_page(environ, start_response)

    if connection != None:
        connection.shutdown()

    connection = None
    cursor = None

    return start_page(environ, start_response)
        
server_address = 'localhost'
server_port = 8051

httpd = make_server(server_address, server_port, start_page)

httpd.handle_request()

while True:
    httpd = make_server(server_address, server_port, choice_page)

    httpd.handle_request()
