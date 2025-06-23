import os
from PIL import Image
import hashlib

class SteganographyUtils:
    @staticmethod
    def hide_message_in_image(image_path, message, secret_key, output_path):
        """Hide a message in an image using LSB steganography"""
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create a key-based seed for message positioning
            key_hash = hashlib.md5(secret_key.encode()).hexdigest()
            seed = int(key_hash[:8], 16)
            
            # Prepare the message with delimiter
            delimiter = "<<<END_OF_MESSAGE>>>"
            full_message = message + delimiter
            binary_message = ''.join(format(ord(char), '08b') for char in full_message)
            
            # Get image dimensions
            width, height = img.size
            pixels = list(img.getdata())
            
            # Check if image can hold the message
            max_chars = (width * height * 3) // 8
            if len(full_message) > max_chars:
                raise ValueError(f"Message too long for image. Maximum {max_chars} characters.")
            
            # Hide message in LSBs
            data_index = 0
            for i in range(len(pixels)):
                if data_index < len(binary_message):
                    pixel = list(pixels[i])
                    for j in range(3):  # RGB channels
                        if data_index < len(binary_message):
                            # Modify LSB
                            pixel[j] = pixel[j] & 0xFE | int(binary_message[data_index])
                            data_index += 1
                    pixels[i] = tuple(pixel)
                else:
                    break
            
            # Create new image with modified pixels
            stego_img = Image.new('RGB', (width, height))
            stego_img.putdata(pixels)
            stego_img.save(output_path)
            
            return True
        except Exception as e:
            raise Exception(f"Steganography hiding failed: {str(e)}")
    
    @staticmethod
    def extract_message_from_image(image_path, secret_key):
        """Extract hidden message from image"""
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get pixels
            pixels = list(img.getdata())
            
            # Extract LSBs
            binary_message = ""
            for pixel in pixels:
                for channel in pixel:
                    binary_message += str(channel & 1)
            
            # Convert binary to text
            message = ""
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    message += char
                    
                    # Check for delimiter
                    if message.endswith("<<<END_OF_MESSAGE>>>"):
                        # Remove delimiter and return message
                        return message[:-len("<<<END_OF_MESSAGE>>>")]
            
            # If we reach here, no valid message was found
            raise ValueError("No valid message found in image or incorrect secret key")
            
        except Exception as e:
            raise Exception(f"Message extraction failed: {str(e)}")
