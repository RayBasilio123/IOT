#!/usr/bin/env python3
# encoding: utf-8
from crypt import methods
from os.path import isfile, join
from os import listdir
import json
from flask import Flask, request, jsonify
import random
import secrets
import string
import jwt
import configparser
config = configparser.ConfigParser()
config.read('api.ini')

rasp_key = config.get('rasp_key', 'token')




app = Flask(__name__)


# def generate_password_letters_numbers(password_length):
#     """Gerar uma senha com letras e números, com o comprimento informado
#     :param comprimento: Comprimento da senha
#     :return: Senha gerada
#     """
#     password_characters = string.ascii_letters + string.digits
#     password = ''.join(secrets.choice(password_characters) for i in range(comprimento))
#     return password

def generate_random_number_not_in_a_list(list_items):
    print(list_items)
    random_number = random.randint(19324, 19326)
    while random_number in list_items:
        random_number = random.randint(19324, 19326)
    return random_number

def check_port(new_port ,all_port_file):
        onlyfiles = [int(f)
                  for f in listdir('ssh/portas') if isfile(join('ssh/portas',f))]
        random_number = random.randint(19324, 19326)



@app.route('/')
def index():
    return request.args

#http://127.0.0.1:5000/get_port?mac_address=1234&nome_dispositivo=rasp2
@app.route('/get_port')
def get_port():
    # all_ports = []
    # all_mac_address = []
    # # consultar nome de arquivos no diretorio ssh
    mac_address = request.args.get('mac_address')
    if mac_address == None:
        return {
            'error': "mac address not found"
        }, 400
        
    nome_dispositivo = request.args.get('nome_dispositivo')
    if nome_dispositivo == None:
        return {
            'error': "nome dispositivo not found"
        }, 400
    
    print(mac_address)
    
    
    all_mac_address = [(f)
                 for f in listdir('ssh/mac_address') if isfile(join('ssh/mac_address', f))]
    
    print(all_mac_address)
    
    if str(mac_address) in all_mac_address:
        print(mac_address,"AQUI")
        with open(f'ssh/mac_address/{mac_address}', 'r') as f:
            ssh_port = f.read()
            f.close()
        return {
        
            'mac_address': mac_address,
            'nome_dispositivo': nome_dispositivo,
            'porta': ssh_port,
        }
    else:
        active_ports = set()
        
        for f in listdir('ssh/portas') :
            print(f)
            with open(f'ssh/portas/{f}', 'r') as file:
                status = file.read()
                if status == 'Ativa':
                    active_ports.add(int(f))
                file.close()
            
        print(active_ports, 'ACTIVE PORTS')
        onlyfiles = {int(f)
                 for f in listdir('ssh/portas') if isfile(join('ssh/portas',f))}
        ssh_port = generate_random_number_not_in_a_list( onlyfiles - active_ports)
        
        with open(f'ssh/portas/{ssh_port}', 'w') as f:
            f.write('Inativa')
            f.close()
        with open(f'ssh/mac_address/{mac_address}', 'w') as f:
            f.write(str(ssh_port))
            f.close()
        with open(f'ssh/dispositivo/{mac_address}', 'w') as f:
            f.write(nome_dispositivo)
            f.close()
        return {
            'porta': ssh_port,
            'mac_address': mac_address,
            'nome_dispositivo': nome_dispositivo
        }
    
    
 

@app.route('/disconect_device')
def disconect_device():
    ssh_port = request.args.get('port')
    

    if ssh_port == None:
        return {
            'error': "port not found"
        }, 400
        
    if not isfile(f'ssh/portas/{ssh_port}'):
        return {
            'error': "port not registered"
        }, 400
        
    with open(f'ssh/portas/{ssh_port}', 'w') as f:
        f.write('Ativa')
        f.close()
    return {
        'porta': ssh_port
    }
    
    
# @app.route('/register_password')
# def register_password():
#     mac_address = request.args.get('mac_address')
#     password = request.args.get('password')
#     with open(f'ssh/passwords/{mac_address}', 'w') as f:
#         f.write(password)
#         f.close()
#     return {
#         'password': generate_password_letters_numbers(4),
#         'mac_address': mac_address
#     }

@app.route('/register_password', methods = ['POST'])
def register_pwd():
    data = request.json
    data2 = jwt.decode(data['package'], "secret", algorithms=["HS256"])
    mac_address = data2['mac_address']
    password = str(data2['key'])
    with open(f'ssh/passwords/{mac_address}', 'w') as f:
         f.write(password)
         f.close()
    return {
        'password': data2['key'],
        'mac_address': data2['mac_address']
    }
    
    
@app.route('/get_devices')
def get_devices():
    list_dir = []
    all_mac_address_port = []
    all_mac_address = [(f)
                 for f in listdir('ssh/mac_address') if isfile(join('ssh/mac_address', f))]
    
    for i in all_mac_address:
        print(i,"AQUI")
        with open(f'ssh/mac_address/{i}') as f:
            porta = f.readline().rstrip()
            all_mac_address_port.append(porta)
            f.close()
        with open(f'ssh/portas/{porta}') as r:
            status = r.readline().rstrip()
            r.close()
        with open(f'ssh/passwords/{i}') as j:
            senha = j.readline().rstrip()
            j.close()
        with open(f'ssh/dispositivo/{i}') as k:
            nome_dispositivo = k.readline().rstrip()
            k.close
            dados = {
                    "nome_dispositivo": nome_dispositivo,
                    "mac_address": i,
                    "porta":porta,
                    "senha":senha,
                    "status":status,
                    "forma_conexao": f"ssh -p  {porta} {nome_dispositivo}@http://ec2-44-192-129-106.compute-1.amazonaws.com"
                    }
        list_dir.append(dados)
    print(all_mac_address_port, "MAC")
    print(all_mac_address_port, "PORTS")
    print(list_dir)
    
    return json.dumps(list_dir)

app.run(debug=True)   


