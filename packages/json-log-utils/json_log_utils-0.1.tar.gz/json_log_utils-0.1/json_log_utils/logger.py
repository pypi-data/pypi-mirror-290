import os
import json
import uuid
from datetime import datetime


class Logger:
    def __init__(self, log_dir="logs", pipeline_id=None):
        self.log_dir = log_dir
        self.pipeline_id = pipeline_id if pipeline_id else str(uuid.uuid4())
        self.session_id = str(uuid.uuid4())
        self.session_dir = os.path.join(log_dir, self.pipeline_id, self.session_id)
        os.makedirs(self.session_dir, exist_ok=True)

    def log(self, data: dict):
        """Log any kind of data as a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"log_{timestamp}.json"
        log_path = os.path.join(self.session_dir, log_filename)
        
        # Save the data as a JSON file
        with open(log_path, "w") as f:
            json.dump(data, f, indent=4)


# logger = Logger(pipeline_id="pipeline_1234")

