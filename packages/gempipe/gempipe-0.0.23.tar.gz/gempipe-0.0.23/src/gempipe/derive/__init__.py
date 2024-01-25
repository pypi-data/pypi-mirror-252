import os


import pandas as pnd
import cobra 


from .strain import derive_strain_specific
from .filler import strain_filler
from .species import derive_rpam
from .species import derive_species_specific



def derive_all(logger, outdir, cores, panmodel, pam, report, minflux):
    
    
    ### PART 1: derive strain-specific models
    
    response = derive_strain_specific(logger, outdir, cores, panmodel, pam, report)
    if response == 1: return 1


    ### PART 2: gap-fill strain-specific models
    
    response = strain_filler(logger, outdir, cores, panmodel, minflux)
    if response == 1: return 1
    
    
    ### PART 3: derive species-specific models
    
    response = derive_rpam(logger, outdir, cores, panmodel)
    if response == 1: return 1
    
    response = derive_species_specific(logger, outdir, cores, panmodel)
    if response == 1: return 1


    return 0



def derive_command(args, logger):
    
    
    # check the existence of the input files:
    if args.inpanmodel == '-' or args.inpam == '-' or args.inreport == '-':
        logger.error("Please specify the input pan-model (-im/--inpanmodel), PAM (-ip/--inpam) and report (-ir/--inreport).")
        return 1
    else:  # all 3 parameters were set
        if not os.path.exists(args.inpanmodel):
            logger.error(f"The specified path for input pan-model (-im/--inpanmodel) does not exist: {args.inpanmodel}.")
            return 1
        if not os.path.exists(args.inpam):
            logger.error(f"The specified path for input PAM (-ip/--inpam) does not exist: {args.inpam}.")
            return 1
        if not os.path.exists(args.inreport):
            logger.error(f"The specified path for input report (-ir/--inreport) does not exist: {args.inreport}.")
            return 1
    
    
    # load input files
    logger.info("Loading input files...")
    panmodel = cobra.io.load_json_model(args.inpanmodel)
    pam = pnd.read_csv(args.inpam, index_col=0)
    report = pnd.read_csv(args.inreport, index_col=0)
    
    
    # create the main output directory: 
    outdir = args.outdir
    if outdir.endswith('/') == False: outdir = outdir + '/'
    os.makedirs(outdir, exist_ok=True)
    
    
    logger.info("Deriving strain- and species specific metabolic models...")
    response = derive_all(logger, outdir, args.cores, panmodel, pam, report, args.minflux)
    if response == 1: return 1
    
    
    return 0
