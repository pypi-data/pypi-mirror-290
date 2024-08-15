import unittest
from ..multiples.is_multiple_of_two import is_multiple_of_two
# from .is_multiple_of_two import is_multiple_of_two

class TestIsMultipleOfTwo(unittest.TestCase):

	def test_is_multiple_of_two(self):
		self.assertTrue(is_multiple_of_two(4))


if __name__ == '__main__': 
      unittest.main()

