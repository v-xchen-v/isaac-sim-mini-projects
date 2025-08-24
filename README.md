# isaac-sim-mini-projects
 A collection of small projects using NVIDIA Isaac Sim. Each mini project explores a specific feature or workflow in robotics simulation — scene setup, robot control, manipulation, or RL/IL integration. Designed as lightweight, reproducible examples for prototyping and learning Isaac Sim capabilities without full-scale robotics project overhead.

## 📁 Project Structure

```
isaac-sim-mini-projects/
├── README.md                    # This documentation
├── LICENSE                      # License file
├── scripts/                     # Docker and utility scripts
│   ├── dockerfile              # Main Dockerfile with Isaac Sim + ROS2
│   ├── entrypoint.sh           # Container initialization script
│   ├── build.sh                # Build Docker image
│   ├── start_gui.sh            # Start container with GUI support
│   ├── into.sh                 # Enter running container
│   └── fix_permissions.sh      # Fix file permissions
├── build_task_layout/          # Example tasks and projects
│   └── tasks/
│       └── task.py
└── setup/                      # Setup and configuration
    └── test_setup.py           # Environment validation
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check NVIDIA Isaac Sim documentation

## 🔗 Useful Links

- [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/)
- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Docker Documentation](https://docs.docker.com/)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)
