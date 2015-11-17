import arcpy


def DeleteIfExists(datasets):
    # deletes all of the things in the datasets list
    for ds in datasets:
        if arcpy.Exists(ds):
            arcpy.Delete_management(ds)


def FindFeatureClassInSDE(fcName, SDE):
    # searches through SDE to find a matching feature class
    arcpy.env.workspace = SDE

    # look in standalone feature classes
    list = arcpy.ListFeatureClasses("*." + fcName)
    if len(list) > 0:
        return SDE + "\\" + list[0]

    # look in datasets
    dss = arcpy.ListDatasets()
    if len(dss) > 0:
        # loop through datasets
        for ds in dss:
            list = arcpy.ListFeatureClasses("*." + fcName, None, ds)
            if len(list) > 0:
                return SDE + "\\" + list[0]

    raise Exception("Could not find {0} in {1}".format(fcName, SDE))
