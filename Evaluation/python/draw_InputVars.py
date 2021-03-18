#!/usr/bin/python
import numpy as n
from ROOT import *
from array import array
import operator
import math  
import sys
import os
import argparse
import random
from math import *

def drawHisto(h1,h2,name,var):
   print "Integral h1 = ",h1.Integral()
   print "Integral h2 = ",h2.Integral()

   gStyle.SetOptStat(0000)
   h1.Scale(1./h1.Integral())
   h2.Scale(1./h2.Integral())

   h1.SetMarkerStyle(20)
   h1.SetMarkerColor(kBlue) 
   h1.SetLineColor(kBlue) 
   h1.SetLineWidth(2) 
   h2.SetMarkerStyle(20)
   h2.SetMarkerColor(kRed) 
   h2.SetLineColor(kRed) 
   h2.SetLineWidth(2) 
   
   h1.GetXaxis().SetTitle(var)
   h1.Scale(41.5)
   if h1.Integral()!=0 and h2.Integral()!=0: h2.Scale(h1.Integral()/h2.Integral())
   h2.GetXaxis().SetTitle(var)

   leg = TLegend(0.455,0.85,0.76,0.89,"","brNDC")
   leg.SetBorderSize(0)  
   leg.SetTextSize(0.035)
   leg.SetFillColor(0)
   leg.SetNColumns(2)
   leg.AddEntry(h1, "w/ weights", "L")
   leg.AddEntry(h2, "w/o weights", "L")
  
   maximum = h1.GetMaximum()
   if h2.GetMaximum()>=maximum:
      maximum = h2.GetMaximum()

   maximum *=1.01
   
   h2.GetYaxis().SetRangeUser(0.,maximum)
   c = TCanvas()
   h2.Draw("HIST")
   h1.Draw("HIST,same") 
   leg.Draw("same")
   c.SaveAs(name+".png","png") 
   c.SaveAs(name+".pdf","pdf") 

   h2.GetYaxis().SetRangeUser(0.001,maximum*5.)
   c.SetLogy() 
   h2.Draw("HIST")
   h1.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+"_log.png","png") 
   c.SaveAs(name+"_log.pdf","pdf") 

if __name__ == '__main__':

  gROOT.SetBatch(kTRUE)

  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--inputTrees", type=str, help="inputTrees", required=True)
  parser.add_argument("-v", "--inputVars", type=str, help="inputVars", required=True)
  parser.add_argument("-s", "--selections", type=str, help="selections", required=False)
  args = parser.parse_args()

  #fill trees
  print "\n--- ############################################################# ---"
  tree = TChain("output_tree")
  tree1 = TChain("output_tree")
  with open(args.inputTrees) as f_list:
     data_list = f_list.read()
  lines = data_list.splitlines() 
  coutFiles = 0
  for iLine,line in enumerate(lines):
     if line[0]!="#": 
        print "InputTree: ",coutFiles,"\t",line
        if coutFiles==0:
          tree.AddFile(line)
          print "tree: file: ",line
        if coutFiles==1:
          tree1.AddFile(line)
          print "tree1: file1: ",line
        coutFiles = coutFiles+1
  print "--- ############################################################# ---\n"
  print "tree: ",tree
  print "tree1: ",tree1

  sel = ''
  sel_noWeight = ''
  if not args.selections:
     sel = 'weight*(Leading_Photon_pt/CMS_hgg_mass>1/3. && Subleading_Photon_pt/CMS_hgg_mass>1/4.)'
     sel_noWeight = 'Leading_Photon_pt/CMS_hgg_mass>1/3. && Subleading_Photon_pt/CMS_hgg_mass>1/4.' 
  else:
     sel = 'weight*('+args.selections+')' 
     sel_noWeight = args.selections

  print "\n--- ############################################################# ---"
  print "Selections: ",sel_noWeight 
  print "--- ############################################################# ---\n"

  #fill variables
  with open(args.inputVars) as f_list:
     data_list = f_list.read()
  lines = data_list.splitlines() 
  for iLine,line in enumerate(lines):
     print iLine, line
     inputs = line.split()
     print "inputs: ",inputs
     # hist_weight = TH1F("h_"+str(inputs[0])+"_weight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     # hist_weight1 = TH1F("h1_"+str(inputs[0])+"_weight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight = TH1F("h_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight1 = TH1F("h1_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     tree.Draw(str(inputs[0])+">>h_"+str(inputs[0])+"_noWeight",sel_noWeight)
     tree1.Draw(str(inputs[0])+">>h1_"+str(inputs[0])+"_noWeight",sel_noWeight)
     # if inputs[0]!="weight": tree.Draw(str(inputs[0])+">>h_"+str(inputs[0])+"_weight",sel)
     # else: tree.Draw(str(inputs[0])+">>h_"+str(inputs[0])+"_weight",sel_noWeight)
     # if inputs[0]!="weight": tree.Draw(str(inputs[0])+">>h1_"+str(inputs[0])+"_weight",sel)
     # else: tree.Draw(str(inputs[0])+">>h1_"+str(inputs[0])+"_weight",sel_noWeight)     
     drawHisto(hist_noWeight,hist_noWeight1,str(inputs[0]),inputs[4])

  
