import unittest
from dotsy import Dicy
import pickle

class test_dicy(unittest.TestCase):
    def test(self):
        d = Dicy()
        with self.assertRaises(AttributeError):
            d.a
            
        d["a"] = 1
        self.assertEqual(d.a, 1)
        self.assertEqual(d["a"], 1)
        
        d.b = 2
        self.assertEqual(d.b, 2)
        self.assertEqual(d["b"], 2)
        
        
        del d.a
        with self.assertRaises(AttributeError):
            d.a

        del d.b
        with self.assertRaises(AttributeError):
            d.b


    def test_readwrite(self):
        d = Dicy()
        d.a = 1
        d.b = 2
        d.c = Dicy()
        d.c.d = 3

        s = pickle.dumps(d)
        d2 = pickle.loads(s)

        self.assertEqual(d2.a, d.a)
        self.assertEqual(d2.b, d.b)
        self.assertEqual(d2.c.d, d.c.d)
        

if __name__ == '__main__':
    unittest.main()
