import customtkinter as ctk
from tkinter import filedialog
from sim import Sim
from theme_selector import ThemeSelector

# Main GUI
class GUI:
    def __init__(self):
        """Initialize the UVSim GUI and its components."""
    # Load color scheme from file and set it as the default theme
        with open('color_scheme.txt', 'r') as f:
            scheme = f.readline().strip()  
        ctk.set_default_color_theme(scheme)  

    # Color Order: Background, Frame/button, Hover/EntryBox, Text 
        self.colors = ['#1e482c', '#275d38', '#578164', '#E5E9F0']

    # Other Variables
        self.new_word = '+0000'
        self.is_closed = False

    # Main Window Initialization
        self.root = ctk.CTk()  
        self.root.resizable(False, False) 
        ctk.set_appearance_mode('dark')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    # Define window dimensions and center it on the screen
        w, h = 1200, 820  
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2) 
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.title('UVSim')  

    # Frame Creation
        # ----------- Main Frames ------------
        self.main_frame = ctk.CTkFrame(self.root) 
        self.input_frame = ctk.CTkFrame(self.root)

        self.main_frame.grid(row=0, column=0, padx=50, pady=20, sticky='nesw')
        self.input_frame.grid(row=1, column=0, padx=50, sticky='nesw')

        # ------------ Sub Frames ------------ 
        self.display_frame = ctk.CTkFrame(self.main_frame)  
        self.register_display = ctk.CTkFrame(self.main_frame)

        self.display_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky='nesw')
        self.register_display.grid(row=0, column=1, padx=(10, 0), pady=0, sticky='nesw')

    # Widget Creation
        # ------------ Text Boxes ------------
        self.entry_box = ctk.CTkEntry(self.input_frame, width=300, height=40)
        self.display_box = ctk.CTkTextbox(self.display_frame, width=900, height=665)  
        self.register_box = ctk.CTkTextbox(self.register_display, width=175, height=575)
        self.sim_output_box = ctk.CTkTextbox(self.register_display, width=175, height=50)

        # -------------- Labels -------------- 
        self.display_label = ctk.CTkLabel(self.display_frame, width=100, height=25, text='--- Ready For Instructions ---', font=('Roboto', 25), pady=5)  
        self.registers_label = ctk.CTkLabel(self.register_display, width=100, height=25, text='Registers', font=('Roboto', 25), pady=5)
        self.input_status_label = ctk.CTkLabel(self.input_frame, width=100, height=10, text='', font=('Roboto', 12), pady=5)
        self.sim_output_label = ctk.CTkLabel(self.register_display, width=100, height=25, text='Output', font=('Roboto', 25))

        # -------------- Buttons -------------
        self.load_instructions_button = ctk.CTkButton(self.input_frame, text='Load Instructions', width=140, height=40) 
        self.save_instructions_button = ctk.CTkButton(self.input_frame, text='Save Instructions', width=140, height=40)  
        self.color_change_button = ctk.CTkButton(self.input_frame, text='Change Color Scheme', width=140, height=40)
        self.run_button = ctk.CTkButton(self.input_frame, text="Run Instructions", width=140, height=40)
        self.submit_button = ctk.CTkButton(self.input_frame,text="Submit", width=140, height=40)

    # Instantiate Widgets
        # ----------- Display Frame -----------
        self.display_label.grid(row=0)  
        self.display_box.grid(row=1)  

        # ----------- Register Frame ----------
        self.registers_label.grid(row=0)
        self.register_box.grid(row=1)
        self.sim_output_label.grid(row=2, pady=(5, 0))
        self.sim_output_box.grid(row=3, pady=(5, 0))

        # ------------ Input Frame ------------
        self.load_instructions_button.grid(row=0, column=0, padx=(0, 10)) 
        self.save_instructions_button.grid(row=0, column=1, padx=(0, 10)) 
        self.run_button.grid(row=0, column=2, padx=(0, 25)) 
        self.color_change_button.grid(row=0, column=3, padx=(5, 5))
        self.entry_box.grid(row=0, column=4, padx=(25, 15))
        self.submit_button.grid(row=0, column=5, padx=(0, 15))
        self.input_status_label.grid(row=1, column=4)

    # Configure Widgets
        self.entry_box.configure(state='disabled', font=('Roboto', 16))
        self.display_box.configure(state='normal', font=('Roboto', 16))
        self.register_box.configure(state='disabled', font=('Roboto', 14))
        self.sim_output_box.configure(state='disabled', font=('Roboto', 14))
        self.color_change_button.configure(command=self.color_button_callback)
        self.load_instructions_button.configure(command=self.load_instructions_button_callback)
        self.save_instructions_button.configure(state='disabled', command=self.save_instructions_button_callback)
        self.run_button.configure(state='disabled', command=self.run_button_callback)
        self.submit_button.configure(state='disabled', command=self.submit_button_callback)

    # Link Main App and GUI
        self.UVSim = Sim(self)

    # -------------------------------------- GUI Functions ----------------------------------------

# Open Theme Selector GUI
    def color_button_callback(self):
        """Open the theme selector for changing color scheme."""
        selector = ThemeSelector(self.root, self.colors, self)

# Load Instructions Into Display and Sim
    def load_instructions_button_callback(self):
        """Load An Instruction File Into Sim.instructions, Display Box, and Update Registers"""
        file = filedialog.askopenfilename()
        if file in ('', None):
            if 'Loaded Instructions' not in self.display_box.get(1.0, 'end'):
                self.lock(['run', 'save'])
            return
        self.unlock(['run', 'save'])
        self.UVSim.load_instructions(file)
        self.write_to_display(self.UVSim.instructions, 'Loaded Instructions')
        self.update_register_display(self.UVSim.registers)
    
# Save Button Function
    def save_instructions_button_callback(self):
        """Saves What Is Shown In The Main Display Box To A File And Loads Them Into Sim"""

    # Save 'Instructions'
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")], title="Save As")

        if file_path: # Prevent saving if user closes filedialog
            text = self.display_box.get(1.0, 'end')
            prepared_text = text.strip()

        # Attempt Save
            try:
                with open(file_path, 'w') as f:
                    f.write(prepared_text)

        # Print Any Errors to Terminal
            except Exception as e:
                print(f'Error While Saving: {e}')
            
        # Load Instructions Into Sim
            self.UVSim.load_instructions(file_path)
            self.write_to_display(self.UVSim.instructions, 'Loaded Instructions')
            self.update_register_display(self.UVSim.registers)

# Write To Display Function
    def write_to_display(self, text, input_type):
        """Writes input_type, two newlines, and text To: self.display_box"""
    # Remove Any Existing Text
        self.clear_display()

    # Add Input Type Header
        self.display_label.configure(text=f'--- {input_type} ---')

    # Write To Display
        if type(text) == list:
            for line in text:
                self.display_box.insert('end', f"{line}\n")
        else:
            self.display_box.insert('end', text)

# Clear Display Function
    def clear_display(self):
        self.display_box.delete(0.0, 'end')

# Write To Output
    def write_to_output(self, text):
        """Should Be Used ONLY By Sim to WRITE (opcode 11)"""
        self.sim_output_box.configure(state='normal')
        self.sim_output_box.insert('end', f'>  {text}\n')
        self.sim_output_box.configure(state='disabled')

# Update Registers
    def update_register_display(self, registers):
        """Accepts Sim's self.registers variable (list) and writes them to register_box"""
    # Remove Current Register List
        self.register_box.configure(state='normal')
        self.register_box.delete(0.0, 'end')

    # Write New Register List
        for i, register in enumerate(registers):
            self.register_box.insert('end', f'Reg {i:02}: {register}\n')
        self.register_box.configure(state='disabled')

# Process Loaded Instructions
    def run_button_callback(self):
        """Calls Sim class .execute_instructions and updates register display"""
        text = self.display_box.get(1.0, 'end')

        prepared_text = [line.strip() for line in text.strip().splitlines() if line.strip()]

        try:
            self.UVSim.load_instructions(prepared_text)
        except Exception as e:
            self.write_to_display(f'{e}', 'Instruction Error')
            return

        self.update_register_display(self.UVSim.registers)
        self.UVSim.execute_instructions()

# Submit Button
    def submit_button_callback(self):
        new_instruction = self.entry_box.get()

    # Validate New Instruction
        ni_len = True if len(new_instruction) == 5 else False
        ni_signed = True if (new_instruction.startswith('+') or new_instruction.startswith('-')) else False
        ni_digit = True if new_instruction[1:].isdigit() else False

    # If New Instruction Is Valid
        if ni_len and ni_signed and ni_digit:
            self.input_status_label.configure(text='')
            self.entry_box.delete(0, 'end')
            self.new_word = new_instruction

        else:
            self.input_status_label.configure(text="Error: Instruction Must Be ('+' or '-') with four digits (####)")

# Waits for user input if a READ operation is performed in SIM
    def wait_for_input(self):
        self.new_word = None

        while self.new_word is None:
            if self.is_closed:
                raise Exception("Window Closed")
            self.root.update()

# Locking And Unlocking Functions
    def unlock(self, target=[]):
        """Works with strings and lists"""
        if isinstance(target, list):
            for t in target:
                match t:
                    case 'color':
                        self.color_change_button.configure(state='normal')
                    case 'load':
                        self.load_instructions_button.configure(state='normal')
                    case 'save':
                        self.save_instructions_button.configure(state='normal')
                    case 'run':
                        self.run_button.configure(state='normal')
                    case 'submit':
                        self.submit_button.configure(state='normal')
                    case 'display':
                        self.display_box.configure(state='normal')
                    case 'entry':
                        self.entry_box.configure(state='normal')
                    case 'buttons':
                        self.unlock(target=['color', 'load', 'save', 'run'])
                    case 'default':
                        self.unlock(target=['color', 'load', 'display'])
                        self.lock(['submit', 'entry', 'run', 'save'])
                    case 'all':
                        self.unlock(target=['color', 'load', 'save', 'run', 'submit', 'display', 'entry'])
                    case _:
                        pass

    def lock(self, target=[]):
        """Accepts lists"""
        if isinstance(target, list):
            for t in target:
                match t:
                    case 'color':
                        self.color_change_button.configure(state='disabled')
                    case 'load':
                        self.load_instructions_button.configure(state='disabled')
                    case 'save':
                        self.save_instructions_button.configure(state='disabled')
                    case 'run':
                        self.run_button.configure(state='disabled')
                    case 'submit':
                        self.submit_button.configure(state='disabled')
                    case 'display':
                        self.display_box.configure(state='disabled')
                    case 'entry':
                        self.entry_box.configure(state='disabled')
                    case 'buttons':
                        self.lock(target=['color', 'load', 'save', 'run'])
                    case 'all':
                        self.lock(target=['color', 'load', 'save', 'run', 'submit', 'display', 'entry'])
                    case _:
                        pass

# Start GUI
    def start_gui(self):
        """Starts The Main GUI Loop"""
        self.root.mainloop()

# Restart To Apply Color
    def restart(self):
        self.on_close()

        new_app = GUI()
        new_app.start_gui()

# Ensure Program Closes Properly
    def on_close(self):
        self.is_closed = True
        self.root.destroy()

# If Run As Main
if __name__ == '__main__':
    app = GUI()
    app.start_gui()