#Behiend the scenes 
##https://app.hackthebox.com/challenges/Behind%20the%20Scenes
Frist try to analyze all the strings in the file via :
```strings behindthescenes```
<i>Note: the output is in strings file.</i>

analyze binary ELF of the file with readelf:
```readelf -a behindthescenes```
<i>Note: the output is in ELF file.</i>
via analyzing ```Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00```
02 class --> 64bit Objects
01 = LSB
Os is Unix and from strings we find ```/lib64/ld-linux-x86-64.so.2``` that means it is linux.
###Analyze the source code with ghidra 
We found main function and decomiled it 
<i>Note: the output is in main file.</i>
We found function call for ```invalidInstructionException();```
After searching for this function in the assemble we found ```UD2```
<i>Note that the UD2 (Undefined Opcode) instruction is used to generate an illegal or undefined opcode exception when executed.</i>
After deassemble the code and tracing it
We find strcmp function each one contains part of the flag
after decombiling them 
<i>Note: the decombiled functions is in main file.</i>
The key will be ```Itz_0nLy_UD2```
```./behindthescenes Itz_0nLy_UD2 > HTB{Itz_0nLy_UD2}```