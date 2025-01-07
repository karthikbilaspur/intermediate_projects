import json
import os
import shutil
import threading
from datetime import datetime
from logger import Logger
from notification import notify
from utils import compress, encrypt, retain_backups

def load_config(file_path):
    """Load configuration from JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def create_backup(src, dst):
    """Create backup by copying files from source to destination."""
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"Backup created successfully: {dst}")
    except Exception as e:
        print(f"Error creating backup: {e}")

def compress_backup(src, dst):
    """Compress backup using zip."""
    try:
        compress(src, dst)
        print(f"Backup compressed successfully: {dst}")
    except Exception as e:
        print(f"Error compressing backup: {e}")

def encrypt_backup(src, dst, password):
    """Encrypt backup using AES."""
    try:
        encrypt(src, dst, password)
        print(f"Backup encrypted successfully: {dst}")
    except Exception as e:
        print(f"Error encrypting backup: {e}")

def main():
    config_file = 'config.json'
    config = load_config(config_file)

    backup_dir = config['backup_dir']
    sources = config['sources']
    compress_backups = config['compress']
    encrypt_backups = config['encrypt']
    retention_policy = config['retention']
    notification = config['notification']

    logger = Logger('backup.log')

    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    threads = []

    for source in sources:
        src_path = source['src']
        dst_path = os.path.join(backup_dir, source['name'] + "_" + timestamp)

        thread = threading.Thread(target=create_backup, args=(src_path, dst_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if compress_backups:
        for source in sources:
            src_path = os.path.join(backup_dir, source['name'] + "_" + timestamp)
            dst_path = src_path + ".zip"

            thread = threading.Thread(target=compress_backup, args=(src_path, dst_path))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    if encrypt_backups:
        password = input("Enter encryption password: ")
        for source in sources:
            src_path = os.path.join(backup_dir, source['name'] + "_" + timestamp + ".zip")
            dst_path = src_path + ".enc"

            thread = threading.Thread(target=encrypt_backup, args=(src_path, dst_path, password))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    retain_backups(backup_dir, retention_policy)

    if notification:
        notify("Backup completed successfully.")

    logger.log("Backup completed successfully.")

if __name__ == "__main__":
    main()