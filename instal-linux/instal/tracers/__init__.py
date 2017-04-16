"""
instal_stable.tracers

New InstAL tracers should extend InstalTracer. Methods that need defining:
    def trace_to_file(self):
        Uses the trace as specified in self.trace, processes it in some way to a file (self.output_file_name)

Use instances of subclasses of InstalTracer as follows:
    instal_tracer = SubclassOfInstalTracer(trace, OUTPUT FILE)
    instal_tracer.trace_to_file()

    Where "trace" is a standard InstAL trace (list of JSON objects), where one timestep is defined by:

    { metadata : {
        // Metadata here.
    },
    state : {
        "observed" : [],
        "occurred" : [],
        "holdsat" : [],
    }
"""

