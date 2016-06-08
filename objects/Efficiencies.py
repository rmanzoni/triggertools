import ROOT
import math
import warnings
import numpy as np
import array as ar
from itertools   import product
from collections import namedtuple
from copy        import deepcopy as dc

ROOT.TH1.SetDefaultSumw2()

class Efficiency(object):
    '''
    Base class, virtual, in a way.
    '''
    def __init__(self, *args, **kwargs):
        pass

    def _fillHistos(self):
        pass

    def _computeEfficiency(self):
        pass
    
    def get(self):
        pass

class Efficiency1D(Efficiency):
    '''
    '''
    def __init__(self, tree, name, variable, histo_name, 
                 cut_num, cut_den, xlabel, ylabel, bins, 
                 bini = None, bine = None, title = '', permissive = True):
        self.tree       = tree
        self.name       = name     
        self.variable   = variable
        self.xlabel     = xlabel
        self.ylabel     = ylabel
        self.title      = title
        self.permissive = permissive
        self.cut_den    = cut_den  
        self.cut_num    = cut_num
        if bini == None and bine == None and isinstance(bins, (list, tuple)):    
            self.bins = np.array(bins)
            self.histo_num = dc(ROOT.TH1F(self.name + '_num', self.name + '_num', len(self.bins) - 1, self.bins)    )
            self.histo_den = dc(ROOT.TH1F(self.name + '_den', self.name + '_den', len(self.bins) - 1, self.bins)    )
        else:
            self.bins = bins
            self.bini = bini
            self.bine = bine
            self.histo_num = dc(ROOT.TH1F(self.name + '_num', self.name + '_num', self.bins, self.bini, self.bine)  )  
            self.histo_den = dc(ROOT.TH1F(self.name + '_den', self.name + '_den', self.bins, self.bini, self.bine)  )  
            
    def _fillHistos(self):
    
        self.directory = ROOT.gDirectory # bella ROOT!
        self.directory.Add(self.histo_num)
        self.directory.Add(self.histo_den)
        # self.directory.ls()
        self.tree.Draw('%s >> %s' %(self.variable, self.histo_num.GetName()), '(%s) * (%s)' %(self.cut_num, self.cut_den))
        self.tree.Draw('%s >> %s' %(self.variable, self.histo_den.GetName()), self.cut_den)
    
    def _computeEfficiency(self):
        x   = []
        y   = []
        exl = []
        eyl = []
        exh = []
        eyh = []
    
        for bin in range(self.histo_den.GetNbinsX()):
            
            mynum = dc(self.histo_num)
            myden = dc(self.histo_den)
            
            bin_centre = mynum.GetBinCenter(bin+1)
            binc_num = mynum.GetBinContent(bin+1)
            binc_den = myden.GetBinContent(bin+1)
            
            if binc_num > binc_den:
                message = ('Efficiency %s  -  cut %s\n'\
                           '\t==> In bin centre %.2f numerator has %.2f content LARGER han denominator %.2f content.\n'\
                           '\t    Pegging numerator bin equal to denominator\'s' %(self.name, self.cut_den, bin_centre, binc_num, binc_den))
                if self.permissive:
                    warnings.warn(message, Warning)
                else:
                    raise ValueError(message)
                                
            binc = min(binc_num, binc_den)
            bine = math.sqrt(max(0., binc))
            
            mynum.SetBinContent(bin+1, binc)
            mynum.SetBinError  (bin+1, bine)
    
            my_x   = myden.GetBinCenter(bin+1)
            my_exl = 0.
            my_exh = 0.
    
            # do this by hand because TEfficiency sucks. It really does.
            if myden.GetBinContent(bin+1) > 0.:
                my_y   = float(binc) / float(myden.GetBinContent(bin+1))
                my_eyl = my_y - ROOT.TEfficiency.ClopperPearson(myden.GetBinContent(bin+1), binc, 0.65, 0)
                my_eyh = ROOT.TEfficiency.ClopperPearson(myden.GetBinContent(bin+1), binc, 0.65, 1) - my_y
            else:
                my_y   = 0.
                my_eyl = 0.
                my_eyh = 0.
            
            x  .append(my_x  )
            y  .append(my_y  )
            exl.append(my_exl)
            eyl.append(my_eyl)
            exh.append(my_exh)
            eyh.append(my_eyh)


        mygraph = ROOT.TGraphAsymmErrors(len(x),
                                         np.array(x  ),
                                         np.array(y  ),
                                         np.array(exl),
                                         np.array(exh),
                                         np.array(eyl),
                                         np.array(eyh))
        
        mygraph.SetTitle(';'.join([self.title, self.xlabel, self.ylabel]))
        mygraph.SetName(self.name)
         
        self.eff_graph = mygraph

    def get(self):
        return self.histo_num, self.histo_den, self.eff_graph


class Efficiency2D(Efficiency):
    pass





