# seaBlock/__init__.py


#Sanctioned Encryption Algorithm (SEA)
#depth should alway private and secure to make the layers more secure and hard to break
import secrets
from Crypto.Hash import SHA3_256


#==============================================
class SEA:
    def __init__(self):
        self.layers = {
            1: self.reverse_order,
            2: self.shift_characters,
            3: self.substitute_characters,
            4: self.caesar_cipher,
            5: self.mirror_alphabet
        }
        self.layer_order = None

    def reverse_order(self, data: str) -> str:
        """Layer 1: Reverse the order of the input data."""
        return data[::-1]

    def shift_characters(self, data: str) -> str:
        """Layer 2: Shift characters in the input data."""
        shifted_data = []
        for char in data:
            if char.isdigit():
                shifted_data.append(str((int(char) + 1) % 10))
            elif char.isalpha():
                if char.islower():
                    shifted_data.append(chr(((ord(char) - 97 + 1) % 26) + 97))
                elif char.isupper():
                    shifted_data.append(chr(((ord(char) - 65 + 1) % 26) + 65))
            else:
                shifted_data.append(char)
        return ''.join(shifted_data)

    def unshift_characters(self, data: str) -> str:
        """Revert the character shifting done in Layer 2."""
        unshifted_data = []
        for char in data:
            if char.isdigit():
                unshifted_data.append(str((int(char) - 1) % 10))
            elif char.isalpha():
                if char.islower():
                    unshifted_data.append(chr(((ord(char) - 97 - 1) % 26) + 97))
                elif char.isupper():
                    unshifted_data.append(chr(((ord(char) - 65 - 1) % 26) + 65))
            else:
                unshifted_data.append(char)
        return ''.join(unshifted_data)

    def substitute_characters(self, data: str) -> str:
        """Layer 3: Substitute characters with a fixed pattern."""
        substitution_pattern = str.maketrans('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                             'B1Z5ikuontScfgImvrT7xpq69CVEA84FOwXWRzDdHPM32YJUjLeyhKGbQaslN0')
        return data.translate(substitution_pattern)

    def unsubstitute_characters(self, data: str) -> str:
        """Revert the character substitution done in Layer 3."""
        reverse_pattern = str.maketrans('B1Z5ikuontScfgImvrT7xpq69CVEA84FOwXWRzDdHPM32YJUjLeyhKGbQaslN0',
                                        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        return data.translate(reverse_pattern)

    def caesar_cipher(self, data: str, shift: int = 3) -> str:
        
        ciphered_data = []
        for char in data:
            if char.islower():
                ciphered_data.append(chr((ord(char) - 97 + shift) % 26 + 97))
            elif char.isupper():
                ciphered_data.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                ciphered_data.append(char)
        return ''.join(ciphered_data)

    def uncaesar_cipher(self, data: str, shift: int = 3) -> str:
        
        return self.caesar_cipher(data, shift=-shift)

    def mirror_alphabet(self, data: str) -> str:
        
        mirrored_data = []
        for char in data:
            if char.islower():
                mirrored_data.append(chr(219 - ord(char)))  # 'a' = 97, 'z' = 122; 219 - 97 = 122
            elif char.isupper():
                mirrored_data.append(chr(155 - ord(char)))  # 'A' = 65, 'Z' = 90; 155 - 65 = 90
            else:
                mirrored_data.append(char)
        return ''.join(mirrored_data)

    def unmirror_alphabet(self, data: str) -> str:
        
        return self.mirror_alphabet(data)  # Symmetric operation

    def depth(self, layer_order: int):
        
        self.layer_order = str(layer_order)

    def guard(self, data: str) -> str:
        
        if self.layer_order is None:
            raise ValueError("Depth not set. Use Sea.depth(layer_order) to set the encryption depth.")
        
        for layer_code in self.layer_order:
            layer_function = self.layers[int(layer_code)]
            data = layer_function(data)
        
        return data

    def unGuard(self, encrypted_data: str) -> str:
        
        if self.layer_order is None:
            raise ValueError("Depth not set. Use Sea.depth(layer_order) to set the decryption depth.")
        
        reversed_layers = {
            1: self.reverse_order,
            2: self.unshift_characters,
            3: self.unsubstitute_characters,
            4: self.uncaesar_cipher,
            5: self.unmirror_alphabet
        }
        
        for layer_code in reversed(self.layer_order):
            layer_function = reversed_layers[int(layer_code)]
            encrypted_data = layer_function(encrypted_data)
        
        return encrypted_data




class Sonar:
    def __init__(self):
        self.length = 12  # Default length is 12

    def range(self, length):
        self.length = length

    def depthGenerator(self):
        sequence = []

        while len(sequence) < self.length:
            # Generate a cryptographically secure random number
            secure_random = secrets.token_bytes(32)
            
            # Hash the random number using SHA3-256 to add quantum resistance
            hash_obj = SHA3_256.new(data=secure_random)
            depthValue = hash_obj.digest()

            # Convert to an integer
            depthMetrics = int.from_bytes(depthValue, 'big')

            # Generate digits between 1 and 5
            while depthMetrics > 0 and len(sequence) < self.length:
                digit = (depthMetrics % 5) + 1
                sequence.append(str(digit))
                depthMetrics //= 5

        return ''.join(sequence)

    def activate(self):
        return self.depthGenerator()




