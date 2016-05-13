# -------------------------------------------------------------------------------
# Name:         create_chainges.py
# Purpose:      This project has been designend to create chainages from a polyline
# 				shapefile.
#
# Author:      Christian Smith
#
# Created:     24/04/2016
# Copyright:   (c) smithc5 2015
# Licence:     <your licence>
# ------------------------------------------------------------------------------
import arcpy
import os


def check_if_gdb_exist(db_filepath):
    """ Checks to see the if .gdb exist. If true, the .gdb is deleted

    Keyword arguments:
       db_filepath -- Full file path to the .gdb
    """

    arcpy.AddMessage("....Checking to see if Basedata.gdb exist")
    #    Prints message to screen

    if arcpy.Exists(db_filepath):
        #    Check to see if the file path exist. If true, the file is deleted

        arcpy.Delete_management(db_filepath)
        #    Deletes file

        arcpy.AddMessage(".......Existing Basedata.gdb - Deleted")
        #    Prints message to screen


def create_gdb(db_output_location, db_name):
    """ Creates the gdb to store the feature classes

    Keyword arguments:
        db_output_location --  Location of gdb to store feature classes
        db_name -- Name of the gdb
    """
    arcpy.AddMessage(db_output_location)
    arcpy.AddMessage(db_name)
    arcpy.AddMessage("....Creating New Database")
    #    Prints message to screen

    arcpy.CreateFileGDB_management(db_output_location, db_name)
    #    Creates the gdb

    arcpy.AddMessage(".......Finished Creating Database")
    #    Prints message to screen


def copy_features(original_fc_alignment, db_filepath):
    """ Copies original feature class to gdb

    Keyword arguments:
        original_fc_alignment -- The file path to the original alignment feature class
        db_filepath -- Full file path to the .gdb
    """

    arcpy.AddMessage("....Copying feature class")
    #    Prints message to screen

    arcpy.CopyFeatures_management(original_fc_alignment, db_filepath)
    #    Copies feature to the new .gdb

    arcpy.AddMessage(".......Finished Copying feature class")
    #    Prints message to screen


def create_route(in_line_features, route_id_field, out_feature_class):
    """ Create a measured route for the new feature class

    Keyword arguments:
        in_line_features -- The features from which routes will be created.
        route_id_field -- The "Name" field containing values that uniquely identify each route.
        out_feature_class -- The feature class to be created.
    """
    arcpy.AddMessage("....Creating measured route")
    #    Prints message to screen

    arcpy.AddField_management(in_line_features, "Start", "SHORT", "", "", "", "", "", "", "")
    #   Adds a field to the attribute table

    cursor = arcpy.UpdateCursor(in_line_features)
    #   Creates a cursor for updating the attribute table

    start_value = 0
    # Variable to store the start measurement

    for row in cursor:

        row.setValue("Start", start_value)

        cursor.updateRow(row)

    del cursor
    # Deletes update cursor

    arcpy.CreateRoutes_lr(in_line_features, route_id_field, out_feature_class, "TWO_FIELDS", "Start", "Shape_Length")
    #    Creates a measured route

    arcpy.AddMessage(".......Finished creating measured route")
    #    Prints message to screen


def create_chainages(line_lyr, pnt_dist, db_output_location, fc_sr_discribe, db_filepath, chainage_fc):
    """ Creates 100m chainages from the measured route alignment

    Keyword arguments:
        line_lyr (feature layer) -- Single part line
        pnt_dist (integer) -- Interval distance in map units as the distance between chainages
        db_output_location -- File path to the .gdb
        fc_sr_discribe -- File path to the feature class used to identify the spatial reference
        db_filepath -- Full file path to the .gdb
        chainages_fc -- This is the output feature class to store the chainages

    """
    arcpy.AddMessage(line_lyr)
    arcpy.AddMessage(pnt_dist)
    arcpy.AddMessage(db_output_location)
    arcpy.AddMessage(fc_sr_discribe)
    arcpy.AddMessage(db_filepath)
    arcpy.AddMessage(chainage_fc)

    arcpy.AddMessage("....Creating points to split line")
    #    Prints message to screen

    points_to_splitline_fc_temp = os.path.join(db_output_location, "points_to_splitline_fc_temp.shp")
    #    Local Variable to store the points used to split the line with . This is to be deleted later

    chainage_fc_temp = os.path.join(db_output_location, "chainage_fc_temp.shp")
    #    Local temp variable to store processed data - Will be deleted
    #    Have used .shp instead of feature class in gdb due to issues with adding attributes

    chainage_fc_tempv2 = os.path.join(db_output_location, "chainage_fc_tempv2.shp")
    #    Local temp variable to store processed data - Will be deleted
    #    Have used .shp instead of feature class in gdb due to issues with adding attributes

    describe_fc = arcpy.Describe(fc_sr_discribe)
    #    Gets the description of the alignment. This is used to get the spatial reference to
    #    assign to the temp point feature class

    spatial_reference = describe_fc.spatialReference
    #    Local variable to store the spatial reference

    arcpy.CreateFeatureclass_management(os.path.dirname(points_to_splitline_fc_temp),
                                        os.path.basename(points_to_splitline_fc_temp),
                                        'POINT', '#', '#', '#', spatial_reference)
    #    Create the temp point feature class to store the chainages

    search_cursor = arcpy.da.SearchCursor(line_lyr, 'SHAPE@')
    #    Search cursor used to pull out shapes geoometry

    insert_cursor = arcpy.da.InsertCursor(points_to_splitline_fc_temp, 'SHAPE@')
    #    Insert cursor used to insert geometery into temp point feature class

    for row in search_cursor:

        # TODO delete multi-line comments below when happy with code
        '''
        #interval_list = [x * float(pnt_dist) for x in range(0, (int(row[0].length)/pnt_dist))]
        '''
        interval_list = [x * float(pnt_dist) for x in range(0, int((row[0].length)/float(pnt_dist)+1))]

        for dist in interval_list:

            point = row[0].positionAlongLine(dist).firstPoint

            insert_cursor.insertRow([point])

        '''
        for dist in range(0, int(row[0].length), float(pnt_dist)):

            point = row[0].positionAlongLine(dist).firstPoint

            insert_cursor.insertRow([point])
        '''

    #    This is used to create points/chainages at specified distance

    del search_cursor
    #    Deletes the search cursor

    del insert_cursor
    #    Deletes the insert cursor

    arcpy.AddMessage(".......Finished creating points to split line")

    arcpy.AddMessage(".....Splitting line")

    splitline_fc_temp = os.path.join(db_filepath, "splitline_fc_temp")
    #    Local Variable to store the split line. This is to be deleted later

    arcpy.SplitLineAtPoint_management(line_lyr, points_to_splitline_fc_temp, splitline_fc_temp, "1 METERS")
    #    Method used to split the alignment based on points

    arcpy.Delete_management(points_to_splitline_fc_temp)
    #    Deletes temp split line feature class points_to_splitline_fc_temp

    arcpy.AddMessage("........Finished splitting line")

    arcpy.AddMessage(".....Creating chainages")

    arcpy.FeatureVerticesToPoints_management(splitline_fc_temp, chainage_fc_temp, "BOTH_ENDS")
    #    Method used to create start and end points of each line

    arcpy.Delete_management(splitline_fc_temp)
    #    Deletes temp split line feature class splitline_fc_temp

    arcpy.AddField_management(chainage_fc_temp, "Filter", "TEXT", "", "", 100)

    arcpy.AddXY_management(chainage_fc_temp)
    #    Adds geometries x y z m values. This is used to create a unique value to be
    #    used in dissolve function.

    cursor2 = arcpy.UpdateCursor(chainage_fc_temp)

    for row in cursor2:

        point_x = row.getValue("POINT_X")

        point_y = row.getValue("POINT_Y")

        my_string = "{0}{1}".format(point_x, point_y)

        row.setValue("Filter", my_string)

        cursor2.updateRow(row)

    del cursor2
    # Deletes update cursor

    dissolve_fields = ["Filter"]
    #    Name of field attribute to use in dissolve function

    arcpy.AddMessage(".....Dissolving double-ups of chainages")

    arcpy.Dissolve_management(chainage_fc_temp, chainage_fc_tempv2, dissolve_fields)
    #    Dissolve is used to remove duplicate points

    arcpy.Delete_management(chainage_fc_temp)
    #    Deletes temporary file

    arcpy.AddXY_management(chainage_fc_tempv2)
    #    Adds geometries x y z m values

    arcpy.AddMessage(".....Sorting chainages based on distance")

    arcpy.Sort_management(chainage_fc_tempv2, chainage_fc, [["POINT_M", "ASCENDING"]])

    arcpy.AddMessage("........Finished sorting chainages")

    arcpy.Delete_management(chainage_fc_tempv2)
    #    Deletes temporary file

    arcpy.AddMessage(".....Labeling chainages")

    arcpy.AddField_management(chainage_fc, "Label", "TEXT", "", "", 100)

    cursor3 = arcpy.UpdateCursor(chainage_fc)

    for row in cursor3:

        point_m = row.getValue("POINT_M")

        chainage = "{0}".format(point_m)

        row.setValue("Label", chainage)

        cursor3.updateRow(row)

    del cursor3
