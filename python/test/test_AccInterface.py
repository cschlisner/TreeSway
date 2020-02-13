import unittest
import TreeSway
from TreeSway import AccInterface
from TreeSway.AccInterface import SerialAcc


class TestAccelerometerInterface(unittest.TestCase):
    def test_acc_init(self):
        dev = SerialAcc()
        self.assertTrue(dev is not None)
        