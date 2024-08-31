import os
import hashlib

def md5_checksum(filename):
    """Compute MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def scan_folders_for_eboot(base_dir):
    """Scan folders for eboot.bin and return a dictionary of checksums and folder names."""
    checksums = {}
    for root, dirs, files in os.walk(base_dir):
        if 'eboot.bin' in files:
            eboot_path = os.path.join(root, 'eboot.bin')
            folder_name = os.path.basename(root)
            checksum = md5_checksum(eboot_path)
            checksums[folder_name] = checksum
    return checksums

def save_checksums_to_file(checksums, output_file):
    """Save the checksums and folder names to a file."""
    with open(output_file, 'w') as f:
        for folder_name, checksum in checksums.items():
            f.write(f"{folder_name}: {checksum}\n")

if __name__ == "__main__":
    base_directory = os.getcwd()  # Use the current working directory
    output_file = 'crc.txt'
    
    checksums = scan_folders_for_eboot(base_directory)
    save_checksums_to_file(checksums, output_file)
    
    print(f"Checksums have been saved to {output_file}")
