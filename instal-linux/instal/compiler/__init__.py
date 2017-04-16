"""
instal_stable.compiler

Wrappers for InstAL Compilers should extend InstalCompilerWrapper. Methods that need defining:
    def __init__(self)
        Self-explanatory
    def compile_ial(self, ial_ast):
        input: An AST for a single Instal institution.
        output: The compiled ASP for specified InstAL institution.
    def compile_bridge(self, bridge_ast):
        input: An AST for a single Instal bridge.
        output: The compiled ASP for specified InstAL institution.

Use an instance of a subclass of InstalCompilerWrapper as follows:
    compiler_wrapper = SubclassOfInstalCompilerWrapper()
    asp_dictionary = compiler_wrapper.compile(irs_dictionary)

    Where irs_dictionary is a dictionary in the form outputted by instal_stable.parser
    and asp_dictionary is a dictionary in the form:
        {
            "institution_asp" : [
                {
                    "filename" : FILENAME,
                    "contents" : ASP_CONTENTS
                }, ...
            ],
            "bridge_asp" : [
                {
                    "filename" : FILENAME,
                    "contents" : ASP_CONTENTS
                }
        }
"""
