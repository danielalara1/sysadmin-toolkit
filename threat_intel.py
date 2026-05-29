import requests
import datetime
from typing import Dict, Any

def consultar_amenaza_ip(ip: str) -> Dict[str, str]:
    """Consulta la API de ipinfo para obtener país y organización."""
    url = f"https://ipinfo.io/{ip}/json"
    resultado = {"pais": "Local/Privada", "organizacion": "Red Interna"}
    
    if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("127."):
        return resultado

    try:
        respuesta = requests.get(url, timeout=4)
        if respuesta.status_code == 200:
            datos: Dict[str, Any] = respuesta.json()
            resultado["pais"] = datos.get("country", "Desconocido")
            resultado["organizacion"] = datos.get("org", "Desconocida")
    except requests.RequestException:
        resultado["pais"] = "Error Red"
        resultado["organizacion"] = "No alcanzable"
        
    return resultado

def generar_tabla_amenazas(conteo_ips: Dict[str, int]) -> None:
    """Dibuja la tabla en consola y exporta un reporte en archivo de texto."""
    lineas_reporte = []
    lineas_reporte.append("="*75)
    lineas_reporte.append(f"{'IP ATACANTE':<18} | {'INTENTOS':<8} | {'PAÍS':<6} | {'ORGANIZACIÓN / ISP'}")
    lineas_reporte.append("="*75)
    
    for ip, intentos in conteo_ips.items():
        info_api = consultar_amenaza_ip(ip)
        lineas_reporte.append(f"{ip:<18} | {intentos:<8} | {info_api['pais']:<6} | {info_api['organizacion']}")
    
    lineas_reporte.append("="*75)
    
    texto_final = "\n".join(lineas_reporte)
    print("\n" + texto_final)
    
    fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
    nombre_archivo = f"reporte_seguridad_{fecha_hoy}.txt"
    
    print(f" Diagnóstico: Intentando escribir {len(lineas_reporte)} líneas en {nombre_archivo}...")
    
    try:
        with open(nombre_archivo, "w+", encoding="utf-8") as f:
            f.write(f" INFORME DE AUDITORÍA SSH - GENERADO EL {fecha_hoy}\n\n")
            f.write(texto_final)
            f.write("\n")
            f.flush() 
            
        print(f" ¡Reporte guardado con éxito como: '{nombre_archivo}'!")
    except Exception as e:
        print(f" Error al escribir el archivo: {e}")