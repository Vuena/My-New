import os
import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(self.log_dir, f"session_{timestamp}.txt")
        self.write(f"=== Oturum Başladı: {timestamp} ===")

    def write(self, message):
        """Log dosyasına ve konsola yazar."""
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_message = f"{timestamp} {message}"
        print(full_message)

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(full_message + "\n")
        except Exception as e:
            print(f"Log yazma hatası: {e}")

    def log_ai_interaction(self, prompt, response):
        """AI ile olan iletişimi özel formatta kaydeder."""
        separator = "-" * 50
        msg = f"\n{separator}\n[AI PROMPT]\n{prompt}\n\n[AI RESPONSE]\n{response}\n{separator}\n"
        self.write(msg)
