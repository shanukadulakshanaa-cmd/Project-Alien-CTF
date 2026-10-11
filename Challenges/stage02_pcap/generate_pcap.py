#!/usr/bin/env python3
"""
Generate telemetry.pcap for Stage 02 (Networking / Packet Analysis).

Creates a PCAP file with:
- ~150 packets of DNS/ARP background noise
- A TCP conversation on port 4444 containing the alien transmission
  with the flag ALIEN{n3tw0rk_ch4tt3r_d3c0d3d} and the Stage 03 cipher text.
"""

from scapy.all import (
    Ether, IP, TCP, UDP, DNS, DNSQR, ARP,
    wrpcap, RandMAC, RandIP, RandShort
)
import random
import os

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/app/static/challenges/telemetry.pcap")

# Stage 02 flag
FLAG = "ALIEN{n3tw0rk_ch4tt3r_d3c0d3d}"

# Stage 03 encoded text (Base64 of ROT13 of the real flag)
STAGE3_CIPHER = "TllWUkF7bzRmcl90MF9vMDB6fQ=="


def generate_dns_noise(count=80):
    """Generate realistic DNS query/response noise."""
    packets = []
    domains = [
        "google.com", "cloudflare.com", "example.org", "github.com",
        "stackoverflow.com", "mozilla.org", "wikipedia.org", "reddit.com",
        "aws.amazon.com", "cdn.jsdelivr.net", "api.openai.com",
        "update.microsoft.com", "ntp.ubuntu.com", "dns.quad9.net"
    ]
    src_ip = "192.168.1.100"
    dns_server = "8.8.8.8"

    for _ in range(count):
        domain = random.choice(domains)
        # DNS Query
        pkt = (
            IP(src=src_ip, dst=dns_server) /
            UDP(sport=RandShort(), dport=53) /
            DNS(rd=1, qd=DNSQR(qname=domain))
        )
        packets.append(pkt)
    return packets


def generate_arp_noise(count=40):
    """Generate ARP request/reply noise."""
    packets = []
    for i in range(count):
        src_ip = f"192.168.1.{random.randint(1, 254)}"
        dst_ip = f"192.168.1.{random.randint(1, 254)}"
        pkt = ARP(
            op=random.choice([1, 2]),
            psrc=src_ip,
            pdst=dst_ip,
            hwsrc=str(RandMAC()),
            hwdst=str(RandMAC())
        )
        packets.append(Ether(dst="ff:ff:ff:ff:ff:ff") / pkt)
    return packets


def generate_http_noise(count=30):
    """Generate some HTTP-like TCP traffic on port 80."""
    packets = []
    src_ip = "192.168.1.100"
    websites = ["93.184.216.34", "151.101.1.69", "140.82.121.4"]

    for _ in range(count):
        dst_ip = random.choice(websites)
        sport = random.randint(49152, 65535)
        pkt = (
            IP(src=src_ip, dst=dst_ip) /
            TCP(sport=sport, dport=80, flags="PA") /
            f"GET /page{random.randint(1,100)} HTTP/1.1\r\nHost: example.com\r\n\r\n"
        )
        packets.append(pkt)
    return packets


def generate_alien_transmission():
    """Generate the hidden TCP conversation on port 4444 with the flag."""
    packets = []
    src_ip = "172.25.0.50"   # Alien relay
    dst_ip = "172.25.0.100"  # Alien ground station
    sport = 4444
    dport = 31337

    # TCP 3-way handshake
    syn = IP(src=dst_ip, dst=src_ip) / TCP(sport=dport, dport=sport, flags="S", seq=1000)
    syn_ack = IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags="SA", seq=2000, ack=1001)
    ack = IP(src=dst_ip, dst=src_ip) / TCP(sport=dport, dport=sport, flags="A", seq=1001, ack=2001)
    packets.extend([syn, syn_ack, ack])

    # Alien transmission messages
    messages = [
        "=== INCOMING TRANSMISSION FROM ORBITAL RELAY ===\n",
        "ORIGIN: Sector 7-G, Proxima Centauri Relay Station\n",
        "ENCRYPTION: None (Emergency Broadcast)\n",
        "PRIORITY: CRITICAL\n",
        "---------------------------------------------------\n",
        "Ground units, this is Relay Command.\n",
        "The landing zone coordinates have been secured.\n",
        "Earth defenses remain unaware of our presence.\n\n",
        f"AUTHORIZATION CODE: {FLAG}\n\n",
        "All factions are to proceed with Phase 2.\n",
        "The following encoded directive contains your next target.\n",
        "Apply standard decryption protocol (Cipher: Terran-ROT / Base-64):\n\n",
        f"ENCODED DIRECTIVE: {STAGE3_CIPHER}\n\n",
        "Relay Command out.\n",
        "=== END TRANSMISSION ===\n",
    ]

    seq = 1001
    ack_num = 2001
    for msg in messages:
        data_pkt = (
            IP(src=src_ip, dst=dst_ip) /
            TCP(sport=sport, dport=dport, flags="PA", seq=ack_num, ack=seq) /
            msg.encode()
        )
        packets.append(data_pkt)
        ack_num += len(msg)

    # TCP FIN
    fin = IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags="FA", seq=ack_num, ack=seq)
    fin_ack = IP(src=dst_ip, dst=src_ip) / TCP(sport=dport, dport=sport, flags="FA", seq=seq, ack=ack_num + 1)
    packets.extend([fin, fin_ack])

    return packets


def main():
    print("[*] Generating telemetry.pcap...")

    all_packets = []

    # Generate noise
    all_packets.extend(generate_dns_noise(80))
    all_packets.extend(generate_arp_noise(40))
    all_packets.extend(generate_http_noise(30))

    # Generate the alien transmission (the hidden signal)
    alien_pkts = generate_alien_transmission()

    # Interleave alien packets among noise (insert them at various positions)
    noise_count = len(all_packets)
    insert_positions = sorted(random.sample(range(noise_count), min(len(alien_pkts), noise_count)))

    for i, pos in enumerate(insert_positions):
        if i < len(alien_pkts):
            all_packets.insert(pos + i, alien_pkts[i])

    # Append any remaining alien packets at the end
    remaining = alien_pkts[len(insert_positions):]
    all_packets.extend(remaining)

    # Write PCAP
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    wrpcap(OUTPUT_PATH, all_packets)
    print(f"[+] Written {len(all_packets)} packets to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
