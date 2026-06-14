<div align="center">
  <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/cpu.svg" width="80" alt="ModelFit Logo">
  
  # ModelFit
  **Local AI Hardware Evaluator & Model Checker**

  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
  [![Ollama](https://img.shields.io/badge/Ollama-Ready-white?style=for-the-badge&logo=ollama)](https://ollama.ai/)
  [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

  <p align="center">
    Descubre qué modelos de Inteligencia Artificial (LLMs, Difusión, Audio, Visión) puedes ejecutar localmente de forma segura sin sobrecargar tu PC.
  </p>
</div>

---

## 🚀 Sobre el Proyecto

**ModelFit** es una potente herramienta web desarrollada con un backend en Python (Flask) y un frontend moderno con diseño *Glassmorphism*. Escanea tu hardware al instante (CPU, RAM, GPU y VRAM) y lo cruza con una base de datos actualizada de los mejores modelos Open Source (Llama 3, Qwen 2.5, SDXL, Flux, Whisper, etc.) para indicarte si puedes ejecutarlos de manera óptima, si el rendimiento será parcial o si definitivamente colapsarán tu sistema.

Además, ¡se integra directamente con **Ollama** para instalar software, descargar modelos con 1 clic y probarlos en un chat en vivo!

---

## ✨ Características Principales

* 🔍 **Hardware Scanner**: Detección automática en tiempo real de núcleos de CPU, porcentaje de uso, memoria RAM y memoria VRAM (Nvidia, AMD, Apple Silicon).
* 🚥 **Tráforo de Compatibilidad**:
  * 🟢 **Óptimo**: El modelo cabe completamente en la VRAM de tu GPU para máxima velocidad.
  * 🟡 **Parcial**: Uso híbrido (CPU + GPU) o descarga (offloading). Será más lento pero seguro.
  * 🔴 **No Recomendado**: Tu RAM/VRAM no es suficiente. Intentar cargarlo congelará el equipo.
* 🛠️ **Integración Nativa con Ollama**:
  * Instalación auto-asistida del software Ollama en Linux/macOS/Windows con 1 clic.
  * Descarga de modelos en segundo plano con barras de progreso.
  * **Playground en vivo** para chatear con los modelos instalados vía Server-Sent Events (SSE).
* 🎛️ **Simulador de Hardware**: Cambia los recursos virtuales con sliders para saber qué PC necesitarías comprar para ejecutar modelos masivos.

---

## 💻 Tecnologías Utilizadas

- **Backend**: Python 3, Flask, Psutil (Escaneo de sistema), Subprocess & Threading.
- **Frontend**: Vanilla JavaScript, CSS3 (Variables, Flexbox/Grid, Glassmorphism), HTML5.
- **APIs**: Conexión a la API de Ollama (`localhost:11434`) y Streaming (SSE).
- **Diseño**: UI/UX Premium, Modo Oscuro Nativo, Iconografía por Lucide.

---

## ⚙️ Instalación y Uso

### Pre-requisitos
Asegúrate de tener instalado **Python 3.8+**.

### En Linux / macOS (Instalación Rápida)

1. Clona el repositorio:
   ```bash
   git clone https://github.com/nredondo26/ModelFit.git
   cd ModelFit
   ```
2. Ejecuta el script automatizado (creará el entorno, instalará dependencias y levantará el servidor):
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
3. Abre tu navegador en **`http://127.0.0.1:5000`**

### En Windows (Manual)

1. Clona el repositorio y abre la carpeta en PowerShell:
   ```powershell
   git clone https://github.com/nredondo26/ModelFit.git
   cd ModelFit
   ```
2. Crea y activa un entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Ejecuta el servidor:
   ```powershell
   python app.py
   ```
5. Abre tu navegador en **`http://127.0.0.1:5000`**

---

## 🤖 Modelos Soportados

La base de datos se actualiza constantemente e incluye (entre muchos otros):
- **LLMs**: Llama 3.1 / 3.3, Mixtral, Qwen 2.5, Gemma 2, Command R.
- **Coding**: Qwen 2.5 Coder, DeepSeek Coder V2, Codestral, StarCoder2.
- **Visión**: Pixtral 12B, Qwen2-VL, Llama 3.2 Vision.
- **Imágenes**: Stable Diffusion 3, SDXL, FLUX.1.
- **Audio**: Whisper Large v3, Bark, Parler-TTS.

---

<div align="center">
  <i>Desarrollado con ❤️ para la comunidad Open Source de Inteligencia Artificial.</i>
</div>
