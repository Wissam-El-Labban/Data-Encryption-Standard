import sys
def text_to_64bit_blocks(plaintext):
    '''convert plaintext to 64-bit blocks'''
    def text_to_binary(text):
        '''convert plaintext to binary string'''
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        return binary_string
    def pad_binary_string(binary_string):
        '''pad binary string to multiple of 64 bits'''
        padding_length = 64 - (len(binary_string) % 64)
        if padding_length != 64:
            binary_string = binary_string + '0' * padding_length
        return binary_string
    def split_into_blocks(binary_string):
        '''split binary string into 64-bit blocks'''
        blocks = [binary_string[i:i + 64] for i in range(0, len(binary_string), 64)]
        return blocks
    
    binary_string = text_to_binary(plaintext)
    padded_binary_string = pad_binary_string(binary_string)
    blocks = split_into_blocks(padded_binary_string)
    return blocks


def blocks_to_text(blocks):
    '''convert 64-bit blocks to plaintext'''
    def binary_to_text(binary_string):
        '''convert binary string to ASCII'''
        byte_chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
        text = ''.join(chr(int(chunk, 2)) for chunk in byte_chunks)
        return text
    binary_string = ''.join(blocks)
    text = binary_to_text(binary_string)
    return text

def initial_permutation(block):
    ip_table = [
        58, 50, 42, 34, 26, 18, 10,  2,
        60, 52, 44, 36, 28, 20, 12,  4,
        62, 54, 46, 38, 30, 22, 14,  6,
        64, 56, 48, 40, 32, 24, 16,  8,
        57, 49, 41, 33, 25, 17,  9,  1,
        59, 51, 43, 35, 27, 19, 11,  3,
        61, 53, 45, 37, 29, 21, 13,  5,
        63, 55, 47, 39, 31, 23, 15,  7
    ]
    if len(block) != 64 or not all (bit in '01' for bit in block):
        raise ValueError("Invalid block")
    
    permuted_block = ''.join(block[i-1] for i in ip_table)
    return permuted_block

#generation of round keys (can also be done in the main 16 round loop but would waste computing power generating the same subkeys
# for different blocks)
def key_generation_algorithm(key):
    def text_to_64bit_key(plaintext):
        '''convert plaintext to 64-bit blocks'''
        def text_to_binary(text):
            '''convert plaintext to binary string'''
            binary_string = ''.join(format(ord(char), '08b') for char in text)
            if len(binary_string) > 64:
                raise ValueError("Key too long!")
            return binary_string
        def pad_binary_string(binary_string):
            '''pad binary string to multiple of 64 bits'''
            padding_length = 64 - (len(binary_string) % 64)
            if padding_length != 64:
                binary_string = binary_string + '0' * padding_length
            return binary_string
        try:
            binary_string = text_to_binary(plaintext)
        except ValueError as e:
            print(e)
            return None
        padded_binary_string = pad_binary_string(binary_string)
        return padded_binary_string

    def PC_1(key):
        pc1_table = [
            57, 49, 41, 33, 25, 17,  9,
            1, 58, 50, 42, 34, 26, 18,
            10,  2, 59, 51, 43, 35, 27,
            19, 11,  3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14,  6, 61, 53, 45, 37, 29,
            21, 13,  5, 28, 20, 12,  4
        ]
        if len(key) != 64 or not all (bit in '01' for bit in key):
            raise ValueError("Invalid key")
        permuted_key = ''.join(key[i-1] for i in pc1_table)
        return permuted_key
    def PC_2(key):
        pc2_table = [
            14, 17, 11, 24,  1,  5,
            3, 28, 15,  6, 21, 10,
            23, 19, 12,  4, 26,  8,
            16,  7, 27, 20, 13,  2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32
        ]
        if len(key) != 56 or not all (bit in '01' for bit in key):
            raise ValueError("Invalid key")
        permuted_key = ''.join(key[i-1] for i in pc2_table)
        return permuted_key

    def left_circular_shift(bits, shift_amount):
        return bits[shift_amount:] + bits[:shift_amount]
    
    binary_key = text_to_64bit_key(key)
    if binary_key == None:
        return None
    Effective_key = PC_1(binary_key)
    shift_amounts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    roundkeys = []
    
    left_half = Effective_key[:28]
    right_half = Effective_key[28:]
    for shift in shift_amounts:
        left_half = left_circular_shift(left_half, shift)
        right_half = left_circular_shift(right_half, shift)
        combined_key = left_half + right_half
        roundkey = PC_2(combined_key)
        roundkeys.append(roundkey)
    return roundkeys
    
if __name__ == '__main__':
    plaintext = "This is a test!"
    key = "mykey"
    round_keys = key_generation_algorithm(key)
    print(round_keys)
    if round_keys == None:
        print("Invalid key")
        sys.exit(1)

    blocks = text_to_64bit_blocks(plaintext)
    
    
    for i , block in enumerate(blocks):
        print(f"block {i+1}: {block}")
        permuted_block = initial_permutation(block)
        # the start of the 16 rounds
        for key in round_keys:
            #code will be filled after round function is written
            pass
    
    print(blocks_to_text(blocks))
    
    