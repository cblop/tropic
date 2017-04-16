from abc import ABCMeta


class InstalTracer(metaclass=ABCMeta):
    """
        InstalTracer
        See __init__.py for more details.
    """

    def __init__(self, trace: list, output_file_name: str, zeroth_term: bool=False):
        self.trace = trace
        self.zeroth_term = zeroth_term
        self.output_file_name = output_file_name
        self.check_trace()

    def check_trace(self):
        pass

    def trace_to_file(self) -> None:
        raise NotImplementedError
