import re


class TwID:
    def valid(self, _id):
        match = re.match(r'^([A-Z])([0-9]{9})$', _id)
        if match:
            first_char, nums = match.groups()
            encoded = self.char_map(first_char) + nums
            encoded_nums = (a * b for a, b in
                            zip(map(int, encoded), [1, 9, 8, 7, 6, 5, 4, 3, 2,
                                                    1, 1]))

            return sum(encoded_nums) % 10 == 0

        return False

    def char_map(self, first_char):
        return str(ord(first_char) - 55)
