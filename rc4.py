def KSA(key):
    """
    Key-Scheduling Algorithm (KSA)
    
    Parâmetros:
    - key: Chave de criptografia (lista de bytes)
    
    Retorna:
    - S: Lista de bytes inicializada com base na chave
    """
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    """
    Pseudo-Random Generation Algorithm (PRGA)
    
    Parâmetros:
    - S: Lista de bytes inicializada pelo KSA
    
    Retorna:
    - Um gerador que produz um fluxo de chave (key stream)
    """
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key, data):
    """
    RC4 Encryption/Decryption
    
    Parâmetros:
    - key: Chave de criptografia (string)
    - data: Dados a serem criptografados/descriptografados (string)
    
    Retorna:
    - Resultado criptografado/descriptografado (bytes)
    """
    # Converte chave e dados para listas de bytes
    key = [ord(c) for c in key]
    data = [ord(c) for c in data]
    
    # Executa o KSA para inicializar S
    S = KSA(key)
    
    # Gera o fluxo de chave e aplica XOR aos dados
    keystream = PRGA(S)
    result = bytes([c ^ next(keystream) for c in data])
    
    return result

# Exemplo de uso do RC4
key = "secretkey"
plaintext = "Hello, World!"

# Criptografa o plaintext
ciphertext = RC4(key, plaintext)
print(f"Encrypted: {ciphertext}")

# Descriptografa o ciphertext
decrypted_text = RC4(key, ciphertext.decode('latin1'))
print(f"Decrypted: {decrypted_text.decode('latin1')}")
