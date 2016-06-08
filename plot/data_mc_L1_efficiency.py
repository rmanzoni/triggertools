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

ROOT.gStyle.SetOptStat(False)

ROOT.gStyle.SetOptFit(000000)

# ROOT.gStyle.SetStatX(0.90)                
# ROOT.gStyle.SetStatY(0.45)                
# ROOT.gStyle.SetStatW(0.25)                
# ROOT.gStyle.SetStatH(0.15)                

c1 = ROOT.TCanvas('', '', 700, 700)

ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

func = ROOT.TF1('func', '0.5 * ([0]*TMath::Erf((x-[1])/[2]) + 1.)', 0., 200.)
# func = ROOT.TF1('func', '[0]*TMath::Erf((x-[1])/[2])', 20., 200.)
# func.SetParameter(0,  1. )
# func.SetParameter(1, 28. )
# func.SetParameter(1,  8. )
# 
# func.SetParLimits(0,  0.,  1.)
# func.SetParLimits(1, 10., 50.)
# func.SetParLimits(2,  2., 50.)
#     
# func.SetParName(0, 'plateau'  )
# func.SetParName(1, 'threshold')
# func.SetParName(2, 'width'    )
# 

# crystal ball plus step
from crystalball import CBeff
func = ROOT.TF1('func', CBeff, 0., 200., 5)
func.SetNpx(100000)
func.SetParameter(0,  27.2 )
func.SetParameter(1,   5.99)
func.SetParameter(2,   5.75)
func.SetParameter(3, 140.  )
func.SetParameter(4,   1.  )

func.SetParLimits(0,  10.  ,  50.  )
func.SetParLimits(1,   0.5 ,  30.  )
func.SetParLimits(2,   0.01,  40.  )
func.SetParLimits(3,   1.01, 999.  )
func.SetParLimits(3,   137.5, 141. )
# func.SetParLimits(4,    .5 ,    .99)
# func.SetParLimits(4,    .5 ,   1.  )
# func.SetParLimits(4,    .5 ,   10.  )

# func.FixParameter(0,  27.2 )
# func.FixParameter(1,   5.99)
# func.FixParameter(2,   5.75)
# func.FixParameter(3, 115.8 )
func.FixParameter(4, 1. )

func.SetParName(0, 'm_{0}')
func.SetParName(1, 'sigma')
func.SetParName(2, 'alpha')
func.SetParName(3, 'n'    )
func.SetParName(4, 'norm' )





def getUncertaintyHisto(graph, color = ROOT.kBlack, style = 3005, cl = 0.68):
    mcg = ROOT.TGraphAsymmErrors(graph)
    mcg.SetMarkerColor(color)
    mcg.SetMarkerSize(1.)
    func.SetLineColor(color)
    
#     for i in range(50):
#         func.FixParameter(3, 3 * i + 200.)
#         print 3 * i + 1.01
#         parameters = mcg.Fit(func, 'RIMS')
    parameters = mcg.Fit(func, 'RIMS')
#         import pdb ; pdb.set_trace()
    mcgeh = mcg.GetHistogram()
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
    




data_file  = ROOT.TFile.Open('plots_efficiencies.root','read')
data_file.cd()
data_graph = data_file.Get('num;1')
# data_graph = data_file.Get('efficiency_barrel;1')
# data_graph = data_file.Get('efficiency_isoTau;1')
data_graph.SetMarkerColor(ROOT.kBlack)
# https://root.cern.ch/phpBB3/viewtopic.php?t=14569
# data_graph.GetFunction('stats').Delete()
dg, dge = getUncertaintyHisto(data_graph)

# mc_file   = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/public/2015trigger/L1_v5_HLT_v4_new_calib/HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v1/GGH125/H2TauTauTreeProducerTauMu/plots_efficiencies.root','read')
# mc_file.cd()
# mc_graph  = mc_file.Get('num;1')
# mc_graph.SetMarkerColor(ROOT.kRed)
# mc_graph.GetFunction('stats').Delete()
# mcg, mcge = getUncertaintyHisto(mc_graph, ROOT.kRed, 3004)



# legacy_file   = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/public/2015trigger/L1_v5_HLT_v4_new_calib/HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v1/2015D/LegacyFromTDR.root','read')
# legacy_file.cd()
# legacy_graph  = legacy_file.Get('Legacy28/L1_legacy28')
# lg, lge = getUncertaintyHisto(legacy_graph, ROOT.kGreen, 2006)



mg = ROOT.TMultiGraph()
# mg.Add(mcg)
mg.Add(dg )
# mg.Add(lg )
mg.Draw('AP')
# mcge.Draw('SAME E4')
dge.Draw('SAME E4')
# lge.Draw('SAME E4')

mg.GetYaxis().SetTitle('L1 efficiency')
mg.GetXaxis().SetTitle('offline #tau p_{T} [GeV]')
mg.GetYaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetTitleOffset(1.3)

dge.GetXaxis().SetRangeUser(0., 200.)
dge.GetYaxis().SetRangeUser(0., 1.05)
mg.GetXaxis().SetRangeUser(0., 200.)
mg.GetYaxis().SetRangeUser(0., 1.05)

leg = ROOT.TLegend( 0.55, 0.4, 0.88, 0.5 )
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

c1.SaveAs('L1efficiencyDataMC.pdf')





