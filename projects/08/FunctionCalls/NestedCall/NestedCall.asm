// init
// set base of stack
@256
D=A
@SP
M=D
// call Sys.init
// push return address to temp var
@Sys.init$ret.1
D=A
@R13
M=D
// push nArgs to temp var
@0
D=A
@R14
M=D
// push func name to temp var
@Sys.init
D=A
@R15
M=D
// jump to call routine
@CALL_ROUTINE
0;JMP
// return here afterwards
(Sys.init$ret.1)
// [File] Sys.vm
// function
// push func name into temp var
(Sys.init)
@Sys.init_AFTER_LOCALS_SET
D=A
@R13
M=D
// push nVars (total local vars number) into temp var
@0
D=A
@R14
M=D
// jump to routine
@DEFINE_FUNC_ROUTINE
0;JMP
// label to return after setting local vars
(Sys.init_AFTER_LOCALS_SET)
// push
@4000	
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
@5000
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
// call
// push return address to temp var
@Sys.main$ret.1
D=A
@R13
M=D
// push nArgs to temp var
@0
D=A
@R14
M=D
// push func name to temp var
@Sys.main
D=A
@R15
M=D
// jump to call routine
@CALL_ROUTINE
0;JMP
// return here afterwards
(Sys.main$ret.1)
// pop
@1
D=A
@R5
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
// label
(Sys.init$LOOP)
// goto
@Sys.init$LOOP
0;JMP
// function
// push func name into temp var
(Sys.main)
@Sys.main_AFTER_LOCALS_SET
D=A
@R13
M=D
// push nVars (total local vars number) into temp var
@5
D=A
@R14
M=D
// jump to routine
@DEFINE_FUNC_ROUTINE
0;JMP
// label to return after setting local vars
(Sys.main_AFTER_LOCALS_SET)
// push
@4001
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
@5001
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
@200
D=A
@SP
M=M+1
A=M-1
M=D
// pop
@1
D=A
@LCL
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
A=M+1
A=M
M=D
// push
@40
D=A
@SP
M=M+1
A=M-1
M=D
// pop
@2
D=A
@LCL
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
A=M+1
A=M
M=D
// push
@6
D=A
@SP
M=M+1
A=M-1
M=D
// pop
@3
D=A
@LCL
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
A=M+1
A=M
M=D
// push
@123
D=A
@SP
M=M+1
A=M-1
M=D
// call
// push return address to temp var
@Sys.add12$ret.1
D=A
@R13
M=D
// push nArgs to temp var
@1
D=A
@R14
M=D
// push func name to temp var
@Sys.add12
D=A
@R15
M=D
// jump to call routine
@CALL_ROUTINE
0;JMP
// return here afterwards
(Sys.add12$ret.1)
// pop
@0
D=A
@R5
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
// push
@2
D=A
@LCL
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// push
@3
D=A
@LCL
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// push
@4
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
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// return
@RETURN_ROUTINE
0;JMP
// function
// push func name into temp var
(Sys.add12)
@Sys.add12_AFTER_LOCALS_SET
D=A
@R13
M=D
// push nVars (total local vars number) into temp var
@0
D=A
@R14
M=D
// jump to routine
@DEFINE_FUNC_ROUTINE
0;JMP
// label to return after setting local vars
(Sys.add12_AFTER_LOCALS_SET)
// push
@4002
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
@5002
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
@0
D=A
@ARG
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// push
@12
D=A
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
