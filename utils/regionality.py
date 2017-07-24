import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import product, combinations, groupby
from collections import OrderedDict
from math import cos, cosh, sqrt
from array import array
import numpy as np

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

events = Events([
    'outputFULL.root'
])

# all particle flow candidates
handle_pf        = Handle ('std::vector<reco::PFCandidate>')
label_pf         = ('hltParticleFlowReg')


# L2 tau jet regions
handle_l2calojet = Handle ('std::vector<reco::CaloJet>')
label_l2calojet  = ('hltL2TausForPixelIsolation')


# pixel tracks
# global
handle_pixtrk    = Handle ('vector<reco::Track>')
label_pixtrk     = ('hltPixelTracks')

# regional
handle_pixtrkreg = Handle ('vector<reco::Track>')
label_pixtrkreg  = ('hltPixelTracksRegForTau')

# hybrid?!
handle_pixtrkhyb = Handle ('vector<reco::Track>')
label_pixtrkhyb  = ('hltPixelTracksHybrid')


# iterative tracking
# iter 0
handle_trkIt0    = Handle ('vector<reco::Track>')
label_trkIt0     = ('hltIter0PFlowTrackSelectionHighPurityTauReg')

# merged iter 0 & 1
handle_trkIt1    = Handle ('vector<reco::Track>')
label_trkIt1     = ('hltIter1MergedTauReg')

# merged iter 0 & 1 & 2
handle_trkIt2    = Handle ('vector<reco::Track>')
label_trkIt2     = ('hltIter2MergedTauReg')

# merged iter 0 & 1 & 2 & muons
handle_trkreg    = Handle ('vector<reco::Track>')
label_trkreg     = ('hltPFMuonMergingTauReg')


# tracking regions
# Iter 0 tracks & tau jets for Iter 1
handle_regforIt1 = Handle ('vector<reco::TrackJet>')
label_regforIt1  = ('hltIter0TrackAndTauJets4Iter1TauReg')

# Iter 0 & 1 tracks & tau jets for Iter 2
handle_regforIt2 = Handle ('vector<reco::TrackJet>')
label_regforIt2  = ('hltIter1TrackAndTauJets4Iter2TauReg')


# taus
# all taus that are build
handle_alltaus   = Handle ('vector<reco::PFTau>')
label_alltaus    = ('hltPFTausReg')

# all taus that have a pt>0 leading track
handle_taustk    = Handle ('trigger::TriggerFilterObjectWithRefs')
label_taustk     = ('hltPFTauTrackReg')

# all taus that pass the final selection
handle_finaltaus = Handle ('trigger::TriggerFilterObjectWithRefs')
label_finaltaus  = ('hltDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg')

##########################################################################################
##########################################################################################

totevents = events.size()

outfile = ROOT.TFile('regions.root', 'recreate')

histos = OrderedDict()

histos['h1_calo'     ] = ROOT.TH2F('h1_calo'     , 'h1_calo'     , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_pf_ch'    ] = ROOT.TH2F('h1_pf_ch'    , 'h1_pf_ch'    , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_pf_n'     ] = ROOT.TH2F('h1_pf_n'     , 'h1_pf_n'     , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_pix'      ] = ROOT.TH2F('h1_pix'      , 'h1_pix'      , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_pixreg'   ] = ROOT.TH2F('h1_pixreg'   , 'h1_pixreg'   , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_pixhyb'   ] = ROOT.TH2F('h1_pixhyb'   , 'h1_pixhyb'   , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_trkIt0'   ] = ROOT.TH2F('h1_trkIt0'   , 'h1_trkIt0'   , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_trkIt1'   ] = ROOT.TH2F('h1_trkIt1'   , 'h1_trkIt1'   , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_trkIt2'   ] = ROOT.TH2F('h1_trkIt2'   , 'h1_trkIt2'   , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_trkreg'   ] = ROOT.TH2F('h1_trkreg'   , 'h1_trkreg'   , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_regfor1'  ] = ROOT.TH2F('h1_regfor1'  , 'h1_regfor1'  , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_regfor2'  ] = ROOT.TH2F('h1_regfor2'  , 'h1_regfor2'  , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_alltaus'  ] = ROOT.TH2F('h1_alltaus'  , 'h1_alltaus'  , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_taustk'   ] = ROOT.TH2F('h1_taustk'   , 'h1_taustk'   , 100, -3.14, 3.14, 100, -3, 3)
histos['h1_finaltaus'] = ROOT.TH2F('h1_finaltaus', 'h1_finaltaus', 100, -3.14, 3.14, 100, -3, 3)

for hh in histos.values():
    hh.GetXaxis().SetTitle('#phi')
    hh.GetYaxis().SetTitle('#eta')
    hh.GetZaxis().SetTitle('p_{T} [GeV]')

for i, event in enumerate(events):

    if i >0:
        break
    
    ######################################################################################
    # all particle flow candidates
    event.getByLabel (label_pf, handle_pf)
    pfcandidates = handle_pf.product()
    
    pf_ch = [pf for pf in pfcandidates if pf.charge() != 0]
    pf_n  = [pf for pf in pfcandidates if pf.charge() == 0]

    for pf in pf_ch:
        histos['h1_pf_ch'].Fill(pf.phi(), pf.eta(), pf.pt())

    for pf in pf_n:
        histos['h1_pf_n'].Fill(pf.phi(), pf.eta(), pf.pt())
    
    ######################################################################################
    # L2 tau jet regions
    event.getByLabel (label_l2calojet, handle_l2calojet)
    l2calojets = handle_l2calojet.product()

    for jet in l2calojets:
        histos['h1_calo'].Fill(jet.phi(), jet.eta(), jet.pt())
    
    ######################################################################################
    # pixel tracks
    # global
    event.getByLabel (label_pixtrk, handle_pixtrk)
    pixeltracks = handle_pixtrk.product()

    # regional
    event.getByLabel (label_pixtrkreg, handle_pixtrkreg)
    pixeltracksreg = handle_pixtrkreg.product()

    # hybrid?!
    event.getByLabel (label_pixtrkhyb, handle_pixtrkhyb)
    pixeltrackshybrid = handle_pixtrkhyb.product()

    for pix in pixeltracks:
        histos['h1_pix'].Fill(pix.phi(), pix.eta(), pix.pt())

    for pix in pixeltracksreg:
        histos['h1_pixreg'].Fill(pix.phi(), pix.eta(), pix.pt())

    for pix in pixeltrackshybrid:
        histos['h1_pixhyb'].Fill(pix.phi(), pix.eta(), pix.pt())

    ######################################################################################
    # iterative tracking
    # iter 0
    event.getByLabel (label_trkIt0, handle_trkIt0)
    trkIt0 = handle_trkIt0.product()

    # merged iter 0 & 1
    event.getByLabel (label_trkIt1, handle_trkIt1)
    trkIt1 = handle_trkIt1.product()

    # merged iter 0 & 1 & 2
    event.getByLabel (label_trkIt2, handle_trkIt2)
    trkIt2 = handle_trkIt2.product()

    # merged iter 0 & 1 & 2 & muons
    event.getByLabel (label_trkreg, handle_trkreg)
    tracksreg = handle_trkreg.product()

    for tk in trkIt0:
        histos['h1_trkIt0'].Fill(tk.phi(), tk.eta(), tk.pt())

    for tk in trkIt1:
        histos['h1_trkIt1'].Fill(tk.phi(), tk.eta(), tk.pt())

    for tk in trkIt2:
        histos['h1_trkIt2'].Fill(tk.phi(), tk.eta(), tk.pt())

    for tk in tracksreg:
        histos['h1_trkreg'].Fill(tk.phi(), tk.eta(), tk.pt())

    ######################################################################################
    # tracking regions
    # Iter 0 tracks & tau jets for Iter 1
    event.getByLabel (label_regforIt1, handle_regforIt1)
    regforIt1 = handle_regforIt1.product()
    
    # Iter 0 & 1 tracks & tau jets for Iter 2
    event.getByLabel (label_regforIt2, handle_regforIt2)
    regforIt2 = handle_regforIt2.product()

    for reg in regforIt1:
        histos['h1_regfor1'].Fill(reg.phi(), reg.eta(), reg.pt())

    for reg in regforIt2:
        histos['h1_regfor2'].Fill(reg.phi(), reg.eta(), reg.pt())

    ######################################################################################
    # taus
    # all taus that are build
    event.getByLabel (label_alltaus, handle_alltaus)
    alltaus = handle_alltaus.product()

    # all taus that have a pt>0 leading track
    event.getByLabel (label_taustk, handle_taustk)
    taustk = handle_taustk.product().pftauRefs()

    # all taus that pass the final selection
    event.getByLabel (label_finaltaus, handle_finaltaus)
    finaltaus = handle_finaltaus.product().pftauRefs()

    for tau in alltaus:
        histos['h1_alltaus'].Fill(tau.phi(), tau.eta(), tau.pt())

    for tau in taustk:
        histos['h1_taustk'].Fill(tau.phi(), tau.eta(), tau.pt())

    for tau in finaltaus:
        histos['h1_finaltaus'].Fill(tau.phi(), tau.eta(), tau.pt())

    ######################################################################################
        
outfile.cd()

for hh in histos.values():
    hh.Write()

outfile.Close()
