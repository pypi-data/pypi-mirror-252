class Logger:
    def __init__(self, distributedLogger):
        self.distributedLogger = distributedLogger

    def write_error(self, error_message):
        print(f"Error: {error_message}")

    def write_init(self, error_message):
        print(f"Error: {error_message}")

    def write_log(self, log_message):
        print(f"Log: {log_message}")