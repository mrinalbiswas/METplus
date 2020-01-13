"""
PCPCombine Bucket Interval
==========================

This use case will run the MET PCPCombine tool in ADD mode to build a 15 hour accumulation field from precipitation accumulation data that dumps the buckets at regular intervals.

"""
##############################################################################
# Scientific Objective
# --------------------
#
# Build a 15 hour precipitation accumulation field from varying accumulation fields.
#

##############################################################################
# Datasets
# --------
#
# | **Forecast:** GFS precipitation accumulation
#
# | **Location:** All of the input data required for this use case can be found in the sample data tarball. Click here to download: https://github.com/NCAR/METplus/releases/download/v2.2/sample_data-met_test-8.1.tgz
# | This tarball should be unpacked into the directory that you will set the value of INPUT_BASE. See 'Running METplus' section for more information.
#
# | **Data Source:** GFS

##############################################################################
# METplus Components
# ------------------
#
# This use case utilizes the METplus PCPCombine wrapper to search for files to build the desired accumulation for a given run time
# using a filename template and a list of available input accumulations. If enough files meeting the criteria are found to build
# the output accumulation, it will generate a command to run PCPCombine to combine the data.

##############################################################################
# METplus Workflow
# ----------------
#
# PCPCombine is the only tool called in this example. It processes the following
# run times:
#
# | **Valid:** 2012-04-09_00Z
# | **Forecast lead:** 15 hour

##############################################################################
# METplus Configuration
# ---------------------
#
# METplus first loads all of the configuration files found in parm/metplus_config,
# then it loads any configuration files passed to METplus via the command line
# with the -c option, i.e. -c parm/use_cases/met_tool_wrapper/PCPCombine/pcp_bucket.conf
#
# .. highlight:: bash
# .. literalinclude:: ../../../../parm/use_cases/met_tool_wrapper/PCPCombine/pcp_bucket.conf

##############################################################################
# MET Configuration
# ---------------------
#
# None. PCPCombine does not use configuration files.
#

##############################################################################
# Running METplus
# ---------------
#
# This use case can be run two ways:
#
# 1) Passing in pcp_bucket.conf then a user-specific system configuration file::
#
#        master_metplus.py -c /path/to/METplus/parm/use_cases/met_tool_wrapper/PCPCombine/pcp_bucket.conf -c /path/to/user_system.conf
#
# 2) Modifying the configurations in parm/metplus_config, then passing in pcp_bucket.conf::
#
#        master_metplus.py -c /path/to/METplus/parm/use_cases/met_tool_wrapper/PCPCombine/pcp_bucket.conf
#
# The former method is recommended. Whether you add them to a user-specific configuration file or modify the metplus_config files, the following variables must be set correctly:
#
# * **INPUT_BASE** - Path to directory where sample data tarballs are unpacked (See Datasets section to obtain tarballs). This is not required to run METplus, but it is required to run the examples in parm/use_cases
# * **OUTPUT_BASE** - Path where METplus output will be written. This must be in a location where you have write permissions
# * **MET_INSTALL_DIR** - Path to location where MET is installed locally
#
# Example User Configuration File::
#
#   [dir]
#   INPUT_BASE = /path/to/sample/input/data
#   OUTPUT_BASE = /path/to/output/dir
#   MET_INSTALL_DIR = /path/to/met-X.Y 
#
# **NOTE:** All of these items must be found under the [dir] section.
#

##############################################################################
# Expected Output
# ---------------
#
# A successful run will output the following both to the screen and to the logfile::
#
#   INFO: METplus has successfully finished running.
#
# Refer to the value set for **OUTPUT_BASE** to find where the output data was generated.
# Output for this use case will be found in pcp_combine_bucket_interval (relative to **OUTPUT_BASE**)
# and will contain the following files:
#
# * gfs_2012040915_A015.nc
#

##############################################################################
# Keywords
# --------
#
# .. note:: `PCPCombineUseCase <https://ncar.github.io/METplus/search.html?q=PCPCombineUseCase&check_keywords=yes&area=default>`_
