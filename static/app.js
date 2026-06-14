// Global State
let systemHardware = null;
let modelsDatabase = [];
let installedModels = []; // Tags of models already pulled in Ollama
let isOllamaRunning = false;
let activeFilters = {
    search: '',
    category: 'all',
    status: 'all'
};
let simulatedResources = {
    enabled: false,
    ram: 16,
    vram: 4
};
let chatHistoryMessages = []; // Messages array for Ollama API
let activeChatModelTag = '';
let activeChatModelId = '';
let activeInstallationIntervals = {}; // Tracks setInterval IDs for model downloads
let ollamaInstallInterval = null;

// DOM Elements
const elements = {
    scanStatusText: document.getElementById('scan-status-text'),
    scanStatusBadge: document.getElementById('scan-status-badge'),
    
    // Hardware panel elements
    hwOs: document.getElementById('hardware-os'),
    hwCpu: document.getElementById('hardware-cpu'),
    hwCpuCores: document.getElementById('hardware-cpu-cores'),
    hwCpuUsage: document.getElementById('hardware-cpu-usage'),
    cpuUsageBar: document.getElementById('cpu-usage-bar'),
    
    hwRam: document.getElementById('hardware-ram'),
    hwRamAvail: document.getElementById('hardware-ram-avail'),
    hwRamPercent: document.getElementById('hardware-ram-percent'),
    ramUsageBar: document.getElementById('ram-usage-bar'),
    
    hwGpuName: document.getElementById('hardware-gpu-name'),
    gpuVendorBadge: document.getElementById('gpu-vendor-badge'),
    hwVram: document.getElementById('hardware-vram'),
    hwVramFree: document.getElementById('hardware-vram-free'),
    vramUsageBar: document.getElementById('vram-usage-bar'),
    
    // Simulator
    toggleSimulator: document.getElementById('toggle-simulator'),
    simRamGroup: document.getElementById('sim-ram-group'),
    simVramGroup: document.getElementById('sim-vram-group'),
    sliderRam: document.getElementById('slider-ram'),
    sliderVram: document.getElementById('slider-vram'),
    simRamVal: document.getElementById('sim-ram-val'),
    simVramVal: document.getElementById('sim-vram-val'),
    
    // Warning banner for Ollama
    ollamaWarningBanner: document.getElementById('ollama-warning-banner'),
    btnInstallOllama: document.getElementById('btn-install-ollama'),
    
    // Filter controls
    searchInput: document.getElementById('search-input'),
    categoryPills: document.getElementById('category-pills'),
    statusPills: document.getElementById('status-pills'),
    
    // Results
    resultsCount: document.getElementById('results-count'),
    modelsContainer: document.getElementById('models-list-container'),
    modelCardTemplate: document.getElementById('model-card-template'),
    
    // Chat Playground
    chatPlayground: document.getElementById('chat-playground'),
    chatModelName: document.getElementById('chat-model-name'),
    closePlaygroundBtn: document.getElementById('close-playground'),
    chatHistory: document.getElementById('chat-history'),
    chatForm: document.getElementById('chat-form'),
    chatInput: document.getElementById('chat-input'),
    chatSendBtn: document.getElementById('chat-send-btn'),
    
    // Terminal Modal (Ollama Software Installer UI)
    terminalModal: document.getElementById('terminal-modal'),
    terminalLogs: document.getElementById('terminal-logs'),
    closeTerminalBtn: document.getElementById('close-terminal'),
    terminalStatusDot: document.getElementById('terminal-status-dot'),
    terminalStatusText: document.getElementById('terminal-status-text')
};

// Initialize the Application
document.addEventListener('DOMContentLoaded', async () => {
    // 1. Fetch System Hardware Info
    await fetchHardware();
    
    // 2. Verify Ollama Connection & Downloaded Models
    await verifyOllamaStatus();
    
    // 3. Fetch Catalogue Database
    await fetchModels();
    
    // 4. Setup Events
    setupEventListeners();
    
    // 5. Initial rendering
    evaluateAndRender();
});

// Fetch system specs from local API
async function fetchHardware() {
    try {
        const response = await fetch('/api/scan');
        if (!response.ok) throw new Error("Fallo en la comunicación con el servidor");
        systemHardware = await response.json();
        
        // Update sidebar with actual hardware
        updateHardwareUI(systemHardware);
        
        // Initialize simulator values to match actual hardware
        if (systemHardware) {
            simulatedResources.ram = Math.round(systemHardware.ram.total_gb);
            elements.sliderRam.value = simulatedResources.ram;
            elements.simRamVal.textContent = `${simulatedResources.ram} GB`;
            
            if (systemHardware.gpus && systemHardware.gpus.length > 0) {
                simulatedResources.vram = Math.round(systemHardware.gpus[0].vram_total_gb);
                elements.sliderVram.value = simulatedResources.vram;
                elements.simVramVal.textContent = `${simulatedResources.vram} GB`;
            } else {
                simulatedResources.vram = 0;
                elements.sliderVram.value = 0;
                elements.simVramVal.textContent = `0 GB`;
            }
        }
        
        elements.scanStatusText.textContent = "Sistema Escaneado";
        elements.scanStatusBadge.className = "status-badge ready";
    } catch (error) {
        console.error("Error al obtener hardware:", error);
        elements.scanStatusText.textContent = "Error de escaneo";
        elements.scanStatusBadge.style.borderColor = "var(--color-red)";
    }
}

// Check if Ollama is running, and get list of installed models
async function verifyOllamaStatus() {
    try {
        const statusRes = await fetch('/api/ollama/status');
        const statusData = await statusRes.json();
        isOllamaRunning = statusData.alive;
        
        if (isOllamaRunning) {
            elements.ollamaWarningBanner.classList.add('hidden');
            
            const installedRes = await fetch('/api/ollama/installed');
            const installedData = await installedRes.json();
            
            // Extract model tags
            installedModels = installedData.models || [];
            console.log("Modelos Ollama instalados:", installedModels);
        } else {
            elements.ollamaWarningBanner.classList.remove('hidden');
            installedModels = [];
        }
    } catch (error) {
        console.error("Error al verificar estado de Ollama:", error);
        isOllamaRunning = false;
        elements.ollamaWarningBanner.classList.remove('hidden');
        installedModels = [];
    }
}

// Fetch models list from local API
async function fetchModels() {
    try {
        const response = await fetch('/api/models');
        if (!response.ok) throw new Error("No se pudo obtener la base de datos de modelos");
        modelsDatabase = await response.json();
    } catch (error) {
        console.error("Error al obtener modelos:", error);
    }
}

// Update the Hardware Status Sidebar UI
function updateHardwareUI(hw) {
    if (!hw) return;
    
    elements.hwOs.textContent = `${hw.os} (${hw.os_release})`;
    elements.hwCpu.textContent = hw.cpu.name;
    elements.hwCpuCores.textContent = `${hw.cpu.cores_physical} núcleos reales / ${hw.cpu.cores_logical} hilos`;
    elements.hwCpuUsage.textContent = `Uso: ${Math.round(hw.cpu.usage_percent)}%`;
    elements.cpuUsageBar.style.width = `${hw.cpu.usage_percent}%`;
    
    elements.hwRam.textContent = `${hw.ram.used_gb} GB / ${hw.ram.total_gb} GB`;
    elements.hwRamAvail.textContent = `${hw.ram.available_gb} GB libres`;
    elements.hwRamPercent.textContent = `${Math.round(hw.ram.percent)}% en uso`;
    elements.ramUsageBar.style.width = `${hw.ram.percent}%`;
    
    if (hw.gpus && hw.gpus.length > 0) {
        const primaryGpu = hw.gpus[0];
        elements.hwGpuName.textContent = primaryGpu.name;
        elements.gpuVendorBadge.textContent = primaryGpu.vendor;
        elements.gpuVendorBadge.style.display = 'inline-block';
        
        if (primaryGpu.vendor === 'Nvidia') {
            elements.gpuVendorBadge.style.background = 'rgba(118, 185, 0, 0.2)';
            elements.gpuVendorBadge.style.color = '#76b900';
        } else if (primaryGpu.vendor === 'AMD') {
            elements.gpuVendorBadge.style.background = 'rgba(237, 28, 36, 0.2)';
            elements.gpuVendorBadge.style.color = '#ed1c24';
        } else if (primaryGpu.vendor === 'Apple') {
            elements.gpuVendorBadge.style.background = 'rgba(255, 255, 255, 0.15)';
            elements.gpuVendorBadge.style.color = '#ffffff';
        }
        
        elements.hwVram.textContent = `${primaryGpu.vram_total_gb} GB`;
        elements.hwVramFree.textContent = `${primaryGpu.vram_free_gb} GB libres`;
        
        const vramUsedPercent = primaryGpu.vram_total_gb > 0 
            ? ((primaryGpu.vram_total_gb - primaryGpu.vram_free_gb) / primaryGpu.vram_total_gb) * 100 
            : 0;
        elements.vramUsageBar.style.width = `${vramUsedPercent}%`;
    } else {
        elements.hwGpuName.textContent = "Sin tarjeta gráfica dedicada";
        elements.gpuVendorBadge.style.display = 'none';
        elements.hwVram.textContent = "0 GB";
        elements.hwVramFree.textContent = "0 GB";
        elements.vramUsageBar.style.width = '0%';
    }
}

// Evaluate Model Compatibility & Render Cards
function evaluateAndRender() {
    if (!modelsDatabase.length) return;
    
    // Get resources to check against (Simulated or Real)
    let ramToCheck = simulatedResources.enabled ? simulatedResources.ram : (systemHardware ? systemHardware.ram.total_gb : 8);
    let vramToCheck = simulatedResources.enabled ? simulatedResources.vram : (systemHardware && systemHardware.gpus.length > 0 ? systemHardware.gpus[0].vram_total_gb : 0);
    
    // Apple Silicon Unified memory consideration
    const isUnified = !simulatedResources.enabled && systemHardware && systemHardware.gpus.length > 0 && systemHardware.gpus[0].unified;
    
    const container = elements.modelsContainer;
    container.innerHTML = '';
    
    let visibleCount = 0;
    
    modelsDatabase.forEach(model => {
        // Find compatibility state for standard/recommended variant (usually first item in array, Q4)
        const defaultVariant = model.variants[0];
        const statusData = calculateCompatibility(model, defaultVariant, ramToCheck, vramToCheck, isUnified);
        
        // Check filter conditions
        const matchesSearch = model.name.toLowerCase().includes(activeFilters.search.toLowerCase()) ||
                              model.provider.toLowerCase().includes(activeFilters.search.toLowerCase()) ||
                              model.description.toLowerCase().includes(activeFilters.search.toLowerCase());
                              
        const matchesCategory = activeFilters.category === 'all' || model.category === activeFilters.category;
        const matchesStatus = activeFilters.status === 'all' || statusData.status === activeFilters.status;
        
        if (matchesSearch && matchesCategory && matchesStatus) {
            visibleCount++;
            
            // Clone template and fill data
            const template = elements.modelCardTemplate.content.cloneNode(true);
            const cardElement = template.querySelector('.model-card');
            
            // Set styles based on compatibility
            cardElement.classList.add(`status-${statusData.status}`);
            cardElement.setAttribute('data-id', model.id);
            
            // Meta info
            cardElement.querySelector('.model-provider').textContent = model.provider;
            cardElement.querySelector('.model-name').textContent = model.name;
            cardElement.querySelector('.model-description').textContent = model.description;
            
            const catNames = { llm: 'Texto (LLM)', programming: 'Programación', image: 'Imagen (Difusión)', audio: 'Audio & Voz', vision: 'Visión' };
            cardElement.querySelector('.category-badge').textContent = catNames[model.category] || model.category;
            
            // Render tags
            const tagsContainer = cardElement.querySelector('.model-tags');
            if (tagsContainer) {
                tagsContainer.innerHTML = '';
                if (model.tags && model.tags.length > 0) {
                    model.tags.forEach(tag => {
                        const span = document.createElement('span');
                        span.className = 'model-tag';
                        span.textContent = tag;
                        tagsContainer.appendChild(span);
                    });
                }
            }
            
            // Status & Performance
            cardElement.querySelector('.status-text').textContent = statusData.statusText;
            cardElement.querySelector('.perf-text').textContent = statusData.performanceText;
            
            // Details
            cardElement.querySelector('.vram-val').textContent = `${defaultVariant.vram_required_gb} GB`;
            cardElement.querySelector('.ram-val').textContent = `${defaultVariant.ram_required_gb} GB`;
            cardElement.querySelector('.size-val').textContent = `${defaultVariant.size_gb} GB (${defaultVariant.name.split(' ')[0]})`;
            
            // Info link
            const infoBtn = cardElement.querySelector('.info-btn');
            infoBtn.href = model.info_url;
            
            // Setup collapsible instructions panel
            const instrBtn = cardElement.querySelector('.toggle-instructions-btn');
            const instrPanel = cardElement.querySelector('.instructions-panel');
            const instrContent = cardElement.querySelector('.instructions-content');
            instrContent.innerHTML = formatInstructions(model.run_instructions);
            
            instrBtn.addEventListener('click', (e) => {
                const isOpen = instrPanel.classList.contains('open');
                instrBtn.classList.toggle('active');
                if (isOpen) {
                    instrPanel.classList.remove('open');
                } else {
                    instrPanel.classList.add('open');
                }
            });
            
            // --- Auto-Assisted Installation Buttons Integration ---
            const installBtn = cardElement.querySelector('.install-btn');
            const chatBtn = cardElement.querySelector('.chat-btn');
            const progressContainer = cardElement.querySelector('.install-progress-container');
            const progressBar = cardElement.querySelector('.install-progress-bar');
            const progressText = cardElement.querySelector('.install-progress-text');
            
            if (model.ollama_tag) {
                // Check if this model is already installed
                const isInstalled = checkIsModelInstalled(model.ollama_tag);
                
                if (isInstalled) {
                    chatBtn.classList.remove('hidden');
                    installBtn.classList.add('hidden');
                    
                    // Bind Chat Playground click
                    chatBtn.addEventListener('click', () => {
                        openChatPlayground(model.id, model.name, model.ollama_tag);
                    });
                } else {
                    // Check if there is an active download going on
                    const activeDownload = activeInstallationIntervals[model.id];
                    
                    if (activeDownload) {
                        installBtn.classList.add('hidden');
                        progressContainer.classList.remove('hidden');
                    } else {
                        installBtn.classList.remove('hidden');
                        chatBtn.classList.add('hidden');
                        progressContainer.classList.add('hidden');
                        
                        // Disable button if Ollama is not active or if model is NOT compatible (No Recomendado)
                        if (!isOllamaRunning) {
                            installBtn.setAttribute('disabled', 'true');
                            installBtn.style.opacity = '0.4';
                            installBtn.title = "Inicia/Instala Ollama primero.";
                        } else if (statusData.status === 'not-recommended') {
                            installBtn.setAttribute('disabled', 'true');
                            installBtn.style.opacity = '0.4';
                            installBtn.title = "No recomendado para tu hardware. Riesgo de bloqueo.";
                        } else {
                            installBtn.removeAttribute('disabled');
                            installBtn.style.opacity = '1';
                            installBtn.title = "Instalar modelo localmente";
                            
                            // Bind installation trigger
                            installBtn.addEventListener('click', () => {
                                startModelInstallation(model.id, model.ollama_tag, installBtn, progressContainer, progressBar, progressText);
                            });
                        }
                    }
                }
            } else {
                // Non-Ollama models don't support auto install yet
                installBtn.classList.add('hidden');
                chatBtn.classList.add('hidden');
            }
            
            container.appendChild(template);
        }
    });
    
    // Update counter
    elements.resultsCount.textContent = `Mostrando ${visibleCount} de ${modelsDatabase.length} modelos`;
    
    if (visibleCount === 0) {
        container.innerHTML = `
            <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <i data-lucide="info" style="width: 40px; height: 40px; margin: 0 auto 1rem; color: var(--text-muted);"></i>
                <h3>Ningún modelo coincide con los filtros</h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">Prueba a cambiar tus criterios de búsqueda o activa el Simulador de Hardware.</p>
            </div>
        `;
        lucide.createIcons();
    } else {
        lucide.createIcons();
    }
}

// Logic: Helper to match model tags with installed tags
function checkIsModelInstalled(tag) {
    if (!installedModels.length) return false;
    
    // Check for exact match or matches starting with tag
    // Ollama tags might return "llama3.2:1b" or "llama3.2:latest"
    const cleanTag = tag.includes(':') ? tag : `${tag}:latest`;
    
    return installedModels.some(inst => {
        const cleanInst = inst.includes(':') ? inst : `${inst}:latest`;
        return cleanInst === cleanTag || inst.startsWith(tag.split(':')[0]);
    });
}

// Logic: Determine hardware capability status
function calculateCompatibility(model, variant, activeRam, activeVram, isUnified = false) {
    const vramReq = variant.vram_required_gb;
    const ramReq = variant.ram_required_gb;
    
    if (isUnified) {
        const totalUnifiedPool = activeRam;
        const availablePoolForModel = totalUnifiedPool * 0.85;
        
        if (variant.size_gb <= availablePoolForModel) {
            return {
                status: 'optimal',
                statusText: 'Óptimo (Memoria Unificada)',
                performanceText: 'Excelente velocidad (GPU nativa)'
            };
        } else if (variant.size_gb <= totalUnifiedPool) {
            return {
                status: 'partial',
                statusText: 'Parcial (Cerca del Límite)',
                performanceText: 'Moderada velocidad (Swap)'
            };
        } else {
            return {
                status: 'not-recommended',
                statusText: 'Riesgo de Bloqueo',
                performanceText: 'Excede memoria total'
            };
        }
    }
    
    // Standard Discrete GPU & CPU system rules
    if (activeVram >= vramReq && activeRam >= ramReq) {
        return {
            status: 'optimal',
            statusText: 'Óptimo (Ejecución en GPU)',
            performanceText: 'Fluido (GPU Acelerado)'
        };
    }
    
    if (model.type === 'gguf') {
        const totalSystemCapacity = activeRam + (activeVram > 0.5 ? activeVram : 0);
        const modelMargin = variant.size_gb + 1.5;
        
        if (activeRam >= ramReq && totalSystemCapacity >= modelMargin) {
            if (activeVram >= 1.5) {
                return {
                    status: 'partial',
                    statusText: 'Parcial (Híbrido CPU/GPU)',
                    performanceText: 'Velocidad Moderada (Offloading)'
                };
            } else {
                return {
                    status: 'partial',
                    statusText: 'Parcial (Ejecución en CPU)',
                    performanceText: 'Lento (Inferencia en CPU)'
                };
            }
        }
    } else {
        if (activeVram >= vramReq * 0.7 && activeRam >= ramReq) {
            return {
                status: 'partial',
                statusText: 'Parcial (Bajo VRAM)',
                performanceText: 'Lento (Memoria Compartida)'
            };
        }
    }
    
    return {
        status: 'not-recommended',
        statusText: 'No Recomendado',
        performanceText: 'Cuelgue / OOM (Falta Memoria)'
    };
}

// Convert instruction markdown snippets to HTML safely
function formatInstructions(instructions) {
    if (!instructions) return '';
    let html = instructions;
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    html = html.split('\n').map(line => {
        if (line.trim().startsWith('<pre>') || line.trim().startsWith('</pre>') || line.trim().startsWith('<code>') || line.trim().startsWith('</code>')) {
            return line;
        }
        return line.trim() ? `<p>${line}</p>` : '';
    }).join('');
    return html;
}

// Start auto-assisted model download from Ollama
async function startModelInstallation(modelId, ollamaTag, btn, progressContainer, progressBar, progressText) {
    try {
        btn.classList.add('hidden');
        progressContainer.classList.remove('hidden');
        progressBar.style.width = '0%';
        progressText.textContent = "Conectando con Ollama...";
        
        const response = await fetch('/api/install', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model_id: modelId, ollama_tag: ollamaTag })
        });
        
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        
        // Start polling installer progress
        const intervalId = setInterval(async () => {
            const statusRes = await fetch(`/api/install/status/${modelId}`);
            const statusData = await statusRes.json();
            
            if (statusData.status === 'downloading' || statusData.status === 'pulling') {
                progressBar.style.width = `${statusData.progress || 0}%`;
                const sizeInfo = statusData.total > 0 
                    ? ` (${round(statusData.completed / (1024**3), 2)} GB / ${round(statusData.total / (1024**3), 2)} GB)`
                    : '';
                progressText.textContent = `Descargando: ${statusData.progress || 0}%${sizeInfo}`;
            } else if (statusData.status === 'success') {
                clearInterval(intervalId);
                delete activeInstallationIntervals[modelId];
                progressBar.style.width = '100%';
                progressText.textContent = "¡Completado con éxito!";
                
                // Refresh list of installed models and re-render
                setTimeout(async () => {
                    await verifyOllamaStatus();
                    evaluateAndRender();
                }, 1500);
            } else if (statusData.status === 'failed') {
                clearInterval(intervalId);
                delete activeInstallationIntervals[modelId];
                progressBar.style.width = '0%';
                progressText.textContent = `Fallo: ${statusData.error || 'Error desconocido'}`;
                progressText.style.color = 'var(--color-red)';
                
                setTimeout(() => {
                    btn.classList.remove('hidden');
                    progressContainer.classList.add('hidden');
                    progressText.style.color = 'var(--text-secondary)';
                }, 4000);
            } else {
                progressText.textContent = statusData.status || "Procesando...";
            }
        }, 8000); // Poll every 8 seconds to prevent console flooding but stay responsive
        
        // Register interval
        activeInstallationIntervals[modelId] = intervalId;
        
    } catch (error) {
        console.error("Fallo al iniciar instalación de modelo:", error);
        alert(`Fallo al iniciar descarga: ${error.message}`);
        btn.classList.remove('hidden');
        progressContainer.classList.add('hidden');
    }
}

// Open Chat Playground Panel
function openChatPlayground(modelId, modelName, modelTag) {
    activeChatModelId = modelId;
    activeChatModelTag = modelTag;
    
    // Set Header
    elements.chatModelName.textContent = modelName;
    
    // Clear chat logs, reset history
    chatHistoryMessages = [];
    elements.chatHistory.innerHTML = `
        <div class="chat-message assistant">
            <div class="message-avatar"><i data-lucide="bot"></i></div>
            <div class="message-bubble">
                ¡Hola! Ya estoy cargado y ejecutándose localmente mediante Ollama. Hazme cualquier pregunta para medir mi velocidad de inferencia en tu hardware.
            </div>
        </div>
    `;
    lucide.createIcons();
    
    // Open panel
    elements.chatPlayground.classList.remove('collapsed');
    elements.chatInput.focus();
}

// Send Message to Model via SSE
async function sendChatMessage(e) {
    if (e) e.preventDefault();
    
    const prompt = elements.chatInput.value.trim();
    if (!prompt || !activeChatModelTag) return;
    
    // Clear input
    elements.chatInput.value = '';
    
    // Disable input while generating
    elements.chatInput.setAttribute('disabled', 'true');
    elements.chatSendBtn.setAttribute('disabled', 'true');
    
    // 1. Append User Message
    appendMessageHTML('user', prompt);
    chatHistoryMessages.push({ role: 'user', content: prompt });
    
    // 2. Append Assistant Placeholder
    const assistantBubble = appendMessageHTML('assistant', 'Pensando...');
    assistantBubble.classList.add('typing-placeholder');
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model_tag: activeChatModelTag,
                messages: chatHistoryMessages
            })
        });
        
        if (!response.ok) throw new Error("Servidor ocupado o apagado.");
        
        // Read SSE stream
        assistantBubble.textContent = ''; // clear placeholder
        assistantBubble.classList.remove('typing-placeholder');
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let fullResponseText = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (!line.trim()) continue;
                try {
                    const parsed = JSON.parse(line);
                    if (parsed.error) {
                        assistantBubble.textContent = `ERROR: ${parsed.error}`;
                        break;
                    }
                    
                    const content = parsed.message?.content || '';
                    fullResponseText += content;
                    
                    // Simple inline formatting wrapper
                    assistantBubble.innerHTML = formatChatResponse(fullResponseText);
                    
                    // Auto scroll history
                    elements.chatHistory.scrollTop = elements.chatHistory.scrollHeight;
                } catch (e) {
                    // Line might be incomplete, ignore parse error
                }
            }
        }
        
        // Save to history
        chatHistoryMessages.push({ role: 'assistant', content: fullResponseText });
        
    } catch (error) {
        console.error("Error al chatear:", error);
        assistantBubble.textContent = `Error: No se pudo recibir respuesta. Asegúrate de que Ollama esté encendido. (${error.message})`;
        assistantBubble.style.color = 'var(--color-red)';
    } finally {
        elements.chatInput.removeAttribute('disabled');
        elements.chatSendBtn.removeAttribute('disabled');
        elements.chatInput.focus();
    }
}

// Append Chat Message Bubble to GUI
function appendMessageHTML(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${role}`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.innerHTML = role === 'user' ? '<i data-lucide="user"></i>' : '<i data-lucide="bot"></i>';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.innerHTML = formatChatResponse(text);
    
    msgDiv.appendChild(avatarDiv);
    msgDiv.appendChild(bubbleDiv);
    elements.chatHistory.appendChild(msgDiv);
    lucide.createIcons();
    
    elements.chatHistory.scrollTop = elements.chatHistory.scrollHeight;
    return bubbleDiv;
}

// Simple Chat formatting (handles paragraphs, bold, code)
function formatChatResponse(text) {
    let html = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    
    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Fenced Code blocks
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    
    // Inline code
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Line breaks
    html = html.replace(/\n/g, '<br>');
    
    return html;
}

// Start auto-assisted Ollama software installation
async function triggerOllamaSoftwareInstallation() {
    try {
        elements.terminalLogs.textContent = "Conectando con el servidor de instalación...\n";
        elements.terminalModal.classList.remove('collapsed');
        elements.terminalStatusText.textContent = "Iniciando instalación...";
        elements.terminalStatusDot.className = "pulse-dot";
        
        const response = await fetch('/api/ollama/install', { method: 'POST' });
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);
        
        // Start polling logs every 500ms
        ollamaInstallInterval = setInterval(async () => {
            const statusRes = await fetch('/api/ollama/install/status');
            const statusData = await statusRes.json();
            
            // Render logs in terminal
            elements.terminalLogs.textContent = statusData.logs || "Cargando logs...";
            elements.terminalLogs.scrollTop = elements.terminalLogs.scrollHeight; // Auto-scroll
            
            if (statusData.status === 'installing') {
                elements.terminalStatusText.textContent = "Instalando Ollama en segundo plano (No cierres esta ventana)...";
            } else if (statusData.status === 'success') {
                clearInterval(ollamaInstallInterval);
                elements.terminalStatusText.textContent = "¡Ollama instalado y activo!";
                elements.terminalStatusDot.className = "pulse-dot";
                elements.terminalStatusDot.style.backgroundColor = "var(--color-green)";
                elements.terminalStatusDot.style.boxShadow = "0 0 8px var(--color-green)";
                
                // Reload status
                setTimeout(async () => {
                    elements.terminalModal.classList.add('collapsed');
                    await verifyOllamaStatus();
                    evaluateAndRender();
                }, 4000);
            } else if (statusData.status === 'failed') {
                clearInterval(ollamaInstallInterval);
                elements.terminalStatusText.textContent = "Fallo en la instalación.";
                elements.terminalStatusDot.className = "";
                elements.terminalStatusDot.style.backgroundColor = "var(--color-red)";
                elements.terminalStatusDot.style.boxShadow = "0 0 8px var(--color-red)";
            }
        }, 800);
        
    } catch (error) {
        console.error("Fallo al instalar Ollama:", error);
        elements.terminalLogs.textContent += `\nERROR CRÍTICO: ${error.message}\n`;
        elements.terminalStatusText.textContent = "Error de instalación.";
        elements.terminalStatusDot.style.backgroundColor = "var(--color-red)";
    }
}

// Set up event listeners for filters & simulator
function setupEventListeners() {
    // Search input
    elements.searchInput.addEventListener('input', (e) => {
        activeFilters.search = e.target.value.trim();
        evaluateAndRender();
    });
    
    // Category pills
    elements.categoryPills.addEventListener('click', (e) => {
        const pill = e.target.closest('.pill');
        if (!pill) return;
        
        elements.categoryPills.querySelectorAll('.pill').forEach(p => {
            p.classList.remove('active');
            p.setAttribute('aria-selected', 'false');
        });
        pill.classList.add('active');
        pill.setAttribute('aria-selected', 'true');
        
        activeFilters.category = pill.dataset.category;
        evaluateAndRender();
    });
    
    // Status pills
    elements.statusPills.addEventListener('click', (e) => {
        const pill = e.target.closest('.pill');
        if (!pill) return;
        
        elements.statusPills.querySelectorAll('.pill').forEach(p => {
            p.classList.remove('active');
            p.setAttribute('aria-selected', 'false');
        });
        pill.classList.add('active');
        pill.setAttribute('aria-selected', 'true');
        
        activeFilters.status = pill.dataset.status;
        evaluateAndRender();
    });
    
    // Simulator Toggle
    elements.toggleSimulator.addEventListener('change', (e) => {
        simulatedResources.enabled = e.target.checked;
        
        if (simulatedResources.enabled) {
            elements.simRamGroup.classList.remove('disabled');
            elements.simVramGroup.classList.remove('disabled');
            elements.sliderRam.removeAttribute('disabled');
            elements.sliderVram.removeAttribute('disabled');
        } else {
            elements.simRamGroup.classList.add('disabled');
            elements.simVramGroup.classList.add('disabled');
            elements.sliderRam.setAttribute('disabled', 'true');
            elements.sliderVram.setAttribute('disabled', 'true');
        }
        
        evaluateAndRender();
    });
    
    // RAM Simulator Slider
    elements.sliderRam.addEventListener('input', (e) => {
        simulatedResources.ram = parseInt(e.target.value);
        elements.simRamVal.textContent = `${simulatedResources.ram} GB`;
        evaluateAndRender();
    });
    
    // VRAM Simulator Slider
    elements.sliderVram.addEventListener('input', (e) => {
        simulatedResources.vram = parseInt(e.target.value);
        elements.simVramVal.textContent = `${simulatedResources.vram} GB`;
        evaluateAndRender();
    });
    
    // Warning banner click -> trigger software installer
    elements.btnInstallOllama.addEventListener('click', triggerOllamaSoftwareInstallation);
    
    // Chat Playground close panel
    elements.closePlaygroundBtn.addEventListener('click', () => {
        elements.chatPlayground.classList.add('collapsed');
    });
    
    // Chat Form submit
    elements.chatForm.addEventListener('submit', sendChatMessage);
    
    // Terminal close panel
    elements.closeTerminalBtn.addEventListener('click', () => {
        if (ollamaInstallInterval) {
            clearInterval(ollamaInstallInterval);
        }
        elements.terminalModal.classList.add('collapsed');
    });
}

// Math helper
function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}
