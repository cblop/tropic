"""
instal.factparser

Use the following method to parse .iaf and .json files:
    def get_facts(self,fact_filenames):
        input: a list of file names to .iaf and .json (standard InstAL json as defined in tk) fact files.
            Note: The state of the LAST state in the JSON is used.
        output: a list of Fun objects of things that hold the initial state of the system.

Use the fact parser in the following way:
    fact_parser = FactParser()
    facts = fact_parser.get_facts(FACT_FILENAMES)
"""
