import sys
sys.path.append('..')
import ROOT
from objects.Fitter import Fitter


class MultiGraph(ROOT.TMultiGraph):
    '''
    '''
    
    def __init__(self, *args,  **kwargs):
        super(MultiGraph, self).__init__(*args)
        
        if 'graphs' not in kwargs.keys():
            raise
        
        self.graphs  = kwargs['graphs']
        self.graphse = []
        

    def Fill(self):

        self.leg = ROOT.TLegend( 0.5, 0.3, 0.88, 0.6 )
        self.leg.SetTextSize(0.027)
        self.leg.SetFillColor(ROOT.kWhite)
        self.leg.SetLineColor(ROOT.kWhite)
    
        for graph in self.graphs:
            file = ROOT.TFile.Open(graph.file, 'read')
            file.cd()
            igraph = file.Get(graph.graph)
            igraph.SetMarkerColor(graph.colour)
            
            if graph.function:
                print '\n=====> Fitting %s' %graph.graph
                fitter = Fitter(igraph, graph.function, colour = graph.colour)
                igraph, igrapherror, results = fitter._fit()
                self.graphse.append(igrapherror)
            
            self.Add(igraph)
            self.leg.AddEntry(igraph, graph.legend, graph.legendOpt)

    def DrawUncertainty(self):
        
        for graphe in self.graphse:
            graphe.Draw('SAME E3')

        
        
        
        
