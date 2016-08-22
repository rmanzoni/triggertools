#!/bin/env python

import ROOT
from copy import deepcopy as dc

ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)
ROOT.TVirtualFitter.SetMaxIterations(10000)

class Fitter(object):
    '''
    takes TH1 or a TGraph, fits with a user defined function
    '''
    def __init__(self, graph, function, fitopt = 'RIMS', 
                 colour = ROOT.kRed, 
                 fillstyle = 3005, cl = 0.68,
                 verbose = False):
                 
        self.graph     = graph
        self.function  = function
        self.fitopt    = fitopt    
        self.colour    = colour 
        self.fillstyle = fillstyle
        self.cl        = cl
        self.verbose   = verbose
     
    def _fit(self):
        mcg = ROOT.TGraphAsymmErrors(self.graph)
        mcg.SetMarkerColor(self.colour)
        mcg.SetMarkerSize(1.)
        self.function.SetLineColor(self.colour)
        parameters = mcg.Fit(self.function, self.fitopt)
        
        if self.verbose:
            print '\t fitted function NDoF %d' %self.function.GetNDF()
            print '\t fitted function Chi2 %f' %self.function.GetChisquare()    
            print '\t fitted function Prob %f' %self.function.GetProb()
        
        if isinstance(self.graph, ROOT.TGraph):
            mcgeh = mcg.GetHistogram()
        elif isinstance(self.graph, ROOT.TH1):
            mcgeh = dc(mcg)
        else:
            raise
        ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(mcgeh, self.cl)
        mcge = ROOT.TGraphAsymmErrors(mcgeh)
        for bin in range(mcge.GetN())[0:mcge.GetN()-1]:
            bineup      = mcge.GetErrorYhigh(bin+1)
            binedown    = mcge.GetErrorYlow (bin+1)
            binc        = mcgeh.GetBinContent(bin+1)
            
            mcge.SetPointEYhigh( bin+1, min( (1.-binc), bineup) )
#             print binc - binedown, binc, binc + bineup
            if bin+1 < 12: 
                mcge.SetPointEYhigh( bin+1, 0. )
                mcge.SetPointEYlow ( bin+1, 0. )
            else:
                mcge.SetPointEYhigh( bin+1, min( (1.-binc), bineup) )
        mcge.SetFillColor(self.colour)
        mcge.SetLineColor(self.colour)
        mcge.SetLineWidth(2)
        mcge.SetFillStyle(self.fillstyle)
        mcge.SetMarkerSize(0.00000001)
        return mcg, mcge, parameters


