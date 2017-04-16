from unittest import SkipTest

class InstalError(Exception):
    """Base class for InstAL errors."""
    pass


class InstalBridgeError(InstalError):
    """Base class for InstAL bridge errors."""
    pass


class InstalCompileError(InstalError):
    """An exception for problems during the compilation/configuration process."""
    pass


class InstalTestNotImplemented(SkipTest, InstalError):
    """A skiptest for firstprinciples tests that haven't been implemented yet."""
    pass


class InstalArgParserError(InstalError):
    """An exception for problems with arguments given to InstAL"""
    pass


class InstalParserError(InstalError):
    """An exception for problems with the instal parser"""
    pass


class InstalParserArgumentError(InstalParserError):
    """An exception for problems with the instal parser regarding arguments of fluents/events."""
    pass


class InstalParserLexerError(InstalParserError):
    """An exception for problems with the instal parser regarding the lexer."""
    pass


class InstalParserSyntaxError(InstalParserError):
    """An exception for syntax errors during parsing."""
    pass


class InstalParserTypeError(InstalParserError):
    """An expception thrown when there is a type error in the arguments of a fluent/event."""
    pass


class InstalParserNotDeclaredError(InstalParserError):
    """An exception thrown when a fluent/event is used but not declared."""
    pass


class InstalBridgeParserError(InstalParserError, InstalBridgeError):
    """An InstalParserError for problems with the instal bridge parser."""
    pass


class InstalBridgeTypeError(InstalBridgeParserError, InstalParserTypeError):
    """An exception thrown where there are type errors in an InstAL bridge."""
    pass


class InstalBridgeCompileError(InstalCompileError, InstalBridgeParserError):
    """An exception thrown when there is a problem in the compilation process for instal bridges,"""
    pass


class InstalRuntimeError(InstalError):
    """A base exception for any InstAL errors that happen at runtime and not at the compile/parser steps."""
    pass
