0x0001055c      00482de9       push {fp, lr}
0x00010560      04b08de2       add fp, var_4h
0x00010564      30d04de2       sub sp, sp, 0x30
0x00010568      9c309fe5       ldr r3, [fcn.0001060c]
0x0001056c      003093e5       ldr r3, [r3]           
0x00010570      08300be5       str r3, [var_8h]       
0x00010574      0030a0e3       mov r3, 0
0x00010578      90309fe5       ldr r3, str.Password 
0x0001057c      30c04be2       sub ip, s2
0x00010580      03e0a0e1       mov lr, r3                 
0x00010584      0f00bee8       ldm lr!, {r0, r1, r2, r3}
0x00010588      0f00ace8       stm ip!, {r0, r1, r2, r3}
0x0001058c      00309ee5       ldr r3, [lr]
0x00010590      0030cce5       strb r3, [ip]
0x00010594      78009fe5       ldr r0, str.Enter_your_password:_ 
0x00010598      601c00eb       bl sym.__printf             ; printf("Enter_your_password")
0x0001059c      1c304be2       sub r3, s1
0x000105a0      0310a0e1       mov r1, r3
0x000105a4      6c009fe5       ldr r0, aav.0x0007b9ec     
0x000105a8      a31c00eb       bl sym.__isoc99_scanf       ; scanf("%s", Password)
0x000105ac      30204be2       sub r2, s2
0x000105b0      1c304be2       sub r3, s1
0x000105b4      0210a0e1       mov r1, r2                  ; const char *s2
0x000105b8      0300a0e1       mov r0, r3                  ; const char *s1
0x000105bc      c48b00eb       bl sym.strcmp               ; int strcmp(const char *s1, const char *s2)
0x000105c0      0030a0e1       mov r3, r0                  
0x000105c4      000053e3       cmp r3, 0                    
0x000105c8      0200001a       bne 0x105d8                 ;
0x000105cc      48009fe5       ldr r0, str.Access_granted._Welcome_  ; "Access granted. Welcome!" ; const char *s
0x000105d0      614b00eb       bl sym.puts                 ; int puts(const char *s)
0x000105d4      010000ea       b 0x105e0                   
0x000105d8      40009fe5       ldr r0, str.Access_denied._Incorrect_password.; "Access denied. Incorrect password." ; const char *s
0x000105dc      5e4b00eb       bl sym.puts                 ; int puts(const char *s)
0x000105e0      0030a0e3       mov r3, 0
0x000105e4      20209fe5       ldr r2, [fcn.0001060c]      
0x000105e8      001092e5       ldr r1, [r2]                
0x000105ec      08201be5       ldr r2, [var_8h]            
0x000105f0      011032e0       eors r1, r2, r1
0x000105f4      0020a0e3       mov r2, 0                    
0x000105f8      0000000a       beq 0x10600                 
0x000105fc      b8a600eb       bl sym.__stack_chk_fail_local
0x00010600      0300a0e1       mov r0, r3
0x00010604      04d04be2       sub sp, var_4h_2
0x00010608      0088bde8       pop {fp, pc}