# ModelFit: Local AI Hardware Evaluator & Model Checker

**ModelFit** es una herramienta web local diseñada para escanear y evaluar las capacidades de tu hardware (CPU, memoria RAM, tarjeta gráfica GPU y VRAM) con el fin de determinar qué modelos de Inteligencia Artificial (modelos de lenguaje LLM, generadores de imágenes por difusión, transcripción de audio y modelos de visión multimodal) puedes ejecutar localmente de manera segura y eficiente, **previniendo bloqueos del sistema o falta de memoria ("que se estalle el PC")**.

La aplicación cuenta con una interfaz web premium y moderna construida en Python (Flask) y Vanilla CSS/JS con efectos de glassmorphism, sliders dinámicos y un potente simulador.

---

## Características Principales

- 🔍 **Escaneo Automático en Tiempo Real**: Detecta tu Sistema Operativo, procesador (CPU y núcleos), memoria RAM total/disponible, modelo de GPU y cantidad exacta de VRAM dedicados (soportando Nvidia, AMD y Apple Silicon).
- 🟢🟡🔴 **Indicadores de Compatibilidad**:
  - **Óptimo (Verde)**: Ejecución directa en la GPU (VRAM suficiente) a máxima velocidad.
  - **Parcial (Amarillo)**: Ejecución híbrida (CPU + GPU) o CPU dedicada. Inferencia más lenta pero segura.
  - **No Recomendado (Rojo)**: Excede los recursos disponibles del sistema. Ejecutarlo podría colgar el ordenador.
- 🎛️ **Simulador de Hardware**: ¿Deseas saber si vale la pena actualizar tu hardware? Activa el simulador y ajusta los controles deslizantes (sliders) de RAM y VRAM para ver instantáneamente cómo cambia la compatibilidad de los modelos.
- 💻 **Instrucciones Paso a Paso**: Cada modelo incluye indicaciones sencillas sobre cómo ejecutarlo localmente utilizando herramientas populares como **Ollama**, **ComfyUI** o scripts de Python.

---

## Requisitos Previos

- **Python 3.8 o superior** instalado en el sistema.
- Conexión a internet (para cargar fuentes e iconos desde CDN en el navegador).

---

## Cómo Ejecutar ModelFit Localmente

El proyecto incluye scripts automatizados para facilitar la puesta en marcha con un solo click.

### En Linux y macOS:

1. Abre la terminal en la carpeta del proyecto.
2. Dale permisos de ejecución al script si es necesario:
   ```bash
   chmod +x run.sh
   ```
3. Ejecuta el script:
   ```bash
   ./run.sh
   ```
4. Abre tu navegador web e ingresa a: **`http://127.0.0.1:5000`**

### En Windows (Manual):

1. Abre PowerShell o el símbolo del sistema en la carpeta del proyecto.
2. Crea el entorno virtual de Python:
   ```powershell
   python -m venv .venv
   ```
3. Activa el entorno virtual:
   ```powershell
   .venv\Scripts\activate
   ```
4. Instala las dependencias requeridas:
   ```powershell
   pip install --upgrade pip
   ```
   ```powershell
   pip install -r requirements.txt
   ```
5. Ejecuta la aplicación:
   ```powershell
   python app.py
   ```
6. Abre tu navegador web e ingresa a: **`http://127.0.0.1:5000`**

---

## Cómo Subir este Proyecto a un Repositorio Público en GitHub

Para compartir este proyecto o publicarlo en tu perfil de GitHub, sigue estos pasos:

1. **Crea un nuevo repositorio en GitHub**:
   - Ve a [GitHub](https://github.com) e inicia sesión.
   - Haz clic en el botón **"New"** (Nuevo) para crear un repositorio.
   - Asígnale un nombre como `modelfit` o `can-i-run-local-ai`.
   - Selecciona la opción **Public** (Público).
   - **IMPORTANTE**: No selecciones "Add a README file", "Add .gitignore" ni "Choose a license" (ya que el proyecto local ya contiene los archivos `.gitignore` y `README.md` necesarios).
   - Haz clic en **Create repository**.

2. **Inicializa Git localmente y vincula el repositorio**:
   - Abre la terminal en la carpeta del proyecto local y ejecuta los siguientes comandos:
     ```bash
     # Inicializar el repositorio Git local
     git init

     # Agregar todos los archivos (el archivo .gitignore evitará subir carpetas basura como .venv)
     git add .

     # Hacer el primer commit local
     git commit -m "Initial commit - ModelFit Hardware Evaluator"

     # Crear la rama principal llamada main
     git branch -M main

     # Vincular tu repositorio local con el de GitHub (reemplaza con tu enlace de GitHub)
     git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git

     # Subir el código a GitHub
     git push -u origin main
     ```

¡Y listo! Tu código estará publicado y disponible para toda la comunidad.
