from storage import BitStorage
from encryption import DESCipher

class Card:
    max_value = 999
    last_card_serial = -1
    @staticmethod
    def generate_card_number(serial: int, value: int):
        if value > Card.max_value:
            raise ValueError("Value is too large")
        card_serial = serial
        card_value = value

        card_serial_str = str(card_serial).zfill(10)
        card_value_str = str(card_value).zfill(3)

        card_int = int(card_serial_str + card_value_str)
        card_bytes = card_int.to_bytes((card_int.bit_length() + 7) // 8, byteorder='big')

        card_number_bytes = DESCipher.encrypt(card_bytes)
        card_number_int = int.from_bytes(card_number_bytes, byteorder='big')

        return card_number_int
    def retrieve_card_info(card_number: int):
        card_number_bytes = card_number.to_bytes((card_number.bit_length() + 7) // 8, byteorder='big')

        decrypted_bytes = DESCipher.decrypt(card_number_bytes)
        card_int = int.from_bytes(decrypted_bytes, byteorder='big')

        card_serial_str = str(card_int)[:-3]
        card_value_str = str(card_int)[-3:]

        card_serial = int(card_serial_str)
        card_value = int(card_value_str)


        return card_serial, card_value

    def check_redemption(card_number: int):
        card_serial, card_value = Card.retrieve_card_info(card_number)
        bit_value = BitStorage.read_bit(card_serial)
        if bit_value == 1:
            return True
        else:
            return False

    def redeem_card(card_number: int):
        card_serial, card_value = Card.retrieve_card_info(card_number)
        BitStorage.write_bit(card_serial, 1)
        return card_value


def test():
    card_number = Card.generate_card_number(1234567890, 100)
    print(card_number)
    card_serial, card_value = Card.retrieve_card_info(card_number)
    print(card_serial, card_value)
    print(Card.check_redemption(card_number))
    print(Card.redeem_card(card_number))
    print(Card.check_redemption(card_number))

if __name__ == "__main__":
    test()