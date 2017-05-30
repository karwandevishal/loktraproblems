import unittest 
from reverse_hash import ReverseHash

class TestReverse(unittest.TestCase):
    """Test ReverseHash class."""
    def setUp(self):
        self.reverse_hash = ReverseHash()
    def test_get_string(self):
        """check if we get original string."""
        hash_val = self.reverse_hash.get_hash('gil')
        get_string = self.reverse_hash.get_string(hash_val)
        self.assertEqual(get_string, 'gil')
        
    def test_allowed_chars(self):
        """check for allowed characters."""
        hash_val = self.reverse_hash.get_hash('123')
        self.assertEqual(hash_val['error'], 'allowed chars {}'.format(self.reverse_hash.letters))
        
    def test_none_hash(self):
        """Error message in case None hash Value."""
        get_string = self.reverse_hash.get_string(None)
        self.assertEqual(get_string['error'], 'hash value passed is None')
    

if __name__ == '__main__':
    unittest.main()
