// function
// push func name into temp var
(_{%FUNCNAME%}_)
@_{%FUNCNAME%}__AFTER_LOCALS_SET
D=A
@R13
M=D
// push nVars (total local vars number) into temp var
@_{%NVARS%}_
D=A
@R14
M=D
// jump to routine
@DEFINE_FUNC_ROUTINE
0;JMP
// label to return after setting local vars
(_{%FUNCNAME%}__AFTER_LOCALS_SET)
