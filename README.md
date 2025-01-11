# NFS Drive Manager

A simple GUI application for Windows to manage NFS drives. Features include:
- Mount NFS drives
- Unmount drives
- View drive properties
- Real-time status monitoring

## Requirements
- Python 3.x
- Windows with NFS Client feature enabled

## Setup

1. Install required Python packages:
```bash
pip install -r requirements.txt
```

2. Enable Windows NFS Client feature:
   - Open "Control Panel"
   - Go to "Programs and Features"
   - Click "Turn Windows features on or off"
   - Check "Services for NFS" and its sub-components
   - Click OK and restart if prompted

## Usage

1. Run the application:
```bash
python nfs_manager.py
```

2. To mount an NFS drive:
   - Enter the server address (e.g., 192.168.1.100)
   - Enter the share path (e.g., /exports/share1)
   - Select a drive letter
   - Click "Mount"

3. To unmount a drive:
   - Select the drive from the list
   - Click "Unmount Selected"

4. View properties by selecting a drive from the list 