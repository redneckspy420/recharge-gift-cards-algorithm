import os
import struct


class BitStorage:
    directory = "storage"
    num_files = 100
    max_bit = 9_999_999_999
    max_bits_per_file = max_bit+1 // num_files

    def get_file_name(bit_index):
        file_index = bit_index // BitStorage.max_bits_per_file
        return f"cards.{file_index}"

    def get_file_path(bit_index):
        return os.path.join(BitStorage.directory, BitStorage.get_file_name(bit_index))

    def create_file_if_not_exists():
        if not os.path.exists(BitStorage.file_path):
            with open(BitStorage.file_path, "w"):
                pass

    def get_bit_index(bit_index):
        return bit_index % BitStorage.max_bits_per_file

    def get_byte_and_offset(bit_index):
        bit_index = BitStorage.get_bit_index(bit_index)
        return divmod(bit_index, 8)

    @staticmethod
    def write_bit(bit_index, bit_value):
        BitStorage.create_file_if_not_exists()
        byte_index, offset = BitStorage.get_byte_and_offset(bit_index)

        with open(BitStorage.file_path, "rb+") as file:
            file.seek(byte_index)

            try:
                byte = struct.unpack("B", file.read(1))[0]
            except struct.error:
                byte = 0

            if bit_value == 1:
                byte |= 1 << offset
            else:
                byte &= ~(1 << offset)

            file.seek(byte_index)
            file.write(struct.pack("B", byte))

    @staticmethod
    def read_bit(bit_index):
        BitStorage.create_file_if_not_exists()
        byte_index, offset = BitStorage.get_byte_and_offset(bit_index)

        with open(BitStorage.file_path, "rb") as file:
            file.seek(byte_index)

            try:
                byte = struct.unpack("B", file.read(1))[0]
            except struct.error:
                byte = 0

        return (byte >> offset) & 1
