from typing import Dict, Set

def parse_auth_log(filepath: str) -> Dict[str, int]:
    ips_unicas: Set[str] = set()  # Un Set evita IPs duplicadas automáticamente
    conteo_ataques: Dict[str, int] = {}  # Diccionario para contar (IP: Intentos)

    with open(filepath, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if "Failed password" in linea:
                partes = linea.split()
                try:
                    indice_from = partes.index("from")
                    ip = partes[indice_from + 1]
                    
                    ips_unicas.add(ip)
                    conteo_ataques[ip] = conteo_ataques.get(ip, 0) + 1
                    
                except (ValueError, IndexError):
                    continue  # Si la línea está malformada, la salta
                    
    return conteo_ataques