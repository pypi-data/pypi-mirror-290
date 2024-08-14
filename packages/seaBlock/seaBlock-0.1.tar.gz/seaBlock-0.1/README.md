# Sanctioned Encryption Algorithm (SEA)

## Overview

The `Sanctioned Encryption Algorithm (SEA)` is a custom encryption library that provides multiple layers of data transformation for enhanced security. Each layer applies a different type of transformation to the input data, making the encryption process more robust. The algorithm supports both encryption and decryption operations, with configurable layers to define the encryption depth.this library is just a simple project which can be used for simple small websites , it is never meant to defeat any algorithm like AES or DES . SEA has a different purpose and it can be used in situation wherew there is not lots of infrastructure or resources . made on 13 aug 2024

## Class: `SEA`

### Methods

#### `__init__(self)`

Initializes the SEA object with predefined layers of transformations:
1. `reverse_order`
2. `shift_characters`
3. `substitute_characters`
4. `caesar_cipher`
5. `mirror_alphabet`


#### `depth(self, layer_order: int)`

Sets the order of layers to be applied for encryption or decryption.

- **Parameters:**
  - `layer_order` (int): An integer representing the sequence of layers to use.
- **Purpose :**

  - **Set Layer Order:** The `depth` method sets the specific order of transformation layers that will be applied to the data. This order determines how the data is processed through various encryption and decryption layers.
  - **Encryption Depth:** By setting the `layer_order`, you define the depth or complexity of the encryption process, which enhances security by creating a more intricate transformation sequence.

- **Parameters:**

  - **`layer_order` (int):** This is an integer that represents the sequence of layers. Each digit of this integer corresponds to a specific transformation layer, with each layer applied in the order of the digits. For example, if you set `layer_order` to `231451`, it means:
  - Layer 2 (`shift_characters`) will be applied first.
  - Layer 3 (`substitute_characters`) will be applied second.
  - Layer 1 (`reverse_order`) will be applied third.
  - Layer 4 (`caesar_cipher`) will be applied fourth.
  - Layer 5 (`mirror_alphabet`) will be applied last.




#### `guard(self, data: str) -> str`

Encrypts the input data based on the set layer order.

- **Parameters:**
  - `data` (str): The input data to be encrypted.
- **Returns:** The encrypted data (str).
- **Raises:** `ValueError` if the depth is not set.

#### `unGuard(self, encrypted_data: str) -> str`

Decrypts the encrypted data based on the set layer order.

- **Parameters:**
  - `encrypted_data` (str): The encrypted data to be decrypted.
- **Returns:** The decrypted data (str).
- **Raises:** `ValueError` if the depth is not set.

## Example

```python
from seaBlock import SEA

# Initialize SEA
sea = SEA()

# Set encryption depth
sea.depth(231451)

# Encrypt data
encrypted = sea.guard("HelloWorld123")

# Decrypt data
decrypted = sea.unGuard(encrypted)

print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")

```
**made under MIT licence**