"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        ram = [0x0] * 256         # 256b of ram
        register = [0x0] * 8      # 8 registers
                                  # R5 is reserved as the interrupt mask (IM)
                                  # R6 is reserved as the interrupt status (IS)
                                  # R7 is reserved as the stack pointer (SP)

        # Internal Registers
        pc = ir = mar = mdr = fl = 0x0
        # PC: Program Counter, address of the currently executing instruction
        # IR: Instruction Register, contains a copy of the currently executing instruction
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        # MDR: Memory Data Register, holds the value to write or the value just read
        # FL: Flags, see below

        # FL bits: 00000LGE

            # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
            # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
            # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.

        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        pass

# Test code
if __name__ == "__main__":
    testCPU = CPU()
