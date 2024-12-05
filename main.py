from netmiko import ConnectHandler

SWITCH_MAIN = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "cisco",
    "password": "cisco",
    }
    
mac_address = input ("Ingrese mac: ")



def show_mac_address_table(conexion, mac):
    connection = ConnectHandler(**conexion)
    salida = connection.send_command("show mac address-table")
    hostname = connection.send_command("show running-config | include hostname")

    buscar = salida.find(mac)
    if buscar != -1:
        puerto = salida.split(mac)[1].split()[1]
        print("\nLa MAC:",mac, "se encuentra en el puerto", puerto, "del dispositivo", hostname[9::])
        return puerto
    else:
        print (f"\nMac",mac, "no encontrada.")
        return buscar

def show_interface(conexion, port):
    connection = ConnectHandler(**conexion)
    comando = "show interface " + port
    salida = connection.send_command(comando)

    interface = salida.split()[0]
    return interface

def cdp_neighbor_details(conexion, interface):
    connection = ConnectHandler(**conexion)
    salida = connection.send_command("show cdp neighbors detail")

    texto = "Interface: " + interface
    dispositivos = salida.split("-------------------------")
    for i in dispositivos:
        if texto in i:
              filtro = i.split("Platform")[0]
              segundofiltro = filtro.split("IP address: ")[1]
              print("Vecino encontrado en ", texto)
              return segundofiltro.strip()
    return -1

def nueva_conexion(IP):
    print("\nConectando a ", IP) 
    SWITCH_MAIN = {
    "device_type": "cisco_ios",
    "host": IP,
    "username": "cisco",
    "password": "cisco",}
    return SWITCH_MAIN


while True: 
    PORT = show_mac_address_table(SWITCH_MAIN, mac_address)
    if PORT == -1:
        break
    INTERFACE = show_interface(SWITCH_MAIN, PORT)
    IP = cdp_neighbor_details(SWITCH_MAIN, INTERFACE)
    if IP == -1:
        break
    SWITCH_MAIN = nueva_conexion(IP)
