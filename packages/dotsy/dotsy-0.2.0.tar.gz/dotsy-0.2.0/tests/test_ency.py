import pickle
import unittest
from .helper.encyTest import encyTest, encyTestSimple

class test_ency(unittest.TestCase):
    def test(self):
        ef = encyTest()
        ef.selfTest(self)
        
            
    def test_readwriteSimple(self):

        ef = encyTestSimple()

        js = pickle.dumps(ef)
        ef2 = pickle.loads(js)

        self.assertEqual(ef2.dot1["a"], ef.dot1["a"])
        self.assertEqual(ef2.dot1["b"], ef.dot1["b"])

    def test_readwrite(self):

        ef = encyTest()

        js = pickle.dumps(ef)
        ef2 = pickle.loads(js)

        ef.selfTest(self)
        ef2.selfTest(self)


if __name__ == '__main__':
    unittest.main()
