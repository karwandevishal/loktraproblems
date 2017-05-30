import sys
class ReverseHash:
    """class for hash and reverse hash."""
    def __init__(self, h=7, salt=37):
        self.letters = 'acdegilmnoprstuw'
        self.h = h
        self.salt = salt

    def get_hash(self, string):
        """Given a string return it's hash value."""
        h = self.h
        try:
            for i in range(len(string)):
                char = string[i]
                h = h * self.salt + self.letters.index(char)
            return h
        except ValueError as e:
            msg = 'allowed chars {}'.format(self.letters)
            return {'error': msg}
        except Exception as e:
            msg = str(e)
            return {'error': msg}
            
    def get_string(self, hash_val):
        """Given a hash value return string."""
        result = []
        length = len(self.letters)
        try:
            while hash_val > self.h:
                remainder = hash_val % self.salt
                result.append(remainder)
                hash_val = hash_val // self.salt
            return ''.join([self.letters[i] for i in result])[::-1]
        except TypeError as te:
            msg = str(te)
            if hash_val is None:
                msg = 'hash value passed is None'
            return {'error': msg}
        except Exception as e:
            msg = str(e)
            return {'error': msg}
       


        
