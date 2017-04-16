from tempfile import NamedTemporaryFile

from .clingo import Symbol, Function


def temporary_text_file(text="", file_extension="", delete=True) -> "File":
    """Returns a NamedTemporaryFile with the specified file extension and prints text to it."""
    tmpfile = NamedTemporaryFile(
        suffix=file_extension, mode="w+t", delete=delete)
    print(text, file=tmpfile)
    return tmpfile


def fun_to_asp(fun: Function) -> str:
    """Takes a gringo fun object and returns what it is in ASP."""
    if isinstance(fun, Symbol):
        return str(fun) + ".\n"
    return ""


def encode_Fun(obj: Symbol) -> dict:
    return {"__Fun__": True, "name": obj.name, "args": obj.arguments}
