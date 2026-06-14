import os
import platform
import subprocess
import re
import psutil

def get_cpu_name():
    """Detects the CPU brand name in a cross-platform way."""
    system = platform.system()
    if system == "Linux":
        try:
            # First try lscpu
            output = subprocess.check_output("lscpu", shell=True).decode()
            for line in output.split("\n"):
                if "Model name" in line:
                    return line.split(":", 1)[1].strip()
        except Exception:
            pass
        
        try:
            # Fallback to /proc/cpuinfo
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line or "Model Name" in line:
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass

    elif system == "Windows":
        try:
            # Query Registry
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            winreg.CloseKey(key)
            return name.strip()
        except Exception:
            pass
        
        try:
            # Fallback to wmic
            output = subprocess.check_output("wmic cpu get name", shell=True).decode()
            lines = [line.strip() for line in output.split("\n") if line.strip()]
            if len(lines) > 1:
                return lines[1]
        except Exception:
            pass

    elif system == "Darwin":
        try:
            return subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
        except Exception:
            pass

    return platform.processor() or "CPU Desconocido"

def get_linux_gpu_vram():
    """Specific helper to find VRAM sizes on Linux for AMD/Intel/Nvidia."""
    vram_data = {}
    
    # Try reading from sysfs for AMD/Intel GPUs
    drm_path = "/sys/class/drm"
    if os.path.exists(drm_path):
        for folder in os.listdir(drm_path):
            if folder.startswith("card") and not "-" in folder:
                card_dir = os.path.join(drm_path, folder, "device")
                total_file = os.path.join(card_dir, "mem_info_vram_total")
                used_file = os.path.join(card_dir, "mem_info_vram_used")
                
                if os.path.exists(total_file):
                    try:
                        with open(total_file, "r") as f:
                            total = int(f.read().strip())
                        used = 0
                        if os.path.exists(used_file):
                            with open(used_file, "r") as f:
                                used = int(f.read().strip())
                        
                        vram_data[folder] = {
                            "total": total,
                            "used": used,
                            "free": max(0, total - used)
                        }
                    except Exception:
                        pass
    return vram_data

def get_gpus():
    """Detects GPUs and VRAM in a cross-platform way, supporting Nvidia, AMD, Intel and Apple Silicon."""
    gpus = []
    system = platform.system()
    
    # 1. Nvidia check using nvidia-smi (universal if drivers are active)
    try:
        # Run nvidia-smi to query name, total memory, and free memory
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL
        ).decode()
        
        for line in output.strip().split("\n"):
            if line:
                parts = line.split(",")
                if len(parts) >= 2:
                    name = parts[0].strip()
                    total_mb = float(parts[1].strip())
                    free_mb = float(parts[2].strip()) if len(parts) > 2 else total_mb
                    gpus.append({
                        "name": name,
                        "vram_total_gb": round(total_mb / 1024.0, 2),
                        "vram_free_gb": round(free_mb / 1024.0, 2),
                        "vendor": "Nvidia",
                        "unified": False
                    })
        return gpus
    except Exception:
        pass

    # 2. Linux specific check for AMD & Intel (e.g., lspci + sysfs)
    if system == "Linux":
        linux_vram = get_linux_gpu_vram()
        
        try:
            # Get list of controllers from lspci
            lspci_out = subprocess.check_output("lspci", shell=True).decode()
            gpu_lines = []
            for line in lspci_out.split("\n"):
                if any(x in line.lower() for x in ["vga compatible controller", "3d controller", "display controller"]):
                    gpu_lines.append(line)
            
            # Match lspci devices with vram files in sysfs
            # Typically card0 is the first VGA, card1 is the second
            for idx, line in enumerate(gpu_lines):
                # Clean up name: remove PCI address prefix
                name = line.split(":", 2)[-1].strip()
                # Remove common boilerplate
                name = re.sub(r'\(rev \w+\)', '', name).strip()
                
                vendor = "Desconocido"
                if "amd" in line.lower() or "advanced micro devices" in line.lower() or "ati" in line.lower():
                    vendor = "AMD"
                elif "intel" in line.lower():
                    vendor = "Intel"
                elif "nvidia" in line.lower():
                    vendor = "Nvidia"
                
                card_key = f"card{idx}"
                vram_info = linux_vram.get(card_key)
                
                # If card_key didn't match directly, try to search in linux_vram keys
                if not vram_info and len(linux_vram) > 0:
                    # Take the first available card as fallback
                    first_key = list(linux_vram.keys())[0]
                    vram_info = linux_vram[first_key]
                
                if vram_info:
                    total_gb = round(vram_info["total"] / (1024**3), 2)
                    free_gb = round(vram_info["free"] / (1024**3), 2)
                else:
                    # Default if we can't find VRAM file (e.g. integrated GPU without dedicated sysfs entry)
                    total_gb = 0.5 if vendor == "Intel" else 2.0
                    free_gb = total_gb
                
                gpus.append({
                    "name": name,
                    "vram_total_gb": total_gb,
                    "vram_free_gb": free_gb,
                    "vendor": vendor,
                    "unified": False
                })
            
            if gpus:
                return gpus
        except Exception:
            pass

    # 3. macOS specific check (Apple Silicon uses Unified Memory)
    elif system == "Darwin":
        try:
            sp_out = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).decode()
            chipset = "Apple Silicon"
            vram_gb = 0.0
            
            # Find Chipset Model
            match_chip = re.search(r"Chipset Model:\s*(.*)", sp_out)
            if match_chip:
                chipset = match_chip.group(1).strip()
            
            # Apple Silicon has unified RAM, so we report VRAM as ~75% of system RAM
            is_apple_silicon = "apple" in chipset.lower()
            
            if is_apple_silicon:
                # Calculate system RAM to estimate unified memory
                total_ram = psutil.virtual_memory().total
                # Apple Silicon allocates up to ~75% of RAM as GPU memory dynamically
                vram_gb = round((total_ram * 0.75) / (1024**3), 2)
                gpus.append({
                    "name": chipset,
                    "vram_total_gb": vram_gb,
                    "vram_free_gb": round((psutil.virtual_memory().available * 0.75) / (1024**3), 2),
                    "vendor": "Apple",
                    "unified": True
                })
            else:
                # Intel Mac with dedicated or integrated GPU
                match_vram = re.search(r"VRAM \(Total\):\s*(\d+)\s*(MB|GB)", sp_out)
                if match_vram:
                    val = float(match_vram.group(1))
                    unit = match_vram.group(2)
                    vram_gb = round(val / 1024.0 if unit == "MB" else val, 2)
                else:
                    vram_gb = 1.5  # fallback
                
                gpus.append({
                    "name": chipset,
                    "vram_total_gb": vram_gb,
                    "vram_free_gb": vram_gb,
                    "vendor": "Intel" if "intel" in chipset.lower() else "AMD",
                    "unified": False
                })
            return gpus
        except Exception:
            pass

    # 4. Windows specific check using WMIC / PowerShell
    elif system == "Windows":
        try:
            # Query via PowerShell (more reliable for total/free VRAM detection)
            ps_cmd = "Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM"
            output = subprocess.check_output(["powershell", "-Command", ps_cmd], stderr=subprocess.DEVNULL).decode()
            
            # Parse output
            lines = [l.strip() for l in output.split("\n") if l.strip()]
            for line in lines[2:]:  # skip headers
                parts = re.split(r'\s{2,}', line)
                if len(parts) >= 2:
                    name = parts[0]
                    try:
                        ram_bytes = int(parts[1])
                        total_gb = round(ram_bytes / (1024**3), 2)
                    except ValueError:
                        total_gb = 2.0  # fallback
                    
                    vendor = "Desconocido"
                    if "nvidia" in name.lower():
                        vendor = "Nvidia"
                    elif "amd" in name.lower() or "radeon" in name.lower():
                        vendor = "AMD"
                    elif "intel" in name.lower():
                        vendor = "Intel"
                    
                    gpus.append({
                        "name": name,
                        "vram_total_gb": total_gb,
                        "vram_free_gb": total_gb, # Hard to get free dynamically without nvidia-smi
                        "vendor": vendor,
                        "unified": False
                    })
            if gpus:
                return gpus
        except Exception:
            pass

    # Generic fallback if no GPU was successfully parsed
    return [{
        "name": "GPU Integrada / Genérica",
        "vram_total_gb": 0.5,
        "vram_free_gb": 0.5,
        "vendor": "Genérico",
        "unified": False
    }]

def scan_hardware():
    """Scans the host hardware specs and returns a structured dictionary."""
    ram = psutil.virtual_memory()
    gpus = get_gpus()
    
    # Check if we have at least one dedicated GPU with non-trivial VRAM
    has_gpu = any(g["vram_total_gb"] > 1.0 for g in gpus)
    
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "cpu": {
            "name": get_cpu_name(),
            "cores_physical": psutil.cpu_count(logical=False) or 1,
            "cores_logical": psutil.cpu_count(logical=True) or 1,
            "usage_percent": psutil.cpu_percent(interval=0.1)
        },
        "ram": {
            "total_gb": round(ram.total / (1024**3), 2),
            "available_gb": round(ram.available / (1024**3), 2),
            "used_gb": round(ram.used / (1024**3), 2),
            "percent": ram.percent
        },
        "gpus": gpus,
        "has_gpu": has_gpu
    }

if __name__ == "__main__":
    # Test script directly
    import json
    print(json.dumps(scan_hardware(), indent=4, ensure_ascii=False))
