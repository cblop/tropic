import ply.lex as lex

from instal.instalexceptions import InstalParserLexerError


class InstalLexer(object):
    """
        InstalLexer
        Lexer for IAL files.
        A significant chunk of this code is legacy and thus fragile.
    """

    def __init__(self):
        self.lexer = lex.lex(module=self)

    reserved = {  # 'and'         : 'AND',
                  'create': 'CREATE',
                  'dissolve': 'DISSOLVE',
                  'event': 'EVENT',
                  'exogenous': 'EXOGENOUS',
                  'fluent': 'FLUENT',
                  'generates': 'GENERATES',
                  'if': 'IF',
                  #'in': 'IN', #Removed for 2.0.0 - capage
                  'initially': 'INITIALLY',
                  'initiates': 'INITIATES',
                  'inst': 'INST',
                  'institution': 'INSTITUTION',
                  'noninertial': 'NONINERTIAL',
                  'not': 'NOT',
                  'obl': 'OBL',
                  'obligation': 'OBLIGATION',
                  'perm': 'PERM',
                  'pow': 'POW',
                  'terminates': 'TERMINATES',
                  'type': 'TYPE',
                  'viol': 'VIOL',
                  'violation': 'VIOLATION',  # 'with'        : 'WITH',
                  'when': 'WHEN',
                  'bridge': 'BRIDGE',
                  'source': 'SOURCE',
                  'sink': 'SINK',
                  'cross': 'CROSS',
                  'gpow': 'GPOW',
                  'ipow': 'IPOW',
                  'tpow': 'TPOW',
                  'xgenerates': 'XGENERATES',
                  'xterminates': 'XTERMINATES',
                  'xinitiates': 'XINITIATES'
    }

    tokens = ['NAME', 'TYPE_NAME', 'NUMBER', 'LPAR', 'RPAR', 'SEMI', 'COMMA', 'EQUALS', 'NOTEQUAL', 'LESS', 'GREATER',
              'LESSEQ', 'GREATEREQ'] + list(reserved.values())

    # Tokens

    t_SEMI = r';'
    t_COMMA = r','
    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_EQUALS = r'=='
    t_NOTEQUAL = r'!='
    t_LESS = r'<'
    t_LESSEQ = r'<='
    t_GREATER = r'>'
    t_GREATEREQ = r'>='

    def t_NAME(self, t):
        r"""[a-z_][a-zA-Z_0-9]*"""
        # changed to allow _ to start a variable name
        t.type = self.reserved.get(t.value, 'NAME')  # Check for reserved words
        return t

    def t_TYPE_NAME(self, t):
        r"""[A-Z][a-zA-Z_0-9]*"""
        return t

    def t_NUMBER(self, t):
        r"""\d+"""
        # note: numbers are parsed but not converted into integers
        # t.value = int(t.value)
        return t

    t_ignore = " \t\r"

    # Comments
    def t_COMMENT(self, t):
        r"""%.*"""
        pass

    # No return value. Token discarded

    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        raise InstalParserLexerError("Illegal character '%s'" % t.value[0])
