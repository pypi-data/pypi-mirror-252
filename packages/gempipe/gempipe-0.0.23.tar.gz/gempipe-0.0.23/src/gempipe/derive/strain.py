import multiprocessing
import itertools
import os
import shutil


import cobra


from ..commons import chunkize_items
from ..commons import load_the_worker
from ..commons import gather_results



def task_derivestrain(accession, args):
    
    
    # get the arguments
    panmodel = args['panmodel']
    pam = args['pam']
    report = args['report']
    outdir = args['outdir']
    
    
    # define key objects: 
    ss_model = panmodel.copy()  # create strain specific model
    modeled_gids = [g.id for g in panmodel.genes]  # get medoled genes ID
    to_remove = []  # genes to delete
    
    
    # iterate the PAM :
    for cluster in pam.index: 
        # consider only if it is modeled:
        if cluster in modeled_gids: 
            cell = pam.loc[cluster, accession]
            if type(cell) == float:  # empty cell
                to_remove.append(ss_model.genes.get_by_id(cluster))
                continue
            # get all the sequences not containing a premature stop:
            seqs = [i for i in cell.split(';') if i.endswith('_stop')==False]
            if len(seqs) == 0:  # they were all '_stop' sequences.
                to_remove.append(ss_model.genes.get_by_id(cluster))
                continue
    
    
    # delete marked genes
    cobra.manipulation.delete.remove_genes(ss_model, to_remove, remove_reactions=True)
    
    
    # get the associated species:
    report = report[report['accession'] == accession]
    if len(report) > 1: 
        logger.error("Duplicated accessions in the provided report. Please report this error to the developer.")
    report = report.reset_index(drop=True)
    species = report.loc[0, 'species']
    
    
    # get some metrics: 
    n_G = len(ss_model.genes)
    n_R = len(ss_model.reactions)
    n_M = len(ss_model.metabolites)
    
    
    # try the FBA: 
    res = ss_model.optimize()
    obj_value = res.objective_value
    status = res.status
    
    
    # save strain specific model to disk
    cobra.io.save_json_model(ss_model, f'{outdir}/{accession}.json')
    
    
    # compose the new row:
    return [{'accession': accession, 'species': species, 'G': n_G, 'R': n_R, 'M': n_M, 'obj_value': obj_value, 'status': status }]



def  derive_strain_specific(logger, outdir, cores, panmodel, pam, report):

    
    # log some messages
    logger.info("Deriving strain-specific models...")
    
   
    # create output dir
    if os.path.exists(outdir + 'strain_models/'):
        # always overwriting if already existing
        shutil.rmtree(outdir + 'strain_models/')  
    os.makedirs(outdir + 'strain_models/', exist_ok=True)
    

    # create items for parallelization: 
    items = []
    for accession in pam.columns:
        items.append(accession)
        
        
    # randomize and divide in chunks: 
    chunks = chunkize_items(items, cores)
    
    
    # initialize the globalpool:
    globalpool = multiprocessing.Pool(processes=cores, maxtasksperchild=1)
    
    
    # start the multiprocessing: 
    results = globalpool.imap(
        load_the_worker, 
        zip(chunks, 
            range(cores), 
            itertools.repeat(['accession', 'G', 'R', 'M', 'obj_value', 'status']), 
            itertools.repeat('accession'), 
            itertools.repeat(logger), 
            itertools.repeat(task_derivestrain),  # will return a new sequences dataframe (to be concat).
            itertools.repeat({'panmodel': panmodel, 'pam': pam, 'report': report, 'outdir': outdir + 'strain_models'}),
        ), chunksize = 1)
    all_df_combined = gather_results(results)
    
    
    # empty the globalpool
    globalpool.close() # prevent the addition of new tasks.
    globalpool.join() 
    
    
    # save tabular output:
    all_df_combined.to_csv(outdir + 'derive_strains.csv')
    
    
    return 0