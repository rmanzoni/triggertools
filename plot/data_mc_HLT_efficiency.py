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

func = ROOT.TF1('func', '0.5 * ([0]*TMath::Erf((x-[1])/[2]) + 1.)', 25., 200.)
func.SetParameter(0,   .8)
func.SetParameter(1, 30. )
func.SetParameter(1, 20. )

func.SetParLimits(0,  0.,  1.)
func.SetParLimits(1, 10., 50.)
func.SetParLimits(2,  5., 50.)
    
func.SetParName(0, 'plateau'  )
func.SetParName(1, 'threshold')
func.SetParName(2, 'width'    )

# crystal ball plus step
func2 = ROOT.TF1('func', CBeff, 25., 200., 5)
func2.SetParameter(0,  30. )
func2.SetParameter(1,  15. )
func2.SetParameter(2, - 0.2)
func2.SetParameter(3,   2. )
func2.SetParameter(4,    .9)

func2.SetParLimits(0,  10.  , 50.)
func2.SetParLimits(1,   2.  , 30.)
func2.SetParLimits(2, - 0.01, 30.)
func2.SetParLimits(3,   1.01, 90.)
func2.SetParLimits(4,    .5 ,  1.)

func2.SetLineColor(ROOT.kBlack)
func2.SetParName(0, 'm_{0}')
func2.SetParName(1, 'sigma')
func2.SetParName(2, 'alpha')
func2.SetParName(3, 'n'    )
func2.SetParName(4, 'norm' )

def getUncertaintyHisto(graph, color = ROOT.kBlack, style = 3005, cl = 0.68):
    mcg = ROOT.TGraphAsymmErrors(graph)
    func.SetLineColor(color)
    mcg.Fit(func2, 'R')
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

# data_file   = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_8_0_5/src/CMGTools/H2TauTau/cfgPython/mt/2016B_HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg/HLTefficiencies_noJson.root','read')
data_file   = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_8_0_5/src/CMGTools/H2TauTau/cfgPython/mt/2016B_HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg/HLTefficiencies.root','read')
data_file.cd()
# data_graph = data_file.Get('baseline/inclusive/eff_pt_sub_baseline_inclusive')
# data_graph = data_file.Get('low_mt/inclusive/eff_pt_sub_low_mt_inclusive')
data_graph = data_file.Get('low_mt_mass_cut/inclusive/eff_pt_sub_low_mt_mass_cut_inclusive')
data_graph.SetMarkerColor(ROOT.kBlack)
dg = ROOT.TGraphAsymmErrors(data_graph)
func2.SetLineColor(ROOT.kBlack)
dg, dge = getUncertaintyHisto(data_graph)

# mc_file   = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_8_0_5/src/CMGTools/H2TauTau/cfgPython/mt/2016B_HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg/HLTefficiencies_noJson.root','read')
# mc_file.cd()
# mc_graph  = mc_file.Get('baseline/inclusive/eff_pt_os_baseline_inclusive')
# mc_graph  = mc_file.Get('low_mt/inclusive/eff_pt_os_low_mt_inclusive')
# mc_graph  = mc_file.Get('low_mt_mass_cut/inclusive/eff_pt_os_low_mt_mass_cut_inclusive')
# mc_graph.SetMarkerColor(ROOT.kRed)
# mcg = ROOT.TGraphAsymmErrors(mc_graph)
# func2.SetLineColor(ROOT.kRed)
# mcg, mcge = getUncertaintyHisto(mc_graph, ROOT.kRed, 3004)

mg = ROOT.TMultiGraph()
# mg.Add(mcg)
mg.Add(dg )
mg.Draw('AP')
# mcge.Draw('SAME E4')
dge.Draw('SAME E4')

# mg.GetYaxis().SetTitle('L1 + L2 + L2.5 + HLT efficiency')
mg.GetYaxis().SetTitle('L1 + HLT efficiency')
mg.GetXaxis().SetTitle('offline #tau p_{T} [GeV]')
mg.GetYaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetTitleOffset(1.3)

leg = ROOT.TLegend( 0.43, 0.3, 0.9, 0.5 )
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

c1.SaveAs('HLTefficiencyDataMC.pdf')





