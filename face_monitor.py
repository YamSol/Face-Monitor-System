#!/usr/bin/env python3
"""
Sistema de Monitoramento de Presença com Reconhecimento Facial
Bloqueia automaticamente a tela quando o usuário se ausenta
"""

import cv2
import time
import subprocess
import threading
import logging
from datetime import datetime, timedelta
import sys
import os

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('face_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class FaceMonitorSystem:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.camera = None
        self.is_running = False
        self.user_present = False
        self.last_detection_time = None
        self.initialization_timeout = 60  # 1 minuto para inicialização
        self.absence_timeout = 10  # 1 minuto de ausência antes de bloquear
        self.monitoring_thread = None
        self.screen_locked = False
        
    def initialize_camera(self):
        """Inicializa a câmera e verifica se está funcionando"""
        try:
            logging.info("Inicializando câmera...")
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                logging.error("Erro: Não foi possível acessar a câmera")
                return False
            
            # Configurações da câmera para melhor performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 15)
            
            logging.info("Câmera inicializada com sucesso")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao inicializar câmera: {e}")
            return False
    
    def detect_face(self, frame):
        """Detecta rostos no frame da câmera"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            return len(faces) > 0
        except Exception as e:
            logging.error(f"Erro na detecção de rosto: {e}")
            return False
    
    def lock_screen(self):
        """Bloqueia a tela usando PowerShell"""
        try:
            if not self.screen_locked:
                logging.info("Bloqueando a tela...")
                subprocess.run([
                    "powershell", 
                    "-Command", 
                    "rundll32.exe user32.dll,LockWorkStation"
                ], check=True)
                self.screen_locked = True
                logging.info("Tela bloqueada com sucesso")
        except subprocess.CalledProcessError as e:
            logging.error(f"Erro ao bloquear a tela: {e}")
        except Exception as e:
            logging.error(f"Erro inesperado ao bloquear tela: {e}")
    
    def wait_for_initial_detection(self):
        """Aguarda detecção inicial do usuário por 1 minuto"""
        logging.info("Aguardando detecção inicial do usuário...")
        start_time = time.time()
        
        while time.time() - start_time < self.initialization_timeout:
            if not self.camera or not self.camera.isOpened():
                logging.error("Câmera não disponível durante inicialização")
                return False
            
            ret, frame = self.camera.read()
            if not ret:
                logging.warning("Falha ao capturar frame da câmera")
                time.sleep(1)
                continue
            
            if self.detect_face(frame):
                self.user_present = True
                self.last_detection_time = time.time()
                logging.info("Usuário detectado! Iniciando monitoramento padrão...")
                return True
            
            time.sleep(0.5)  # Verifica a cada 500ms
        
        logging.info("Tempo limite de inicialização atingido. Finalizando...")
        return False
    
    def monitor_user_presence(self):
        """Monitora continuamente a presença do usuário"""
        logging.info("Iniciando monitoramento de presença...")
        
        while self.is_running:
            try:
                if not self.camera or not self.camera.isOpened():
                    logging.error("Câmera desconectada durante monitoramento")
                    break
                
                ret, frame = self.camera.read()
                if not ret:
                    logging.warning("Falha ao capturar frame")
                    time.sleep(1)
                    continue
                
                face_detected = self.detect_face(frame)
                current_time = time.time()
                
                if face_detected:
                    if not self.user_present:
                        logging.info("Usuário retornou")
                        self.screen_locked = False  # Reset do estado de bloqueio
                    
                    self.user_present = True
                    self.last_detection_time = current_time
                    
                else:
                    if self.user_present:
                        logging.info("Usuário ausente. Iniciando contagem regressiva...")
                        self.user_present = False
                    
                    # Verifica se o tempo de ausência foi excedido
                    if (self.last_detection_time and 
                        current_time - self.last_detection_time >= self.absence_timeout):
                        
                        logging.warning(f"Usuário ausente por {self.absence_timeout} segundos")
                        self.lock_screen()
                        # Continua monitorando após bloquear
                
                time.sleep(1)  # Verifica a cada segundo
                
            except Exception as e:
                logging.error(f"Erro durante monitoramento: {e}")
                time.sleep(2)
    
    def start_monitoring_thread(self):
        """Inicia o thread de monitoramento"""
        self.monitoring_thread = threading.Thread(target=self.monitor_user_presence)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def run(self):
        """Executa o sistema principal"""
        logging.info("=== Iniciando Sistema de Monitoramento Facial ===")
        
        try:
            # Inicializa a câmera
            if not self.initialize_camera():
                logging.error("Falha na inicialização da câmera. Finalizando...")
                return False
            
            self.is_running = True
            
            # Aguarda detecção inicial
            if not self.wait_for_initial_detection():
                logging.info("Usuário não detectado no tempo limite. Finalizando...")
                return False
            
            # Inicia monitoramento contínuo
            self.start_monitoring_thread()
            
            # Loop principal - mantém o programa rodando
            try:
                while self.is_running:
                    time.sleep(1)
                    
                    # Verifica se o thread ainda está ativo
                    if not self.monitoring_thread.is_alive():
                        logging.error("Thread de monitoramento parou. Reiniciando...")
                        self.start_monitoring_thread()
                        
            except KeyboardInterrupt:
                logging.info("Interrupção pelo usuário (Ctrl+C)")
                
        except Exception as e:
            logging.error(f"Erro fatal no sistema: {e}")
            return False
            
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Limpa recursos e finaliza o sistema"""
        logging.info("Finalizando sistema...")
        self.is_running = False
        
        if self.camera:
            self.camera.release()
            logging.info("Câmera liberada")
        
        cv2.destroyAllWindows()
        logging.info("Sistema finalizado")
    
    def stop(self):
        """Para o sistema externamente"""
        self.is_running = False


def setup_windows_startup():
    """Configura o script para iniciar automaticamente com o Windows"""
    try:
        import winreg
        script_path = os.path.abspath(__file__)
        python_path = sys.executable
        
        # Comando completo para executar o script
        command = f'"{python_path}" "{script_path}"'
        
        # Adiciona ao registro do Windows
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.SetValueEx(key, "FaceMonitorSystem", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        logging.info("Script configurado para iniciar com o Windows")
        return True
        
    except Exception as e:
        logging.error(f"Erro ao configurar startup: {e}")
        return False


def main():
    """Função principal"""
    logging.info("Iniciando aplicação...")
    
    # Verifica se deve configurar o startup
    if len(sys.argv) > 1 and sys.argv[1] == "--setup-startup":
        setup_windows_startup()
        return
    
    # Cria e executa o sistema de monitoramento
    monitor = FaceMonitorSystem()
    
    try:
        success = monitor.run()
        if success:
            logging.info("Sistema executado com sucesso")
        else:
            logging.error("Sistema finalizado com erro")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()