import unittest, os, sys

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
        self.assertFalse(agrc.update.checkForChanges(r'C:\MapData\SGID10.gdb\DNROilGasFields', r'Z:\Documents\Projects\agrc\tests\data\SGID10.sde\SGID10.ENERGY.DNROilGasFields'))
        self.assertFalse(agrc.update.checkForChanges(r'C:\MapData\SGID10.gdb\Parcels_SaltLake', r'Z:\Documents\Projects\agrc\tests\data\SGID10.sde\SGID10.CADASTRE.Parcels_SaltLake'))
        self.assertFalse(agrc.update.checkForChanges(r'Z:\Documents\Projects\agrc\tests\data\checkForChanges2.gdb\SpringsNHDHighRes', r'Z:\Documents\Projects\agrc\tests\data\SGID10.sde\SGID10.WATER.SpringsNHDHighRes'))
        self.assertFalse(agrc.update.checkForChanges(r'Z:\Documents\Projects\agrc\tests\data\checkForChanges.gdb\DNROilGasWells', r'Z:\Documents\Projects\agrc\tests\data\SGID10.sde\SGID10.ENERGY.DNROilGasWells'))
        self.assertFalse(agrc.update.checkForChanges(r'Z:\Documents\Projects\agrc\tests\data\SGID10.sde\SGID10.CADASTRE.Parcels_Cache', r'Z:\Documents\Projects\agrc\tests\data\checkForChanges.gdb\Parcels_Cache'))
        self.assertFalse(agrc.update.checkForChanges(r'Z:\Documents\Projects\agrc\tests\data\SGID10.sde\SGID10.CADASTRE.Parcels_Summit', r'Z:\Documents\Projects\agrc\tests\data\checkForChanges.gdb\Parcels_Summit'))
        
    def test_filter_shape_fields(self):
        self.assertEquals(agrc.update.filter_fields(['shape', 'test', 'Shape_length', 'Global_ID']), ['test'])