if __name__ == "__main__":
    raise NotImplementedError(
        "Try running ../instaltrace.py instead, this file is just an interface.")

from .instalargparse import buildtraceargparser

from .instaljsonhelpers import check_trace_integrity, trace_dicts_from_file

from .tracers.InstalTextTracer import InstalTextTracer
from .tracers.InstalGanttTracer import InstalGanttTracer
from .tracers.InstalPDFTracer import InstalPDFTracer
import os

def instal_pdf_trace(trace: list, pdf_file: str) -> None:
    instal_pdf_tracer = InstalPDFTracer(trace, pdf_file)
    instal_pdf_tracer.trace_to_file()


def instal_text(trace: list, text_file: str) -> None:
    instal_text_tracer = InstalTextTracer(trace, text_file)
    instal_text_tracer.trace_to_file()


def instal_gantt(trace: list, gantt_file: str) -> None:
    instal_gantt_tracer = InstalGanttTracer(trace, gantt_file)
    instal_gantt_tracer.trace_to_file()


def instal_trace_preprocess_with_args(args, unk) -> None:
    def get_new_filename(oldfilename, extension, tracetype):
        path, fil = os.path.split(oldfilename)
        newfilename, file_extension = os.path.splitext(fil)
        return "{}_{}{}".format(newfilename, tracetype, extension)

    if not args.json_file:
        raise Exception("No JSON file provided.")
    if not (args.trace_file or args.gantt_file or args.text_file):
        raise Exception("No output mode specified.")
    if os.path.isdir(args.json_file):
        is_dir = True
        traces = []
        for t in os.listdir(args.json_file):
            traces += [{"trace": trace_dicts_from_file(
                args.json_file + t), "filename": args.json_file + t}]
    else:
        is_dir = False
        traces = [{"trace": trace_dicts_from_file(
            args.json_file), "filename": args.json_file}]
    for trace in traces:
        if args.trace_file:
            if is_dir:
                filename = args.trace_file + "/" + \
                    get_new_filename(trace["filename"], ".tex", "trace")
            else:
                filename = args.trace_file
            instal_pdf_trace(trace["trace"], filename)

        if args.gantt_file:
            if is_dir:
                filename = args.gantt_file + "/" + \
                    get_new_filename(trace["filename"], ".tex", "gantt")
            else:
                filename = args.gantt_file
            instal_gantt(trace["trace"], filename)

        if args.text_file:
            if is_dir:
                filename = args.text_file + "/" + \
                    get_new_filename(trace["filename"], ".txt", "txt")
            else:
                filename = args.text_file
            instal_text(trace["trace"], filename)


def instal_trace_keyword(trace_file: str=None, gantt_file: str=None, text_file: str=None, json_file: str=None) -> None:
    args = []
    parser = buildtraceargparser()

    if trace_file:
        args += ["-t", trace_file]

    if gantt_file:
        args += ["-g", gantt_file]

    if text_file:
        args += ["-x", text_file]

    if json_file:
        args += ["-j", json_file]

    (a, u) = parser.parse_known_args(args)
    return instal_trace_preprocess_with_args(a, u)


def instal_trace():
    argparser = buildtraceargparser()
    # got following line from http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
    # which allows fileinput and argparse to co-exist, but might be better to
    # use .REMAINDER
    args, unk = argparser.parse_known_args()
    return instal_trace_preprocess_with_args(args, unk)


if __name__ == "__main__":
    instal_trace()
