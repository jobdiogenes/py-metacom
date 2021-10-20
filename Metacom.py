import numpy as np
import pandas as pd
import progressbar
from fanalysis.ca import CA

m = pd.read_csv("~/Dropbox/develop/julia/example.tsv",delimiter='\t') 

def Coherence(comm, method= "r1", sims=100, scores=1, order=True, orderNulls=False, 
              allowEmpty=False, binary=True, verbose=False, seed=1):
    
    def coherence(web):
        zeros = np.argwhere(web==0)
        ret = np.zeros((1,2),dtype=np.int) 
        uncols = np.argwhere(web.sum(axis=0)>1)
        for i in range(0,len(uncols)):
            temp =  zeros[zeros[:,1] == uncols[i]] 
            tempmin = min(np.argwhere(web[:,uncols[i,0]]==1))
            tempmax = max(np.argwhere(web[:,uncols[i,0]]==1))
            if (len(temp)<3):
                if tempmin<=temp[i,0] <=tempmax:
                   ret = np.vstack((ret,temp)) 
            else:
                temp = temp[(temp[:,0] >= tempmin) & (temp[:,0]<=tempmax),:]
                ret = np.vstack((ret,temp))
                
        unrows = np.argwhere(web.sum(axis=1)>1)
        for j in range(0,len(uncols)):
            temp =  zeros[zeros[:,1] == unrows[j]] 
            tempmin = min(np.argwhere(web[:,unrows[j,0]]==1))
            tempmax = max(np.argwhere(web[:,unrows[j,0]]==1))
            if (len(temp)<3):
                if tempmin<=temp[j,0] <=tempmax:
                   ret = np.vstack((ret,temp)) 
            else:
                temp = temp[(temp[:,0] >= tempmin) & (temp[:,0]<=tempmax),:]
                ret = np.vstack((ret,temp))
        ret = ret[1:,:]
        ret = np.unique(ret)
        return len(ret)
    
    if not isinstance(comm,pd.DataFrame):
        raise ValueError("Coomunity must be a pandas dataframe")
        
    if order==True:
       comm = OrderMatrix(comm, scores=scores, binary=binary)
    
    statisic = coherence(comm)
    nulls = NullMaker(comm=comm, sims=sims,method=method, ordinate=orderNulls,
                          allowEmpty=allowEmpty, verbose=verbose, seed=seed)
    
    simstat = map(coherence,nulls)
    varstat = np.std(simstat)
    z = (statisic - np.mean(simstat))/ varstat
    pval = 2 * np.no
    return {"embAbs": statisic,"z":z,"p":p,"simMean":np.mean(simstat),
            "simVariance":varstat,"method":method}
    
def OrderMatrix(comm, scores=1,outputScore=False,binary=True):
    if binary:
        comm = (comm>0).astype(int)
    temp = CA(row_labels=comm.index.values,col_labels=comm.columns.values)
    temp.fit(comm.values)
    if outputScore:
        print(temp)
        return {'speciesscores' : temp.col_coord_[:, scores],
                'sitesscores': temp.row_coord_[:, scores]}
    else:
        ret = comm
        ret.reindex(np.argsort(temp.row_coord_[:,scores])[::-1])
        ret = ret[ret.columns[np.argsort(temp.col_coord_[:,scores])]]
        ret = (ret>0) + 0
        return ret
    
def NullMaker(comm, sims = 1000, method = "r1",  ordinate = False, scores = 1,
  allowEmpty = False, verbose = FALSE, seed = 1):
 
    if verbose:
        bar = progressbar.ProgressBar()
        
    c=OrderMatrix(m)