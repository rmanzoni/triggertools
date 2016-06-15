#!/bin/env python
import ROOT
import sys
sys.path.append('..')
from objects.FitFunctions import crystalballEfficiency
from objects.Fitter       import Fitter
from plot.CMSStyle        import CMS_lumi
from plot.PlotStyle       import PlotStyle

# PlotStyle.initStyle()

ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

# PlotStyle.initStyle()
ROOT.gStyle.SetLegendFont(42)

ROOT.gStyle.SetOptStat(False)

ROOT.gStyle.SetOptFit(000000)


c1 = ROOT.TCanvas('', '', 700, 700)

ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

func = ROOT.TF1('func', crystalballEfficiency, 20., 200., 5)
func.SetNpx(100000)
func.SetParameter(0,  37.5 )
func.SetParameter(1,   6.3 )
func.SetParameter(2,  6.4  )
func.SetParameter(3,139.   )
func.SetParameter(4,   0.96)

# func.SetParLimits(0,  10.  ,  50.  )
# func.SetParLimits(1,   0.5 ,  30.  )
# func.SetParLimits(2,   0.01,  40.  )
# func.SetParLimits(3,   1.01, 999.  )
func.SetParLimits(3,  1.01, 141. )

# func.FixParameter(0, 37. )
# func.FixParameter(1, 7.  )
# func.FixParameter(2, 0.92 )
# func.FixParameter(3, 139. )
# func.FixParameter(4, 0.94 )

func.SetParName(0, 'm_{0}')
func.SetParName(1, 'sigma')
func.SetParName(2, 'alpha')
func.SetParName(3, 'n'    )
func.SetParName(4, 'norm' )


    

data_file = ROOT.TFile.Open('../test/muletto.root','read')
data_file.cd()
data_graph = data_file.Get('sub_HLT/tau_pt')
data_graph.SetMarkerColor(ROOT.kBlack)
# https://root.cern.ch/phpBB3/viewtopic.php?t=14569
# data_graph.GetFunction('stats').Delete()
fitter = Fitter(data_graph, func, colour = ROOT.kBlack)
dg, dge, results = fitter._fit()

mg = ROOT.TMultiGraph()
mg.Add(dg )
mg.Draw('AP')
dge.Draw('SAME E4')

mg.GetYaxis().SetTitle('L1 + HLT efficiency')
mg.GetXaxis().SetTitle('offline #tau p_{T} [GeV]')
mg.GetYaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetTitleOffset(1.3)

dge.GetXaxis().SetRangeUser(0., 170.)
dge.GetYaxis().SetRangeUser(0., 1.05)
mg.GetXaxis().SetRangeUser(0., 170.)
mg.GetYaxis().SetRangeUser(0., 1.05)

leg = ROOT.TLegend( 0.55, 0.4, 0.88, 0.5 )
leg.SetTextSize(0.027)
leg.SetFillColor(ROOT.kWhite)
leg.SetLineColor(ROOT.kWhite)
leg.AddEntry(dg  , 'data'                      , 'EP')
leg.AddEntry(dge , 'fit to data and 68% C.I.'        )
leg.Draw('SAMEAPZL')

ROOT.gPad.Update()
CMS_lumi(ROOT.gPad, 4, 0)

c1.SaveAs('L1efficiencyDataMC.pdf')





