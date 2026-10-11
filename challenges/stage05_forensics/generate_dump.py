#!/usr/bin/env python3
"""
Generate drone_core.raw — a simulated memory dump for Stage 05 (Digital Forensics).

Creates a ~5MB binary file containing:
- Fake process table entries (mimicking ps/tasklist output)
- Random binary padding (simulating memory regions)
- Hidden flag inside a suspicious "alien_proc" process memory region
- Red herrings and distractors

Solvable with: strings drone_core.raw | grep -i "ALIEN{"
Or by finding the suspicious process and examining its memory region.
"""

import os
import random
import struct

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/app/static/challenges/drone_core.raw")
FLAG = "ALIEN{m3m0ry_d03s_n0t_l13}"
DUMP_SIZE = 5 * 1024 * 1024  # 5 MB


def generate_fake_pe_header():
    """Generate a fake PE-like header."""
    header = b"MZ" + b"\x90" * 58  # DOS stub
    header += b"PE\x00\x00"  # PE signature
    header += struct.pack("<HH", 0x14C, 6)  # Machine: i386, 6 sections
    header += os.urandom(48)  # Rest of COFF header
    return header


def generate_process_table():
    """Generate a fake process listing embedded in memory."""
    processes = [
        "PID   PPID  NAME                STATUS    MEMORY",
        "----  ----  ------------------  --------  --------",
        "0     0     [System]            Running   0 KB",
        "4     0     System              Running   128 KB",
        "88    4     Registry            Running   45312 KB",
        "392   4     smss.exe            Running   1024 KB",
        "496   392   csrss.exe           Running   5120 KB",
        "564   392   wininit.exe         Running   2048 KB",
        "588   564   services.exe        Running   8192 KB",
        "596   564   lsass.exe           Running   10240 KB",
        "700   588   svchost.exe         Running   15360 KB",
        "756   588   svchost.exe         Running   8704 KB",
        "840   588   svchost.exe         Running   4096 KB",
        "1024  700   dwm.exe             Running   32768 KB",
        "1200  588   spoolsv.exe         Running   7168 KB",
        "1456  588   SearchIndexer.exe   Running   25600 KB",
        "1832  1024  explorer.exe        Running   51200 KB",
        "2048  1832  notepad.exe         Running   3072 KB",
        "2196  1832  chrome.exe          Running   102400 KB",
        "2344  2196  chrome.exe          Running   65536 KB",
        "2500  1832  cmd.exe             Running   2048 KB",
        "3072  588   alien_proc.exe      Running   16384 KB",   # SUSPICIOUS
        "3200  3072  xcom_relay.dll      Running   8192 KB",    # SUSPICIOUS
        "3456  588   WmiPrvSE.exe        Running   6144 KB",
        "3700  588   msdtc.exe           Running   4096 KB",
    ]
    return "\n".join(processes).encode("utf-8")


def generate_alien_memory_region():
    """Generate the suspicious alien_proc memory region containing the flag."""
    region = b""

    # Alien process header
    region += b"\x00" * 64
    region += b"ALIEN_PROC_MEMORY_REGION_START\x00"
    region += os.urandom(128)

    # Fake alien communications
    comms = [
        "XCOM_RELAY: Connection established to mothership",
        "XCOM_RELAY: Downloading navigation update...",
        "DRONE_NAV: Coordinates locked - Target: Earth Sector 7",
        "DRONE_NAV: Altitude: 35,000ft | Speed: Mach 3.2",
        "SELF_DESTRUCT: Module loaded - Awaiting trigger",
        "SELF_DESTRUCT: Encryption key stored in volatile memory",
        f"SELF_DESTRUCT_CODE: {FLAG}",
        "XCOM_RELAY: WARNING - A.R.G.U.S. radar detected",
        "DRONE_NAV: Evasive maneuvers initiated",
        "DRONE_NAV: CRITICAL - Engine failure detected",
        "XCOM_RELAY: Connection lost to mothership",
        "SELF_DESTRUCT: Timer activated - 30 seconds",
        "SYSTEM: Memory dump initiated by crash handler",
    ]

    for comm in comms:
        region += os.urandom(random.randint(32, 128))
        region += comm.encode("utf-8")
        region += b"\x00" * random.randint(1, 16)

    region += os.urandom(256)
    region += b"ALIEN_PROC_MEMORY_REGION_END\x00"
    region += b"\x00" * 64

    return region


def generate_red_herrings():
    """Generate misleading strings to make grep harder."""
    herrings = [
        b"ALIEN_PROTOCOL_VERSION=3.14159",
        b"ALIEN_COMM_CHANNEL=encrypted",
        b"ALIEN_FACTION_ID=ZETA_RETICULI",
        b"config.alien.network.port=9999",
        b"alien_driver.sys loaded at 0xFFFF8000",
        b"WARNING: alien filesystem detected",
        b"alien{this_is_not_the_flag}",          # Wrong format (lowercase)
        b"ALIEN{XXXXXXXXXXXXXXXXXXXXXXX}",        # Fake/corrupted flag
        b"AL1EN{not_quite_right_either}",         # Misspelled
    ]
    return herrings


def main():
    print("[*] Generating drone_core.raw...")

    data = bytearray()

    # 1. PE Header region
    data.extend(generate_fake_pe_header())
    data.extend(os.urandom(4096))  # Padding

    # 2. Process table (embedded in kernel memory)
    data.extend(b"\x00" * 256)
    data.extend(b"PROCESS_TABLE_BEGIN\x00")
    data.extend(generate_process_table())
    data.extend(b"\x00PROCESS_TABLE_END\x00")
    data.extend(os.urandom(8192))

    # 3. Random memory regions with red herrings scattered through
    herrings = generate_red_herrings()
    for herring in herrings:
        data.extend(os.urandom(random.randint(1024, 4096)))
        data.extend(herring)
        data.extend(b"\x00" * random.randint(1, 64))

    # 4. Large padding before the alien region (to make it harder to find)
    data.extend(os.urandom(DUMP_SIZE // 3))

    # 5. The actual alien process memory region with the real flag
    data.extend(generate_alien_memory_region())

    # 6. Fill remaining space with random data
    remaining = DUMP_SIZE - len(data)
    if remaining > 0:
        # Write in chunks to avoid huge memory allocation
        chunk_size = 65536
        while remaining > 0:
            write_size = min(chunk_size, remaining)
            data.extend(os.urandom(write_size))
            remaining -= write_size

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(bytes(data))

    print(f"[+] Written {len(data)} bytes ({len(data) / (1024*1024):.1f} MB) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
