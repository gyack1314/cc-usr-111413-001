"""既有来源接口及拒绝错误资料的测试。"""
import unittest,tempfile
from pathlib import Path
from common import read,money,number,release,latest
class CommonTests(unittest.TestCase):
    def test_precise_money_and_finite_measurement(self):
        self.assertEqual(money('0.1')+money('0.2'),money('0.3'))
        with self.assertRaises(ValueError):number(float('nan'))
        with self.assertRaises(ValueError):money(.1)
    def test_release_reuse_and_corruption(self):
        with tempfile.TemporaryDirectory() as folder:
            key=release(folder,{'x':1});self.assertEqual(release(folder,{'x':1}),key)
            Path(folder,key+'.json').write_text('{"x":2}')
            with self.assertRaises(ValueError):release(folder,{'x':1})

from assignment import draw
from weighing import prepared
class DomainTests(unittest.TestCase):
    def test_real_design_preserves_block_counts(self):
        d=read();z=draw(d,13)
        self.assertEqual(z,draw(d,13))
        for b in range(4):self.assertEqual(sum(z[f'c{i}'] for i in range(b*6,b*6+6)),3)
    def test_missing_is_separate_from_measured_zero(self):
        d=read();rows=prepared(d,40);self.assertGreater(rows[0]['missing_weighings'],0)
        d['weighings'][0]['waste_kg']=0;self.assertEqual(prepared(d,40)[0]['missing_weighings'],0)
        d['weighings'].append(dict(d['weighings'][0],waste_kg=99))
        with self.assertRaises(ValueError):prepared(d,40)
