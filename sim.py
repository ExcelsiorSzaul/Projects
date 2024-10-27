class Sim:
    def __init__(self, gui):
        self.GUI = gui
        self.instructions = []
        self.registers = [f'+{0:04}'] * 100 # Ensures all register contain signed four digit words
        self.accumulator = '+0000'

    def execute_instructions(self):
        i = 0
        try:
            while i < 100:
                sign = self.registers[i][0]
                instruction = int(self.registers[i][1:]) // 100
                operand = int(self.registers[i][1:]) % 100
                print(f'Accumulator: {self.accumulator} Instruction: {instruction}')

                if sign == '+': # Check if it is an instruction
                
                # ------------- I/O Operations -------------
                # Read - Opcode 10
                    if instruction == 10:
                        self.GUI.write_to_display(
                        "Enter A Signed Four Digit 'Word' (+ or -####) Into The Input Box (Bottom Right) And Press Submit", "READ OPERATION"
                        )
                        self.GUI.lock(target=['all']) # Prepare for input
                        self.GUI.unlock(target=['submit', 'entry']) # Allow Input
                        self.GUI.entry_box.focus() # Set Focus to GUI Entry Box
                        try:
                            self.GUI.wait_for_input()
                        except Exception as e:
                            if str(e) == "Window Closed":
                                print('Exiting: GUI Closed')
                                break
                            else:
                                raise

                        self.GUI.unlock(target=['default']) # Reset to default
                        self.GUI.clear_display()

                    # Get New Word From GUI And READ Into Register
                        self.registers[operand] = self.GUI.new_word

                    # Update GUI Register Display
                        self.GUI.update_register_display(self.registers)

                # Write - Opcode 11
                    elif instruction == 11:
                        self.GUI.write_to_output(f'REG {operand}: {self.registers[operand]}')
                
                # ---------- Load/Store Operations ---------
                # Load - Opcode 20
                    elif instruction == 20:
                        self.accumulator = self.registers[operand]
                    
                # Store - Opcode 21
                    elif instruction == 21:
                        self.registers[operand] = self.accumulator
                
                # ---------- Arithmetic Operations ---------
                # Add - Opcode 30
                    elif instruction == 30:
                        calculation = int(self.accumulator) + int(self.registers[operand])

                        self.validate_and_store(calculation)
                    
                # Subtract - Opcode 31
                    elif instruction == 31:
                        calculation = int(self.accumulator) - int(self.registers[operand])

                        self.validate_and_store(calculation)

                # Divide - Opcode 32
                    elif instruction == 32:
                        if int(self.registers[operand]) == 0: # Divide by Zero Error
                            raise ZeroDivisionError('ZeroDivisionError')
                        
                        if int(self.accumulator) == 0: # Divide Zero by Non-Zero = 0
                            i += 1
                            continue
                        
                        calculation = int(self.accumulator) // int(self.registers[operand])

                        self.validate_and_store(calculation)
                    
                # Multiply - Opcode 33
                    elif instruction == 33:
                        if int(self.accumulator) == 0: # Multiply by Zero = 0
                            i += 1
                            continue

                        calculation = int(self.accumulator) * int(self.registers[operand])

                        self.validate_and_store(calculation)

                # ---------- Control Operations ------------
                # Branch - Opcode 40
                    elif instruction == 40:
                        i = operand
                        continue
                    
                # Branch NEG - Opcode 41
                    elif instruction == 41:
                        if int(self.accumulator) < 0:
                            i = operand
                            continue
                    
                # Branch ZERO - Opcode42
                    elif instruction == 42:
                        if int(self.accumulator) == 0:
                            i = operand
                            continue

                # Halt - Opcode 43
                    elif instruction == 43:
                        break

            # Move To Next Index
                i += 1

            self.GUI.write_to_display('Instructions Executed: Please Load New Instructions', 'Instructions Finished')
        
        except (OverflowError, ZeroDivisionError) as e:
            if isinstance(e, OverflowError):
                self.GUI.write_to_display(f'{e}: Arithmetic Operation Result Is Too Large - Result Must Be Between -9999 and +9999', 'Runtime Exception')
            else:
                self.GUI.write_to_display(f'{e}: Cannot Divide By Zero', 'Runtime Exception')

# Catch Overflow And Store In Accumulator
    def validate_and_store(self, calculation):
        if calculation >= 10000 or calculation <= -10000:
                raise OverflowError('OverflowError')
                
        if calculation < 0:
            self.accumulator = f'{calculation:+05}'
        else:
            self.accumulator = f'+{calculation:04}'

# Load initial instructions from file
    def load_instructions(self, i):
        self.instructions = []
        self.registers = [f'+{0:04}'] * 100

        if type(i) == str:
            with open(i, 'r') as f:
                for line in f:
                    self.instructions.append(line.strip())
        
        elif type(i) == list:
            self.instructions = i

        if len(self.instructions) > 100:
            raise ValueError(f"Your Instructions May Only Have A Maximum Of 100 Values")
        
        for i in range(len(self.instructions)):
            instruction = self.instructions[i]
            if self.validate_txt(instruction):
                self.registers[i] = self.instructions[i]
            else:
                raise ValueError(f"Invalid Instruction Found In Register {i}: '{instruction}'")
        self.end_of_instructions = len(self.instructions)  

# Validate Instructions        
    def validate_txt(self, instruction):
        if len(instruction) != 5:
            return False
        if instruction[0] not in ('+', '-'):
            return False
        if not instruction[1:].isdigit():
            return False
        return True