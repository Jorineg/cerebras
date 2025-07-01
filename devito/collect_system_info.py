#!/usr/bin/env python3
"""
Standalone script to collect comprehensive system information for thesis documentation.
Gathers CPU, memory, GPU, and software details and writes them to a markdown file.
"""

import subprocess
import sys
import os
import platform
import argparse
from datetime import datetime

def safe_get_command_output(cmd, description=""):
    """Safely execute a command and return its output, with graceful failure."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=15)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Warning: Failed to get {description} (non-zero exit code)")
            return "Not available"
    except subprocess.TimeoutExpired:
        print(f"Warning: Timeout getting {description}")
        return "Not available"
    except Exception as e:
        print(f"Warning: Error getting {description}: {e}")
        return "Not available"

def get_cpu_info():
    """Gather comprehensive CPU information."""
    print("  - CPU details...")
    cpu_info = {}
    
    # Basic platform info
    cpu_info['architecture'] = platform.machine()
    cpu_info['platform'] = platform.platform()
    cpu_info['processor'] = platform.processor()
    
    # Try to get detailed CPU info from /proc/cpuinfo
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            lines = cpuinfo.split('\n')
            for line in lines:
                if 'model name' in line:
                    cpu_info['model_name'] = line.split(':')[1].strip()
                    break
            for line in lines:
                if 'cpu cores' in line:
                    cpu_info['physical_cores'] = line.split(':')[1].strip()
                    break
            for line in lines:
                if 'cpu MHz' in line:
                    cpu_info['current_mhz'] = line.split(':')[1].strip()
                    break
            for line in lines:
                if 'flags' in line or 'Features' in line:
                    flags = line.split(':')[1].strip()
                    # Check for important features
                    important_flags = ['avx', 'avx2', 'avx512', 'sse4', 'fma']
                    present_flags = [flag for flag in important_flags if flag in flags.lower()]
                    if present_flags:
                        cpu_info['cpu_features'] = ', '.join(present_flags)
                    break
    except:
        pass
    
    # Try lscpu for additional details
    lscpu_output = safe_get_command_output("lscpu", "CPU details via lscpu")
    if lscpu_output != "Not available":
        for line in lscpu_output.split('\n'):
            if 'CPU(s):' in line and 'NUMA' not in line:
                cpu_info['logical_cpus'] = line.split(':')[1].strip()
            elif 'Thread(s) per core:' in line:
                cpu_info['threads_per_core'] = line.split(':')[1].strip()
            elif 'Core(s) per socket:' in line:
                cpu_info['cores_per_socket'] = line.split(':')[1].strip()
            elif 'Socket(s):' in line:
                cpu_info['sockets'] = line.split(':')[1].strip()
            elif 'CPU max MHz:' in line:
                cpu_info['max_mhz'] = line.split(':')[1].strip()
            elif 'CPU min MHz:' in line:
                cpu_info['min_mhz'] = line.split(':')[1].strip()
            elif 'L1d cache:' in line:
                cpu_info['l1d_cache'] = line.split(':')[1].strip()
            elif 'L1i cache:' in line:
                cpu_info['l1i_cache'] = line.split(':')[1].strip()
            elif 'L2 cache:' in line:
                cpu_info['l2_cache'] = line.split(':')[1].strip()
            elif 'L3 cache:' in line:
                cpu_info['l3_cache'] = line.split(':')[1].strip()
            elif 'NUMA node(s):' in line:
                cpu_info['numa_nodes'] = line.split(':')[1].strip()
    
    return cpu_info

def get_memory_info():
    """Gather comprehensive memory information."""
    print("  - Memory details...")
    mem_info = {}
    
    # Basic memory from /proc/meminfo
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
            lines = meminfo.split('\n')
            for line in lines:
                if 'MemTotal:' in line:
                    mem_kb = int(line.split()[1])
                    mem_info['total_ram_gb'] = round(mem_kb / 1024 / 1024, 2)
                elif 'MemAvailable:' in line:
                    mem_kb = int(line.split()[1])
                    mem_info['available_ram_gb'] = round(mem_kb / 1024 / 1024, 2)
                elif 'SwapTotal:' in line:
                    swap_kb = int(line.split()[1])
                    mem_info['swap_gb'] = round(swap_kb / 1024 / 1024, 2)
    except:
        pass
    
    # Try to get memory details via dmidecode (requires sudo, may fail gracefully)
    dmidecode_output = safe_get_command_output("sudo dmidecode --type memory 2>/dev/null", "memory details via dmidecode")
    if dmidecode_output != "Not available":
        # Parse dmidecode output for memory speed, type, etc.
        lines = dmidecode_output.split('\n')
        speeds = []
        types = []
        sizes = []
        for line in lines:
            if 'Speed:' in line and 'Unknown' not in line and 'Not Specified' not in line:
                speed = line.split(':')[1].strip()
                if speed not in speeds and speed != "":
                    speeds.append(speed)
            elif 'Type:' in line and 'Unknown' not in line and 'Not Specified' not in line:
                mem_type = line.split(':')[1].strip()
                if mem_type not in types and mem_type != "":
                    types.append(mem_type)
            elif 'Size:' in line and 'No Module Installed' not in line:
                size = line.split(':')[1].strip()
                if size not in sizes and size != "":
                    sizes.append(size)
        
        if speeds:
            mem_info['memory_speed'] = ', '.join(speeds)
        if types:
            mem_info['memory_type'] = ', '.join(types)
        if sizes:
            mem_info['memory_modules'] = ', '.join(sizes)
    
    # Try lshw for memory info (alternative, no sudo required)
    lshw_output = safe_get_command_output("lshw -short -C memory 2>/dev/null", "memory info via lshw")
    if lshw_output != "Not available" and 'memory_speed' not in mem_info:
        mem_info['memory_details_lshw'] = lshw_output.replace('\n', '; ')
    
    return mem_info

def get_gpu_info():
    """Gather comprehensive GPU information."""
    print("  - GPU and CUDA details...")
    gpu_info = {}
    
    # Try nvidia-smi for NVIDIA GPUs
    nvidia_smi_output = safe_get_command_output("nvidia-smi --query-gpu=gpu_name,driver_version,memory.total,compute_cap --format=csv,noheader,nounits", "NVIDIA GPU info")
    if nvidia_smi_output != "Not available":
        lines = nvidia_smi_output.split('\n')
        gpus = []
        for line in lines:
            if line.strip():
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 4:
                    gpus.append({
                        'name': parts[0],
                        'driver_version': parts[1],
                        'memory_mb': parts[2],
                        'compute_capability': parts[3]
                    })
        if gpus:
            gpu_info['nvidia_gpus'] = gpus
    
    # Get more detailed GPU info with nvidia-smi
    nvidia_detailed = safe_get_command_output("nvidia-smi --query-gpu=name,pci.bus_id,power.max_limit,clocks.max.graphics,clocks.max.memory --format=csv,noheader,nounits", "detailed NVIDIA GPU info")
    if nvidia_detailed != "Not available":
        lines = nvidia_detailed.split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 5 and i < len(gpu_info.get('nvidia_gpus', [])):
                    gpu_info['nvidia_gpus'][i].update({
                        'pci_bus_id': parts[1],
                        'max_power_w': parts[2],
                        'max_graphics_clock_mhz': parts[3],
                        'max_memory_clock_mhz': parts[4]
                    })
    
    # Get CUDA version
    cuda_version = safe_get_command_output("nvcc --version", "CUDA version")
    if cuda_version != "Not available":
        # Extract version from nvcc output
        for line in cuda_version.split('\n'):
            if 'release' in line.lower():
                gpu_info['cuda_version'] = line.strip()
                break
    
    # Alternative CUDA version checks
    if 'cuda_version' not in gpu_info:
        cuda_alt = safe_get_command_output("cat /usr/local/cuda/version.txt 2>/dev/null", "CUDA version from file")
        if cuda_alt != "Not available":
            gpu_info['cuda_version'] = cuda_alt
    
    # CUDA runtime version
    if 'cuda_version' not in gpu_info:
        cuda_runtime = safe_get_command_output("nvidia-smi | grep 'CUDA Version'", "CUDA runtime version")
        if cuda_runtime != "Not available":
            gpu_info['cuda_runtime_version'] = cuda_runtime.strip()
    
    # Try to get GPU details via nvidia-ml-py if available
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        detailed_gpus = []
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            try:
                power_limit = pynvml.nvmlDeviceGetPowerManagementLimitConstraints(handle)
                power_range = f"{power_limit[0]/1000:.1f}-{power_limit[1]/1000:.1f}"
            except:
                power_range = "Not available"
            
            detailed_gpus.append({
                'name': name,
                'memory_total_gb': round(memory_info.total / 1024**3, 2),
                'power_limit_range_w': power_range
            })
        if detailed_gpus:
            gpu_info['detailed_nvidia_gpus'] = detailed_gpus
    except:
        pass
    
    # Check for other GPU vendors
    lspci_gpu = safe_get_command_output("lspci | grep -i 'vga\\|3d\\|display'", "All GPUs via lspci")
    if lspci_gpu != "Not available":
        gpu_info['all_gpus_lspci'] = lspci_gpu.replace('\n', '; ')
    
    return gpu_info

def get_system_info():
    """Gather general system information."""
    print("  - System details...")
    sys_info = {}
    
    # Basic system info
    sys_info['hostname'] = platform.node()
    sys_info['os'] = platform.system()
    sys_info['os_release'] = platform.release()
    sys_info['os_version'] = platform.version()
    
    # Distribution info
    try:
        with open('/etc/os-release', 'r') as f:
            os_release = f.read()
            for line in os_release.split('\n'):
                if line.startswith('PRETTY_NAME='):
                    sys_info['distribution'] = line.split('=')[1].strip('"')
                    break
    except:
        pass
    
    # Kernel version
    sys_info['kernel'] = safe_get_command_output("uname -r", "kernel version")
    
    # Python version
    sys_info['python_version'] = sys.version.replace('\n', ' ')
    
    # Uptime
    sys_info['uptime'] = safe_get_command_output("uptime", "system uptime")
    
    # Load average
    try:
        load_avg = os.getloadavg()
        sys_info['load_average'] = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
    except:
        pass
    
    # Disk space
    disk_usage = safe_get_command_output("df -h / | tail -1", "root disk usage")
    if disk_usage != "Not available":
        sys_info['root_disk_usage'] = disk_usage.strip()
    
    return sys_info

def get_software_versions():
    """Get versions of relevant software packages."""
    print("  - Software versions...")
    software = {}
    
    # Python packages relevant to scientific computing
    packages_to_check = ['numpy', 'scipy', 'devito', 'cupy', 'sympy', 'matplotlib', 'pandas']
    for package in packages_to_check:
        try:
            if package == 'cupy':
                import cupy
                software[f'{package}_version'] = cupy.__version__
                # Try to get CUDA version from CuPy
                try:
                    cuda_version = cupy.cuda.runtime.runtimeGetVersion()
                    major = cuda_version // 1000
                    minor = (cuda_version % 1000) // 10
                    software['cupy_cuda_version'] = f"CUDA {major}.{minor}"
                except:
                    pass
            else:
                module = __import__(package)
                software[f'{package}_version'] = getattr(module, '__version__', 'Unknown')
        except ImportError:
            software[f'{package}_version'] = 'Not installed'
        except Exception as e:
            software[f'{package}_version'] = f'Error: {e}'
    
    # Compiler versions
    software['gcc_version'] = safe_get_command_output("gcc --version | head -1", "GCC version")
    software['g++_version'] = safe_get_command_output("g++ --version | head -1", "G++ version")
    
    # NVIDIA HPC SDK if available
    software['nvc_version'] = safe_get_command_output("nvc --version | head -1", "NVIDIA nvc compiler version")
    
    # Additional build tools
    software['cmake_version'] = safe_get_command_output("cmake --version | head -1", "CMake version")
    software['make_version'] = safe_get_command_output("make --version | head -1", "Make version")
    
    software['python_executable'] = sys.executable
    
    return software

def format_system_info_markdown(cpu_info, mem_info, gpu_info, sys_info, software):
    """Format all system information as markdown."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_content = f"""

---

## System Configuration

**Generated:** {timestamp}

### CPU Information
"""
    
    # CPU details
    if 'model_name' in cpu_info:
        md_content += f"- **Processor:** {cpu_info['model_name']}\n"
    if 'architecture' in cpu_info:
        md_content += f"- **Architecture:** {cpu_info['architecture']}\n"
    if 'sockets' in cpu_info:
        md_content += f"- **Sockets:** {cpu_info['sockets']}\n"
    if 'cores_per_socket' in cpu_info:
        md_content += f"- **Cores per Socket:** {cpu_info['cores_per_socket']}\n"
    if 'threads_per_core' in cpu_info:
        md_content += f"- **Threads per Core:** {cpu_info['threads_per_core']}\n"
    if 'logical_cpus' in cpu_info:
        md_content += f"- **Logical CPUs:** {cpu_info['logical_cpus']}\n"
    if 'max_mhz' in cpu_info:
        md_content += f"- **Max Frequency:** {cpu_info['max_mhz']} MHz\n"
    if 'current_mhz' in cpu_info:
        md_content += f"- **Current Frequency:** {cpu_info['current_mhz']} MHz\n"
    if 'numa_nodes' in cpu_info:
        md_content += f"- **NUMA Nodes:** {cpu_info['numa_nodes']}\n"
    if 'cpu_features' in cpu_info:
        md_content += f"- **Key Features:** {cpu_info['cpu_features']}\n"
    
    # Cache info
    cache_info = []
    for cache in ['l1d_cache', 'l1i_cache', 'l2_cache', 'l3_cache']:
        if cache in cpu_info:
            cache_name = cache.replace('_cache', '').upper()
            cache_info.append(f"{cache_name}: {cpu_info[cache]}")
    if cache_info:
        md_content += f"- **Cache:** {', '.join(cache_info)}\n"
    
    # Memory information
    md_content += "\n### Memory Information\n"
    if 'total_ram_gb' in mem_info:
        md_content += f"- **Total RAM:** {mem_info['total_ram_gb']} GB\n"
    if 'available_ram_gb' in mem_info:
        md_content += f"- **Available RAM:** {mem_info['available_ram_gb']} GB\n"
    if 'swap_gb' in mem_info:
        md_content += f"- **Swap:** {mem_info['swap_gb']} GB\n"
    if 'memory_type' in mem_info:
        md_content += f"- **Memory Type:** {mem_info['memory_type']}\n"
    if 'memory_speed' in mem_info:
        md_content += f"- **Memory Speed:** {mem_info['memory_speed']}\n"
    if 'memory_modules' in mem_info:
        md_content += f"- **Memory Modules:** {mem_info['memory_modules']}\n"
    
    # GPU information
    md_content += "\n### GPU Information\n"
    if 'nvidia_gpus' in gpu_info and gpu_info['nvidia_gpus']:
        for i, gpu in enumerate(gpu_info['nvidia_gpus']):
            md_content += f"- **GPU {i+1}:** {gpu['name']}\n"
            md_content += f"  - **Memory:** {gpu['memory_mb']} MB\n"
            md_content += f"  - **Compute Capability:** {gpu['compute_capability']}\n"
            md_content += f"  - **Driver Version:** {gpu['driver_version']}\n"
            if 'pci_bus_id' in gpu:
                md_content += f"  - **PCI Bus ID:** {gpu['pci_bus_id']}\n"
            if 'max_power_w' in gpu:
                md_content += f"  - **Max Power:** {gpu['max_power_w']} W\n"
            if 'max_graphics_clock_mhz' in gpu:
                md_content += f"  - **Max Graphics Clock:** {gpu['max_graphics_clock_mhz']} MHz\n"
            if 'max_memory_clock_mhz' in gpu:
                md_content += f"  - **Max Memory Clock:** {gpu['max_memory_clock_mhz']} MHz\n"
    
    if 'cuda_version' in gpu_info:
        md_content += f"- **CUDA Version:** {gpu_info['cuda_version']}\n"
    elif 'cuda_runtime_version' in gpu_info:
        md_content += f"- **CUDA Runtime:** {gpu_info['cuda_runtime_version']}\n"
    
    if 'all_gpus_lspci' in gpu_info:
        md_content += f"- **All Display Devices:** {gpu_info['all_gpus_lspci']}\n"
    
    # System information
    md_content += "\n### System Information\n"
    if 'distribution' in sys_info:
        md_content += f"- **OS:** {sys_info['distribution']}\n"
    else:
        md_content += f"- **OS:** {sys_info['os']} {sys_info['os_release']}\n"
    
    if 'kernel' in sys_info and sys_info['kernel'] != "Not available":
        md_content += f"- **Kernel:** {sys_info['kernel']}\n"
    if 'hostname' in sys_info:
        md_content += f"- **Hostname:** {sys_info['hostname']}\n"
    if 'uptime' in sys_info and sys_info['uptime'] != "Not available":
        md_content += f"- **Uptime:** {sys_info['uptime']}\n"
    if 'root_disk_usage' in sys_info:
        md_content += f"- **Root Disk Usage:** {sys_info['root_disk_usage']}\n"
    
    # Software versions
    md_content += "\n### Software Versions\n"
    md_content += f"- **Python:** {platform.python_version()}\n"
    
    # Group by categories
    scientific_packages = ['numpy', 'scipy', 'devito', 'cupy', 'sympy', 'matplotlib', 'pandas']
    compilers = ['gcc', 'g++', 'nvc']
    build_tools = ['cmake', 'make']
    
    for category, packages in [("Scientific Libraries", scientific_packages), 
                              ("Compilers", compilers), 
                              ("Build Tools", build_tools)]:
        category_items = []
        for package in packages:
            key = f'{package}_version'
            if key in software and software[key] not in ['Not installed', 'Unknown', 'Not available']:
                value = software[key]
                if 'Error:' not in value:
                    category_items.append(f"**{package.upper()}:** {value}")
        
        if category_items:
            md_content += f"\n#### {category}\n"
            for item in category_items:
                md_content += f"- {item}\n"
    
    # Special handling for CuPy CUDA version
    if 'cupy_cuda_version' in software:
        md_content += f"- **CuPy CUDA Runtime:** {software['cupy_cuda_version']}\n"
    
    return md_content

def main():
    """Main function to collect system info and write to file."""
    parser = argparse.ArgumentParser(description='Collect comprehensive system information')
    parser.add_argument('-o', '--output', default='system_info.md', 
                       help='Output file (default: system_info.md)')
    parser.add_argument('-a', '--append', action='store_true',
                       help='Append to existing file instead of overwriting')
    args = parser.parse_args()
    
    print("System Information Collection")
    print("=" * 50)
    print("Gathering comprehensive system information...")
    
    # Collect system information
    print("Collecting information:")
    cpu_info = get_cpu_info()
    mem_info = get_memory_info()
    gpu_info = get_gpu_info()
    sys_info = get_system_info()
    software = get_software_versions()
    
    # Format as markdown
    print("\nFormatting results...")
    system_info_md = format_system_info_markdown(cpu_info, mem_info, gpu_info, sys_info, software)
    
    # Write to file
    mode = 'a' if args.append else 'w'
    try:
        with open(args.output, mode) as f:
            if args.append:
                f.write(system_info_md)
            else:
                f.write("# System Information\n")
                f.write(system_info_md)
        
        action = "appended to" if args.append else "written to"
        print(f"\nSystem information has been {action} '{args.output}'")
        print("=" * 50)
        print("Complete!")
        
    except Exception as e:
        print(f"Error writing to {args.output}: {e}")
        print("\nSystem information:")
        print(system_info_md)

if __name__ == '__main__':
    main() 