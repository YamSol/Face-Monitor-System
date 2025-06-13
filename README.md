# Face Monitor System (Alpha)

Sistema de monitoramento de presença com reconhecimento facial para bloqueio automático de tela em ambientes Windows.

## Descrição

O Face Monitor System é uma solução de segurança que utiliza reconhecimento facial através da webcam para monitorar a presença do usuário e bloquear automaticamente a tela quando detecta ausência prolongada. O sistema foi desenvolvido para aumentar a segurança de estações de trabalho, prevenindo acesso não autorizado quando o usuário se afasta temporariamente.

## Características Principais

### Detecção Inicial
- Tempo limite de 1 minuto para detecção inicial do usuário
- Finalização automática caso não detecte presença humana
- Verificação de disponibilidade e funcionalidade da câmera

### Monitoramento Contínuo
- Detecção facial em tempo real usando algoritmos OpenCV
- Monitoramento constante da presença do usuário
- Sistema tolerante a falhas temporárias de hardware

### Bloqueio Automático
- Bloqueio da estação de trabalho após 1 minuto de ausência
- Integração nativa com sistema de segurança do Windows
- Continuidade do monitoramento após bloqueio

### Sistema de Logs
- Registro detalhado de todas as operações
- Arquivo de log rotativo para auditoria
- Timestamps precisos para rastreabilidade

## Requisitos do Sistema

### Hardware
- Webcam funcional (integrada ou USB)
- Processador com suporte a instruções de ponto flutuante
- Mínimo de 2GB de RAM disponível
- Sistema operacional Windows 10 ou superior

### Software
- Python 3.7 ou superior
- OpenCV 4.x
- NumPy 1.21 ou superior
- PowerShell (incluído no Windows)

## Instalação

### Instalação Automática

1. Faça o download do projeto.
2. Desempacote o arquivo compactado.
3. Execute o arquivo `setup.bat` como administrador.
4. O script instalará automaticamente todas as dependências
5. Configure o sistema para inicialização automática

### Instalação Manual

1. Clone ou faça download do repositório
```
git clone https://github.com/YamSol/Face-Monitor-System.git
cd face-monitor-system
```

2. Instale as dependências Python
```
pip install -r requirements.txt
```

3. Configure para inicialização automática (opcional)
```
python face_monitor.py --setup-startup
```

## Uso

### Execução Manual
```
python face_monitor.py
```

### Execução como Serviço de Sistema
Após configurar a inicialização automática, o sistema será executado automaticamente a cada boot do Windows.

### Parâmetros de Linha de Comando
- `--setup-startup`: Configura o sistema para inicialização automática
- Sem parâmetros: Execução normal do monitoramento

## Configuração

### Parâmetros Ajustáveis

As constantes podem ser modificadas diretamente no código fonte:

- `initialization_timeout`: Tempo limite para detecção inicial (padrão: 60 segundos)
- `absence_timeout`: Tempo de ausência antes do bloqueio (padrão: 60 segundos)
- Configurações de câmera: resolução, FPS, parâmetros de detecção

### Configurações de Detecção Facial

O sistema utiliza Haar Cascade Classifiers com os seguintes parâmetros otimizados:
- Scale Factor: 1.1
- Min Neighbors: 5
- Tamanho mínimo de face: 60x60 pixels

## Arquivos de Log

### Localização
- Arquivo principal: `face_monitor.log` (diretório de execução)
- Saída de console: stdout em tempo real

### Conteúdo dos Logs
- Inicialização e finalização do sistema
- Detecções de presença e ausência
- Operações de bloqueio de tela
- Erros de hardware e software
- Status de threads e processos

### Formato de Log
```
YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE
```

## Arquitetura do Sistema

### Componentes Principais

1. **FaceMonitorSystem**: Classe principal de controle
2. **Camera Handler**: Gerenciamento de captura de vídeo
3. **Face Detection Engine**: Processamento de reconhecimento facial
4. **Screen Lock Controller**: Interface com sistema de bloqueio Windows
5. **Logging System**: Sistema de registro e auditoria

### Fluxo de Operação

1. Inicialização da câmera e verificação de hardware
2. Período de detecção inicial (60 segundos)
3. Transição para modo de monitoramento contínuo
4. Detecção de ausência e ativação de timer
5. Bloqueio automático após timeout
6. Continuidade do monitoramento pós-bloqueio

## Tratamento de Erros

### Recuperação Automática
- Reinicialização de threads que falham
- Reconexão automática de câmera desconectada
- Continuidade após erros temporários de hardware

### Situações de Falha
- Câmera não disponível: finalização controlada
- Erro de sistema: log detalhado e tentativa de recuperação
- Falta de permissões: notificação no log

## Segurança

### Proteções Implementadas
- Execução em espaço de usuário (não requer privilégios administrativos)
- Integração com sistema de segurança nativo do Windows
- Logs auditáveis para conformidade

### Considerações de Privacidade
- Processamento local de imagens (sem transmissão de dados)
- Não armazena imagens ou dados biométricos
- Detecção baseada apenas em presença/ausência

## Desempenho

### Otimizações Implementadas
- Processamento de imagem otimizado para baixo consumo de CPU
- Configurações de câmera ajustadas para performance
- Algoritmos de detecção balanceados entre precisão e velocidade

### Consumo de Recursos
- CPU: aproximadamente 5-10% em sistema médio
- RAM: aproximadamente 50-100MB
- Largura de banda: nenhuma (processamento local)

## Desinstalação

### Remoção da Inicialização Automática
1. Abra o Editor de Registro (regedit)
2. Navegue até `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
3. Remova a entrada "FaceMonitorSystem"

### Remoção Completa
1. Remova da inicialização automática (conforme acima)
2. Delete os arquivos do projeto
3. Desinstale as dependências Python (opcional)
```
pip uninstall opencv-python numpy
```

## Solução de Problemas

### Problemas Comuns

**Câmera não detectada**
- Verifique se a câmera está conectada e funcionando
- Confirme que nenhum outro aplicativo está usando a câmera
- Reinicie o sistema se necessário

**Sistema não bloqueia a tela**
- Verifique se o PowerShell está disponível
- Confirme as permissões de execução do usuário
- Consulte os logs para erros específicos

**Alto consumo de CPU**
- Ajuste as configurações de resolução da câmera
- Modifique a frequência de verificação no código
- Verifique se há outros processos concorrentes

### Logs de Diagnóstico
Consulte sempre o arquivo `face_monitor.log` para informações detalhadas sobre erros e operações do sistema.

## Suporte Técnico

Para questões técnicas, problemas de implementação ou sugestões de melhorias, consulte a documentação do código fonte ou entre em contato através dos canais oficiais de suporte.

## Licença

Este software é fornecido "como está", sem garantias expressas ou implícitas. O uso é de responsabilidade do usuário final.

## Versão

Versão atual: 1.0.0
Data de lançamento: 2025
