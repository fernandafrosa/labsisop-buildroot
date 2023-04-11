from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

HOST_NAME = "127.0.0.1" # mudar depois pro IP do target
PORT_NUMBER = 8080

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    
    def do_GET(self):
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(bytes("<html><head><title>T1 LABORATÓRIO DE SISOP</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>Trabalho 1 - Laboratorio de Sistemas Operacionais</h1>", "utf-8"))
        self.wfile.write(bytes("<h2>Fernanda Rosa e Morgana Weber</h2>", "utf-8"))
        self.wfile.write(bytes("<p>Dados do servidor:</p>", "utf-8"))
        self.wfile.write(bytes(f"<li>Data e hora do sistema: {self.getDataEHora()} </li>", "utf-8"))
        self.wfile.write(bytes(f"<li>Uptime em segundos: {self.getUptime()} </li>", "utf-8"))
        self.wfile.write(bytes(f"<li>Modelo do processador: {self.getModelName()} </li>", "utf-8"))
        self.wfile.write(bytes(f"<li>Velocidade do processador (CPU Speed): {self.getVelocity()} MHz</li>", "utf-8"))
        self.wfile.write(bytes("<li>Capacidade ocupada do processador (%): </li>", "utf-8"))
        self.wfile.write(bytes(f"<li>Quantidade de memoria RAM total (MB): {self.getTotalRAM()} MB </li>", "utf-8"))
        self.wfile.write(bytes(f"<li>Quantidade de memória RAM usada (MB): {self.getUsedRAM()} MB </li>", "utf-8"))
        self.wfile.write(bytes(f"<li>Versao do sistema: {self.getSystemVersion()} </li>", "utf-8"))
        
        self.wfile.write(bytes(f"<li>LISTA DE PROCESSOS:  </li>", "utf-8"))
        
        processes = self.getRunningProcesses()
        for name, pid in processes:
            self.wfile.write(bytes(f"<ul>Process PID: {pid} | Process name: {name}</ul>", "utf-8"))


    # Modelo do processador
    def getModelName(self):
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    model_name = line.strip().split(':')[1]
                    return model_name
                
    # Velocidade do processador
    def getVelocity(self):
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'cpu MHz' in line:
                    cpu_speed = float(line.strip().split(':')[1])
                    return cpu_speed

    # Versao do sistema
    def getSystemVersion(self):
        with open('/proc/version', 'r') as f:
            version_info = f.readline().strip()
            return version_info
    
    # Uptime
    def getUptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return uptime_seconds

    # RAM total
    def getTotalRAM(self):
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal'):
                    total_memory = int(line.split()[1]) / 1024  # convert to MB
                    return total_memory
    
    # RAM usada
    def getUsedRAM(self):
        total_memory = self.getTotalRAM()
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemFree'):
                    free_memory = int(line.split()[1])
                    used_memory = total_memory - free_memory
                    return used_memory

    # Data e hora do sistema
    def getDataEHora(self):
        t = time.localtime()
        current_time = time.asctime(t)
        return current_time
    
    # Processos em execucao
    def getRunningProcesses(self):
        processes = []
        for pid in os.listdir('/proc'):
            if pid.isdigit():
                try:
                    with open(f"/proc/{pid}/comm", 'r') as f:
                        name = f.read().strip()
                        processes.append((name, pid))
                except IOError:
                    continue
        return processes



if __name__ == "__main__":              
    server = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print("Server in: http://%s:%s" % (HOST_NAME, PORT_NUMBER))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
    print("Server stopped.")


