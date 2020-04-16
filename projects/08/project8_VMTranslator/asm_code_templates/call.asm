// call
// push return address to temp var
@_{%FUNCNAME%}_$ret._{%CALLCOUNT%}_
D=A
@R13
M=D
// push nArgs to temp var
@_{%NARGS%}_
D=A
@R14
M=D
// push func name to temp var
@_{%FUNCNAME%}_
D=A
@R15
M=D
// jump to call routine
@CALL_ROUTINE
0;JMP
// return here afterwards
(_{%FUNCNAME%}_$ret._{%CALLCOUNT%}_)
