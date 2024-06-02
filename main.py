import argparse
from FolderSynchronizer import FolderSynchronizer


def get_arguments():
    """
    create argument parser that accepts command-line values
    :return: ArgumentParser with parsed arguments
    """
    parser = argparse.ArgumentParser(prog='Folder Synchronization')
    parser.add_argument('--source_folder', help='Path of the source folder', type=str)
    parser.add_argument('--replica_folder', help='Path of the replica folder', type=str)
    parser.add_argument('--interval_seconds', help='Interval of synchronization (in seconds)', type=int)
    parser.add_argument('--log_file', help='Path to the log file', type=str)

    return parser.parse_args()


def main():
    """ Main program """
    args = get_arguments()
    synchronizer = FolderSynchronizer(args.source_folder, args.replica_folder, args.interval_seconds, args.log_file)
    return 0


if __name__ == "__main__":
    main()
