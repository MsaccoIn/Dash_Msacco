import os
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Caminho para o arquivo Excel que será monitorado
WATCH_FILE = os.path.abspath("Resumo_Operacional_Com_Graficos.xlsx")

# Caminho para o executável do Google Drive (modifique conforme necessário)
DRIVE_EXECUTABLE = r"C:\Program Files\Google\Drive File Stream\googledrivesync.exe"

# Função para calcular o hash do arquivo
def calculate_file_hash(file_path):
    """Calcula o hash (checksum) do conteúdo do arquivo."""
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        return file_hash
    except FileNotFoundError:
        return None

# Função para reiniciar o Google Drive
def restart_google_drive():
    """Reinicia o Google Drive para forçar a sincronização."""
    try:
        print("Encerrando o Google Drive...")
        os.system("taskkill /f /im googledrivesync.exe")

        print("Aguardando 5 segundos antes de reiniciar...")
        time.sleep(5)

        print("Reiniciando o Google Drive...")
        os.system(f'"{DRIVE_EXECUTABLE}"')
        print("Google Drive reiniciado com sucesso.")
    except Exception as e:
        print(f"Erro ao reiniciar o Google Drive: {e}")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_hash = calculate_file_hash(WATCH_FILE)

    def on_modified(self, event):
        if event.src_path == WATCH_FILE:
            current_hash = calculate_file_hash(WATCH_FILE)
            if current_hash != self.last_hash:
                self.last_hash = current_hash
                print(f"Alteração detectada no arquivo: {WATCH_FILE}")
                self.execute_git_commands()

    def execute_git_commands(self):
        """Adiciona, commita e envia alterações ao GitHub."""
        try:
            print("Adicionando arquivo ao Git...")
            os.system(f'git add "{WATCH_FILE}"')

            print("Criando commit...")
            os.system('git commit -m "Atualização automática pelo monitor.py"')

            print("Enviando alterações para o GitHub...")
            push_result = os.system('git push origin main')

            if push_result != 0:
                print("Erro ao enviar alterações para o GitHub. Verifique a configuração de autenticação.")
            else:
                print("Alterações enviadas para o GitHub com sucesso!")

        except Exception as e:
            print(f"Erro durante o processo de envio: {e}")

if __name__ == "__main__":
    # Reiniciar o Google Drive antes de iniciar o monitoramento
    restart_google_drive()

    directory = os.path.dirname(WATCH_FILE)
    if not os.path.exists(WATCH_FILE):
        print(f"Erro: O arquivo {WATCH_FILE} não foi encontrado!")
        exit(1)

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    print(f"Monitorando alterações no arquivo: {WATCH_FILE}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
