import sys
import json
sys.path.append('..')
import ROOT
import numpy as np
from array import array
from objects.Fitter import Fitter


class MultiGraph(ROOT.TMultiGraph):
    '''
    '''
    
    def __init__(self, *args,  **kwargs):
        super(MultiGraph, self).__init__(*args)
        
        if 'graphs' not in kwargs.keys():
            raise

        if 'legendPosition' not in kwargs.keys():
            raise

        if 'json' in kwargs.keys():
            self.json = kwargs['json']
        else:
            self.json = None
        
        self.graphs  = kwargs['graphs']
        self.graphse = []

        for graph in self.graphs:
            file = ROOT.TFile.Open(graph.file, 'read')
            file.cd()
            graph.graph = file.Get(graph.graphname)
            graph.graph.SetMarkerColor(graph.colour)

        self.legpos = kwargs['legendPosition']

                
    def Fill(self):

        if self.legpos == 0: self.leg = ROOT.TLegend( 0.5, 0.3, 0.88, 0.6 )
        if self.legpos == 1: self.leg = ROOT.TLegend( 0.35, 0.73, 0.88, 0.88 )
        if self.legpos == 2: self.leg = ROOT.TLegend( 0.4, 0.25, 0.88, 0.7 )
        if self.legpos == 3: self.leg = ROOT.TLegend( 0.5, 0.7, 0.88, 0.88 )
        if self.legpos == 4: self.leg = ROOT.TLegend( 0.4, 0.16, 0.88, 0.35 )
        if self.legpos == 5: self.leg = ROOT.TLegend( 0.4, 0.16, 0.88, 0.5 )
        if self.legpos == 6: self.leg = ROOT.TLegend( 0.25, 0.16, 0.88, 0.5 )
        if self.legpos == 7: self.leg = ROOT.TLegend( 0.6, 0.2, 0.88, 0.3  )
        self.leg.SetTextSize(0.027)
        self.leg.SetFillColor(ROOT.kWhite)
        self.leg.SetLineColor(ROOT.kWhite)
    
        myjson = {}
        for graph in self.graphs:
            
            if graph.function:
                print '\n=====> Fitting %s' %graph.graph
                fitter = Fitter(graph.graph, graph.function, colour = graph.colour)
                graph.graph, graph.grapherror, results = fitter._fit()
                self.graphse.append(graph.grapherror)
                if self.json:
                    if not self.json.endswith('.json'):
                        self.json = json + '.json'
                    myjson.update({graph.legend : {results.GetParameterName(i) : results.GetParams()[i] for i in range(results.NPar())}})
            self.Add(graph.graph)
            self.leg.AddEntry(graph.graph, graph.legend, graph.legendOpt)

        f1 = open(self.json, 'a')
        print >> f1, json.dumps(myjson, indent=4)            
        
        f1.close()

    def DrawUncertainty(self):
        
        for graphe in self.graphse:
            graphe.Draw('SAME E3')

        
    def returnRatios(self):
        '''
        '''
        references = [graph for graph in self.graphs if graph.reference == 1]
        others     = [graph for graph in self.graphs if graph.reference == 0]
        
        if len(references)>1:
            print 'ERROR! more than one reference, returning None'
            return None
        if not len(references):
            print 'ERROR! no reference specified, returning None '
            return None

        reference = references[0]
        
        ratiomg = ROOT.TMultiGraph()

        x_ref = []
        y_ref = []

        n_ref = reference.graph.GetN()
        
        for i in range(n_ref):
            x = ROOT.Double()
            y = ROOT.Double()
            reference.graph.GetPoint(i, x, y)
            x_ref.append(x)
            y_ref.append(y)

        
        x_ref = np.array(x_ref)
        y_ref = np.array(y_ref)

        for gg in others:
            x_gg = []
            y_gg = []
            for i in range(n_ref):
                x = ROOT.Double()
                y = ROOT.Double()
                gg.graph.GetPoint(i, x, y)
                x_gg.append(x)
                y_gg.append(y)
    
            x_gg = np.array(x_gg)
            y_gg = np.array(y_gg)

            
            if x_gg.all() != x_ref.all():
                print 'ERROR! dividing two graphs with different x'
                return None
                    
            y_new = np.divide(y_gg, y_ref)

            x_cleaned = []
            y_cleaned = []
            
            for x, y in zip(x_ref, y_new):
                if np.isnan(y) or np.isinf(y):
                    continue
                x_cleaned.append(x)
                y_cleaned.append(y)
                    
            gg_new = ROOT.TGraph(len(x_cleaned), array('f', x_cleaned), array('f', y_cleaned))
            gg_new.SetMarkerColor(gg.colour)
            gg_new.SetMarkerStyle(8)
            ratiomg.Add(gg_new)
        
        return ratiomg
        
        
        
