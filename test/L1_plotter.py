import sys
sys.path.append('..')
from objects.Efficiencies import Efficiency1D

import ROOT
import numpy as np
import array as ar
from itertools import product
from copy import deepcopy as dc

ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()

baseline = '&'.join([
    ' l1_pt > 20 '                                 ,
    ' abs(l1_eta) < 2.1 '                          ,
    ' l1_reliso05 < 0.1 '                          ,
    ' l1_muonid_medium > 0.5 '                     ,
    ' l2_pt > 20 '                                 ,
    ' abs(l2_eta) < 2.1 '                          ,
    ' abs(l2_charge) == 1 '                        ,
    ' l2_decayModeFinding '                        ,
    ' l2_byCombinedIsolationDeltaBetaCorr3Hits > 1',
    ' l2_againstMuon3 > 1.5 '                      ,
    ' l2_againstElectronMVA6 > 0.5 '               ,
    ' n_bjets == 0 '                               ,
    ' mt < 30 '                                    ,
    ' pass_leptons == 1 '                          ,
    ' veto_dilepton == 0 '                         ,
    ' veto_thirdlepton == 0 '                      ,
    ' veto_otherlepton == 0 '                      ,
    ' mvis > 40. && mvis < 80. '
])

subtraction = ' ( (l1_charge != l2_charge) - (l1_charge == l2_charge) ) '

eta_bins = {
     'barrel' : ' abs(l2_eta) <= 1.4 ',
     'endcap' : ' abs(l2_eta) <  1.4 ',
     ''       : ' 1 '                 ,
}

decaymode = {
    'dm0'  : ' l2_decayMode == 0  ',
    'dm1'  : ' l2_decayMode == 1  ',
    'dm10' : ' l2_decayMode == 10 ',
    ''     : ' 1 '                 ,
}

L1selection = {
    'tau'    : ' l2_L1_type == 7 & l2_L1_bx == 0 '                 ,
    'isotau' : ' l2_L1_type == 7 & l2_L1_bx == 0 & l2_L1_iso == 1 ',
}

L1pt = {
    ''       : '1'                ,
    'L1pt28' : ' l2_L1_pt > 27.5 ',
    'L1pt32' : ' l2_L1_pt > 31.5 ',
}

filenames = [
    '../../SingleMuon_Run2016B_PromptReco_v1/H2TauTauTreeProducerTauMu/tree.root',
    '../../SingleMuon_Run2016B_PromptReco_v2/H2TauTauTreeProducerTauMu/tree.root',    
]

t1 = ROOT.TChain('tree')

for fname in filenames:
    t1.Add(fname)

L1tauPt = 28
nbins   = 40
bins    = [0., 10., 20., 25., 30., 32.5, 35., 37.5, 40., 42.5, 45., 50., 55., 60., 70., 90., 120., 200.]

selections = ' (%s) * (%s) * (%s) * (%s) ' %(baseline, subtraction, eta_bins[''], decaymode[''])

variables = [
    Efficiency1D(tree=t1, name='tau_eta', variable='l2_eta'    , histo_name='tau_eta_iso', cut_num='1', cut_den='1', xlabel='offline #tau #eta' , ylabel='iso L1 #tau efficiency', bins=nbins, bini=-3.  , bine=3.  ),
    Efficiency1D(tree=t1, name='tau_phi', variable='l2_phi'    , histo_name='tau_phi_iso', cut_num='1', cut_den='1', xlabel='offline #tau #phi' , ylabel='iso L1 #tau efficiency', bins=nbins, bini=-3.15, bine=3.15),
    Efficiency1D(tree=t1, name='npv'    , variable='n_vertices', histo_name='npv_iso'    , cut_num='1', cut_den='1', xlabel='# PV'              , ylabel='iso L1 #tau efficiency', bins=10   , bini= 0   , bine=30  ),
    Efficiency1D(tree=t1, name='L1_pt'  , variable='l2_L1_pt'  , histo_name='L1_pt_iso'  , cut_num='1', cut_den='1', xlabel='L1 #tau E_{T}'     , ylabel='iso L1 #tau efficiency', bins=bins ,                      ),
    Efficiency1D(tree=t1, name='tau_pt' , variable='l2_pt'     , histo_name='tau_pt_iso' , cut_num='1', cut_den='1', xlabel='offline #tau p_{T}', ylabel='iso L1 #tau efficiency', bins=bins ,                      ),
    Efficiency1D(tree=t1, name='mvis'   , variable='mvis'      , histo_name='mvis_iso'   , cut_num='1', cut_den='1', xlabel='offline #tau #eta' , ylabel='iso L1 #tau efficiency', bins=nbins, bini= 0.  , bine=100.),
]

outfile = ROOT.TFile.Open('L1_plots.root', 'recreate')

for i in product(variables, eta_bins, decaymode, L1selection, L1pt):
    variable = i[0]
    eta_bin  = eta_bins   [i[1]]
    dm       = decaymode  [i[2]]
    l1sel    = L1selection[i[3]]
    l1pt     = L1pt       [i[4]]

    cut_den = ' (%s) * (%s) * (%s) * (%s) ' %(baseline, subtraction, eta_bin, dm)
    cut_num = ' (%s) * (%s) ' %(l1sel, l1pt)

    variable.cut_den = cut_den
    variable.cut_num = cut_num

    variable._fillHistos()
    variable._computeEfficiency()

    num, den, eff = variable.get()
    
    outfile.cd()
    
    dirname = '_'.join([j for j in i[1:] if len(j)])
    print dirname
    
    ROOT.gDirectory.mkdir(dirname)
    ROOT.gDirectory.cd(dirname)

    eff.Draw()
    
    num.Write()
    den.Write()    
    eff.Write()    
        
outfile.Close()


