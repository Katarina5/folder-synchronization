class FolderSynchronizer:
    def __init__(self, source, replica, interval_seconds, log_file):
        self.source = source
        self.replica = replica
        self.interval_seconds = interval_seconds
        self.log_file = log_file
        print(self.source, self.replica, self.log_file, self.interval_seconds)
