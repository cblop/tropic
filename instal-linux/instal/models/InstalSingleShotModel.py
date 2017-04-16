
import time

from io import StringIO
import os

from .Sensor import Sensor
from .InstalModel import InstalModel


def dummy_callback(x, y):  # why is this a thing?
    return


class InstalSingleShotModel(InstalModel):
    """
        InstalSingleShotModel
        Deals with single shot solving - instance of InstalModel.
        Used for instalsolve
    """

    def __init__(self, instal_args):
        super(InstalSingleShotModel, self).__init__(instal_args)
        self.timestamp = time.time()
        self.previous_timestamp = 0
        self.sensor = Sensor(self.initial_facts,
                             self.model_files, self.domain_facts, instal_args)
        self.check_and_output_json()

    def solve(self, query_text):
        self.answersets.append([])
        queryIO = StringIO(query_text)
        self.answersets[0].append(self.get_json())
        for event in queryIO.readlines():
            self.solve_increment(event)
            self.answersets[0].append(self.get_json())

        self.check_and_output_json()

    def solve_increment(self, event):
        self.previous_timestamp = self.timestamp
        self.timestamp = time.time()
        self.sensor.solve(event)

    def get_json(self):
        state_json = self.sensor.get_state_json()
        metadata = self.generate_json_metadata()
        out_json = state_json
        out_json["metadata"] = metadata
        return out_json

    def generate_json_metadata(self):
        metadata = {
            "pid": os.getpid(),
            "source_files": self.instal_args.input_files + self.instal_args.domain_files,
            "timestamp": self.timestamp,
            "previous_timestamp": self.previous_timestamp,
            "mode": "single_shot",
            "answer_set_n": 1,
            "answer_set_of": 1,
        }

        return metadata
