import os
import subprocess
import sys

def install_requirements():
    print("[KURULUM] Gerekli kütüphaneler yükleniyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def build_exe():
    print("[DERLEME] EXE dosyası oluşturuluyor...")
    print("Bu işlem birkaç dakika sürebilir, lütfen bekleyin.")

    # PyInstaller komutu
    # --onefile: Tek bir .exe dosyası oluşturur
    # --name: Dosya adı
    # --clean: Önbelleği temizler
    # --noconfirm: Klasörler varsa sormadan üzerine yazar

    command = [
        "pyinstaller",
        "--onefile",
        "--name", "DofusAI_Bot",
        "--clean",
        "--noconfirm",
        "main.py"
    ]

    try:
        subprocess.check_call(command)
        print("\n" + "="*50)
        print("[BAŞARILI] EXE dosyası oluşturuldu!")
        print(f"Dosyanızı şu klasörde bulabilirsiniz: {os.path.join(os.getcwd(), 'dist', 'DofusAI_Bot.exe')}")
        print("="*50 + "\n")
    except subprocess.CalledProcessError as e:
        print(f"\n[HATA] EXE oluşturulurken bir hata oluştu: {e}")
    except FileNotFoundError:
        print("\n[HATA] PyInstaller bulunamadı. Lütfen 'pip install pyinstaller' komutunu çalıştırın veya requirements.txt dosyasını yükleyin.")

if __name__ == "__main__":
    try:
        install_requirements()
        build_exe()
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

    input("Çıkmak için Enter'a basın...")
