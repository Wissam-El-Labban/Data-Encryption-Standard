import sys
def text_to_64bit_blocks(plaintext):
    '''convert plaintext to 64-bit blocks'''
    def text_to_binary(text):
        '''convert plaintext to binary string'''
        binary_string = ''.join(format(ord(char), '08b') for char in text)
        return binary_string
    def pad_binary_string(binary_string, text):
        '''convert plaintext to 64-bit blocks with PKCS7 padding'''
        #recieveing the amount of bytes (8 bit chunks) that need to be padded
        padding_length = 8 - (len(text) % 8)
        if padding_length != 64:
            padding_byte = format(padding_length, '08b') * (padding_length)
            binary_string = binary_string + padding_byte
        return binary_string
    def split_into_blocks(binary_string):
        '''split binary string into 64-bit blocks'''
        blocks = [binary_string[i:i + 64] for i in range(0, len(binary_string), 64)]
        
        return blocks
    
    binary_string = text_to_binary(plaintext)
    padded_binary_string = pad_binary_string(binary_string, plaintext)
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
            if len(binary_string) != 64:
                raise ValueError("Key must be 64 bits!")
            return binary_string
        try:
            binary_string = text_to_binary(plaintext)
        except ValueError as e:
            print(e)
            return None
        return binary_string

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

def des_round(left, right, round_key):
    expansion_table = [
        32,  1,  2,  3,  4,  5,
         4,  5,  6,  7,  8,  9,
         8,  9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32,  1
    ]
    
    expanded_right = ''.join(right[i-1] for i in expansion_table)
    xor_result = ''.join('1' if expanded_right[i] != round_key[i] else '0' for i in range(48))
    s_boxes = [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]
    def apply_s_boxes(input_bits):
        output_bits = ''
        for i in range(8):
            block = input_bits[i * 6: (i+1)*6]
            row = int(block[0] + block[5], 2)
            col = int(block[1:5], 2)
            s_box_value = s_boxes[i][row][col]
            output_bits += format(s_box_value, '04b')
        return output_bits
    
    s_box_output = apply_s_boxes(xor_result)
    permutation_table = [
        16,  7, 20, 21,
        29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25
    ]
    permuted_s_box_output = ''.join(s_box_output[i-1] for i in permutation_table)
    new_right = ''.join('1' if left[i] != permuted_s_box_output[i] else '0' for i in range(32))
    new_left = right
    
    return new_left, new_right


def inverse_initial_permutation(block):
    if len(block) != 64 or not all (bit in '01' for bit in block):
        raise ValueError("Invalid block")
    inv_ip_table =[
        40,  8, 48, 16, 56, 24, 64, 32,
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25
    ]
    
    permuted_block = ''.join(block[i-1] for i in inv_ip_table)
    return permuted_block

def binary_to_hex(binary):
    binary_string = ''
    for i in binary:
        binary_string += i
    
    byte_array = bytearray()
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        byte_array.append(int(byte, 2))
    #hex_string = ''.join(f'\\x{byte:02x}' for byte in byte_array)
    hex_string = byte_array.hex()
    return hex_string

if __name__ == '__main__':
    plaintext = "this is the test that will finally work!"
    key = "abcdefgh"
    round_keys = key_generation_algorithm(key)
    final_block_store = []
    #print(round_keys)
    if round_keys == None:
        print("Invalid key")
        sys.exit(1)

    blocks = text_to_64bit_blocks(plaintext)
    #print(blocks)
    
    
    for i , block in enumerate(blocks):
        #print(f"block {i+1}: {block}")
        permuted_block = initial_permutation(block)
        # the start of the 16 rounds
        left, right = permuted_block[:32], permuted_block[32:]
        for key in round_keys:
            left, right = des_round(left, right, key)
        # end of the 16 rounds
        #32 bit swap
        swapped_block = right + left
        # inverse initial permutation
        final_block = inverse_initial_permutation(swapped_block)
        final_block_store.append(final_block)
        
        
    #printing the ciphertext
    ciphertext = blocks_to_text(final_block_store)
    print('Encrypted:', binary_to_hex(final_block_store))
    
    #print(ciphertext)
    