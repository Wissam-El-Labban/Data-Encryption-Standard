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


plaintext = "This is a test!"
blocks = text_to_64bit_blocks(plaintext)
for i , block in enumerate(blocks):
    print(f"block {i+1}: {block}")

print(blocks_to_text(blocks))
    

