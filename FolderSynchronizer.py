from filecmp import cmp
import logging
from os import walk
import shutil
from time import sleep
from pathlib import Path


def ensure_folder_exists(folder):
    """
    Ensure that a folder exists. If it doesn't, create it.
    :param folder: Path to the folder that should exist.
    """
    if not folder.exists():
        folder.mkdir()
        logging.info(f'Created folder {folder}.')


def sync_single_file(source_file, replica_file):
    """
    Ensure that the replica file is the same as the source file.
    :param source_file: Path to the source file.
    :param replica_file: Path to the file in the replica.
    """
    # if replica does not exist at all, copy it from source
    if not replica_file.exists():
        shutil.copyfile(source_file, replica_file)
        logging.info(f'Copied file from {source_file} to {replica_file}.')

    # if replica exists but has different content than source, remove it first, then copy
    elif not cmp(source_file, replica_file):
        replica_file.unlink()
        logging.info(f'Removed file {replica_file}.')
        shutil.copyfile(source_file, replica_file)
        logging.info(f'Copied file from {source_file} to {replica_file}.')


def change_folder_in_path(full_path, old_path, new_path):
    """
    Modify a file/folder path to change the root folder.
    :param full_path: The original full path.
    :param old_path: The original part of the path to be replaced.
    :param new_path: The new part of the path to replace the old_path.
    :return: The modified path with the changed folder.
    """
    relative_path = Path(full_path).relative_to(old_path)
    return new_path / relative_path


def ensure_folder_does_not_exist(replica_folder, source_folder):
    """
    Ensure that a folder doesn't exist in replica if it doesn't exist in source. If it does, remove it.
    :param source_folder: Folder path in source.
    :param replica_folder: Folder path in replica.
    """
    if not source_folder.exists():
        replica_folder.rmdir()
        logging.info(f'Removed folder {replica_folder}.')


def ensure_file_does_not_exist(replica_file, source_file):
    """
    Ensure that a file doesn't exist in replica if it doesn't exist in source. If it does, remove it.
    :param source_file: File path in source.
    :param replica_file: File path in replica.
    """
    if not source_file.exists():
        replica_file.unlink()
        logging.info(f'Removed file {replica_file}.')


class FolderSynchronizer:
    def __init__(self, source, replica, interval_seconds, log_file):
        """
        Initialize the FolderSynchronizer with source and replica paths, synchronization interval, and log file.
        :param source: Path to the source folder.
        :param replica: Path to the replica folder.
        :param interval_seconds: Time interval (in seconds) between synchronizations.
        :param log_file: Path to the log file.
        """
        self.source = source
        self.replica = replica
        self.interval_seconds = interval_seconds
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """
        Set up log format, log file name and logging to console.
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler(self.log_file),
                                logging.StreamHandler()
                            ])

    def sync(self):
        """
        Synchronize the replica folder to be identical to the source folder.
        """
        while True:
            self.copy_from_source_to_replica()
            self.remove_replica_if_not_in_source()
            logging.info(f'Synchronization finished. Repeating again in {self.interval_seconds} seconds.')
            sleep(self.interval_seconds)

    def copy_from_source_to_replica(self):
        """
        Synchronize all folders and files that are in the source and not in the replica to the replica.
        """
        for root, dirs, files in walk(self.source):
            # Filepath in replica folder equivalent to the current source folder.
            replica_root = change_folder_in_path(root, self.source, self.replica)

            for f in files:
                # Paths to the current file in source and replica folders.
                source_file = Path(root) / f
                replica_file = Path(replica_root) / f

                sync_single_file(source_file, replica_file)

            for d in dirs:
                # Path to the current folder in the replica folder.
                replica_folder = Path(replica_root) / d

                ensure_folder_exists(replica_folder)

    def remove_replica_if_not_in_source(self):
        """
        Remove all folders and files from the replica which are not in the source. Walks the folder bottom-up.
        """
        for root, dirs, files in walk(self.replica, topdown=False):
            # Filepath in the source folder equivalent to the current replica folder.
            source_root = change_folder_in_path(root, self.replica, self.source)

            for f in files:
                # Paths to the current file in source and replica folders.
                source_file = Path(source_root) / f
                replica_file = Path(root) / f

                ensure_file_does_not_exist(replica_file, source_file)

            for d in dirs:
                # Paths to the current folder in the source and replica folders.
                source_folder = Path(source_root) / d
                replica_folder = Path(root) / d

                ensure_folder_does_not_exist(replica_folder, source_folder)
