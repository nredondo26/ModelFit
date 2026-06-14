from flask import Flask, jsonify, render_template, request, Response
import threading
import json
import urllib.request
import urllib.error
import platform
import subprocess
import os
import scanner
import models_db

app = Flask(__name__)

# Global dictionary to track active downloads: model_id -> status_data
installations = {}

# Global variable to track Ollama software installation progress
ollama_install_status = {
    "status": "idle", # "idle", "installing", "success", "failed"
    "logs": "",
    "error": None
}

def check_ollama_alive():
    """Checks if Ollama service is running locally on port 11434."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/", timeout=1.5) as response:
            return response.status == 200
    except Exception:
        return False

def ollama_pull_thread(model_id, ollama_tag):
    """Background thread to handle pulling a model from Ollama registry."""
    global installations
    installations[model_id] = {
        "status": "downloading",
        "progress": 0,
        "completed": 0,
        "total": 0,
        "error": None
    }
    
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/pull",
            data=json.dumps({"name": ollama_tag}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        # Read stream of progress lines from Ollama
        with urllib.request.urlopen(req) as response:
            for line in response:
                if not line.strip():
                    continue
                try:
                    status_data = json.loads(line.decode('utf-8'))
                    status_text = status_data.get("status", "")
                    
                    # Update status
                    installations[model_id]["status"] = status_text
                    
                    if "completed" in status_data and "total" in status_data:
                        completed = status_data["completed"]
                        total = status_data["total"]
                        installations[model_id]["completed"] = completed
                        installations[model_id]["total"] = total
                        if total > 0:
                            progress = round((completed / total) * 100, 1)
                            installations[model_id]["progress"] = progress
                    
                    if status_text == "success":
                        installations[model_id]["status"] = "success"
                        installations[model_id]["progress"] = 100
                        break
                except Exception:
                    pass
    except urllib.error.URLError as e:
        installations[model_id]["status"] = "failed"
        installations[model_id]["error"] = f"Error de conexión con Ollama: {str(e.reason)}"
    except Exception as e:
        installations[model_id]["status"] = "failed"
        installations[model_id]["error"] = str(e)

@app.route('/')
def index():
    """Renders the main dashboard page."""
    return render_template('index.html')

@app.route('/api/scan', methods=['GET'])
def api_scan():
    """Scans system hardware specs."""
    try:
        data = scanner.scan_hardware()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/models', methods=['GET'])
def api_models():
    """Returns the models database."""
    return jsonify(models_db.MODELS)

@app.route('/api/ollama/status', methods=['GET'])
def ollama_status():
    """Checks if Ollama is running locally."""
    is_alive = check_ollama_alive()
    return jsonify({"alive": is_alive})

@app.route('/api/ollama/installed', methods=['GET'])
def ollama_installed():
    """Gets lists of models currently pulled in local Ollama service."""
    if not check_ollama_alive():
        return jsonify({"alive": False, "models": []})
    
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as response:
            data = json.loads(response.read().decode())
            # Extract tags (e.g. "llama3.2:1b" or "llama3.2:latest")
            models = [m["name"] for m in data.get("models", [])]
            return jsonify({"alive": True, "models": models})
    except Exception as e:
        return jsonify({"alive": True, "error": str(e), "models": []})

@app.route('/api/install', methods=['POST'])
def install_model():
    """Triggers background installation (pull) of an Ollama model."""
    global installations
    req_data = request.get_json() or {}
    model_id = req_data.get("model_id")
    ollama_tag = req_data.get("ollama_tag")
    
    if not model_id or not ollama_tag:
        return jsonify({"error": "Faltan parámetros model_id o ollama_tag"}), 400
        
    if not check_ollama_alive():
        return jsonify({"error": "Ollama no está ejecutándose en tu PC. Inícialo primero."}), 503
        
    current = installations.get(model_id)
    if current and current["status"] in ["downloading", "pulling", "verifying"]:
        return jsonify({"status": "already_installing"})
        
    # Start thread
    t = threading.Thread(target=ollama_pull_thread, args=(model_id, ollama_tag))
    t.daemon = True
    t.start()
    
    return jsonify({"status": "started"})

@app.route('/api/install/status/<model_id>', methods=['GET'])
def install_status(model_id):
    """Returns the current download progress of a model."""
    global installations
    status_data = installations.get(model_id)
    if not status_data:
        return jsonify({"status": "not_started"})
    return jsonify(status_data)

@app.route('/api/chat', methods=['POST'])
def chat_playground():
    """Proxies a chat request to Ollama and streams the response back to client."""
    req_data = request.get_json() or {}
    model_tag = req_data.get("model_tag")
    messages = req_data.get("messages")
    
    if not model_tag or not messages:
        return jsonify({"error": "Faltan parámetros model_tag o messages"}), 400
        
    if not check_ollama_alive():
        return jsonify({"error": "Servicio Ollama inaccesible"}), 503
        
    def generate_stream():
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:11434/api/chat",
                data=json.dumps({
                    "model": model_tag,
                    "messages": messages,
                    "stream": True
                }).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                for line in response:
                    if line.strip():
                        yield line.decode('utf-8') + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"
            
    return Response(generate_stream(), mimetype='text/event-stream')

def install_ollama_bg_thread():
    """Background thread to download and install Ollama cross-platform."""
    global ollama_install_status
    ollama_install_status["status"] = "installing"
    ollama_install_status["logs"] = "Iniciando instalador auto-asistido de Ollama...\n"
    ollama_install_status["error"] = None
    
    system = platform.system()
    try:
        if system == "Linux":
            ollama_install_status["logs"] += "Detectado sistema Linux. Descargando script oficial de Ollama...\n"
            # Launch installation script and stream stdout/stderr
            process = subprocess.Popen(
                "curl -fsSL https://ollama.com/install.sh | sh",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in process.stdout:
                ollama_install_status["logs"] += line
            
            process.wait()
            if process.returncode == 0:
                ollama_install_status["status"] = "success"
                ollama_install_status["logs"] += "\n¡Ollama instalado correctamente! Iniciando el servicio...\n"
                # Start service
                subprocess.Popen("ollama serve", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                ollama_install_status["status"] = "failed"
                ollama_install_status["error"] = f"El script salió con código de error {process.returncode}."
                ollama_install_status["logs"] += f"\nERROR: Falló la instalación (código {process.returncode}).\nSi requiere permisos de administrador, asegúrate de correrlo en una terminal con sudo o configurar permisos sin contraseña.\nPuedes ejecutar de forma manual: curl -fsSL https://ollama.com/install.sh | sh\n"

        elif system == "Darwin":
            ollama_install_status["logs"] += "Detectado macOS. Descargando paquete oficial...\n"
            zip_url = "https://ollama.com/download/Ollama-darwin.zip"
            zip_path = "/tmp/Ollama-darwin.zip"
            
            ollama_install_status["logs"] += "Descargando Ollama-darwin.zip...\n"
            urllib.request.urlretrieve(zip_url, zip_path)
            
            ollama_install_status["logs"] += "Extrayendo en /Applications/...\n"
            subprocess.run(f"unzip -o {zip_path} -d /Applications/", shell=True)
            
            ollama_install_status["status"] = "success"
            ollama_install_status["logs"] += "\n¡Ollama instalado en /Applications/ con éxito!\nIniciando aplicación...\n"
            subprocess.Popen("open -a Ollama", shell=True)

        elif system == "Windows":
            ollama_install_status["logs"] += "Detectado Windows. Descargando instalador oficial...\n"
            installer_url = "https://ollama.com/download/OllamaSetup.exe"
            temp_dir = os.environ.get("TEMP", "C:\\Temp")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            installer_path = os.path.join(temp_dir, "OllamaSetup.exe")
            
            ollama_install_status["logs"] += "Descargando OllamaSetup.exe...\n"
            urllib.request.urlretrieve(installer_url, installer_path)
            
            ollama_install_status["logs"] += "Ejecutando instalador silencioso...\n"
            process = subprocess.Popen(f'"{installer_path}" /silent', shell=True)
            process.wait()
            
            ollama_install_status["status"] = "success"
            ollama_install_status["logs"] += "\n¡Ollama instalado correctamente en Windows!\nIniciando servicio...\n"
            
        else:
            raise Exception(f"Sistema '{system}' no soportado para instalación automática.")
            
    except Exception as e:
        ollama_install_status["status"] = "failed"
        ollama_install_status["error"] = str(e)
        ollama_install_status["logs"] += f"\nOcurrió un error inesperado durante la instalación: {str(e)}\n"

@app.route('/api/ollama/install', methods=['POST'])
def install_ollama():
    """Triggers background thread to install Ollama itself."""
    global ollama_install_status
    if ollama_install_status["status"] == "installing":
        return jsonify({"status": "already_running"})
        
    t = threading.Thread(target=install_ollama_bg_thread)
    t.daemon = True
    t.start()
    return jsonify({"status": "started"})

@app.route('/api/ollama/install/status', methods=['GET'])
def get_ollama_install_status():
    """Returns the accumulated logs and status of the Ollama software installer."""
    global ollama_install_status
    return jsonify(ollama_install_status)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
