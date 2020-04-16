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
