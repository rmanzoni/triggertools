#!/bin/env python
import ROOT
import sys
sys.path.append('..')

from objects.GraphContainer import GraphContainer
from objects.MultiGraph     import MultiGraph
from objects.FitFunctions   import crystalballEfficiency
from objects.Fitter         import Fitter
from plot.CMSStyle          import CMS_lumi
from plot.PlotStyle         import PlotStyle

ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetLegendFont(42)

ROOT.gStyle.SetOptStat(False)

ROOT.gStyle.SetOptFit(000000)

# c1 = ROOT.TCanvas('', '', 700, 1000)
c1 = ROOT.TCanvas('', '', 700, 700)


func = ROOT.TF1('func', crystalballEfficiency, 0., 500., 5)
# func.SetNpx(100000)
func.SetParameter(0,  30.5 )
func.SetParameter(1,   2.3 )
func.SetParameter(2,   1.4 )
func.SetParameter(3,   3.  )
func.SetParameter(4,   1.  )

func.SetParLimits(0,  10.  ,  50.  )
func.SetParLimits(1,   0.5 ,  30.  )
func.SetParLimits(2,   0.01,  40.  )
# func.SetParLimits(3,   1.01, 999.  )
func.SetParLimits(3,  1.01, 141. )
func.SetParLimits(4,  0.5, 1. )





# func.SetParameter(0,  19.8       )
# func.SetParameter(1,  0.2         )
# func.SetParameter(2,  0.077)
# func.SetParameter(3,  1.67)
# func.SetParameter(4,  .98)
# 
# func.SetParLimits(0,  10.  ,  50.  )
# func.SetParLimits(1,   0.1 ,  30.  )
# func.SetParLimits(2,   0.01,  40.  )
# # func.SetParLimits(3,   1.01, 999.  )
# func.SetParLimits(3,  1.01, 141. )
# func.SetParLimits(4,  0.5, 1. )



# func.FixParameter(0, 20.1)
# func.FixParameter(1, 5.63137e-01)
# func.FixParameter(2,  5.27363e-01)
# func.FixParameter(3,  1.64738e+00)
# func.FixParameter(4, 9.65390e-01)
# func.FixParameter(4, 1.)

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



file_data       = '../test/mediumiso_plots_v3.root'
file_mc_pt      = '../test/mediumiso_plots_mc_TEST.root'
file_mc_eta_npv = '../test/mediumiso_plots_mc_npv_eta.root'

graphs = [

#     GraphContainer(file=file_data  , graphname='lowmt_zmass_sub_MediumIso_L1/tau_pt'  , function=func, colour=ROOT.kRed+2    , legend='L1 data 2016BCDEFG'  , legendOpt='EP', reference=False),
#     GraphContainer(file=file_mc_pt , graphname='lowmt_zmass_sub_MediumIso_L1/tau_pt'  , function=func, colour=ROOT.kRed-7    , legend='L1 reHLT DY MC NLO'  , legendOpt='EP', reference=True ),
# 
#     GraphContainer(file=file_data  , graphname='lowmt_zmass_sub_MediumIso_L2/tau_pt'  , function=func, colour=ROOT.kBlue+2   , legend='L2 data 2016BCDEFG'  , legendOpt='EP', reference=-1),
#     GraphContainer(file=file_mc_pt , graphname='lowmt_zmass_sub_MediumIso_L2/tau_pt'  , function=func, colour=ROOT.kBlue-7   , legend='L2 reHLT DY MC NLO'  , legendOpt='EP', reference=-1),
# 
#     GraphContainer(file=file_data  , graphname='lowmt_zmass_sub_MediumIso_L2p5/tau_pt', function=func, colour=ROOT.kGreen+2  , legend='L2.5 data 2016BCDEFG', legendOpt='EP', reference=-1),
#     GraphContainer(file=file_mc_pt , graphname='lowmt_zmass_sub_MediumIso_L2p5/tau_pt', function=func, colour=ROOT.kGreen-7  , legend='L2.5 reHLT DY MC NLO', legendOpt='EP', reference=-1),
# 
#     GraphContainer(file=file_data  , graphname='lowmt_zmass_sub_MediumIso_HLT/tau_pt' , function=func, colour=ROOT.kMagenta+2, legend='HLT data 2016BCDEFG' , legendOpt='EP', reference=-1),
#     GraphContainer(file=file_mc_pt , graphname='lowmt_zmass_sub_MediumIso_HLT/tau_pt' , function=func, colour=ROOT.kMagenta-7, legend='HLT reHLT DY MC NLO' , legendOpt='EP', reference=-1),

#     GraphContainer(file=file_data  , graphname='lowmt_zmass_sub_MediumIso_HLT/tau_eta'                   , function=func, colour=ROOT.kBlack, legend='data 2016BCDEFG', legendOpt='EP', reference=False),
#     GraphContainer(file=file_mc_eta, graphname='lowmt_zmass_sub_MediumIso_HLT/tau_eta'                   , function=func, colour=ROOT.kRed  , legend='reHLT DY MC NLO', legendOpt='EP', reference=True ),

    GraphContainer(file=file_mc_pt , graphname='lowmt_zmass_sub_MediumIso_HLT/tau_pt' , function=func, colour=ROOT.kRed  , legend='Simulation', legendOpt='EP', reference=-1),
    GraphContainer(file=file_data  , graphname='lowmt_zmass_sub_MediumIso_HLT/tau_pt' , function=func, colour=ROOT.kBlack, legend='Data'      , legendOpt='EP', reference=-1),

]


c1.cd()
# stackPad = ROOT.TPad('stackPad','stackPad',0.,0.3,1.,1.,0,0)
# stackPad.Draw()
# stackPad.cd()
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.SetLogx()
   
mg = MultiGraph(graphs=graphs, json='fitresults_final.json', legendPosition=7)
mg.Fill()
mg.Draw('AP')

# mg.GetYaxis().SetTitle('efficiency')
mg.GetYaxis().SetTitle('L1 + HLT efficiency')
# mg.GetYaxis().SetTitle('HLT efficiency')
# mg.GetYaxis().SetTitle('L1 efficiency')
mg.GetXaxis().SetTitle('offline #tau p_{T} [GeV]')
mg.GetYaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetTitleOffset(1.3)
mg.GetYaxis().SetTitleSize(1.2 * mg.GetYaxis().GetTitleSize())
mg.GetXaxis().SetTitleSize(1.2 * mg.GetXaxis().GetTitleSize())
ROOT.gPad.SetLeftMargin(0.12)
ROOT.gPad.SetBottomMargin(0.12)


# mg.GetXaxis().SetRangeUser(0., 500.)
mg.GetYaxis().SetRangeUser(0., 1.05)

# ROOT.gPad.SetLogx()
mg.leg.Draw('SAMEAPZL')

mg.GetXaxis().SetLimits(20., 500.)
# mg.GetXaxis().SetLimits(-2., 202.)

mg.GetXaxis().SetMoreLogLabels(True)


ROOT.gPad.Update()
CMS_lumi(ROOT.gPad, 4, 0)

# c1.cd()
# ratioPad = ROOT.TPad('ratioPad','ratioPad',0.,0.3,1,.1,0,0)
# ratioPad.Draw()
# ratioPad.cd()
# ROOT.gPad.SetGridx()
# ROOT.gPad.SetGridy()
# 
# ROOT.gPad.SetLogx()
# ROOT.gPad.SetLeftMargin(0.12)
# ROOT.gPad.SetBottomMargin(0.12)

# ratios = mg.returnRatios()
# ratios.Draw('AP')
# ratios.GetYaxis().SetTitle('data / MC')
# ratios.GetYaxis().SetTitleSize(.1)
# ratios.GetYaxis().SetTitleOffset(0.5)
# ratios.GetYaxis().SetLabelSize(.1)
# ratios.GetXaxis().SetLabelSize(.1)
# ratios.GetXaxis().SetLimits(mg.GetXaxis().GetXmin(), mg.GetXaxis().GetXmax())
# ratios.GetYaxis().SetLimits(0.7, 1.3)
# ratios.GetYaxis().SetRangeUser(0.7, 1.3)

ROOT.gPad.Update()

# c1.SaveAs('medium_iso_2016BCDEFG_all_levels.pdf')
# c1.SaveAs('medium_iso_2016BCDEFG_comparison.pdf')
c1.SaveAs('medium_iso_2016BCDEFG_comparison_dps.pdf')
