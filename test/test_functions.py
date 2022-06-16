import unittest
from ..core.mesh import vector_angle

class TestFunctions(unittest.TestCase):

    def test_vector_angle(self):
        self.assertEqual(vector_angle([0, 0, 1], [0, 0, 1]), 0)
        self.assertEqual(vector_angle([0, 1, 0], [0, 0, 1]), 90)

if __name__ == "__main__":
    suite = unittest.makeSuite(TestFunctions)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
