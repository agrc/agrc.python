import unittest
import os
import sys

currentFolder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFolder + '/../..')
import agrc.update


class UpdateTest(unittest.TestCase):
    def test_checkForChanges(self):
        def run(fc1, fc2):
            f1 = os.path.join(currentFolder, 'data\checkForChanges.gdb', fc1)
            f2 = os.path.join(currentFolder, 'data\checkForChanges.gdb', fc2)
            return agrc.update.checkForChanges(f1, f2)

        self.assertFalse(run('ZipCodes', 'ZipCodes_same'))
        self.assertTrue(run('ZipCodes', 'ZipCodes_geoMod'))
        self.assertTrue(run('ZipCodes', 'ZipCodes_attMod'))
        self.assertTrue(run('ZipCodes', 'ZipCodes_newFeature'))

    def test_filter_shape_fields(self):
        self.assertEquals(agrc.update.filter_fields(['shape', 'test', 'Shape_length', 'Global_ID']), ['test'])
