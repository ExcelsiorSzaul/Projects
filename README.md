This is a school project I made.

It should be run from the GUI file.
The GUI is able to load instructions to a display so that the user can edit them before running or saving them.
You are also able to change the color of the GUI. This is done through two other GUI files: theme_selector, and preview.
The Sim file is supposed to simulate a 100 register 'computer' and has an 'accumulator' that you can perform arithmatic on, load a register into it, or store the value in a register.
Registers hold four digit signed 'words' such as +0000, -9999, or +9999.
Words are interpreted as instructions if signed with + and ignored if -
Words are structured as follows:
Example: +1210
'+' (instruction), 12 (op code), 10 (register)

There are several op codes:
10 - Read a word into a register (+1011 would read a user input into register 11)
11 - Write a word to output (+1100 would write the word stored in register 0 to output)
20 - Load a word into the accumulator (+2005 would load the word at register 5 into the accumulator)
21 - Store the word in the accumulator into a register
30 - Add a word in a register to the value in the accumulator
31 - Subtract a word in a register from the accumulator
32 - Divide the accumulator by a word in a register other than +0000
33 - Multiply the accumulator by a word in a register
40 - Branch to a register (+4012 would branch to register 12)
41 - Branch NEG will branch if the accumulator value is negative (If accumulator = -1200, then +4102 will branch to register 2)
42 - Branch ZERO will branch if the accumulator is +0000
43 - HALT will stop the program
