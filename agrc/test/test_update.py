import unittest
import os
import sys
import arcpy

currentFolder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFolder + '/../..')
from agrc import update

checkForChangesGDB = os.path.join(currentFolder, 'data', 'checkForChanges.gdb')
checkForChangesGDB2 = os.path.join(currentFolder, 'data', 'checkForChanges2.gdb')
updateTestsSDE = os.path.join(currentFolder, 'data', 'UPDATE_TESTS.sde')


def runCheckForChanges(fc1, fc2):
    f1 = os.path.join(checkForChangesGDB, fc1)
    f2 = os.path.join(checkForChangesGDB, fc2)
    return update.checkForChanges(f1, f2, False)


class UpdateTest(unittest.TestCase):
    def test_checkForChanges(self):

        self.assertFalse(runCheckForChanges('ZipCodes', 'ZipCodes_same'))
        self.assertTrue(runCheckForChanges('ZipCodes', 'ZipCodes_geoMod'))
        self.assertTrue(runCheckForChanges('ZipCodes', 'ZipCodes_attMod'))
        self.assertTrue(runCheckForChanges('ZipCodes', 'ZipCodes_newFeature'))

    def test_checkForChangesNullDateFields(self):
        self.assertTrue(runCheckForChanges('NullDates', 'NullDates2'))

    def test_filter_shape_fields(self):
        self.assertEquals(update.filter_fields(['shape', 'test', 'Shape_length', 'Global_ID']), ['test'])

    def test_no_updates(self):
        testGDB = os.path.join(currentFolder, 'Test.gdb')
        if arcpy.Exists(testGDB):
            arcpy.Delete_management(testGDB)
        arcpy.Copy_management(checkForChangesGDB2, testGDB)

        changes = update.updateFGDBfromSDE(testGDB, updateTestsSDE)[1]

        self.assertEquals(len(changes), 0)

    def test_update_tables(self):
        testGDB = os.path.join(currentFolder, 'Test.gdb')
        if arcpy.Exists(testGDB):
            arcpy.Delete_management(testGDB)
        arcpy.Copy_management(checkForChangesGDB, testGDB)

        changes = update.updateFGDBfromSDE(testGDB, updateTestsSDE)[1]

        self.assertEquals(changes[0], 'PROVIDERS')
