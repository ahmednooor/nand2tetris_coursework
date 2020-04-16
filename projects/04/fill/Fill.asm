// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// -- START PROC MAIN_LOOP --
(MAIN_LOOP)
@KBD
D=M
@FILL_SCREEN
D;JNE
@UNFILL_SCREEN
D;JEQ
@MAIN_LOOP
0;JMP
// -- END PROC MAIN_LOOP --

// -- START PROC FILL_SCREEN --
(FILL_SCREEN)

@SCREEN
D=A

(LBL1_FILL_SCREEN)
A=D
M=-1

D=D+1

@R0
M=D

@KBD
D=A-D
@END_FILL_SCREEN
D;JEQ

@R0
D=M

@LBL1_FILL_SCREEN
0;JMP

(END_FILL_SCREEN)
@MAIN_LOOP
0;JMP
// -- END PROC FILL_SCREEN --

// -- START PROC UNFILL_SCREEN --
(UNFILL_SCREEN)

@SCREEN
D=A

(LBL1_UNFILL_SCREEN)
A=D
M=0

D=D+1

@R0
M=D

@KBD
D=A-D
@END_UNFILL_SCREEN
D;JEQ

@R0
D=M

@LBL1_UNFILL_SCREEN
0;JMP

(END_UNFILL_SCREEN)
@MAIN_LOOP
0;JMP
// -- END PROC UNFILL_SCREEN --

