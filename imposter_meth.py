import numpy as np
import similarity_measures as sm
from numba import jit


@jit
def get_score(x,y,imposters,sim):
    '''Compute for how many random feature sets out of 100 sim(x,y) is greater than sim(x,z) for all z in imposters'''	
    score = 0
    sim_xy = sim(x,y) 
    for k in range(100):
        ran_el = np.sort(np.random.choice(range(len(x)), (1,round(len(x) / 2)), replace = False))        
        c_x = x[ran_el][0]
        c_y = y[ran_el][0]
        sim_xy = sim(c_x,c_y)


        for yi in imposters:
            if sim(c_x, np.take(yi,ran_el)[0]) > sim_xy:
                break
        else:
            score += 1

    return score / 100.0  # 
   

def imposters(y, universe, m = 125, n = 25):
    '''Return n imposters. Compute the m most similar files in universe and randomly select n from them '''
    minmax_vec = np.array([sm.cminmax(t,y) for t in universe])
    pot_imp_ind = minmax_vec.argsort()[:-(m+1):-1] # Last m entries
    pot_imp_ind = np.sort(np.random.choice(pot_imp_ind, n))
    return [universe[k] for k in pot_imp_ind[::-1]]  # Have the most similar imposters first, to hope for a quicker break in the get_score algorithm
    

def blog_same_author(x,y,text_corpus, threshold, nr_imposters = 25):
    '''Return true if x and y are by the same author according to the algorithm in the paper'''
    imposters_y = imposters(y, text_corpus.Y, n = nr_imposters)
    score_xy = get_score(x,y,imposters_y, sm.cminmax)
    
    imposters_x = imposters(x, text_corpus.X, n = nr_imposters)
    score_yx = get_score(y,x,imposters_x, sm.cminmax)
    
    if (score_xy + score_yx ) /2.0 > threshold:
        return True
    else:
        return False


