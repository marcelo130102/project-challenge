"""
Script de ejecución conveniente para el servidor Briefcase
"""
import uvicorn
import sys
import io

# Configurar salida UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == "__main__":
    print("[*] Iniciando servidor Briefcase...")
    print("[*] Accede a: http://localhost:8000")
    print("[*] API Docs: http://localhost:8000/docs")
    print("\n[*] Presiona CTRL+C para detener el servidor\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

