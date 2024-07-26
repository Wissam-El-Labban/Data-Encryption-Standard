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
    
if __name__ == '__main__':
    plaintext = "This is a test!"
    key = "mykey"
    binary_key = text_to_64bit_key(key)
    Effective_key = PC_1(binary_key)
    if binary_key == None:
        sys.exit(1)
    print(f"binary key: {binary_key}")
    blocks = text_to_64bit_blocks(plaintext)
    for i , block in enumerate(blocks):
        print(f"block {i+1}: {block}")
        print(initial_permutation(block))
    
    print(blocks_to_text(blocks))
    
    