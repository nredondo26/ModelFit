# Database of popular open-source AI models and their hardware requirements.

MODELS = [
    # --- LARGE LANGUAGE MODELS (LLMs) ---
    {
        "id": "llama-3.2-1b",
        "name": "Llama 3.2 (1B)",
        "category": "llm",
        "provider": "Meta",
        "description": "Modelo de lenguaje ultra-ligero de Meta. Excelente para dispositivos de gama baja, tareas simples de texto y asistentes integrados rápidos.",
        "type": "gguf",
        "ollama_tag": "llama3.2:1b",
        "tags": ["General", "Texto", "Ligero"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 1.2, "ram_required_gb": 4.0, "vram_required_gb": 1.8},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 1.8, "ram_required_gb": 6.0, "vram_required_gb": 2.5},
            {"name": "Original (FP16)", "size_gb": 2.5, "ram_required_gb": 8.0, "vram_required_gb": 3.2}
        ],
        "run_instructions": "Se recomienda usar **Ollama**. Comando de ejecución:\n```bash\nollama run llama3.2:1b\n```",
        "info_url": "https://huggingface.co/meta-llama/Llama-3.2-1B"
    },
    {
        "id": "llama-3.2-3b",
        "name": "Llama 3.2 (3B)",
        "category": "llm",
        "provider": "Meta",
        "description": "El balance perfecto entre inteligencia y rendimiento local. Muy bueno para redacción, resúmenes y agentes conversacionales estándar.",
        "type": "gguf",
        "ollama_tag": "llama3.2",
        "tags": ["General", "Conversacional"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 2.0, "ram_required_gb": 6.0, "vram_required_gb": 2.8},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 3.4, "ram_required_gb": 8.0, "vram_required_gb": 4.2},
            {"name": "Original (FP16)", "size_gb": 6.4, "ram_required_gb": 12.0, "vram_required_gb": 7.5}
        ],
        "run_instructions": "Se recomienda usar **Ollama**. Comando de ejecución:\n```bash\nollama run llama3.2\n```",
        "info_url": "https://huggingface.co/meta-llama/Llama-3.2-3B"
    },
    {
        "id": "llama-3.1-8b",
        "name": "Llama 3.1 (8B)",
        "category": "llm",
        "provider": "Meta",
        "description": "El estándar de oro para LLMs locales. Altamente competente en razonamiento, matemáticas, programación y traducción de idiomas.",
        "type": "gguf",
        "ollama_tag": "llama3.1",
        "tags": ["Razonamiento", "General", "Python"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 4.7, "ram_required_gb": 10.0, "vram_required_gb": 5.8},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 8.5, "ram_required_gb": 14.0, "vram_required_gb": 9.5},
            {"name": "Original (FP16)", "size_gb": 16.0, "ram_required_gb": 24.0, "vram_required_gb": 18.0}
        ],
        "run_instructions": "Se recomienda usar **Ollama** con GPU. Comando de ejecución:\n```bash\nollama run llama3.1\n```",
        "info_url": "https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct"
    },
    {
        "id": "llama-3.1-70b",
        "name": "Llama 3.1 / 3.3 (70B)",
        "category": "llm",
        "provider": "Meta",
        "description": "Modelo masivo de grado empresarial. Supera a muchos modelos propietarios comerciales en razonamiento, matemáticas y tareas complejas.",
        "type": "gguf",
        "ollama_tag": "llama3.1:70b",
        "tags": ["Experto", "Razonamiento Complejo", "Masivo"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 40.0, "ram_required_gb": 64.0, "vram_required_gb": 48.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 75.0, "ram_required_gb": 96.0, "vram_required_gb": 80.0}
        ],
        "run_instructions": "Requiere múltiples GPUs profesionales o muchísima RAM (lento). Comando de ejecución:\n```bash\nollama run llama3.1:70b\n```",
        "info_url": "https://huggingface.co/meta-llama/Meta-Llama-3.1-70B-Instruct"
    },
    {
        "id": "mistral-nemo-12b",
        "name": "Mistral NeMo (12B)",
        "category": "llm",
        "provider": "Mistral AI",
        "description": "Colaboración con NVIDIA. Un modelo de 12B que cabe en GPUs de 12-16GB ofreciendo un razonamiento superior a modelos de 8B con un contexto masivo de 128k.",
        "type": "gguf",
        "ollama_tag": "mistral-nemo",
        "tags": ["Razonamiento", "Ventana de Contexto Grande"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 7.1, "ram_required_gb": 12.0, "vram_required_gb": 8.5},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 13.0, "ram_required_gb": 20.0, "vram_required_gb": 14.5}
        ],
        "run_instructions": "Se recomienda usar **Ollama**. Comando de ejecución:\n```bash\nollama run mistral-nemo\n```",
        "info_url": "https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407"
    },
    {
        "id": "mixtral-8x7b",
        "name": "Mixtral 8x7B",
        "category": "llm",
        "provider": "Mistral AI",
        "description": "Modelo Mixture of Experts (MoE). Muy eficiente, rápido y altamente capaz, rivalizando con GPT-3.5.",
        "type": "gguf",
        "ollama_tag": "mixtral",
        "tags": ["MoE", "Rápido", "General"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 26.0, "ram_required_gb": 32.0, "vram_required_gb": 28.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 50.0, "ram_required_gb": 64.0, "vram_required_gb": 55.0}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run mixtral\n```",
        "info_url": "https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1"
    },
    {
        "id": "qwen-2.5-7b",
        "name": "Qwen 2.5 (7B)",
        "category": "llm",
        "provider": "Alibaba",
        "description": "Modelo base de la familia Qwen 2.5. Excelente soporte multilingüe y altísimo rendimiento en benchmarks de su tamaño.",
        "type": "gguf",
        "ollama_tag": "qwen2.5:7b",
        "tags": ["Multilingüe", "General", "Eficiente"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 4.7, "ram_required_gb": 10.0, "vram_required_gb": 5.8},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 7.7, "ram_required_gb": 14.0, "vram_required_gb": 8.8}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run qwen2.5:7b\n```",
        "info_url": "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct"
    },
    {
        "id": "qwen-2.5-32b",
        "name": "Qwen 2.5 (32B)",
        "category": "llm",
        "provider": "Alibaba",
        "description": "El punto dulce de Qwen. Rendimiento que compite con modelos masivos pero en un tamaño manejable con 32GB de RAM/VRAM.",
        "type": "gguf",
        "ollama_tag": "qwen2.5:32b",
        "tags": ["Matemáticas", "Razonamiento Avanzado", "Multilingüe"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 20.0, "ram_required_gb": 32.0, "vram_required_gb": 22.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 34.0, "ram_required_gb": 48.0, "vram_required_gb": 36.0}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run qwen2.5:32b\n```",
        "info_url": "https://huggingface.co/Qwen/Qwen2.5-32B-Instruct"
    },
    {
        "id": "gemma-2-9b",
        "name": "Gemma 2 (9B)",
        "category": "llm",
        "provider": "Google",
        "description": "Modelo de alto nivel técnico de Google. Supera a muchos modelos de mayor tamaño en análisis crítico y razonamiento lógico.",
        "type": "gguf",
        "ollama_tag": "gemma2",
        "tags": ["Razonamiento", "General", "Escritura"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 5.5, "ram_required_gb": 12.0, "vram_required_gb": 6.8},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 9.6, "ram_required_gb": 16.0, "vram_required_gb": 11.0}
        ],
        "run_instructions": "Se recomienda correr en GPU o modo híbrido en **Ollama**:\n```bash\nollama run gemma2\n```",
        "info_url": "https://huggingface.co/google/gemma-2-9b-it"
    },
    {
        "id": "gemma-2-27b",
        "name": "Gemma 2 (27B)",
        "category": "llm",
        "provider": "Google",
        "description": "La versión mayor de Gemma 2. Excelente en redacción, análisis y tareas lógicas extensas.",
        "type": "gguf",
        "ollama_tag": "gemma2:27b",
        "tags": ["Razonamiento Avanzado", "Redacción Compleja"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 16.0, "ram_required_gb": 24.0, "vram_required_gb": 18.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 28.0, "ram_required_gb": 40.0, "vram_required_gb": 32.0}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run gemma2:27b\n```",
        "info_url": "https://huggingface.co/google/gemma-2-27b-it"
    },
    {
        "id": "phi-3.5-mini-3.8b",
        "name": "Phi-3.5 Mini (3.8B)",
        "category": "llm",
        "provider": "Microsoft",
        "description": "Modelo ligero de Microsoft entrenado con datos sintéticos de alta calidad. Capacidad matemática y lógica sorprendente.",
        "type": "gguf",
        "ollama_tag": "phi3.5",
        "tags": ["Matemáticas", "Lógica", "Python"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 2.2, "ram_required_gb": 6.0, "vram_required_gb": 3.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 3.8, "ram_required_gb": 8.0, "vram_required_gb": 4.6}
        ],
        "run_instructions": "Ejecutar rápidamente en **Ollama**:\n```bash\nollama run phi3.5\n```",
        "info_url": "https://huggingface.co/microsoft/Phi-3.5-mini-instruct"
    },
    {
        "id": "command-r-35b",
        "name": "Command R (35B)",
        "category": "llm",
        "provider": "Cohere",
        "description": "Optimizado masivamente para RAG (Retrieval Augmented Generation) y uso de herramientas/APIs. Excelente para sistemas de búsqueda corporativos.",
        "type": "gguf",
        "ollama_tag": "command-r",
        "tags": ["RAG", "Uso de Herramientas", "Empresarial"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 21.0, "ram_required_gb": 32.0, "vram_required_gb": 24.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 38.0, "ram_required_gb": 48.0, "vram_required_gb": 40.0}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run command-r\n```",
        "info_url": "https://huggingface.co/CohereForAI/c4ai-command-r-v01"
    },

    # --- PROGRAMACIÓN (CODING) ---
    {
        "id": "qwen-2.5-coder-1.5b",
        "name": "Qwen 2.5 Coder (1.5B)",
        "category": "programming",
        "provider": "Alibaba",
        "description": "Versión especializada en código de Qwen 2.5. Excelente para autocompletado y scripts rápidos en la IDE.",
        "type": "gguf",
        "ollama_tag": "qwen2.5-coder:1.5b",
        "tags": ["Python", "JS", "C++", "Autocompletado"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 1.0, "ram_required_gb": 4.0, "vram_required_gb": 1.6},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 1.7, "ram_required_gb": 6.0, "vram_required_gb": 2.4}
        ],
        "run_instructions": "Ejecución rápida con **Ollama**:\n```bash\nollama run qwen2.5-coder:1.5b\n```",
        "info_url": "https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct"
    },
    {
        "id": "qwen-2.5-coder-7b",
        "name": "Qwen 2.5 Coder (7B)",
        "category": "programming",
        "provider": "Alibaba",
        "description": "Modelo enfocado en programación muy potente. Soporta docenas de lenguajes, análisis de repositorios y resolución de bugs complejos.",
        "type": "gguf",
        "ollama_tag": "qwen2.5-coder:7b",
        "tags": ["Python", "JavaScript", "Java", "C++", "SQL"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 4.7, "ram_required_gb": 10.0, "vram_required_gb": 5.8},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 7.7, "ram_required_gb": 14.0, "vram_required_gb": 8.8}
        ],
        "run_instructions": "Ejecución óptima en **Ollama**:\n```bash\nollama run qwen2.5-coder:7b\n```",
        "info_url": "https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct"
    },
    {
        "id": "qwen-2.5-coder-32b",
        "name": "Qwen 2.5 Coder (32B)",
        "category": "programming",
        "provider": "Alibaba",
        "description": "Modelo de nivel experto para programación (state-of-the-art en open source). Rivaliza con GPT-4 en benchmarks de código.",
        "type": "gguf",
        "ollama_tag": "qwen2.5-coder:32b",
        "tags": ["Experto", "Python", "Rust", "Go", "Web"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 20.0, "ram_required_gb": 32.0, "vram_required_gb": 22.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 34.0, "ram_required_gb": 48.0, "vram_required_gb": 36.0}
        ],
        "run_instructions": "Requiere 32GB+ de RAM o GPU profesional con 24GB+ VRAM.\n```bash\nollama run qwen2.5-coder:32b\n```",
        "info_url": "https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct"
    },
    {
        "id": "deepseek-coder-6.7b",
        "name": "DeepSeek Coder (6.7B)",
        "category": "programming",
        "provider": "DeepSeek",
        "description": "Entrenado específicamente en billones de líneas de código. Eficiente y espectacular en Python y C++.",
        "type": "gguf",
        "ollama_tag": "deepseek-coder:6.7b",
        "tags": ["Python", "C++", "Java", "C#"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 4.1, "ram_required_gb": 8.0, "vram_required_gb": 5.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 7.2, "ram_required_gb": 12.0, "vram_required_gb": 8.2}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run deepseek-coder:6.7b\n```",
        "info_url": "https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct"
    },
    {
        "id": "deepseek-coder-v2",
        "name": "DeepSeek Coder V2",
        "category": "programming",
        "provider": "DeepSeek",
        "description": "Introduce arquitectura MoE para un rendimiento excepcional en razonamiento lógico y código en decenas de lenguajes.",
        "type": "gguf",
        "ollama_tag": "deepseek-coder-v2",
        "tags": ["Multi-lenguaje", "Razonamiento", "MoE"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 8.9, "ram_required_gb": 16.0, "vram_required_gb": 10.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 16.0, "ram_required_gb": 24.0, "vram_required_gb": 18.0}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run deepseek-coder-v2\n```",
        "info_url": "https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct"
    },
    {
        "id": "codestral-22b",
        "name": "Codestral (22B)",
        "category": "programming",
        "provider": "Mistral AI",
        "description": "El modelo de código de Mistral. Muy versátil y capaz en tareas de refactorización y generación de proyectos enteros.",
        "type": "gguf",
        "ollama_tag": "codestral",
        "tags": ["Refactorización", "Proyectos Complejos", "Bash"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 13.0, "ram_required_gb": 20.0, "vram_required_gb": 14.5},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 24.0, "ram_required_gb": 32.0, "vram_required_gb": 26.0}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run codestral\n```",
        "info_url": "https://huggingface.co/mistralai/Codestral-22B-v0.1"
    },
    {
        "id": "starcoder2-15b",
        "name": "StarCoder2 (15B)",
        "category": "programming",
        "provider": "BigCode",
        "description": "Entrenado de forma muy transparente por la comunidad BigCode. Fuerte en repositorios y lenguajes poco comunes.",
        "type": "gguf",
        "ollama_tag": "starcoder2:15b",
        "tags": ["Transparente", "Repositorios", "Lenguajes Raros"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 8.5, "ram_required_gb": 16.0, "vram_required_gb": 10.0},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 16.0, "ram_required_gb": 24.0, "vram_required_gb": 18.0}
        ],
        "run_instructions": "Ejecutar con **Ollama**:\n```bash\nollama run starcoder2:15b\n```",
        "info_url": "https://huggingface.co/bigcode/starcoder2-15b"
    },

    # --- IMAGE GENERATION (DIFUSIÓN) ---
    {
        "id": "stable-diffusion-xl",
        "name": "Stable Diffusion XL (SDXL)",
        "category": "image",
        "provider": "Stability AI",
        "description": "Generación nativa en 1024x1024. Produce imágenes con mucho mayor detalle, anatomía mejorada y textos legibles.",
        "type": "diffusers",
        "ollama_tag": None,
        "tags": ["Arte", "Fotorealismo", "Alta Resolución"],
        "variants": [
            {"name": "Base FP16", "size_gb": 6.5, "ram_required_gb": 16.0, "vram_required_gb": 8.0},
            {"name": "Base + Refiner FP16", "size_gb": 12.5, "ram_required_gb": 24.0, "vram_required_gb": 12.0}
        ],
        "run_instructions": "Se recomienda usar **ComfyUI** por su bajo consumo de VRAM o **Automatic1111** con `--medvram` habilitado.",
        "info_url": "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0"
    },
    {
        "id": "sd3-medium",
        "name": "Stable Diffusion 3 (Medium)",
        "category": "image",
        "provider": "Stability AI",
        "description": "Arquitectura MM-DiT. Mejora abismalmente la comprensión de los prompts largos y la renderización de texto explícito.",
        "type": "diffusers",
        "ollama_tag": None,
        "tags": ["Tipografía", "Prompting Complejo", "MM-DiT"],
        "variants": [
            {"name": "Base FP16", "size_gb": 4.5, "ram_required_gb": 12.0, "vram_required_gb": 6.0},
            {"name": "Con T5-XXL Encoder", "size_gb": 14.5, "ram_required_gb": 24.0, "vram_required_gb": 16.0}
        ],
        "run_instructions": "Se requiere **ComfyUI**. Utilizar los flujos de trabajo (workflows) oficiales para SD3.",
        "info_url": "https://huggingface.co/stabilityai/stable-diffusion-3-medium"
    },
    {
        "id": "flux-1-schnell",
        "name": "FLUX.1 Schnell",
        "category": "image",
        "provider": "Black Forest Labs",
        "description": "Modelo ultra rápido destilado (4 steps). Genera imágenes hiperrealistas y de altísima fidelidad a los prompts de manera casi instántanea.",
        "type": "diffusers",
        "ollama_tag": None,
        "tags": ["Ultra-realista", "Rápido", "Textos perfectos"],
        "variants": [
            {"name": "Cuantizado (NF4/8-bit)", "size_gb": 12.0, "ram_required_gb": 16.0, "vram_required_gb": 12.0},
            {"name": "Precisión Completa (FP16)", "size_gb": 24.0, "ram_required_gb": 32.0, "vram_required_gb": 24.0}
        ],
        "run_instructions": "Se recomienda usar **ComfyUI** con checkpoints en formato GGUF o NF4 para optimizar la VRAM.",
        "info_url": "https://huggingface.co/black-forest-labs/FLUX.1-schnell"
    },
    {
        "id": "flux-1-dev",
        "name": "FLUX.1 Dev",
        "category": "image",
        "provider": "Black Forest Labs",
        "description": "Versión completa y base de FLUX para desarrollo. Mayor libertad artística y flexibilidad que Schnell, aunque requiere más pasos.",
        "type": "diffusers",
        "ollama_tag": None,
        "tags": ["State-of-the-Art", "Alta Fidelidad", "Arte"],
        "variants": [
            {"name": "Cuantizado (GGUF Q8)", "size_gb": 18.0, "ram_required_gb": 24.0, "vram_required_gb": 16.0},
            {"name": "Precisión Completa (FP16)", "size_gb": 24.0, "ram_required_gb": 32.0, "vram_required_gb": 24.0}
        ],
        "run_instructions": "Usar **ComfyUI**. Soporta uso de LoRAs y ControlNets complejos de la comunidad.",
        "info_url": "https://huggingface.co/black-forest-labs/FLUX.1-dev"
    },

    # --- AUDIO & SPEECH ---
    {
        "id": "whisper-large-v3",
        "name": "Whisper Large v3",
        "category": "audio",
        "provider": "OpenAI",
        "description": "El mejor modelo open source de reconocimiento de voz. Identifica puntuación, múltiples idiomas en un mismo audio y ruido de fondo.",
        "type": "pytorch",
        "ollama_tag": None,
        "tags": ["Voz a texto", "Transcripción Experta", "Multi-idioma"],
        "variants": [
            {"name": "Large v3 (FP16)", "size_gb": 3.1, "ram_required_gb": 8.0, "vram_required_gb": 4.5}
        ],
        "run_instructions": "Usar localmente mediante `faster-whisper` para multiplicar por 4 la velocidad de transcripción.",
        "info_url": "https://huggingface.co/openai/whisper-large-v3"
    },
    {
        "id": "bark-suno",
        "name": "Bark (TTS)",
        "category": "audio",
        "provider": "Suno",
        "description": "Generación de voz y audio realista que soporta inflexiones emocionales, risas, suspiros y música de fondo.",
        "type": "pytorch",
        "ollama_tag": None,
        "tags": ["Texto a voz", "Emociones", "Efectos sonoros"],
        "variants": [
            {"name": "Modelo Completo", "size_gb": 4.5, "ram_required_gb": 12.0, "vram_required_gb": 6.0}
        ],
        "run_instructions": "Disponible como librería de Python `pip install git+https://github.com/suno-ai/bark.git`.",
        "info_url": "https://github.com/suno-ai/bark"
    },
    {
        "id": "parler-tts-mini",
        "name": "Parler-TTS Mini",
        "category": "audio",
        "provider": "Hugging Face",
        "description": "Texto a voz de alta calidad donde puedes controlar explícitamente el tono de voz, acento y ambiente del narrador mediante texto.",
        "type": "pytorch",
        "ollama_tag": None,
        "tags": ["Texto a voz", "Voz Controlable"],
        "variants": [
            {"name": "Mini", "size_gb": 2.0, "ram_required_gb": 8.0, "vram_required_gb": 4.0}
        ],
        "run_instructions": "Se ejecuta en Python importando la librería `parler-tts`.",
        "info_url": "https://huggingface.co/parler-tts/parler-tts-mini-v1"
    },

    # --- VISION & MULTIMODAL ---
    {
        "id": "llama-3.2-vision",
        "name": "Llama 3.2 Vision (11B)",
        "category": "vision",
        "provider": "Meta",
        "description": "El primer modelo multimodal de Meta. Excelente para análisis semántico de imágenes, OCR, y responder preguntas complejas visuales.",
        "type": "gguf",
        "ollama_tag": "llama3.2-vision",
        "tags": ["Análisis de imagen", "OCR", "Multimodal"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 7.5, "ram_required_gb": 16.0, "vram_required_gb": 8.5},
            {"name": "Original (FP16)", "size_gb": 22.0, "ram_required_gb": 32.0, "vram_required_gb": 24.0}
        ],
        "run_instructions": "Disponible en **Ollama** (versión de 11B parámetros):\n```bash\nollama run llama3.2-vision\n```",
        "info_url": "https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct"
    },
    {
        "id": "llava-1.5-7b",
        "name": "LLaVA 1.5 (7B)",
        "category": "vision",
        "provider": "Haotian Liu et al.",
        "description": "Clásico modelo de visión que conecta un encoder de imágenes con Vicuna (Llama). Muy eficiente para describir imágenes.",
        "type": "gguf",
        "ollama_tag": "llava:7b",
        "tags": ["Descripciones", "Ligero"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 4.5, "ram_required_gb": 8.0, "vram_required_gb": 5.5}
        ],
        "run_instructions": "Ejecutar con **Ollama** adjuntando una ruta de imagen:\n```bash\nollama run llava \"¿Qué hay en esta imagen? /ruta/imagen.jpg\"\n```",
        "info_url": "https://llava-vl.github.io/"
    },
    {
        "id": "qwen2-vl-7b",
        "name": "Qwen2-VL (7B)",
        "category": "vision",
        "provider": "Alibaba",
        "description": "Sobresaliente en comprensión de video e imágenes. Interpreta gráficos, documentos matemáticos y textos complejos visuales mejor que la mayoría.",
        "type": "gguf",
        "ollama_tag": "qwen2.5-vl:7b", # assuming 2.5-vl is available soon or 2-vl exists under tags
        "tags": ["Matemáticas Visuales", "Gráficos", "Video"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 5.0, "ram_required_gb": 10.0, "vram_required_gb": 6.5},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 8.5, "ram_required_gb": 16.0, "vram_required_gb": 10.0}
        ],
        "run_instructions": "Soportado por **Ollama** pronto o mediante `vLLM`.",
        "info_url": "https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct"
    },
    {
        "id": "pixtral-12b",
        "name": "Pixtral (12B)",
        "category": "vision",
        "provider": "Mistral AI",
        "description": "Primer modelo multimodal de Mistral. Destaca en la lectura de documentos estructurados, capturas de pantalla de código y diagramas.",
        "type": "gguf",
        "ollama_tag": "pixtral-12b",
        "tags": ["Lectura de Código Visual", "Diagramas", "Mistral"],
        "variants": [
            {"name": "Cuantizado (Q4_K_M)", "size_gb": 8.2, "ram_required_gb": 16.0, "vram_required_gb": 9.5},
            {"name": "Precisión Alta (Q8_0)", "size_gb": 15.0, "ram_required_gb": 24.0, "vram_required_gb": 16.5}
        ],
        "run_instructions": "Asegúrate de tener un backend actualizado que soporte su arquitectura visual.",
        "info_url": "https://huggingface.co/mistralai/Pixtral-12B-2409"
    }
]
