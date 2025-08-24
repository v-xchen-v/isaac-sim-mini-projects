# 🚀 Quick Start Guide

This guide will get you up and running with Isaac Sim 4.5 + ROS2 in under 1 hour.

## Prerequisites Check

Before starting, ensure you have:

- ✅ Linux system (Ubuntu 22.04 recommended)
- ✅ NVIDIA GPU with drivers version 535.129.03+
- ✅ At least 32GB RAM and 50GB free disk space
- ✅ Stable internet connection (for downloading ~15GB image)
- ✅ GPU: GeForce RTX 3070 or higher
- ✅ **Docker**
- ✅ **NVIDIA Container Toolkit**: Required for GPU support

## Step-by-Step Setup

### 1. Clone and Setup Repository

```bash
# Clone repository
git clone https://github.com/your-username/isaac-sim-mini-projects.git
cd isaac-sim-mini-projects

# Fix permissions and make scripts executable
./scripts/fix_permissions.sh
```

### 2. Build Isaac Sim Container

```bash
# Build container (this will take ~30 minutes)
./scripts/build.sh
```

### 3. Start Isaac Sim

```bash
# Create assets directory or a existing assets directory
mkdir -p ~/isaac_sim_assets

# Start container with GUI support
SIM_ASSETS=~/isaac_sim_assets ./scripts/start_gui.sh

# In another terminal, enter the container
./scripts/into.sh
```

### 4. Validate Setup

```bash
# Inside the container, run validation
python3 setup/validate_environment.py

# Test Isaac Sim
omni_python setup/test_sim_gui_setup.py
```

## What You Should See

### Successful Container Start
```
✅ Container isaac-sim-mini-projects started successfully
✅ GPU access: NVIDIA GeForce RTX 4090 or A6000
✅ ROS2 Humble ready
✅ Isaac Sim 4.5.0 loaded
```

### Validation Results
```
🎉 ALL TESTS PASSED! Environment is ready for Isaac Sim + ROS2.
✅ Passed: all
❌ Failed: 0
```

### Isaac Sim Test
An Isaac Sim window popped up showing a cube falling onto the ground.
```
✅ Isaac Sim world initialized, stepping simulation...
Step 0: cube at [0.       0.       0.991825]
Step 30: cube at [-1.4153240e-07  6.6009349e-08  5.0000157e-02]
Step 60: cube at [-4.493792e-08  7.887256e-09  5.000016e-02]
Step 90: cube at [-4.4663217e-08  7.1089863e-09  5.0000161e-02]
✅ Simulation ran successfully.
```

## Common Commands

### Container Management
```bash
# Start container
SIM_ASSETS=~/isaac_sim_assets ./scripts/start_gui.sh

# Enter running container
./scripts/into.sh

# Stop container
docker stop isaac-sim-mini-projects

# Restart container
docker restart isaac-sim-mini-projects

# View logs
docker logs isaac-sim-mini-projects
```

### Isaac Sim Usage
```bash
# Inside container

# Start Isaac Sim GUI
cd /isaac-sim
./runapp.sh

# Start Isaac Sim Headless
cd /isaac-sim
./runheadless.sh
```

### ROS2 Commands
```bash
# Inside container

# List ROS2 topics
ros2 topic list

# Echo a topic
ros2 topic echo /some_topic

# Run ROS2 node
ros2 run package_name node_name
```

## Next Steps

1. **Learn Isaac Sim**: Check out examples in `/isaac-sim/standalone_examples/`
2. **ROS2 Integration**: Explore ROS2 bridge examples in `/isaac-sim/standalone_examples/omni.isaac.ros2_bridge/`
3. **Custom Projects**: Create your own simulations in the `build_task_layout/` directory
4. **Documentation**: Read the [full README.md](README.md) for advanced configuration

## Getting Help

### Troubleshooting
- Check the [Troubleshooting section](README.md#troubleshooting) in README.md
- Run `python3 setup/validate_environment.py` to diagnose issues
- Check Docker logs: `docker logs isaac-sim-mini-projects`

### Common Issues

**GPU not detected:**
```bash
# Check host GPU
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi
```

**Permission denied:**
```bash
# Fix permissions
./scripts/fix_permissions.sh
```

**Display issues:**
```bash
# Allow X11 forwarding
xhost +local:docker
```

### Resources
- [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/)
- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Docker GPU Support](https://docs.docker.com/config/containers/resource_constraints/#gpu)

---

**🎉 Congratulations!** You now have a fully functional Isaac Sim 4.5 + ROS2 environment running in Docker with GPU acceleration and GUI support!
