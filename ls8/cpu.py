"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0x0] * 256         # 256b of ram
        self.reg = [0x0] * 8           # 8 registers
        self.reg[7] = 0xF4             # Stack pointer
                                  # R5 is reserved as the interrupt mask (IM)
                                  # R6 is reserved as the interrupt status (IS)
                                  # R7 is reserved as the stack pointer (SP)

        # Internal Registers
        self.pc = self.ir = self.mar = self.mdr = self.fl = 0x0
        # PC: Program Counter, address of the currently executing instruction
        # IR: Instruction Register, contains a copy of the currently executing instruction
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        # MDR: Memory Data Register, holds the value to write or the value just read
        # FL: Flags, see below

        # FL bits: 00000LGE

            # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
            # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
            # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.

    def load(self):
        program = []
        
        """ Read program from file. """        

        if len(sys.argv) != 2:
            print("ERROR: system arguments must be equal to 2!")
            exit()

        with open(sys.argv[1]) as f:
            line = f.readline()

            while line != "":
                if line[0] == '0' or line[0] == '1':
                    program.append(int(line[:8], 2))
                line = f.readline()

        if len(program) > 256:
            print("ERROR: Program length > 256 instructions")
            exit()

        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]

        elif op == "CMP":
            valA = self.reg[reg_a]
            valB = self.reg[reg_b]

            # Clear FL bits
            self.fl = 0x0
            fl_bin_string = bin(self.fl)[2:].zfill(8)

            if valA == valB:
                # Set E flag to 1
                fl_bin_string[-1] = '1'
            else:
                # set E flag to 0
                fl_bin_string[-1] = '0'

            if valA < valB:
                # Set L flag to 1
                fl_bin_string[-3] = '1'
            else:
                # Set L flag to 0
                fl_bin_string[-3] = '0'
            
            if valA > valB:
                # Set G flag to 1
                fl_bin_string[-2] = '1'
            else:
                # Set G flag to 0
                fl_bin_string[-2] = '0'

            # Convert fl_bin_string into int format and store the result in fl
            self.fl = int(fl_bin_string, 2)
        
        elif op == "DEC":
            self.reg[reg_a] -= 1
        
        elif op == "DIV":
            # Catch any divide-by-zero attempts
            if self.reg[reg_b] == 0:
                print("ERROR: Cannot DIVide by 0")
                exit()

            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "INC":
            self.reg[reg_a] += 1
        
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        
        elif op == "MOD":
            # Catch any modulo-by-zero attempts
            if self.reg[reg_b] == 0:
                print("ERROR: Cannot MODulo by 0")
                exit()

            self.reg[reg_a] %= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "NOT":
            # Python ~ operator doesn't work for this, XOR using a bitmask for NOT effect
            self.reg[reg_a] ^= 0b11111111

        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]

        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_b] >> self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")
        
        # & 0xFF register
        self.reg[reg_a] &= 0xFF

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

    def ram_read(self, addr):        # NOTE: ram methods do not bounds check
        self.mar = addr
        self.mdr = self.ram[addr]
        return self.mdr
    
    def ram_write(addr, value):
        if (value & 0xFF) != value:
            print('WARNING: ram_write() called with value > 255')

        self.mar = addr
        self.mdr = value
        self.ram[addr] = value

    def run(self):
        """Run the CPU."""
        while 1:
            # It needs to read the memory address that's stored in register PC, and store that result in IR, the Instruction Register
            # (Fetch instruction from RAM)
            self.ir = self.ram_read(self.pc)

            # Some instructions requires up to the next two bytes of data after the PC in memory to perform operations on. Sometimes the byte value is a register number, other times it's a constant value (in the case of LDI). Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            # NOTE: pc > 253 will attempt to have one or more operands read OOB data
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            # Then, depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec.

            # Decode instruction

            # Convert ir to binary:
            bin_ir =        bin(self.ir)[2:].zfill(8) 

            # Decode binary rep
            operandCount =  int(bin_ir[:2], 2)
            isALU =         int(bin_ir[2], 2)
            setsPC =        int(bin_ir[3], 2)
            identifer =     int(bin_ir[4:], 2)

            # Execute instruction

            # Maps opcode string to int representation
            t = {
                    0xA0: 'ADD',
                    0xA8: 'AND',
                    0x50: 'CALL',
                    0xA7: 'CMP',
                    0x66: 'DEC',
                    0xA3: 'DIV',
                    0x01: 'HLT',
                    0x65: 'INC',
                    0x52: 'INT',
                    0x13: 'IRET',
                    0x55: 'JEQ',
                    0x5A: 'JGE',
                    0x57: 'JGT',
                    0x59: 'JLE',
                    0x58: 'JLT',
                    0x54: 'JMP',
                    0x56: 'JNE',
                    0x83: 'LD',
                    0x82: 'LDI',
                    0xA4: 'MOD',
                    0xA2: 'MUL',
                    0x00: 'NOP',
                    0x69: 'NOT',
                    0xAA: 'OR',
                    0x46: 'POP',
                    0x48: 'PRA',
                    0x47: 'PRN',
                    0x45: 'PUSH',
                    0x11: 'RET',
                    0xAC: 'SHL',
                    0xAD: 'SHR',
                    0x84: 'ST',
                    0xA1: 'SUB',
                    0xAB: 'XOR'
                    }        

            print(t[self.ir])
           
            # Run ALU operation if applicable
            if isALU == 1: 
                self.alu(t[self.ir], operand_a, operand_b)
            else:
                # Non-ALU opcodes
                if t[self.ir] == 'HLT':
                    exit()

                if t[self.ir] == 'LDI':
                    self.reg[operand_a] = (operand_b & 0xFF)

                elif t[self.ir] == 'PRN':
                    print(self.reg[operand_a])
        
                elif t[self.ir] == 'PUSH':
                    self.reg[7] -= 1
                    self.ram[self.reg[7]] = self.reg[operand_a]
                
                elif t[self.ir] == 'POP':
                    self.reg[operand_a] = self.ram[self.reg[7]]
                    self.reg[7] += 1
            
            # Set Program Counter
            if setsPC == 0:
                self.pc += operandCount + 1
    

# Test code
if __name__ == "__main__":
    testCPU = CPU()
    testCPU.load()
    testCPU.run()
