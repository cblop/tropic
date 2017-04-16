"""
instal.parser

Wrappers for InstAL Parsers should extend InstalParser Wrapper. Methods that need defining:
    def __init__(self):
        Self-explanatory
    def parse_ial(self, ial_text):
        input: The text of an InstAL institution.
        output: An AST/intermediate representation of the specified InstAL institution.
    def parse_bridge(self, bridge_text):
        input: The text of an InstAL bridge.
        output: An AST/intermediate representation of the specified InstAL bridge.

Use an instance of a subclass of InstalCompilerWrapper as follows:
    parser_wrapper = subclassOfInstalParserWrapper()
    instal_dictionary = parser_wrapper.get_instal_dictionary(solve_args.ial_files, solve_args.bridge_file)
    irs_dictionary = parser_wrapper.parse(instal_dictionary)

    Where instal_dictionary is a dictionary generated using
        parser_wrapper.get_instal_dictionary(LIST OF IAL FILENAMES, LIST OF BRIDGE FILENAMES)

    and irs_dictionary is a dictionary in the form:
        {
            "institution_ir" : [
                {
                    "filename" : FILENAME,
                    "contents" : IR_CONTENTS
                }, ...
            ],
            "bridge_ir" : [
                {
                    "filename" : FILENAME,
                    "contents" : IR_CONTENTS
                }
        }

    irs_dictionary can then be used as specified in instal_stable.compiler
"""
