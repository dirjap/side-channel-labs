import os
import sys
from capstone import Cs
from unicorn import UcError
from qiling import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions import pipe
class Emulator:
    def __init__(self, code, root_fs) -> None:
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.ql = Qiling([code],root_fs,verbose=QL_VERBOSE.DISABLED)
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    def simple_diassembler(self,ql: Qiling,address: int,size: int,md: Cs) -> None:
        buf = self.ql.mem.read(address, size)
        for insn in md.disasm(buf, address):
            print(f'{insn.address:#x} : 'f'{insn.mnemonic:10s} 'f'{insn.op_str}')
    def skip_instruction(self, ql: Qiling) -> None:
        self.ql.arch.regs.arch_pc += 4
    def setup_skip_instruction(self, inst=None, debug=False) -> None:
        if inst is not None:
            self.ql.hook_address(self.skip_instruction,inst)
        if debug:
            self.ql.hook_code(self.simple_diassembler,user_data=self.ql.arch.disassembler,begin=0x1055c,end=0x10608)
        self.ql.run()
    def setup_skip_delay(self, delay=None, debug=False) -> None:
        if delay is not None:
            base = 0x10550
            inst = base + 4 * ((delay - 100) // 4)
            self.ql.hook_address(self.skip_instruction,inst)
        if debug:
            self.ql.hook_code(self.simple_diassembler,user_data=self.ql.arch.disassembler,begin=0x1055c,end=0x10608)
        self.ql.run()