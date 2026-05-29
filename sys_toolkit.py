import sys
import os
import os_utils
import log_parser
import threat_intel  
from typing import NoReturn

def mostrar_menu() -> None:
    print("\n" + "="*45)
    print("   KIT DE HERRAMIENTAS SYSADMIN (DÍA 3)")
    print("="*45)
    print("1. Verificar conectividad (Ping)")
    print("2. Comprobar espacio en disco")
    print("3. Auditoría de Seguridad SSH (Logs + API)") # <--- NOMBRE MEJORADO
    print("4. Salir")
    print("="*45)

def ejecutar_opcion(opcion: str) -> None:
    if opcion == "1":
        ip = input("Introduce la IP o dominio a verificar: ").strip()
        print(f"⏳ Enviando ping a {ip}...")
        if os_utils.check_ping(ip):
            print("¡El host está activo y responde!")
        else:
            print(" El host NO responde.")
            
    elif opcion == "2":
        ruta_defecto = "C:\\" if os.name == 'nt' else "/"
        ruta = input(f"Introduce la ruta a verificar [{ruta_defecto}]: ").strip()
        if not ruta:
            ruta = ruta_defecto
        os_utils.check_disk_space(ruta)
        
    elif opcion == "3":
        print(" Paso 1: Parseando el archivo auth.log local...")
        conteo_ips = log_parser.parse_auth_log("auth.log")
        
        if not conteo_ips:
            print(" No se detectaron ataques en el log.")
        else:
            print("🌐 Paso 2: Consultando geolocalización de IPs en Internet...")
            threat_intel.generar_tabla_amenazas(conteo_ips)
                
    elif opcion == "4":
        print(" Saliendo del kit. ¡Buen turno de guardia!")
        sys.exit(0)
    else:
        print(" Opción no válida.")

def main() -> NoReturn:
    while True:
        mostrar_menu()
        seleccion = input("Selecciona una opción (1-4): ").strip()
        ejecutar_opcion(seleccion)

if __name__ == "__main__":
    main()