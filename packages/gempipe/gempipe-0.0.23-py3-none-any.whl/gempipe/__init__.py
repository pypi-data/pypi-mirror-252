import argparse
import sys
import multiprocessing 
import logging 
from logging.handlers import QueueHandler
import traceback
import importlib.metadata


from .recon import recon_command
from .derive import derive_command
from .autopilot import autopilot_command


from .curate.gaps import *
from .curate.sanity import *
from .curate.medium import *
# set up the cobra solver


# cobra was already imported from other statements above
try: cobra.Configuration().solver = "cplex"
except:  cobra.Configuration().solver = "glpk" # "glpk_exact"


from .flowchart import Flowchart



def main(): 
    
    
    # define the header of main- and sub-commands. 
    pub_details = 'TODO'
    header = f'gempipe v{importlib.metadata.metadata("gempipe")["Version"]}, please cite "{pub_details}".\nFull documentation available at https://gempipe.readthedocs.io/en/latest/index.html.'
    
    
    # create the command line arguments:
    parser = argparse.ArgumentParser(description=header, add_help=False)
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-v", "--version", action="version", version=f"v{importlib.metadata.metadata('gempipe')['Version']}", help="Show version number and exit.")
    subparsers = parser.add_subparsers(title='gempipe subcommands', dest='subcommand', help='', required=True)

    
    # create the 3 subparsers:
    recon_parser = subparsers.add_parser('recon', description=header, help='Reconstruct a draft pan-model and a PAM.', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
    derive_parser = subparsers.add_parser('derive', description=header, help='Derive strain- and species-specific models.', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
    autopilot_parser = subparsers.add_parser('autopilot', description=header, help='Run recon + derive, with automated pan-model gap-filling. Use with consciousness!', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
    
    
    # add arguments for the 'derive' command
    derive_parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    derive_parser.add_argument("-v", "--version", action="version", version=f"v{importlib.metadata.metadata('gempipe')['Version']}", help="Show version number and exit.")
    derive_parser.add_argument("-c", "--cores", metavar='', type=int, default=1, help="How many parallel processes to use.")
    derive_parser.add_argument("-o", "--outdir", metavar='', type=str, default='./', help="Main output directory (will be created if not existing).")
    derive_parser.add_argument("--verbose", action='store_true', help="Make stdout messages more verbose, including debug messages.")
    derive_parser.add_argument("-im", "--inpanmodel", metavar='', type=str, default='-', help="Path to the input pan-model.")
    derive_parser.add_argument("-ip", "--inpam", metavar='', type=str, default='-', help="Path to the input PAM.")
    derive_parser.add_argument("-ir", "--inreport", metavar='', type=str, default='-', help="Path to the input report file.")
    derive_parser.add_argument("--minflux", metavar='', type=float, default=0.1, help="Minimum flux through the objective of strain-specific models.")
    
    
    # add arguments for the 'recon'/'autopilot' command
    for subparser in [recon_parser, autopilot_parser]:
        subparser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
        subparser.add_argument("-v", "--version", action="version", version=f"v{importlib.metadata.metadata('gempipe')['Version']}", help="Show version number and exit.")
        subparser.add_argument("-c", "--cores", metavar='', type=int, default=1, help="Number of parallel processes to use.")
        subparser.add_argument("-o", "--outdir", metavar='', type=str, default='./', help="Main output directory (will be created if not existing).")
        subparser.add_argument("--verbose", action='store_true', help="Make stdout messages more verbose, including debug messages.")
        subparser.add_argument("--overwrite", action='store_true', help="Delete the working/ directory at the startup.")
        subparser.add_argument("-t", "--taxids", metavar='', type=str, default='-', help="Taxids of the species to model (comma separated, for example '252393,68334').")
        subparser.add_argument("-g", "--genomes", metavar='', type=str, default='-', help="Input genome files or folder containing the genomes (see documentation).")
        subparser.add_argument("-p", "--proteomes", metavar='', type=str, default='-', help="Input proteome files or folder containing the proteomes (see documentation).")
        subparser.add_argument("-s", "--staining", metavar='', type=str, default='neg', help="Gram staining, 'pos' or 'neg'.")
        subparser.add_argument("-b", "--buscodb", metavar='', type=str, default='bacteria_odb10', help="Busco database to use ('show' to see the list of available databases).")
        subparser.add_argument("--buscoM", metavar='', type=str, default='2%', help="Maximum number of missing Busco's single copy orthologs (absolute or percentage).")
        subparser.add_argument("--ncontigs", metavar='', type=int, default=200, help="Maximum number of contigs allowed per genome.")
        subparser.add_argument("--N50", metavar='', type=int, default=50000, help="Minimum N50 allowed per genome.")
        subparser.add_argument("--identity", metavar='', type=int, default=30, help="Minimum percentage amino acidic sequence identity to use when aligning against the BiGG gene database.")
        subparser.add_argument("--coverage", metavar='', type=int, default=70, help="Minimum percentage coverage to use when aligning against the BiGG gene database.")
        subparser.add_argument("-rm", "--refmodel", metavar='', type=str, default='-', help="Model to be used as reference.")
        subparser.add_argument("-rp", "--refproteome", metavar='', type=str, default='-', help="Proteome to be used as reference.")
        subparser.add_argument("-mc", "--mancor", metavar='', type=str, default='-', help="Manual corrections to apply during the reference expansion.")
    
    
    # add arguments specifically for the 'autopilot' command
    autopilot_parser.add_argument("-m", "--media", metavar='', type=str, default='-', help="Medium definition file or folder containing media definitions, to be used during the automatic prioritized gap-filling.")
    autopilot_parser.add_argument("--minflux", metavar='', type=float, default=0.1, help="Minimum flux through the objective of strain-specific models.")
    

    # check the inputted subcommand, automatic sys.exit(1) if a bad subprogram was specied. 
    args = parser.parse_args()
    
    
    # set the multiprocessing context
    multiprocessing.set_start_method('fork') 
    
    
    # create a logging queue in a dedicated process.
    def logger_process_target(queue):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger('gempipe')
        logger.addHandler(handler)
        while True:
            message = queue.get() # block until a new message arrives
            if message is None: # sentinel message to exit the loop
                break
            logger.handle(message)
    queue = multiprocessing.Queue()
    logger_process = multiprocessing.Process(target=logger_process_target, args=(queue,))
    logger_process.start()
    
    
    # connect the logger for this (main) process: 
    logger = logging.getLogger('gempipe')
    logger.addHandler(QueueHandler(queue))
    if args.verbose: logger.setLevel(logging.DEBUG) # debug (lvl 10) and up
    else: logger.setLevel(logging.INFO) # debug (lvl 20) and up
    
    
    # show a welcome message:
    print('\n' + header + '\n', file=sys.stdout)
    command_line = '' # print the full command line:
    for arg, value in vars(args).items():
        if arg == 'subcommand': command_line = command_line + f"gempipe {value} "
        else: command_line = command_line + f"--{arg} {value} "
    print('Inputted command line: "' + command_line + '".\n')
    logger.info("Welcome to gempipe! Launching the pipeline...")
    

    try: 
        # choose which subcommand to lauch: 
        if args.subcommand == 'recon':
            response = recon_command(args, logger)
        if args.subcommand == 'derive':
            response = derive_command(args, logger)
        if args.subcommand == 'autopilot':
            response = autopilot_command(args, logger)
    except: 
        # show the error stack trace for this un-handled error: 
        response = 1
        logger.error(traceback.format_exc())


    # Terminate the program:
    if response == 1: 
        queue.put(None) # send the sentinel message
        logger_process.join() # wait for all logs to be digested
        sys.exit(1)
    else: 
        # show a bye message
        logger.info("gempipe terminated without errors!")
        queue.put(None) # send the sentinel message
        logger_process.join() # wait for all logs to be digested
        print('\n' + header + '\n', file=sys.stdout)
        sys.exit(0) # exit without errors
        
        
        
if __name__ == "__main__":
    main()
    
