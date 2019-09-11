#!/usr/bin/env python

"""
Program Name: master_metplus.py
Contact(s): George McCabe, Julie Prestopnik, Jim Frimel, Minna Win
Abstract: Runs METplus Wrappers scripts
History Log:  Initial version
Usage:
Parameters: None
Input Files:
Output Files:
Condition codes:
"""

from __future__ import print_function

import os
import sys

py_version = sys.version.split(' ')[0]
if py_version < '3.6.3':
    print("Must be using Python 3.6.3 or higher. You are using {}".format(py_version))
    exit(1)

import logging
import shutil
import produtil.setup
import met_util as util
import config_metplus

# wrappers are referenced dynamically based on PROCESS_LIST values
# import of each wrapper is required
# pylint:disable=unused-import
from ensemble_stat_wrapper import EnsembleStatWrapper
from pcp_combine_wrapper import PcpCombineWrapper
from grid_stat_wrapper import GridStatWrapper
from regrid_data_plane_wrapper import RegridDataPlaneWrapper
from tc_pairs_wrapper import TcPairsWrapper
from extract_tiles_wrapper import ExtractTilesWrapper
from series_by_lead_wrapper import SeriesByLeadWrapper
from series_by_init_wrapper import SeriesByInitWrapper
from stat_analysis_wrapper import StatAnalysisWrapper
from make_plots_wrapper import MakePlotsWrapper
from mode_wrapper import ModeWrapper
from mtd_wrapper import MTDWrapper
from usage_wrapper import UsageWrapper
from command_builder import CommandBuilder
from tcmpr_plotter_wrapper import TCMPRPlotterWrapper
# Keep cyclone_plotter commented out in repository. It requires cartopy
# If cartopy is not present then master_metplus will error and exit.
# from cyclone_plotter_wrapper import CyclonePlotterWrapper
from pb2nc_wrapper import PB2NCWrapper
from point_stat_wrapper import PointStatWrapper
from tc_stat_wrapper import TcStatWrapper
from gempak_to_cf_wrapper import GempakToCFWrapper
from example_wrapper import ExampleWrapper

'''!@namespace master_metplus
Main script the processes all the tasks in the PROCESS_LIST
'''

def main():
    """!Main program.
    Master METplus script that invokes the necessary Python scripts
    to perform various activities, such as series analysis."""
    # Setup Task logger, Until Conf object is created, Task logger is
    # only logging to tty, not a file.
    logger = logging.getLogger('master_metplus')
    logger.info('Starting METplus v%s', util.get_version_number())

    # Parse arguments, options and return a config instance.
    config = config_metplus.setup(filename='master_metplus.py')

    # NOW we have a conf object p, we can now get the logger
    # and set the handler to write to the LOG_METPLUS
    # TODO: Frimel setting up logger file handler.
    # Setting up handler i.e util.get_logger should be moved to
    # the setup wrapper and encapsulated in the config object.
    # than you would get it this way logger=p.log(). The config
    # object has-a logger we want.
    logger = util.get_logger(config)

    logger.info('Running METplus v%s called with command: %s',
                util.get_version_number(), ' '.join(sys.argv))

    # check for deprecated config items and warn user to remove/replace them
    util.check_for_deprecated_config(config, logger)

    util.check_user_environment(config)

    # set staging dir to OUTPUT_BASE/stage if not set
    if not config.has_option('dir', 'STAGING_DIR'):
        config.set('dir', 'STAGING_DIR',
                   os.path.join(config.getdir('OUTPUT_BASE'), "stage"))

    # handle dir to write temporary files
    util.handle_tmp_dir(config)

    config.env = os.environ.copy()

    # Use config object to get the list of processes to call
    process_list = util.getlist(config.getstr('config', 'PROCESS_LIST'))

    # Keep this comment.
    # When running commands in the process_list, reprocess the
    # original command line using (item))[sys.argv[1:]].
    #
    # You could call each task (ie. run_tc_pairs.py) without any args since
    # the final METPLUS_CONF file was just created from config_metplus.setup,
    # and each task, also calls setup, which use an existing final conf
    # file over command line args.
    #
    # both work ...
    # Note: Using (item))sys.argv[1:], is preferable since
    # it doesn't depend on the conf file existing.
    processes = []
    for item in process_list:
        try:
            logger = config.log(item)
            command_builder = \
                getattr(sys.modules[__name__],
                        item + "Wrapper")(config, logger)
            # if Usage specified in PROCESS_LIST, print usage and exit
            if item == 'Usage':
                command_builder.run_all_times()
                exit(1)
        except AttributeError:
            raise NameError("Process %s doesn't exist" % item)

        processes.append(command_builder)

    loop_order = config.getstr('config', 'LOOP_ORDER', '')
    if loop_order == '':
        loop_order = config.getstr('config', 'LOOP_METHOD')

    if loop_order == "processes":
        for process in processes:
            # referencing using repr(process.app_name) in
            # log since it may be None,
            # if not set in the command builder subclass' contsructor,
            # and no need to generate an exception because of that.
            produtil.log.postmsg('master_metplus Calling run_all_times '
                                 'in: %s wrapper.' % repr(process.app_name))
            process.run_all_times()

    elif loop_order == "times":
        util.loop_over_times_and_call(config, processes)

    else:
        logger.error("Invalid LOOP_METHOD defined. " + \
              "Options are processes, times")
        exit()

    # scrub staging directory if requested
    if config.getbool('config', 'SCRUB_STAGING_DIR', False) and\
       os.path.exists(config.getdir('STAGING_DIR')):
        staging_dir = config.getdir('STAGING_DIR')
        logger.info("Scrubbing staging dir: %s", staging_dir)
        shutil.rmtree(staging_dir)

    # rewrite final conf so it contains all of the default values used
    util.write_final_conf(config, logger)

    logger.info('METplus has successfully finished running.')

    exit()

if __name__ == "__main__":
    try:
        # If jobname is not defined, in log it is 'NO-NAME'
        if 'JLOGFILE' in os.environ:
            produtil.setup.setup(send_dbn=False, jobname='run-METplus',
                                 jlogfile=os.environ['JLOGFILE'])
        else:
            produtil.setup.setup(send_dbn=False, jobname='run-METplus')

        main()
    except Exception as exc:
        produtil.log.jlogger.critical(
            'master_metplus  failed: %s' % (str(exc),), exc_info=True)
        sys.exit(2)
