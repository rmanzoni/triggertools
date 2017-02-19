import ROOT
import numpy as np
from copy import deepcopy as dc

class FuncRatio():
    '''
    returns a TF1 which is the ratio of other two TF1s fnum and fden
    in the minimum common range of the two.
    Inspired to https://root.cern.ch/phpBB3/viewtopic.php?t=10862
    '''
    def __init__(self, fnum, fden, start=None, stop=None):
        global ifnum # yes, need to be global
        global ifden        
        ifnum = fnum
        ifden = fden
        self.fnum = fnum
        self.fden = fden
        if not start:
            self.start = max(fnum.GetMinimumX(), fden.GetMinimumX())
        else:
            self.start = start
        if not stop:
            self.stop = min(fnum.GetMaximumX(), fden.GetMaximumX())
        else:
            self.stop = stop

    def __call__(self):
        # do a deep copy, otherwise it'd keep fishing the last fuctions assigned to the 
        # corresponding global variables when doing multiple calls
        ratio = dc(ROOT.TF1('ratio', self.doratio, self.start, self.stop, 0)) 
        ratio.SetLineColor(self.fnum.GetLineColor())
        ratio.SetLineStyle(self.fnum.GetLineStyle())
        # ratio.SetNpx(10000) # too may points make the function disappear, too few make the function look shit. ROOT, what's not to love? 
        return ratio
    
    @staticmethod
    def doratio(x, par=None):
        if par:
            iden = ifden.EvalPar(x,par)
            num = ifnum.EvalPar(x,par)
        else:
            iden = ifden.EvalPar(x)
            num = ifnum.EvalPar(x)        
        den = iden if abs(iden) > 0. else (np.sign(iden) * 1.e-30)
        ratio = num / den
        return ratio

if __name__ == '__main__':

   fnum = ROOT.TF1("f1", "x^2 + 4",2,10)
   fden = ROOT.TF1("f2", "x + 3"  ,0,7)
   ratio = FuncRatio(fnum, fden)()
   ratio.Draw()
   
