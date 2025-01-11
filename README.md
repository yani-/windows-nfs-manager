# Windows NFS Manager

A simple GUI application for managing NFS drives on Windows.

![NFS Manager](docs/application.png)

## Features
- 🔌 Easy mounting of NFS drives through a graphical interface
- ⚙️ Advanced mount settings configuration
- 📊 Real-time drive status and properties monitoring
- 🛡️ Safe unmounting of drives

## Quick Start

### Option 1: Download Executable
1. Download the [latest release](https://github.com/yani-/windows-nfs-manager/releases/latest)
2. Enable Windows NFS Client feature if not already enabled
3. Run the application

### Option 2: Build from Source
1. Clone the repository
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python nfs_manager.py
```

## Setup Windows NFS Client

1. Open "Control Panel"
2. Go to "Programs and Features"
3. Click "Turn Windows features on or off"
4. Check "Services for NFS" and its sub-components
5. Click OK and restart if prompted

## Usage

1. Enter the NFS server address (e.g., 192.168.1.100)
2. Enter the share path (e.g., /exports/share1)
3. Select a drive letter
4. (Optional) Configure mount settings via the ⚙️ button
5. Click "Mount"

## Mount Settings

- User/Group IDs: Match with NFS server permissions
- Transfer Sizes: Larger = better performance (if stable)
- Timeout: Lower = faster reconnect on issues
- File Access: 755 = standard read/write/execute
- Soft Mount: Recommended for better reliability

## More Information

Visit our [project page](https://yani-.github.io/windows-nfs-manager/) for detailed documentation and screenshots.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.