import numpy as np
from decimal import Decimal

# Fungsi Hamming Weight
def hamming_weight(x):
    return bin(x).count('1')

# Fungsi Walsh Transform untuk menghitung Nonlinearity
def walsh_transform(f):
    n = len(f)
    W = np.zeros(n, dtype=int)
    for u in range(n):
        for x in range(n):
            W[u] += (-1) ** (hamming_weight(u & x) + f[x])
    return W

# Nonlinearity (NL)
def calculate_nonlinearity(sbox):
    n = len(sbox)
    max_nonlin = 0
    for i in range(4):
        f = [(sbox[x] >> i) & 1 for x in range(n)]
        W = walsh_transform(f)
        nonlinearity = (n // 2) - (max(abs(W)) // 2)
        max_nonlin = max(max_nonlin, nonlinearity)
    return max_nonlin

# Strict Avalanche Criterion (SAC)
def calculate_sac(sbox):
    
    n = len(sbox)
    bits = int(np.log2(n))  
    sac_matrix = np.zeros((bits, bits))

    for input_bit in range(bits):
        for output_bit in range(bits):
            flipped = 0
            for x in range(n):
                x_flipped = x ^ (1 << input_bit)

                if x_flipped < n:
                    # Bandingkan bit output sbox[x] dengan sbox[x_flipped]
                    if ((sbox[x] >> output_bit) & 1) != ((sbox[x_flipped] >> output_bit) & 1):
                        flipped += 1
            sac_matrix[input_bit][output_bit] = flipped / n

    # Rata-rata nilai SAC dari semua bit input dan output
    return np.mean(sac_matrix)

# Bit Independence Criterion Nonlinearity (BIC-NL)
def calculate_bic_nl(sbox):
    n = len(sbox)
    total_bic_nl = 0
    total_pairs = 0

    for output_bit1 in range(8):
        for output_bit2 in range(output_bit1 + 1, 8):
            f1 = [(sbox[x] >> output_bit1) & 1 for x in range(n)]
            f2 = [(sbox[x] >> output_bit2) & 1 for x in range(n)]

            W1 = walsh_transform(f1)
            W2 = walsh_transform(f2)

            nl1 = (n // 2) - (max(abs(W1)) // 2)
            nl2 = (n // 2) - (max(abs(W2)) // 2)

            independent_count = 0
            for x in range(n):
                independent_count += f1[x] ^ f2[x]
            independence = independent_count / n

            bic_nl = (nl1 + nl2) * independence
            total_bic_nl += bic_nl
            total_pairs += 1

    result = total_bic_nl / total_pairs
    return round(result)

# Bit Independence Criterion Strict Avalanche Criterion (BIC-SAC)
def calculate_bic_sac(sbox):
    n = len(sbox) 
    bit_length = 8 
    total_pairs = 0
    total_independence = 0

    for i in range(bit_length):
        for j in range(i + 1, bit_length):
            independence_sum = 0
            for x in range(n):
                for bit_to_flip in range(bit_length): 
                    flipped_x = x ^ (1 << bit_to_flip)
                    y1 = sbox[x]
                    y2 = sbox[flipped_x]

                    independence_sum += ((y1 >> i) & 1 ^ (y2 >> i) & 1) ^ ((y1 >> j) & 1 ^ (y2 >> j) & 1)

            total_independence += independence_sum / (n * bit_length)
            total_pairs += 1

    average_bic_sac = total_independence / total_pairs
    return average_bic_sac

# Linear Approximation Probability (LAP)
def calculate_lap(sbox):
    n = len(sbox)
    max_lap = 0
    for a in range(1, n):
        for b in range(1, n):
            count = 0
            for x in range(n):
                if hamming_weight(a & x) % 2 == hamming_weight(b & sbox[x]) % 2:
                    count += 1
            lap = abs(count - n / 2) / n
            max_lap = max(max_lap, lap)
    return f"{max_lap:.4f}"

# Differential Approximation Probability (DAP)
def calculate_dap(sbox):
    n = len(sbox)
    max_dap = Decimal(0)  
    for delta_input in range(1, n):
        for delta_output in range(1, n):
            count = 0
            for x in range(n):
                if sbox[x] ^ sbox[x ^ delta_input] == delta_output:
                    count += 1
            dap = Decimal(count) / Decimal(n)  
            max_dap = max(max_dap, dap)
    return max_dap