#!/usr/bin/env python3
"""
Environment Validation Script for Isaac Sim 4.5 + ROS2 Docker Setup

This script validates that all components are properly installed and configured:
- Docker environment
- NVIDIA GPU support
- ROS2 installation
- Isaac Sim functionality
- X11 display (if GUI enabled)

Usage:
    # Inside the Docker container
    python3 setup/validate_environment.py
    
    # Or with Isaac Sim Python
    omni_python setup/validate_environment.py
"""

import os
import sys
import subprocess
import importlib
from typing import List, Tuple, Optional

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text: str) -> None:
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

def print_test(test_name: str, status: bool, message: str = "") -> None:
    """Print test result with colored status"""
    status_symbol = f"{Colors.GREEN}✅{Colors.END}" if status else f"{Colors.RED}❌{Colors.END}"
    status_text = f"{Colors.GREEN}PASS{Colors.END}" if status else f"{Colors.RED}FAIL{Colors.END}"
    
    print(f"{status_symbol} {Colors.BOLD}{test_name}{Colors.END}: {status_text}")
    if message:
        print(f"   {Colors.CYAN}ℹ️  {message}{Colors.END}")

def run_command(command: str, capture_output: bool = True) -> Tuple[bool, str, str]:
    """Run a shell command and return success status and output"""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=capture_output,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_docker_environment() -> List[Tuple[str, bool, str]]:
    """Check Docker environment"""
    tests = []
    
    # Check if running in Docker
    in_docker = os.path.exists('/.dockerenv')
    tests.append(("Running in Docker container", in_docker, 
                 "Container detected" if in_docker else "Not running in Docker"))
    
    # Check Docker environment variables
    required_env_vars = [
        ("ACCEPT_EULA", "Y"),
        ("PRIVACY_CONSENT", "Y"),
        ("ROS_DISTRO", "humble")
    ]
    
    for env_var, expected in required_env_vars:
        value = os.environ.get(env_var)
        is_correct = value == expected
        tests.append((f"Environment variable {env_var}", is_correct,
                     f"Expected: {expected}, Got: {value}"))
    
    return tests

def check_nvidia_gpu() -> List[Tuple[str, bool, str]]:
    """Check NVIDIA GPU support"""
    tests = []
    
    # Check nvidia-smi
    success, stdout, stderr = run_command("nvidia-smi")
    tests.append(("NVIDIA SMI accessible", success,
                 "GPU detected" if success else f"Error: {stderr}"))
    
    if success:
        # Parse GPU information
        lines = stdout.split('\n')
        gpu_info = [line for line in lines if 'GeForce' in line or 'RTX' in line or 'GTX' in line or 'Tesla' in line or 'Quadro' in line]
        if gpu_info:
            tests.append(("GPU information", True, gpu_info[0].strip()))
        
        # Check CUDA version
        cuda_lines = [line for line in lines if 'CUDA Version:' in line]
        if cuda_lines:
            cuda_version = cuda_lines[0].split('CUDA Version:')[1].strip().split()[0]
            tests.append(("CUDA version", True, f"CUDA {cuda_version}"))
    
    # Check /dev/nvidia* devices
    nvidia_devices = [f for f in os.listdir('/dev') if f.startswith('nvidia')]
    tests.append(("NVIDIA devices available", len(nvidia_devices) > 0,
                 f"Found devices: {nvidia_devices}" if nvidia_devices else "No NVIDIA devices found"))
    
    return tests

def check_ros2_installation() -> List[Tuple[str, bool, str]]:
    """Check ROS2 installation"""
    tests = []
    
    # Check ROS2 executable
    success, stdout, stderr = run_command("ros2")
    tests.append(("ROS2 command available", success,
                 stdout.strip() if success else f"Error: {stderr}"))
    
    # Check ROS2 environment
    ros_distro = os.environ.get('ROS_DISTRO')
    tests.append(("ROS_DISTRO environment", ros_distro == 'humble',
                 f"ROS_DISTRO={ros_distro}"))
    
    # Check if ROS2 is sourced
    success, stdout, stderr = run_command("ros2 pkg list")
    package_count = len(stdout.split('\n')) if success else 0
    tests.append(("ROS2 packages available", package_count > 10,
                 f"Found {package_count} packages" if success else f"Error: {stderr}"))
    
    # Check specific ROS2 packages
    required_packages = ['image_transport', 'compressed_image_transport']
    for package in required_packages:
        success, stdout, stderr = run_command(f"ros2 pkg prefix {package}")
        tests.append((f"ROS2 package {package}", success,
                     "Package found" if success else f"Package missing: {stderr}"))
    
    return tests

def check_python_environment() -> List[Tuple[str, bool, str]]:
    """Check Python environment and Isaac Sim"""
    tests = []
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    tests.append(("Python version", True, f"Python {python_version}"))
    
    # Check Isaac Sim Python imports
    isaac_modules = [
        'omni.isaac.kit',
        'omni.kit.app'
    ]
    
    
    # Check Isaac Sim Python imports after simulation app initialization
    isaac_modules_after_init = [
        'omni.isaac.core',
        'pxr'
    ]
    
    for module in isaac_modules:
        try:
            importlib.import_module(module)
            tests.append((f"Import {module}", True, "Module available"))
        except ImportError as e:
            tests.append((f"Import {module}", False, f"Import failed: {e}"))
    
    try:
        from omni.isaac.kit import SimulationApp
        # Launch Isaac Sim in headless or GUI mode
        config = {"headless": False}
        simulation_app = SimulationApp(config)
        for module in isaac_modules_after_init:
            try:
                importlib.import_module(module)
                tests.append((f"Import {module}", True, "Module available"))
            except ImportError as e:
                tests.append((f"Import {module}", False, f"Import failed: {e}"))
        simulation_app.close()
    except ImportError as e:
        for module in isaac_modules_after_init:
            tests.append((f"Import {module}", False, f"Import failed: omni.isaac.kit not available ({e})"))
    
    # Check essential Python packages
    essential_packages = ['numpy', 'matplotlib']
    for package in essential_packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'unknown')
            tests.append((f"Python package {package}", True, f"Version {version}"))
        except ImportError:
            tests.append((f"Python package {package}", False, "Package not found"))
    
    
    return tests

def check_display_system() -> List[Tuple[str, bool, str]]:
    """Check X11 display system"""
    tests = []
    
    # Check DISPLAY environment variable
    display = os.environ.get('DISPLAY')
    tests.append(("DISPLAY environment variable", display is not None,
                 f"DISPLAY={display}" if display else "DISPLAY not set"))
    
    return tests

def check_file_system() -> List[Tuple[str, bool, str]]:
    """Check file system and mount points"""
    tests = []
    
    # Check key directories
    key_dirs = [
        ('/isaac-sim', 'Isaac Sim installation'),
        ('/opt/ros/humble', 'ROS2 Humble installation'),
        ('/root/workspace/main', 'Workspace mount'),
        ('/root/assets', 'Assets mount')
    ]
    
    for path, description in key_dirs:
        exists = os.path.exists(path)
        tests.append((f"Directory {path}", exists,
                     f"{description} {'found' if exists else 'missing'}"))
        
        if exists and os.path.isdir(path):
            try:
                contents = len(os.listdir(path))
                tests.append((f"Contents of {path}", contents > 0,
                             f"{contents} items found" if contents > 0 else "Directory empty"))
            except PermissionError:
                tests.append((f"Contents of {path}", False, "Permission denied"))
    
    # Check Isaac Sim Python executable
    isaac_python = '/isaac-sim/python.sh'
    if os.path.exists(isaac_python):
        tests.append(("Isaac Sim Python executable", True, "python.sh found"))
        # Test execution
        success, stdout, stderr = run_command(f"{isaac_python} --version")
        tests.append(("Isaac Sim Python execution", success,
                     stdout.strip() if success else f"Execution failed: {stderr}"))
    else:
        tests.append(("Isaac Sim Python executable", False, "python.sh not found"))

    return tests

def run_isaac_sim_test() -> List[Tuple[str, bool, str]]:
    """Run a simple Isaac Sim test (headless)"""
    tests = []
    
    try:
        # Only import Isaac Sim if omni modules are available
        import omni.isaac.kit
        from omni.isaac.kit import SimulationApp
        
        # Test headless mode
        config = {"headless": True, "renderer": "RayTracedLighting"}
        app = SimulationApp(config)
        
        tests.append(("Isaac Sim headless startup", True, "Application started successfully"))
        
        try:
            from omni.isaac.core import World
            world = World(stage_units_in_meters=1.0)
            tests.append(("Isaac Sim World creation", True, "World created successfully"))
            
            # Test basic simulation step
            world.reset()
            world.step(render=False)
            tests.append(("Isaac Sim simulation step", True, "Simulation step completed"))
            
        except Exception as e:
            tests.append(("Isaac Sim World creation", False, f"World creation failed: {e}"))
        
        app.close()
        tests.append(("Isaac Sim shutdown", True, "Application closed successfully"))
        
    except ImportError as e:
        tests.append(("Isaac Sim import", False, f"Cannot import Isaac Sim: {e}"))
    except Exception as e:
        tests.append(("Isaac Sim test", False, f"Test failed: {e}"))
    
    return tests

def generate_summary(all_tests: List[List[Tuple[str, bool, str]]]) -> None:
    """Generate and print test summary"""
    total_tests = sum(len(test_group) for test_group in all_tests)
    passed_tests = sum(sum(1 for _, status, _ in test_group if status) for test_group in all_tests)
    failed_tests = total_tests - passed_tests
    
    print_header("VALIDATION SUMMARY")
    
    print(f"{Colors.BOLD}Total Tests:{Colors.END} {total_tests}")
    print(f"{Colors.GREEN}✅ Passed:{Colors.END} {passed_tests}")
    print(f"{Colors.RED}❌ Failed:{Colors.END} {failed_tests}")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    if success_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! Environment is ready for Isaac Sim + ROS2.{Colors.END}")
    elif success_rate >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Most tests passed ({success_rate:.1f}%). Check failed tests above.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Many tests failed ({success_rate:.1f}%). Environment needs attention.{Colors.END}")
    
    print(f"\n{Colors.CYAN}For troubleshooting, refer to the README.md file.{Colors.END}")

def main():
    """Main validation function"""
    print_header("ISAAC SIM 4.5 + ROS2 ENVIRONMENT VALIDATION")
    print(f"{Colors.CYAN}Validating Docker container environment for Isaac Sim and ROS2...{Colors.END}\n")
    
    # Run all test categories
    test_categories = [
        ("Docker Environment", check_docker_environment),
        ("NVIDIA GPU Support", check_nvidia_gpu),
        ("ROS2 Installation", check_ros2_installation),
        ("Python Environment", check_python_environment),
        ("Display System", check_display_system),
        ("File System", check_file_system),
        ("Isaac Sim Functionality", run_isaac_sim_test)
    ]
    
    all_tests = []
    
    for category_name, test_function in test_categories:
        print_header(category_name)
        try:
            tests = test_function()
            all_tests.append(tests)
            
            for test_name, status, message in tests:
                print_test(test_name, status, message)
                
        except Exception as e:
            print_test(f"{category_name} (category)", False, f"Category test failed: {e}")
            all_tests.append([])
    
    # Generate summary
    generate_summary(all_tests)

if __name__ == "__main__":
    main()
