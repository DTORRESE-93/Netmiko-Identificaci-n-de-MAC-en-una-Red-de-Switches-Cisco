# Practica Netmiko: Identificación de MAC en una Red de Switches Cisco
### Por: Torres Estrada Danna Carolina.

Este proyecto tiene como objetivo automatizar la búsqueda de una dirección MAC específica en una red de switches Cisco, aprovechando las capacidades de los protocolos CDP (Cisco Discovery Protocol) y comandos de gestión remota.

La solución emplea la librería **Netmiko**, diseñada para facilitar la conexión y ejecución de comandos en dispositivos de red mediante SSH, y permite rastrear de manera eficiente una dirección MAC a través de múltiples dispositivos conectados en cascada.

## Funcionalidades principales

1.  **Búsqueda de MAC Address**: Localiza el puerto en el que se encuentra una dirección MAC específica en el switch principal.
2.  **Consulta de Vecinos CDP**: Identifica los dispositivos vecinos conectados al puerto donde se encuentra la MAC, para continuar el rastreo en caso necesario.
3.  **Conexión Automática**: Establece conexión con switches vecinos y continúa el proceso hasta encontrar el dispositivo donde está ubicada la MAC o llegar al final de la topología.

## Requisitos

-   **Dispositivos Cisco con CDP habilitado**.
-   **Acceso SSH a los switches** (con credenciales válidas).
-   **Python 3.x** con las siguientes librerías:
    -   `Netmiko`

## Cómo funciona

1.  El programa solicita la dirección MAC a rastrear.
2.  Se conecta al switch principal y busca la MAC en la tabla de direcciones.
3.  Si se encuentra la MAC, identifica el puerto correspondiente y consulta detalles de los vecinos conectados mediante CDP.
4.  Si se encuentra un vecino, el programa se conecta automáticamente y repite el proceso.
5.  El proceso finaliza al encontrar la MAC o cuando no hay más vecinos disponibles.

Este proyecto simplifica la tarea de administración de redes al reducir el tiempo necesario para localizar dispositivos y solucionar problemas relacionados con su ubicación en la topología.

## Código: 
	from  netmiko  import  ConnectHandler

	SWITCH_MAIN  = {
	"device_type": "cisco_ios",
	"host": "192.168.1.1",
	"username": "cisco",
	"password": "cisco",
	}

	mac_address  =  input ("Ingrese mac: ")
  
	def  show_mac_address_table(conexion, mac):
	connection  =  ConnectHandler(**conexion)
	salida  =  connection.send_command("show mac address-table")
	hostname  =  connection.send_command("show running-config | include hostname")

	buscar  =  salida.find(mac)
	if  buscar  !=  -1:
	puerto  =  salida.split(mac)[1].split()[1]
	print("\nLa MAC:",mac, "se encuentra en el puerto", puerto, "del dispositivo", hostname[9::])
	return  puerto
	else:
	print (f"\nMac",mac, "no encontrada.")
	return  buscar

	def  show_interface(conexion, port):
	connection  =  ConnectHandler(**conexion)
	comando  =  "show interface "  +  port
	salida  =  connection.send_command(comando)
	interface  =  salida.split()[0]
	return  interface

	def  cdp_neighbor_details(conexion, interface):
	connection  =  ConnectHandler(**conexion)
	salida  =  connection.send_command("show cdp neighbors detail")
	texto  =  "Interface: "  +  interface
	dispositivos  =  salida.split("-------------------------")

	for  i  in  dispositivos:
	if  texto  in  i:
	filtro  =  i.split("Platform")[0]
	segundofiltro  =  filtro.split("IP address: ")[1]
	print("Vecino encontrado en ", texto)
	return  segundofiltro.strip()
return  -1

	def  nueva_conexion(IP):
	print("\nConectando a ", IP)

	SWITCH_MAIN  = {
	"device_type": "cisco_ios",
	"host": IP,
	"username": "cisco",
	"password": "cisco",}
	return  SWITCH_MAIN

	while  True:
	PORT  =  show_mac_address_table(SWITCH_MAIN, mac_address)
	if  PORT  ==  -1:
	break

	INTERFACE  =  show_interface(SWITCH_MAIN, PORT)
	IP  =  cdp_neighbor_details(SWITCH_MAIN, INTERFACE)
	if  IP  ==  -1:
	break
	SWITCH_MAIN  =  nueva_conexion(IP)