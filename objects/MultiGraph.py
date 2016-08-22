import sys
import json
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

        if 'json' in kwargs.keys():
            self.json = kwargs['json']
        else:
            self.json = None
        
        self.graphs  = kwargs['graphs']
        self.graphse = []
        

    def Fill(self):

        #self.leg = ROOT.TLegend( 0.5, 0.3, 0.88, 0.6 )
        self.leg = ROOT.TLegend( 0.35, 0.73, 0.88, 0.88 )
        self.leg.SetTextSize(0.027)
        self.leg.SetFillColor(ROOT.kWhite)
        self.leg.SetLineColor(ROOT.kWhite)
    
        myjson = {}
        for graph in self.graphs:
            file = ROOT.TFile.Open(graph.file, 'read')
            file.cd()
            igraph = file.Get(graph.graph)
            igraph.SetMarkerColor(graph.colour)
            #igraph.SetMarkerSize(0.00000001)
            
            if graph.function:
                print '\n=====> Fitting %s' %graph.graph
                fitter = Fitter(igraph, graph.function, colour = graph.colour)
                igraph, igrapherror, results = fitter._fit()
                self.graphse.append(igrapherror)
                if self.json:
                    if not self.json.endswith('.json'):
                        self.json = json + '.json'
                    myjson.update({graph.legend : {results.GetParameterName(i) : results.GetParams()[i] for i in range(results.NPar())}})
            self.Add(igraph)
            self.leg.AddEntry(igraph, graph.legend, graph.legendOpt)

        f1 = open(self.json, 'a')
        print >> f1, json.dumps(myjson, indent=4)            
        
        f1.close()

    def DrawUncertainty(self):
        
        for graphe in self.graphse:
            graphe.Draw('SAME E3')

        
        
        
        
