"""
instal.domainparser

Use the following method to parse .idc files:
    def get_groundings(self, domain_files : list):
        input: a list of file names to .idc files
        output: a defaultdict(set) of the types and values of those types in those files

Use the domain parser in the following way:
    domain_parser = DomainParser()
    domain_facts = domain_parser.get_groundings(DOMAIN_FILENAMES)
"""
