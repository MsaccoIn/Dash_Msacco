import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Caminho para o arquivo Excel que será monitorado
WATCH_FILE = os.path.abspath("Resumo_Operacional_Com_Graficos.xlsx")

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == WATCH_FILE:
            print(f"Arquivo modificado: {event.src_path}")
            # Executa comandos do Git para atualizar o repositório
            subprocess.run(["git", "add", WATCH_FILE])
            subprocess.run(["git", "commit", "-m", "Atualização automática: Arquivo Excel modificado"])
            subprocess.run(["git", "push", "origin", "main"])
            print("Alterações enviadas para o GitHub.")

if __name__ == "__main__":
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
