import PyInstaller.__main__
import os
import sys

def build():
    # Get version from command line or use default
    version = sys.argv[1] if len(sys.argv) > 1 else "0.0.1"
    
    # Create version info file with proper format
    version_info = f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({",".join(version.split(".") + ["0"]*(4-len(version.split("."))))}),
    prodvers=({",".join(version.split(".") + ["0"]*(4-len(version.split("."))))}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        "040904B0",
        [StringStruct("CompanyName", "NFS Manager"),
        StringStruct("FileDescription", "NFS Drive Manager for Windows"),
        StringStruct("FileVersion", "{version}"),
        StringStruct("InternalName", "nfs_manager"),
        StringStruct("LegalCopyright", ""),
        StringStruct("OriginalFilename", "NFS-Manager.exe"),
        StringStruct("ProductName", "NFS Manager"),
        StringStruct("ProductVersion", "{version}")])
    ]),
    VarFileInfo([VarStruct("Translation", [1033, 1200])])
  ]
)
'''
    
    with open("file_version_info.txt", "w") as f:
        f.write(version_info)
    
    # PyInstaller options
    opts = [
        "nfs_manager.py",  # Your main script
        "--name=NFS-Manager",  # Name of the executable
        "--onefile",  # Create a single executable
        "--noconsole",  # Don't show console window
        "--version-file=file_version_info.txt",  # Version info
        "--icon=icon/icon.ico",  # Add icon if exists
        "--clean",  # Clean cache
    ]
    
    # Remove empty options
    opts = [x for x in opts if x]
    
    # Run PyInstaller
    PyInstaller.__main__.run(opts)
    
    # Clean up version file
    if os.path.exists("file_version_info.txt"):
        os.remove("file_version_info.txt")

if __name__ == "__main__":
    build() 