#!/usr/bin/env python3
import binascii
from Crypto.Cipher import AES
import hashlib

def decode_dnscat2_traffic(pcap_file, session_key_hex):
    import scapy.all
    
    # Prepare session key
    session_key = bytes.fromhex(session_key_hex)
    
    # DNScat2 uses a specific encryption scheme
    # The key for encryption is derived from the session key
    def derive_key(session_key, salt=b'dnscat'):
        return hashlib.sha256(session_key + salt).digest()[:16]
    
    encrypt_key = derive_key(session_key, b'dnscat-data')
    
    packets = rdpcap(pcap_file)
    decoded_data = []
    
    for pkt in packets:
        if pkt.haslayer(DNS) and pkt[DNS].qr == 0:
            dns = pkt[DNS]
            if dns.qd:
                qname = dns.qd.qname.decode()
                
                # Extract subdomain (skip dnscat. part)
                if 'dnscat.' in qname:
                    parts = qname.split('.')
                    if len(parts) > 2:
                        data_part = parts[1]  # After dnscat, before domain
                        
                        try:
                            # Data is hex encoded
                            encrypted = bytes.fromhex(data_part)
                            
                            # Decrypt (simplified - actual DNScat2 uses more complex scheme)
                            cipher = AES.new(encrypt_key, AES.MODE_ECB)
                            decrypted = cipher.decrypt(encrypted)
                            
                            # Remove padding
                            decrypted = decrypted.rstrip(b'\x00')
                            
                            if decrypted:
                                decoded_data.append(decrypted)
                                print(f"Decoded: {decrypted}")
                        except:
                            pass
    
    return decoded_data

# Use the session key from handshake
decoded = decode_dnscat2_traffic("good_traffic.pcap", "28b700329a268a00")
