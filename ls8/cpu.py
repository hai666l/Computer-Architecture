"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        ram = [0x0] * 256         # 256b of ram
        reg = [0x0] * 8           # 8 registers
        reg[7] = 0xF4             # Set as per "power on state"
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

        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]

        elif op == "CMP":
            valA = reg[reg_a]
            valB = reg[reg_b]

            # Clear FL bits
            fl = 0x0
            fl_bin_string = bin(fl)[2:].zfill(8)

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
            fl = int(fl_bin_string, 2)
        
        elif opcode == "DEC":
            reg[reg_a] -= 1
        
        elif opcode == "DIV":
            # Catch any divide-by-zero attempts
            if reg[reg_b] == 0:
                print("ERROR: Cannot DIVide by 0")
                exit()

            reg[reg_a] /= reg[reg_b]

        elif opcode == "INC":
            reg[reg_a] += 1
        
        elif opcode == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        
        elif opcode == "MOD":
            # Catch any modulo-by-zero attempts
            if reg[reg_b] == 0:
                print("ERROR: Cannot MODulo by 0")
                exit()

            self.reg[reg_a] %= self.reg[reg_b]

        elif opcode == "MUL":
            reg[reg_a] *= reg[reg_b]

        elif opcode == "NOT":
            # Python ~ operator doesn't work for this, XOR using a bitmask for NOT effect
            reg[reg_a] ^= 0b11111111

        elif opcode == "OR":
            reg[reg_a] |= reg[reg_b]

        elif opcode == "SHL":
            reg[reg_a] = reg[reg_a] << reg[reg_b]
        
        elif opcode == "SHR":
            reg[reg_a] = reg[reg_b] >> reg[reg_b]

        elif opcode == "SUB":
            reg[reg_a] -= reg[reg_b]

        elif opcode == "XOR":
            reg[reg_a] ^= reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

        # & 0xFF registers 
        reg[reg_a] &= 0xFF
        reg[reg_b] &= 0xFF

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
        # It needs to read the memory address that's stored in register PC, and store that result in IR, the Instruction Register
        # (Fetch instruction from RAM)
        ir = ram_read(pc)

        # Some instructions requires up to the next two bytes of data after the PC in memory to perform operations on. Sometimes the byte value is a register number, other times it's a constant value (in the case of LDI). Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
        # NOTE: pc > 253 will attempt to have one or more operands read OOB data
        operand_a = ram_read(pc+1)
        operand_b = ram_read(pc+2)
    
        # Then, depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec.

        # Decode instruction

        # Convert ir to binary:
        bin_ir =        bin(ir)[2:].zfill(8) 

        # Decode binary rep
        #operandCount =  int(bin_ir[:2], 2)
        isALU =         int(bin_ir[2], 2)
        #setsPC =        int(bin_ir[3], 2)
        #identifer =        int(bin_ir[4:], 2)

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
       
        if isAlu: 
            alu(t[ir], operand_a, operand_b)
        
        # If the instruction does not set PC, PC is advanced to point to the subsequent instruction - NOTE: what determines sub. instruction?
        
        # If the CPU is not halted by HLT, begin again @ ir = ram_read(pc)
        
    
    # Added methods
    def ram_read(addr):        # NOTE: ram methods do not bounds check
        return ram[addr]
    
    def ram_write(addr, value):
        if (value & 0xFF) != value:
            print('WARNING: ram_write() called with value > 255')
        ram[addr] = value

# Test code
if __name__ == "__main__":
    testCPU = CPU()
