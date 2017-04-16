from .InstalCompilerWrapper import InstalCompilerWrapper
from .newcompiler import instalialcompiler, instaliabcompiler


class InstalCompilerNew(InstalCompilerWrapper):
    """
        InstalCompilerNew
        Implementation of ABC InstalCompilerWrapper for the 2017 InstAL compiler.
    """

    def __init__(self):
        super().__init__()

    def compile_ial(self, ial_ast: dict) -> str:
        """

        input: an ast produced by the instal parser
        output: compiled ASP for that institution
        """
        compiler = instalialcompiler.InstalCompiler()
        return compiler.compile_ial(ial_ast)

    def compile_bridge(self, bridge_ast: dict, ial_ast: dict) -> str:
        """
        input: an ast produced by the instal bridge parser
        output: compiled ASP for that bridge
        """
        source_compiler = instalialcompiler.InstalCompiler()
        sink_compiler = instalialcompiler.InstalCompiler()
        compiler = instaliabcompiler.InstalBridgeCompiler(
            source_compiler, sink_compiler)

        for inst in ial_ast:
            if inst["contents"]["names"]["institution"] == bridge_ast["names"]["source"]:
                source_compiler.compile_ial(inst["contents"])
            if inst["contents"]["names"]["institution"] == bridge_ast["names"]["sink"]:
                sink_compiler.compile_ial(inst["contents"])
        return compiler.compile_iab(bridge_ast)
