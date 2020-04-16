// ---
@SP
A=M-1
D=M

@SP
M=M-1

@SP
A=M-1
M=M+D // +/-/&/|


// ---
@SP
A=M-1
M=-M // -/!

// ---
@SP
A=M-1
D=M

@SP
M=M-1

@SP
A=M-1
D=M-D

@SET__TRUE__
D;JEQ // eq:JEQ/gt:JGT/lt:JLT

@SP
A=M-1
M=0

@SET__TRUE__END__
0;JMP

(SET__TRUE__)
@SP
A=M-1
M=-1

(SET__TRUE__END__)
@SP
M=M-1


// ---
@i
D=i

// if segment not constant
@SEGMENT //LCL/ARG/THIS/THAT/etc.
A=A+i // i=1/2/3...
D=M

@SP
A=M
M=D

@SP
M=M+1

// ---
@SP
M=M-1
A=M
D=M

@SEGMENT //LCL/ARG/THIS/THAT/etc.
A=A+i // i=1/2/3...
M=D



// _{%COMMAND%}_
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@SET__TRUE___{%UUID%}_
D;_{%SYMBOL%}_ 
@SP
A=M-1
M=0
@SET__TRUE__END___{%UUID%}_
0;JMP
(SET__TRUE___{%UUID%}_)
@SP
A=M-1
M=-1
(SET__TRUE__END___{%UUID%}_)



// st------------ eq_gt_lt second -----------------
// _{%COMMAND%}_
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@R13
M=D
@RTN_{%UUID%}_
D=A
@R14
M=D
@SET__STACK___{%SYMBOL%}___TRUE__FALSE
0;JMP
(RTN_{%UUID%}_)
// en------------ eq_gt_lt second -----------------

// blp for ------------ eq_gt_lt second -----------------
(SET__STACK__JEQ__TRUE__FALSE)
@R13
D=M
@SET__STACK__JEQ__TRUE
D;JEQ
@SP
A=M-1
M=0
@SET__STACK__TRUE__FALSE__END
0;JMP
(SET__STACK__JEQ__TRUE)
@SP
A=M-1
M=-1
@SET__STACK__TRUE__FALSE__END
0;JMP
(SET__STACK__JGT__TRUE__FALSE)
@R13
D=M
@SET__STACK__JGT__TRUE
D;JGT
@SP
A=M-1
M=0
@SET__STACK__TRUE__FALSE__END
0;JMP
(SET__STACK__JGT__TRUE)
@SP
A=M-1
M=-1
@SET__STACK__TRUE__FALSE__END
0;JMP
(SET__STACK__JLT__TRUE__FALSE)
@R13
D=M
@SET__STACK__JLT__TRUE
D;JLT
@SP
A=M-1
M=0
@SET__STACK__TRUE__FALSE__END
0;JMP
(SET__STACK__JLT__TRUE)
@SP
A=M-1
M=-1
@SET__STACK__TRUE__FALSE__END
0;JMP
(SET__STACK__TRUE__FALSE__END)
@R14
A=M
0;JMP














// ----- eq gt lt v3 with boilerplate
// _{%COMMAND%}_
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
@RTN_{%UUID%}_
D=A
@SP
A=M
M=D
@EQ_GT_LT_ROUTINE__{%SYMBOL%}_
0;JMP
(RTN_{%UUID%}_)


(EQ_GT_LT_ROUTINE_JEQ)
@SP
A=M-1
D=M
@EQ_GT_LT_ROUTINE_TRUE
D;JEQ
@SP
A=M-1
M=0
@EQ_GT_LT_ROUTINE_RET
0;JMP

(EQ_GT_LT_ROUTINE_JGT)
@SP
A=M-1
D=M
@EQ_GT_LT_ROUTINE_TRUE
D;JGT
@SP
A=M-1
M=0
@EQ_GT_LT_ROUTINE_RET
0;JMP

(EQ_GT_LT_ROUTINE_JLT)
@SP
A=M-1
D=M
@EQ_GT_LT_ROUTINE_TRUE
D;JLT
@SP
A=M-1
M=0
@EQ_GT_LT_ROUTINE_RET
0;JMP

(EQ_GT_LT_ROUTINE_TRUE)
@SP
A=M-1
M=-1
(EQ_GT_LT_ROUTINE_RET)
@SP
A=M
0;JMP
// ----------------------------------