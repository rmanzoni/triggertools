#!/bin/env python

import ROOT
import numpy as np
from itertools import product
from math import sqrt
from crystalball import CBeff
from CMSStyle  import CMS_lumi
from PlotStyle import PlotStyle
from copy import deepcopy as dc

ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

PlotStyle.initStyle()
ROOT.gStyle.SetLegendFont(42)

# ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetOptFit(000000)

# ROOT.gStyle.SetStatX(0.90)                
# ROOT.gStyle.SetStatY(0.45)                
# ROOT.gStyle.SetStatW(0.25)                
# ROOT.gStyle.SetStatH(0.15)                

c1 = ROOT.TCanvas('', '', 700, 700)

ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

from crystalball import crystalball, doubleSidedCrystalball
func = ROOT.TF1('func', doubleSidedCrystalball, -2., 2., 7)
func.SetParameter(0,  0.  )
func.SetParameter(1,  0.1 )
func.SetParameter(2, -0.6 )
func.SetParameter(3,100.  )
func.SetParameter(4,  0.3 )
func.SetParameter(5,  0.6 )
func.SetParameter(6,100.  )

func.SetLineColor(ROOT.kRed)
func.SetParName(0, '#mu'   )
func.SetParName(1, 'sigma' )
func.SetParName(2, 'alpha1')
func.SetParName(3, 'n1'    )
func.SetParName(4, 'scale1')
func.SetParName(5, 'alpha2')
func.SetParName(6, 'n2'    )

func.SetParLimits(0, -0.2  ,  0.2 )
func.SetParLimits(1,  0.01 ,  0.6 )
func.SetParLimits(2, -3.   , -0.01)
func.SetParLimits(3,  1.05 , 999. )
func.SetParLimits(4,  1.e-4,  1.  )
func.SetParLimits(5,  3.   ,  0.01)
func.SetParLimits(6,  1.05 , 999. )

from doubleGauss import doubleGaussSameMean
func = ROOT.TF1('func', doubleGaussSameMean, -2., 2., 5)
func.SetParameter(0,  0.   )
func.SetParameter(1,  0.15 )
func.SetParameter(2,  0.05 )
func.SetParameter(3,  0.3  )
func.SetParameter(4,  0.02 )

func.SetParName(0, '#mu'   )
func.SetParName(1, 'sigma1')
func.SetParName(2, 'scale1')
func.SetParName(3, 'sigma2')
func.SetParName(4, 'scale2')

# func.SetParLimits(0, -0.2  ,  0.2 )
# func.SetParLimits(1,  0.01 ,  0.6 )
# func.SetParLimits(2, -3.   , -0.01)
# func.SetParLimits(3,  1.05 , 999. )
# func.SetParLimits(4,  1.e-4,  1.  )

# func.FixParameter(0,  0.01 )
# func.FixParameter(1,  0.15 )
# func.FixParameter(2,  0.05 )
# func.FixParameter(3,  0.3  )
# func.FixParameter(4,  0.02 )

def getUncertaintyHisto(graph, color = ROOT.kBlack, style = 3005, cl = 0.68):
    #mcg = ROOT.TGraphAsymmErrors(graph)
    mcg = graph
    mcg.SetMarkerColor(color)
    mcg.SetMarkerSize(1.)
    func.SetLineColor(color)
    mcg.Fit(func, 'RIM')
    mcgeh = mcg.Clone()#GetHistogram()
    ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(mcgeh, cl)
    mcge = ROOT.TGraphAsymmErrors(mcgeh)
    for bin in range(mcge.GetN())[0:mcge.GetN()-1]:
        bineup      = mcge.GetErrorYhigh(bin+1)
        binedown    = mcge.GetErrorYlow (bin+1)
        binc        = mcgeh.GetBinContent(bin+1) 
        mcge.SetPointEYhigh( bin+1, min( (1.-binc), bineup) )
    mcge.SetFillColor(color)
    mcge.SetLineColor(color)
    mcge.SetLineWidth(2)
    mcge.SetFillStyle(style)
    mcge.SetMarkerSize(0.00000001)
    return mcg, mcge


data_file  = ROOT.TFile.Open('plots_pull.root','read')
# data_file  = ROOT.TFile.Open('deltaBeta3HitsTight/plots_pull.root','read')
data_file.cd()
# data_histo = data_file.Get('L1_pull')
data_histo = data_file.Get('L1_pull_isoTau')
data_histo.Scale(1./data_histo.Integral())
data_histo.GetYaxis().SetTitleOffset(1.4)
# print 'dakjsdlkajsldkjalj',data_histo.GetYaxis().GetNdivisions()
data_histo.GetYaxis().SetNdivisions(205)
data_histo.GetYaxis().SetTitle('a.u.')
# data_histo.GetFunction('stats').Delete()
data_histo.SetMaximum(0.1)
data_histo.SetMinimum(0.)
dg, dge = getUncertaintyHisto(data_histo)


# mc_file   = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_7_4_3/src/CMGTools/H2TauTau/cfgPython/mt/michalPU/dy_plus_ggh125/plots_pull.root','read')
# mc_file   = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/public/2015trigger/L1_v5_HLT_v4_new_calib/HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v1/GGH125/H2TauTauTreeProducerTauMu/plots_pull.root','read')
# mc_file.cd()
# mc_histo  = mc_file.Get('L1_pull')
# mc_histo.Scale(1./mc_histo.Integral())
# mc_histo.GetYaxis().SetNdivisions(205)
# mc_histo.GetYaxis().SetTitle('a.u.')
# mc_histo.GetYaxis().SetTitleOffset(1.4)
# mc_histo.GetFunction('stats').Delete()
# mc_histo.SetMaximum(0.1)
# mc_histo.SetMinimum(0.)
# mcg, mcge = getUncertaintyHisto(mc_histo, ROOT.kRed, 3004)

# dg  .Draw('E')
# dge .Draw('E4SAME')
# mcg .Draw('ESAME')
# mcge.Draw('SAME E4')

dge .Draw('E3')
dg  .Draw('ESAME')

leg = ROOT.TLegend( 0.17, 0.82, 0.48, 0.93 )
leg.SetTextSize(0.027)
leg.SetFillColor(ROOT.kWhite)
leg.SetLineColor(ROOT.kWhite)
leg.AddEntry(dg  , 'data'                      , 'EP')
leg.AddEntry(dge , 'fit to data and 68% C.I.'        )
# leg.AddEntry(mcg , 'simulation'                , 'EP')
# leg.AddEntry(mcge, 'fit to simulation and 68% C.I.'  )
leg.Draw('SAMEAPZL')

ROOT.gPad.Update()
CMS_lumi(ROOT.gPad, 4, 0)

c1.SaveAs('L1PullDataMC.pdf')






