# ИСПРАВЛЕННЫЙ код
def fixed_ksa(key):
    key_len, S, j = len(key), list(range(256)), 0
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 255  # ИСПРАВЛЕНО: % 256
        S[i], S[j] = S[j], S[i]
    return S

def fixed_prga(S):
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[i]) % 256]  # ИСПРАВЛЕНО: S[i] + S[j]
        yield k

def decrypt_with_algorithm(ksa_func, prga_func, key, ciphertext_hex):
    key_bytes = [ord(c) for c in key]
    ciphertext_bytes = [int(ciphertext_hex[i:i+2], 16) for i in range(0, len(ciphertext_hex), 2)]
    
    S = ksa_func(key_bytes)
    keystream = prga_func(S)
    plaintext = []
    for byte in ciphertext_bytes:
        plaintext.append(chr(byte ^ next(keystream)))
    return ''.join(plaintext)

key = 'Za1EDolzhrRdPAehiGHu82HXkPa92zpd1Ofg'
target = '3F7307755A4336416DA27ED3CE1DE715387285E84CE3130EC0CD8F748CAA'

print("ИСПРАВЛЕННЫЙ алгоритм:")
result_fixed = decrypt_with_algorithm(fixed_ksa, fixed_prga, key, target)
print(result_fixed)
