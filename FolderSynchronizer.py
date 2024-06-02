import logging


class FolderSynchronizer:
    def __init__(self, source, replica, interval_seconds, log_file):
        self.source = source
        self.replica = replica
        self.interval_seconds = interval_seconds
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """
        set up log format, log file name and logging to console
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler(self.log_file),
                                logging.StreamHandler()
                            ])
