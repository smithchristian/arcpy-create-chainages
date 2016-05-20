#-------------------------------------------------------------------------------
# Name:         Main.py
# Purpose:      This script creates chainages from a single or mutile line
#
# Author:      smithc5
#
# Created:     10/02/2015
# Copyright:   (c) smithc5 2015
# Licence:     <your licence>
#------------------------------------------------------------------------------

import os
import arcpy
import sys
import traceback
from modules import create_chainages

source_align_location = arcpy.GetParameterAsText(0)
#   Variable to store the location of the original source alignment.


database_location = arcpy.GetParameterAsText(1)
#   Variable to store the location where the database is created to store the.
#   feature classes.

chainage_distance = arcpy.GetParameterAsText(2)

new_fc_name = os.path.basename(source_align_location[:-4])
#    New name for the copied feature class. Original name minus file extension

database_name = "{}.gdb".format(new_fc_name)
#    Variable to store the name of the .gdb to store the feature classes.

DATABASE_FLIEPATH = os.path.join(database_location, database_name)

new_fc_filepath = os.path.join(DATABASE_FLIEPATH, new_fc_name)
#    New file path to the copied feature class

new_fc_filepath_with_m = "{0}_M".format(new_fc_filepath)
#    New file path to the copied feature class

chainage_feature_class = "{0}_Chainages".format(new_fc_filepath)
#   This is the output feature class to store the chainages.



def main():

    try:

        create_chainages.check_if_gdb_exist(DATABASE_FLIEPATH)

        create_chainages.create_gdb(database_location, database_name)

        create_chainages.copy_features(source_align_location, new_fc_filepath)

        create_chainages.create_route(new_fc_filepath, "Name", new_fc_filepath_with_m)

        create_chainages.create_chainages(new_fc_filepath_with_m, chainage_distance,
                                          database_location, new_fc_filepath_with_m,
                                          DATABASE_FLIEPATH, chainage_feature_class)

    except:

        tb = sys.exc_info()[2]

        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\nTraceback Info:\n{0}\nError Info:\n     {1}: {2}\n".format(tbinfo,
                                                                                             str(sys.exc_type),
                                                                                             str(sys.exc_value))
        msgs = "ARCPY ERRORS:\n{}\n".format(arcpy.GetMessages(2))

        arcpy.AddError(msgs)

        arcpy.AddError(pymsg)

        print msgs

        print pymsg

        arcpy.AddMessage(arcpy.GetMessages(1))

        print arcpy.GetMessages(1)

if __name__ == '__main__':
    main()
