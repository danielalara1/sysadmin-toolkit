import subprocess
import shutil
import platform

def check_ping(ip: str) -> bool:
    parametro = "-n" if platform.system().lower() == "windows" else "-c"
   
    comando = ["ping", parametro, "1", ip]
    
    try:
        resultado = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        return resultado.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False

def check_disk_space(path: str) -> bool:
    try:
        total, usado, libre = shutil.disk_usage(path)
        
        
        porcentaje_libre = (libre / total) * 100
        
        
        total_gb = total // (2**30)
        libre_gb = libre // (2**30)
        
        print(f"\n[INFO] Analizando ruta: {path}")
        print(f"       Espacio Total: {total_gb} GB")
        print(f"       Espacio Libre: {libre_gb} GB ({porcentaje_libre:.2f}%)")
        
        if porcentaje_libre < 20.0:
            print(f"  [ALERTA] ¡El espacio libre está por debajo del 20%!")
            return False
        
        print(" [OK] El espacio en disco es saludable.")
        return True
        
    except FileNotFoundError:
        print(f" Error: La ruta '{path}' no existe en este sistema.")
        return False