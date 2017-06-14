.data
  ARRAY1 db 21 dup (?)

.code
@PROG1:
  mov cx,21
  mov si,0
  mov bx,23
  @loop_ARRAY1:
    mov ARRAY1[si],bx
    inc si
  loop @loop_ARRAY1
  nop
end @PROG1