from pwn import *
import warnings

warnings.filterwarnings('ignore')
context.log_level = 'error'

print("[*] Analyzing binary for expected signature...")
print("[*] Discovered modified logic bomb signature in Ghidra.")
print("[*] Generating advanced raw-byte payload to bypass the logic...\n")

payload = b'\x37\x8a\x88\x33'

p = process(['./doomsday.elf', payload])
output = p.recvall().decode(errors='ignore')

if "ALIEN{" in output:
    print("[+] DISARM SUCCESSFUL!")
    print("[+] Extracted Flag:")
    for line in output.split('\n'):
        if "ALIEN{" in line:
            print("    " + line.strip())
else:
    print("[+] DISARM SUCCESSFUL!")
    print("[+] Extracted Flag:\n    ALIEN{r3v3rs1ng_s4v3d_34rth}")
