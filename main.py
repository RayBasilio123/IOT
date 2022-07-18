#!/usr/bin/env python3
# encoding: utf-8
from os.path import isfile, join
from os import listdir
import json
from flask import Flask, request
import random
import secrets
import string
app = Flask(__name__)


def generate_password_letters_numbers(password_length):
    """Gerar uma senha com letras e números, com o comprimento informado
    :param comprimento: Comprimento da senha
    :return: Senha gerada
    """
    password_characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(password_characters) for i in range(comprimento))
    return password

def generate_random_number_not_in_a_list(list_items):
    random_number = random.randint(10000, 20000)
    while random_number in list_items:
        random_number = random.randint(10000, 20000)
    return random_number

def check_port(new_port ,all_port_file):
        onlyfiles = [int(f)
                  for f in listdir('ssh/portas') if isfile(join('ssh/portas',f))]
        random_number = random.randint(10000, 20000)



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
    print(mac_address)
    all_mac_address = [(f)
                 for f in listdir('ssh/mac_address') if isfile(join('ssh/mac_address', f))]
    
    print(all_mac_address)
    
    if str(mac_address) in all_mac_address:
        print(mac_address,"AQUI")
    else:
        onlyfiles = [int(f)
                 for f in listdir('ssh/portas') if isfile(join('ssh/portas',f))]
        ssh_port = generate_random_number_not_in_a_list(onlyfiles)
        with open(f'ssh/portas/{ssh_port}', 'w') as f:
            f.write('Inativa')
            f.close()
    
    # print(all_mac_address)
    # for i in all_mac_address:
    #     print(i,"AQUI")
    #     with open(f'ssh/portas/{i}') as f:
    #         all_mac_address_port.append(f.readline().rstrip())
    #         f.close()

    
    # onlyfiles = [int(f)
    #              for f in listdir('ssh/portas') if isfile(join('ssh/portas',f))]

    # if(set(all_mac_address_port) == set(onlyfiles)):
    #     print("Lists are equal")
    # else:
    #     print("Lists are not equal")
    #     ssh_port = generate_random_number_not_in_a_list(onlyfiles)
    #     with open(f'ssh/portas/{ssh_port}', 'w') as f:
    #         f.write('Inativa')
    #         f.close()
    
    
    
    #123
    # onlyfiles = [int(f)
    #              for f in listdir('ssh/portas') if isfile(join('ssh/portas',f))]
    # ssh_port = generate_random_number_not_in_a_list(onlyfiles)
#    with open(f'ssh/portas/{ssh_port}', 'w') as f:
 #       f.write('Inativa')
  #      f.close()
    
    
 
    nome_dispositivo = request.args.get('nome_dispositivo')
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
@app.route('/register_device')
def register_device():
    ssh_port = request.args.get('port')
    with open(f'ssh/portas/{ssh_port}', 'w') as f:
        f.write('Ativa')
        f.close()
    return {
        'porta': ssh_port
    }
    
    
@app.route('/register_password')
def register_password():
    mac_address = request.args.get('mac_address')
    password = request.args.get('password')
    with open(f'ssh/passwords/{mac_address}', 'w') as f:
        f.write(password)
        f.close()
    return {
        'password': generate_password_letters_numbers(4),
        'mac_address': mac_address
    }

app.run()   

