import unittest
from selloff import SellStrategy
from selloff import SellOff

class MyTestCase(unittest.TestCase):
    def test_selloffs_top(self):
        so = SellOff(SellStrategy.SELL_THE_TOP, 1, 11, 1000, 20, None, 1.0)
        self.assertEqual(so.get_sell_thr(), 1.0)
        self.assertEqual(so.sell(), 10000)
        self.assertEqual(so.get_rem_tokens(), 0)
        self.assertEqual(so.set_sell_thr(None), 0.95)
        self.assertEqual(so.set_sell_thr(1.3), 0.95)
        self.assertEqual(so.set_sell_thr(0), 0.95)
        self.assertEqual(so.set_sell_thr(0.9), 0.9)
        self.assertEqual(so.sell(), 9000)

    def test_selloffs_linear(self):
        so = SellOff(SellStrategy.SELL_LINEAR, 1, 11, 1000, 0.2, 2.0, 1.0)
        self.assertEqual(so.get_sell_thr(), 1.0)
        so.set_selloffs(0)
        self.assertEqual(so.sell(), -1)
        so.set_selloffs(100)
        self.assertEqual(so.sell(), -1)
        so.set_selloffs(3)
        self.assertNotEqual(so.sell(), -1)
        so2 = SellOff(SellStrategy.SELL_LINEAR, 0, 100, 1000, 0.2, 2.0, 1.0)
        so2.set_selloffs(10)
        self.assertEqual(so2.sell(), 33893.87264)
        self.assertEqual(so.get_rem_tokens(), 107.37418240000005)

if __name__ == '__main__':
    unittest.main()
