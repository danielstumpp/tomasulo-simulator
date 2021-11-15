ld, R10, 0(R0)
ld, R11, 0(R4)
ld, F10, 8(R0)
ld, F11, 12(R0)
add, R20, R10, R1
sub, R21, R6, R11
addi, R21, R21, 1
mult.d, F20, F11, F5
add.d, F11, F20, F10
sub.d, F31, F20, F11
sd, R21, 16(R0)
sd, F31, 20(R0)