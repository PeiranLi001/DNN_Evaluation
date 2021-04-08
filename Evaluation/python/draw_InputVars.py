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
   leg.AddEntry(h1, "Signal", "L")
   leg.AddEntry(h2, "QCD (data)", "L")

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

def drawHisto3Hist(h1,h2,h3,name,var):
   print "Integral h1 = ",h1.Integral()
   print "Integral h2 = ",h2.Integral()
   print "Integral h3 = ",h3.Integral()

   gStyle.SetOptStat(0000)
   h1.Scale(1./h1.Integral())
   h2.Scale(1./h2.Integral())
   h3.Scale(1./h3.Integral())

   h1.SetMarkerStyle(20)
   h1.SetMarkerColor(kBlue)
   h1.SetLineColor(kBlue)
   h1.SetLineWidth(2)
   h2.SetMarkerStyle(20)
   h2.SetMarkerColor(kRed)
   h2.SetLineColor(kRed)
   h2.SetLineWidth(2)

   h3.SetMarkerStyle(20)
   h3.SetMarkerColor(kGreen)
   h3.SetLineColor(kGreen)
   h3.SetLineWidth(2)

   h1.GetXaxis().SetTitle(var)
   # h1.Scale(41.5)
   # if h1.Integral()!=0 and h2.Integral()!=0: h2.Scale(h1.Integral()/h2.Integral())
   # h2.GetXaxis().SetTitle(var)

   leg = TLegend(0.455,0.80,0.76,0.89,"","brNDC")
   leg.SetBorderSize(0)
   leg.SetTextSize(0.035)
   leg.SetFillColor(0)
   leg.SetNColumns(2)
   leg.AddEntry(h1, "Signal", "L")
   leg.AddEntry(h2, "DiPhoton", "L")
   leg.AddEntry(h3, "QCD(data)", "L")

   maximum = h1.GetMaximum()
   if h2.GetMaximum()>=maximum:
      maximum = h2.GetMaximum()
   if h3.GetMaximum()>=maximum:
      maximum = h3.GetMaximum()

   maximum *=1.01

   h2.GetYaxis().SetRangeUser(0.,maximum)
   c = TCanvas()
   h2.Draw("HIST")
   h1.Draw("HIST,same")
   h3.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+".png","png")
   c.SaveAs(name+".pdf","pdf")

   h2.GetYaxis().SetRangeUser(0.001,maximum*5.)
   c.SetLogy()
   h2.Draw("HIST")
   h1.Draw("HIST,same")
   h3.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+"_log.png","png")
   c.SaveAs(name+"_log.pdf","pdf")

def drawHisto(h1,h2,h3,h4,name,var):
   print "Integral h1 = ",h1.Integral()
   print "Integral h2 = ",h2.Integral()
   print "Integral h3 = ",h3.Integral()
   print "Integral h3 = ",h4.Integral()

   gStyle.SetOptStat(0000)
   h1.Scale(1./h1.Integral())
   h2.Scale(1./h2.Integral())
   h3.Scale(1./h3.Integral())
   h4.Scale(1./h4.Integral())

   h1.SetMarkerStyle(20)
   h1.SetMarkerColor(kBlue)
   h1.SetLineColor(kBlue)
   h1.SetLineWidth(2)
   h2.SetMarkerStyle(20)
   h2.SetMarkerColor(kRed)
   h2.SetLineColor(kRed)
   h2.SetLineWidth(2)

   h3.SetMarkerStyle(20)
   h3.SetMarkerColor(kGreen)
   h3.SetLineColor(kGreen)
   h3.SetLineWidth(2)
   h4.SetMarkerStyle(20)
   h4.SetMarkerColor(kViolet)
   h4.SetLineColor(kViolet)
   h4.SetLineWidth(2)

   h1.GetXaxis().SetTitle(var)
   # h1.Scale(41.5)
   # if h1.Integral()!=0 and h2.Integral()!=0: h2.Scale(h1.Integral()/h2.Integral())
   # h2.GetXaxis().SetTitle(var)

   leg = TLegend(0.455,0.80,0.76,0.89,"","brNDC")
   leg.SetBorderSize(0)
   leg.SetTextSize(0.035)
   leg.SetFillColor(0)
   leg.SetNColumns(2)
   leg.AddEntry(h1, "Signal", "L")
   leg.AddEntry(h2, "DiPhoton", "L")
   leg.AddEntry(h3, "QCD(data)", "L")
   leg.AddEntry(h4, "data", "L")

   maximum = h1.GetMaximum()
   if h2.GetMaximum()>=maximum:
      maximum = h2.GetMaximum()
   if h3.GetMaximum()>=maximum:
      maximum = h3.GetMaximum()
   if h4.GetMaximum()>=maximum:
      maximum = h4.GetMaximum()

   maximum *=1.01

   h2.GetYaxis().SetRangeUser(0.,maximum)
   c = TCanvas()
   h2.Draw("HIST")
   h1.Draw("HIST,same")
   h3.Draw("HIST,same")
   h4.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+".png","png")
   c.SaveAs(name+".pdf","pdf")

   h2.GetYaxis().SetRangeUser(0.001,maximum*5.)
   c.SetLogy()
   h2.Draw("HIST")
   h1.Draw("HIST,same")
   h3.Draw("HIST,same")
   h4.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+"_log.png","png")
   c.SaveAs(name+"_log.pdf","pdf")

def drawHisto6Hist(h1,h2,h3,h4,h5,h6,h7,name,var):
   print("Integral h1 = %f"%h1.Integral())
   print("Integral h2 = %f"%h2.Integral())
   print("Integral h3 = %f"%h3.Integral())
   print("Integral h4 = %f"%h4.Integral())
   print("Integral h5 = %f"%h5.Integral())
   print("Integral h6 = %f"%h6.Integral())
   print("Integral h7 = %f"%h7.Integral())

   gStyle.SetOptStat(0000)
   h1.Scale(1./h1.Integral())
   h2.Scale(1./h2.Integral())
   h3.Scale(1./h3.Integral())
   h4.Scale(1./h4.Integral())
   h5.Scale(1./h5.Integral())
   h6.Scale(1./h6.Integral())
   h7.Scale(1./h7.Integral())

   h1.SetMarkerStyle(20)
   h1.SetMarkerColor(1)
   h1.SetLineColor(1)
   h1.SetLineWidth(2)
   h2.SetMarkerStyle(20)
   h2.SetMarkerColor(2)
   h2.SetLineColor(2)
   h2.SetLineWidth(2)

   h3.SetMarkerStyle(20)
   h3.SetMarkerColor(3)
   h3.SetLineColor(3)
   h3.SetLineWidth(2)
   h4.SetMarkerStyle(20)
   h4.SetMarkerColor(4)
   h4.SetLineColor(4)
   h4.SetLineWidth(2)

   h5.SetMarkerStyle(20)
   h5.SetMarkerColor(8)
   h5.SetLineColor(8)
   h5.SetLineWidth(2)

   h6.SetMarkerStyle(20)
   h6.SetMarkerColor(6)
   h6.SetLineColor(6)
   h6.SetLineWidth(2)

   h7.SetMarkerStyle(20)
   h7.SetMarkerColor(7)
   h7.SetLineColor(7)
   h7.SetLineWidth(2)

   h1.GetXaxis().SetTitle(var)
   # h1.Scale(41.5)
   # if h1.Integral()!=0 and h2.Integral()!=0: h2.Scale(h1.Integral()/h2.Integral())
   # h2.GetXaxis().SetTitle(var)

   leg = TLegend(0.455,0.60,0.76,0.89,"","brNDC")
   leg.SetBorderSize(0)
   leg.SetTextSize(0.035)
   leg.SetFillColor(0)
   leg.SetNColumns(2)
   leg.AddEntry(h1, "Signal", "L")
   leg.AddEntry(h2, "DiPhoton", "L")
   leg.AddEntry(h3, "QCD(data)", "L")
   leg.AddEntry(h4, "ggh", "L")
   leg.AddEntry(h5, "tth", "L")
   leg.AddEntry(h6, "VH", "L")
   leg.AddEntry(h7, "vbfH", "L")

   maximum = h1.GetMaximum()
   if h2.GetMaximum()>=maximum:
      maximum = h2.GetMaximum()
   if h3.GetMaximum()>=maximum:
      maximum = h3.GetMaximum()
   if h4.GetMaximum()>=maximum:
      maximum = h4.GetMaximum()
   if h5.GetMaximum()>=maximum:
      maximum = h5.GetMaximum()
   if h6.GetMaximum()>=maximum:
      maximum = h6.GetMaximum()
   if h7.GetMaximum()>=maximum:
      maximum = h7.GetMaximum()

   maximum *=1.01

   h2.GetYaxis().SetRangeUser(0.,maximum)
   c = TCanvas()
   h2.Draw("HIST")
   h1.Draw("HIST,same")
   h3.Draw("HIST,same")
   h4.Draw("HIST,same")
   h5.Draw("HIST,same")
   h6.Draw("HIST,same")
   h7.Draw("HIST,same")
   leg.Draw("same")
   c.SaveAs(name+".png","png")
   c.SaveAs(name+".pdf","pdf")

   h2.GetYaxis().SetRangeUser(0.001,maximum*5.)
   c.SetLogy()
   h2.Draw("HIST")
   h1.Draw("HIST,same")
   h3.Draw("HIST,same")
   h4.Draw("HIST,same")
   h5.Draw("HIST,same")
   h6.Draw("HIST,same")
   h7.Draw("HIST,same")
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
  #tree = TChain("tagsDumper/trees/GluGluToHHTo2G4Q_node_cHHH1_13TeV_HHWWggTag_1")
  #tree1 = TChain("tagsDumper/trees/DiPhotonJetsBox_MGG_80toInf_13TeV_Sherpa_13TeV_HHWWggTag_1")
  #tree2 = TChain("tagsDumper/trees/Data_13TeV_HHWWggTag_1")
  tree = TChain("output_tree")
  tree1 = TChain("output_tree")
  tree2 = TChain("output_tree")
  tree3 = TChain("output_tree")
  tree4 = TChain("output_tree")
  tree5 = TChain("output_tree")
  tree6 = TChain("output_tree")
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
        if coutFiles==2:
          tree2.AddFile(line)
          print "tree2: file2: ",line
        if coutFiles==3:
          tree3.AddFile(line)
          print "tree3: file3: ",line
        if coutFiles==4:
          tree4.AddFile(line)
          print "tree4: file4: ",line
        if coutFiles==5:
          tree5.AddFile(line)
          print "tree5: file5: ",line
        if coutFiles==6:
          tree6.AddFile(line)
          print "tree6: file6: ",line

        coutFiles = coutFiles+1
  print "--- ############################################################# ---\n"
  print "tree: ",tree
  print "tree1: ",tree1
  print "tree2: ",tree2
  print "tree3: ",tree3
  print "tree4: ",tree4
  print "tree5: ",tree5
  print "tree6: ",tree6

  sel = ''
  sel_noWeight = ''
  if not args.selections:
     sel = 'weight*(Leading_Photon_pt/CMS_hgg_mass>1/3. && Subleading_Photon_pt/CMS_hgg_mass>1/4.)'
     # (0.1, 0.91, 0.97, 1.0)
     sel_noWeight = '(Leading_Photon_pt/CMS_hgg_mass>1/3. && Subleading_Photon_pt/CMS_hgg_mass>1/4. && (DNN_evaluation<1.0 && DNN_evaluation>0.97))'
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
     if line[0] == "#": continue
     inputs = line.split()
     print "inputs: ",inputs
     # hist_weight = TH1F("h_"+str(inputs[0])+"_weight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     # hist_weight1 = TH1F("h1_"+str(inputs[0])+"_weight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight = TH1F("h_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight1 = TH1F("h1_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight2 = TH1F("h2_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight3 = TH1F("h3_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight4 = TH1F("h4_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight5 = TH1F("h5_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     hist_noWeight6 = TH1F("h6_"+str(inputs[0])+"_noWeight",str(inputs[0]),int(inputs[1]),float(inputs[2]),float(inputs[3]))
     tree.Draw(str(inputs[0])+">>h_"+str(inputs[0])+"_noWeight",sel_noWeight)
     tree1.Draw(str(inputs[0])+">>h1_"+str(inputs[0])+"_noWeight",sel_noWeight)
     tree2.Draw(str(inputs[0])+">>h2_"+str(inputs[0])+"_noWeight",sel_noWeight)
     tree3.Draw(str(inputs[0])+">>h3_"+str(inputs[0])+"_noWeight",sel_noWeight)
     tree4.Draw(str(inputs[0])+">>h4_"+str(inputs[0])+"_noWeight",sel_noWeight)
     tree5.Draw(str(inputs[0])+">>h5_"+str(inputs[0])+"_noWeight",sel_noWeight)
     tree6.Draw(str(inputs[0])+">>h6_"+str(inputs[0])+"_noWeight",sel_noWeight)
     print("integral: %f"%hist_noWeight.Integral())
     print("integral: %f"%hist_noWeight1.Integral())
     print("integral: %f"%hist_noWeight2.Integral())
     print("integral: %f"%hist_noWeight3.Integral())
     print("integral: %f"%hist_noWeight4.Integral())
     print("integral: %f"%hist_noWeight5.Integral())
     print("integral: %f"%hist_noWeight6.Integral())
     # if inputs[0]!="weight": tree.Draw(str(inputs[0])+">>h_"+str(inputs[0])+"_weight",sel)
     # else: tree.Draw(str(inputs[0])+">>h_"+str(inputs[0])+"_weight",sel_noWeight)
     # if inputs[0]!="weight": tree.Draw(str(inputs[0])+">>h1_"+str(inputs[0])+"_weight",sel)
     # else: tree.Draw(str(inputs[0])+">>h1_"+str(inputs[0])+"_weight",sel_noWeight)
     # drawHisto3Hist(hist_noWeight,hist_noWeight1,hist_noWeight2,str(inputs[0]),inputs[4])
     # drawHisto(hist_noWeight,hist_noWeight1,hist_noWeight2,hist_noWeight3,str(inputs[0]),inputs[4])
     drawHisto6Hist(hist_noWeight,hist_noWeight1,hist_noWeight2,hist_noWeight3,hist_noWeight4,hist_noWeight5,hist_noWeight6,str(inputs[0]),inputs[4])


