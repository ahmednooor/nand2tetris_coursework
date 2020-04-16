// [File] SimpleFunction.vm
// function
// push func name into temp var
(SimpleFunction.test)
@SimpleFunction.test_AFTER_LOCALS_SET
D=A
@R13
M=D
// push nVars (total local vars number) into temp var
@2
D=A
@R14
M=D
// jump to routine
@DEFINE_FUNC_ROUTINE
0;JMP
// label to return after setting local vars
(SimpleFunction.test_AFTER_LOCALS_SET)
// push
@0
D=A
@LCL
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// push
@1
D=A
@LCL
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
// not
@SP
A=M-1
M=!M
// push
@0
D=A
@ARG
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
// push
@1
D=A
@ARG
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
// return
@RETURN_ROUTINE
0;JMP
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
// DEFINE_FUNC_ROUTINE
(DEFINE_FUNC_ROUTINE)
// set new LCL
@SP
A=M
D=A
@LCL
M=D
// push 0 to stack nVars times
(PUSH_NVARS_ZEROES)
@R14
M=M-1
D=M
@PUSH_NVARS_ZEROES_STOP
D;JLT
@SP
M=M+1
A=M-1
M=0
// if D > 0 then loop again
@PUSH_NVARS_ZEROES
0;JMP
(PUSH_NVARS_ZEROES_STOP)
// pull function name from temp var and jump there
@R13
A=M
0;JMP
// CALL_ROUTINE
(CALL_ROUTINE)
// pull return address from temp var and push it on stack
@R13
D=M
@SP
M=M+1
A=M-1
M=D
// push LCL
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
// push ARG
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
// push THIS
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
// push THAT
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
// pull nArgs from temp var and then set new ARG
@R14
D=M
@5
D=D+A
@SP
A=M
D=A-D
@ARG
M=D
// pull func name from temp var and go to function definition
@R15
A=M
0;JMP
// RETURN_ROUTINE
(RETURN_ROUTINE)
// temp var frame = lcl
@LCL
D=M
@R13
M=D
// temp var for return
@5
D=A
@R13
A=M-D
D=M
@R14
M=D
// pop arg 0
@SP
A=M-1
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D
// restore THAT
@R13
M=M-1
A=M
D=M
@THAT
M=D
// restore THIS
@R13
M=M-1
A=M
D=M
@THIS
M=D
// restore ARG
@R13
M=M-1
A=M
D=M
@ARG
M=D
// restore LCL
@R13
M=M-1
A=M
D=M
@LCL
M=D
// jump to return address
@R14
A=M
0;JMP
