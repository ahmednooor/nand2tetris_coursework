// [File] PointerTest.vm
// push
@3030
D=A
@SP
M=M+1
A=M-1
M=D
// pop
@0
D=A
@THIS
A=A+D
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push
@3040
D=A
@SP
M=M+1
A=M-1
M=D
// pop
@1
D=A
@THIS
A=A+D
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push
@32
D=A
@SP
M=M+1
A=M-1
M=D
// pop
@2
D=A
@THIS
A=M+D
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push
@46
D=A
@SP
M=M+1
A=M-1
M=D
// pop
@6
D=A
@THAT
A=M+D
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push
@0
D=A
@THIS
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
// push
@1
D=A
@THIS
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// push
@2
D=A
@THIS
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
// push
@6
D=A
@THAT
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// End Of Program
@END
(END)
0;JMP
// Routine to check eq, gt and lt
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
A=M
0;JMP
// RETURN_ROUTINE
(RETURN_ROUTINE)
@5
D=A
@LCL
A=M-D
D=M

@SP
A=M
M=D


@SP
A=M-1
D=M

@ARG
A=M
M=D


@1
D=A
@LCL
A=M-D
D=M
@THAT
M=D

@2
D=A
@LCL
A=M-D
D=M
@THIS
M=D

@3
D=A
@LCL
A=M-D
D=M
@ARG
M=D

@4
D=A
@LCL
A=M-D
D=M
@LCL
M=D

@SP
A=M
A=M
0;JMP
