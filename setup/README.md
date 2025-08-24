# Isaac Sim 4.5 + ROS2 Docker Setup

A comprehensive Docker-based setup for NVIDIA Isaac Sim 4.5 with ROS2 Humble integration, with GPU acceleration and GUI support.

## 🚀 Features

- **Isaac Sim 4.5**: Latest NVIDIA Isaac Sim with Omniverse integration
- **ROS2 Humble**: Full ROS2 ecosystem with image transport plugins
- **GPU Acceleration**: NVIDIA GPU support with proper drivers
- **GUI Support**: X11 forwarding for graphical applications
- **Persistent Storage**: Optimized caching and data persistence
- **Cross-Platform**: Works on Linux systems with NVIDIA GPUs

## 📋 Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 22.04 recommended)
- **GPU**: GeForce RTX 3070 or higher
- **RAM**: Minimum 32GB+ recommended
- **Storage**: At least 50GB free space

### Software Dependencies

1. **Docker Engine**
2. **NVIDIA Container Toolkit**
3. **X11 Server** (for GUI)
4. **NVIDIA Drivers** (version 535.129.03+)

## 🛠️ Installation Guide

### Step 4: Clone and Setup Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd isaac-sim-mini-projects

# Make scripts executable
chmod +x scripts/*.sh
```


## [QuickStart Section](QUICKSTART.md)


## 🖥️ Container Features

### Environment Variables

The container sets up the following environment variables automatically:

```bash
export ROS_DISTRO=humble
export ROS_LOCALHOST_ONLY=1
export SIM_ASSETS=/root/assets
export SIM_REPO_ROOT=/root/workspace/main
```

### Available Tools

- **omni_python**: Isaac Sim Python interpreter (`omni_python script.py`)
- **ROS2 CLI**: Full ROS2 command-line interface
- **Development tools**: vim, git, cmake, build-essential

### Persistent Storage

The container mounts several directories for persistence:

- **Isaac Sim cache**: `~/docker/isaac-sim/cache/`
- **Assets**: `$SIM_ASSETS` → `/root/assets`
- **Workspace**: Current directory → `/root/workspace/main`

## 🔧 Usage Examples

### Running with ROS2

```bash
# Terminal 1: Start Isaac Sim with ROS2 bridge
omni_python <ROS2 Example at /isaac-sim/standalone_examples/api>

# Terminal 2: Check ROS2 topics inside container
ros2 topic list
```

### Running GUI Applications

```bash
# Start Isaac Sim GUI
./isaac-sim/runapp.sh
```

## 🐛 Troubleshooting

### GPU Issues

**Problem**: `nvidia-smi` not working in container
```bash
# Check NVIDIA drivers on host
nvidia-smi

# Verify Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi
```

**Problem**: GPU not detected in Isaac Sim
```bash
# Check if container has GPU access
nvidia-smi
lspci | grep -i nvidia
```

### Display Issues

**Problem**: Cannot open display
```bash
# On host, allow X11 forwarding
xhost +local:docker

# Check DISPLAY variable
echo $DISPLAY
```

### Container Startup Issues

**Problem**: Container fails to start
```bash
# Check Docker logs
docker logs isaac-sim-mini-projects

# Remove existing container
docker rm -f isaac-sim-mini-projects
```



