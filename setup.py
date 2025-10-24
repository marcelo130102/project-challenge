"""
Script de configuración inicial del proyecto
Instala dependencias y prepara la base de datos
"""
import subprocess
import sys
import os
import io

# Configurar salida UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def run_command(command, description):
    """Ejecuta un comando y muestra el progreso"""
    print(f"\n{'='*60}")
    print(f"[*] {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(command, shell=True, capture_output=False)
    
    if result.returncode != 0:
        print(f"\n[ERROR] Error en: {description}")
        sys.exit(1)
    
    print(f"\n[OK] Completado: {description}")


def main():
    print("""
    ========================================================
            BRIEFCASE - CONFIGURACION INICIAL
        Sistema Seguro de Entrega de Documentos
    ========================================================
    """)
    
    # Verificar si estamos en un entorno virtual
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("[!] ADVERTENCIA: No estas en un entorno virtual!")
        print("\nPor favor, activa el entorno virtual primero:")
        print("\n  Windows PowerShell:  .\\venv\\Scripts\\Activate.ps1")
        print("  Windows CMD:         venv\\Scripts\\activate.bat")
        print("  macOS/Linux:         source venv/bin/activate")
        sys.exit(1)
    
    print("[OK] Entorno virtual detectado\n")
    
    # Instalar dependencias
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Actualizando pip"
    )
    
    run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Instalando dependencias desde requirements.txt"
    )
    
    # Ejecutar seed
    print("\n" + "="*60)
    print("[?] Deseas crear usuarios de prueba en la base de datos?")
    print("="*60)
    response = input("\nEscribe 's' para continuar o 'n' para saltar: ").lower()
    
    if response == 's':
        run_command(
            f"{sys.executable} seed.py",
            "Creando usuarios de prueba"
        )
    
    print("\n" + "="*60)
    print("[OK] CONFIGURACION COMPLETADA!")
    print("="*60)
    print("\n[INFO] Proximos pasos:\n")
    print("  1. Ejecutar el servidor:")
    print(f"     {sys.executable} run.py")
    print("\n  2. Abrir en el navegador:")
    print("     http://localhost:8000")
    print("\n  3. Login con usuario de prueba:")
    print("     Email:    alice@briefcase.com")
    print("     Password: password123")
    print("\n[OK] Disfruta usando Briefcase!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[X] Configuracion cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[ERROR] Error inesperado: {e}")
        sys.exit(1)

