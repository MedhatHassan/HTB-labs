# Simple Encryptor
### https://app.hackthebox.com/challenges/simple-encryptor

Basic info about the file via `file encrypt`
encrypt: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=0bddc0a794eca6f6e2e9dac0b6190b62f07c4c75, for GNU/Linux 3.2.0, not stripped
Dumbing all Strings in the file via `strings encrypt`
<i>--Note that the output is in strings file.--</i>
From string file we found that the os is ```(Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0``` 
Dumbing all ELF via `readelf -d encrypt`
<i>--Note that the output is in elf file.--</i>
From analyzings elf :
MagicAnalyzer:
- 64bit objects
- LSB data
- Version 1
- OS is None

the size of the entire binary = 17120 bit = 2140.0 bytes
Start section headers:  15136
Number of section headers  31
Size section headers 64
Dumbing the assembly of .text via `objdump -D -M intel -j .text encrypt`
<i>--Note that the output is in text file.--</i>

---
###The real FUN begins
analyzing the progam via ghidra 
*--Note: the compiled main is in the main file.--*
We found function call for `__stack_chk_fail()` 
The main code reflected to be an encryption function that use Xor and bit-shifting 
to encrypt the flag data.
XOR Operation: For each byte in the "flag" data `(*(byte *)((long)local_20 + local_38))`, a random integer (iVar1) is generated using the `rand()` function, and this integer is used for XOR-ing the byte. The iVar1 value can be any 32-bit integer, and it is used as the XOR key for each byte individually.

Bit-Shifting Operation: Another random integer (local_3c) is generated for each byte in the range [0, 7] using `rand()`. This value is used for both **left and right bit-shifting** operations on the byte. The bit-shifting amount (local_3c) can be anywhere from 0 to 7 bits, and it is determined randomly for each byte.

Because these values `(iVar1 for XOR and local_3c for bit-shifting)` are generated randomly during each execution of the code, there is no fixed or predetermined number of bits for these operations. 

The good thing is the number of characters (bytes) in the "flag" data should remain the same after encryption.

After deep investication the code uses the frist 4 bytes in Unix timestamp to seed the nrandom value `local_40` the Unix timestamp starts since 1970.

Dumping the HEX eqwvilant with `hexdump flah.enc`
*--Note: the compiled main is in the flag_hex file.--*

Write a Decryptor in C for the reversed sequance of the assembly
1. fseek() moves the file pointer to the of the file.
2. ftell() returns the size of the file and we store it in a long **(32-bit value)** called size.
3. rewind(fp) moves the file pointer to the beginning of the file.
4. we dynamically allocate memory on the heap via malloc() with size as an argument. we set the data type to char, as they're a byte in size.

reading the file into our dynamically allocated memory.
afterwards, we print out the contents in hex to compare with it.
thereafter we make an int called seed. we use memcpy
to copy the first 32 bits of data from our allocated memory into the seed variable and print the seed.

###important part 
As we know the frist 4 bytes are from Unix timestamp so, starting From 5th byte until the end. we set our random numbers accordingly. we print out the byte we're working with and the two random numbers. then we do our right shift followed by XOR, and print out the final byte.

####Note that the flag schema is `HTB{TEXT}`
So we allredy now that the frist 4 chars are `HTB{` and the last one will be `}`
Ex: The frist char in the flag.enc file is `Z` the hex value is 5A and `H` is 48
In binary 5A is `01011010` and 48 is `01001000`
> New
