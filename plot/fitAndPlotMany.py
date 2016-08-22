#!/bin/env python
import ROOT
import sys
sys.path.append('..')
from collections import namedtuple

from objects.MultiGraph   import MultiGraph
from objects.FitFunctions import crystalballEfficiency
from objects.Fitter       import Fitter
from plot.CMSStyle        import CMS_lumi
from plot.PlotStyle       import PlotStyle

ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetLegendFont(42)

ROOT.gStyle.SetOptStat(False)

ROOT.gStyle.SetOptFit(000000)

c1 = ROOT.TCanvas('', '', 700, 700)

ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

func = ROOT.TF1('func', crystalballEfficiency, 0., 500., 5)
func.SetNpx(100000)
# func.SetParameter(0,  37.5 )
# func.SetParameter(1,   2.3 )
# func.SetParameter(2,   1.4  )
# func.SetParameter(3,   3.   )
# func.SetParameter(4,   0.96)
# 
# func.SetParLimits(0,  10.  ,  50.  )
# func.SetParLimits(1,   0.5 ,  30.  )
# func.SetParLimits(2,   0.01,  40.  )
# # func.SetParLimits(3,   1.01, 999.  )
# func.SetParLimits(3,  1.01, 141. )
# func.SetParLimits(4,  0.5, 1. )





func.SetParameter(0,  19.8       )
func.SetParameter(1,  0.2         )
func.SetParameter(2,  0.077)
func.SetParameter(3,  1.67)
func.SetParameter(4,  .98)

func.SetParLimits(0,  10.  ,  50.  )
func.SetParLimits(1,   0.1 ,  30.  )
func.SetParLimits(2,   0.01,  40.  )
# func.SetParLimits(3,   1.01, 999.  )
func.SetParLimits(3,  1.01, 141. )
func.SetParLimits(4,  0.5, 1. )



func.FixParameter(0, 20.1)
# func.FixParameter(1, 5.63137e-01)
# func.FixParameter(2,  5.27363e-01)
# func.FixParameter(3,  1.64738e+00)
# func.FixParameter(4, 9.65390e-01)
func.FixParameter(4, 1.)

func.SetParName(0, 'm_{0}')
func.SetParName(1, 'sigma')
func.SetParName(2, 'alpha')
func.SetParName(3, 'n'    )
func.SetParName(4, 'norm' )










# func = ROOT.TF1('func', '[0]*TMath::Erf((x-[1])/[2])', 0., 180.)  # non def pos erf
# func = ROOT.TF1('func', '0.5 * ([0]*TMath::Erf((x-[1])/[2]) + 1)', 0., 180.) # def pos erf
# func.SetParameter(0,  0.9)
# func.SetParameter(1, 20. )
# func.SetParameter(2, 10. )
# 
# func.SetParName(0, 'plateau')
# func.SetParName(1, 'threshold')
# func.SetParName(2, 'width')






myGraph = namedtuple('mygraph', 'file graph function colour legend legendOpt')

# file = '../test/diTau_plots.root'
# file = '../test/diTau_plots_good.root'
# file = '../test/diTau_plots_high_mt_os.root'
# file = '../test/diTau_plots_ss.root'
# file = '../test/mu_tau_singleL1_plots.root'
# file = '../test/mu_tau_singleL1_plots_high_mt_os.root'
# file = '../test/mu_tau_singleL1_plots_ss.root'
# file = '../test/mu_tau_crossL1_plots.root'
# file = '../test/mu_tau_crossL1_plots_high_mt_os.root'
# file = '../test/mu_tau_crossL1_plots_ss.root'

# file = '../test/ichep/diTau_plots_ICHEP.root'
# file = '../test/ichep/mu_tau_crossL1_plots_ICHEP.root'
file = '../test/ichep/mu_tau_singleL1_plots_ICHEP.root'



graphs = [
    myGraph(file=file, graph='lowmt_zmass_sub_LooseIso_HLT/tau_pt' , function=func, colour=ROOT.kBlack, legend='data', legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_MediumIso_HLT/tau_pt', function=func, colour=ROOT.kBlack, legend='data', legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_MediumIso_L1/tau_pt' , function=func, colour=ROOT.kBlack, legend='data', legendOpt='EP'),
]

# graphs = [
#     myGraph(file=file, graph='lowmt_zmass_sub_MediumIso_HLT/tau_pt'      , function=func, colour=ROOT.kOrange-6, legend='data'     , legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_VLooseIso_HLT/tau_pt'  , function=func, colour=ROOT.kOrange-4, legend='VLooseIso' , legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_LooseIso_HLT/tau_pt'   , function=func, colour=ROOT.kOrange-2, legend='LooseIso'  , legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_MediumIso_HLT/tau_pt'  , function=func, colour=ROOT.kOrange  , legend='MediumIso' , legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_TightIso_HLT/tau_pt'   , function=func, colour=ROOT.kOrange+2, legend='TightIso'  , legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_VTightIso_HLT/tau_pt'  , function=func, colour=ROOT.kOrange+4, legend='VTightIso' , legendOpt='EP'),
#     myGraph(file=file, graph='lowmt_zmass_sub_VVTightIso_HLT/tau_pt' , function=func, colour=ROOT.kOrange+6, legend='VVTightIso', legendOpt='EP'),
# ]

# graphs = [
#     myGraph(file=file, graph='highmt_os_NoIso_HLT/tau_pt'      , function=func, colour=ROOT.kAzure-6, legend='NoIso'     , legendOpt='EP'),
#     myGraph(file=file, graph='highmt_os_VLooseIso_HLT/tau_pt'  , function=func, colour=ROOT.kAzure-4, legend='VLooseIso' , legendOpt='EP'),
#     myGraph(file=file, graph='highmt_os_LooseIso_HLT/tau_pt'   , function=func, colour=ROOT.kAzure-2, legend='LooseIso'  , legendOpt='EP'),
#     myGraph(file=file, graph='highmt_os_MediumIso_HLT/tau_pt'  , function=func, colour=ROOT.kAzure  , legend='MediumIso' , legendOpt='EP'),
#     myGraph(file=file, graph='highmt_os_TightIso_HLT/tau_pt'   , function=func, colour=ROOT.kAzure+2, legend='TightIso'  , legendOpt='EP'),
#     myGraph(file=file, graph='highmt_os_VTightIso_HLT/tau_pt'  , function=func, colour=ROOT.kAzure+4, legend='VTightIso' , legendOpt='EP'),
#     myGraph(file=file, graph='highmt_os_VVTightIso_HLT/tau_pt' , function=func, colour=ROOT.kAzure+6, legend='VVTightIso', legendOpt='EP'),
# ]

# graphs = [
#     myGraph(file=file, graph='ss_NoIso_HLT/tau_pt'      , function=func, colour=ROOT.kViolet-6, legend='NoIso'     , legendOpt='EP'),
#     myGraph(file=file, graph='ss_VLooseIso_HLT/tau_pt'  , function=func, colour=ROOT.kViolet-4, legend='VLooseIso' , legendOpt='EP'),
#     myGraph(file=file, graph='ss_LooseIso_HLT/tau_pt'   , function=func, colour=ROOT.kViolet-2, legend='LooseIso'  , legendOpt='EP'),
#     myGraph(file=file, graph='ss_MediumIso_HLT/tau_pt'  , function=func, colour=ROOT.kViolet  , legend='MediumIso' , legendOpt='EP'),
#     myGraph(file=file, graph='ss_TightIso_HLT/tau_pt'   , function=func, colour=ROOT.kViolet+2, legend='TightIso'  , legendOpt='EP'),
#     myGraph(file=file, graph='ss_VTightIso_HLT/tau_pt'  , function=func, colour=ROOT.kViolet+4, legend='VTightIso' , legendOpt='EP'),
#     myGraph(file=file, graph='ss_VVTightIso_HLT/tau_pt' , function=func, colour=ROOT.kViolet+6, legend='VVTightIso', legendOpt='EP'),
# ]

    
mg = MultiGraph(graphs=graphs, json='fitresults.json')
mg.Fill()
mg.Draw('AP')

# mg.GetYaxis().SetTitle('L1 + HLT efficiency')
mg.GetYaxis().SetTitle('HLT efficiency')
# mg.GetYaxis().SetTitle('L1 efficiency')
mg.GetXaxis().SetTitle('offline #tau p_{T} [GeV]')
mg.GetYaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetTitleOffset(1.3)
mg.GetYaxis().SetTitleSize(1.2 * mg.GetYaxis().GetTitleSize())
mg.GetXaxis().SetTitleSize(1.2 * mg.GetXaxis().GetTitleSize())
ROOT.gPad.SetLeftMargin(0.12)
ROOT.gPad.SetBottomMargin(0.12)


mg.GetXaxis().SetRangeUser(0., 500.)
mg.GetYaxis().SetRangeUser(0., 1.05)

# ROOT.gPad.SetLogx()
mg.leg.Draw('SAMEAPZL')

# mg.GetXaxis().SetRangeUser(20., 200.)
# ROOT.gPad.SetLogx()

ROOT.gPad.Update()
CMS_lumi(ROOT.gPad, 4, 0)

c1.SaveAs('L1efficiencyDataMC_ICHEP.pdf')
# c1.SaveAs('L1efficiencyDataMC_ICHEP_log.pdf')



