import ROOT
import sifca_utils
import click
import os

# ROOT configuration
save_plots = True
FORMAT = ".pdf"
omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(0)

# Name of histograms Scoring_Plane_XPVolHist_ + cml_Int, cml_rad, p2p_Int, p2p_rad, hit_map
histogram_type = ["cml_Int", "cml_rad", "p2p_Int", "p2p_rad", "hit_map"]
def get_tree(file):
    """
    This function returns the tree of the rootfile
    """
    f = ROOT.TFile(file)
    f.cd("GiGaMT/GiGaActionInitializer")  
    tree = f.Get("RadLengthColl")
    return tree  

def left_right(file):
    """
    This function plot the rootfile with the results of the SP0, P0 SP1, P1, SP2
    And the P0 and P1 are displaced between them 
    """
    f = get_tree(file)
    for i in range(3):
        name = "Scoring_Plane_"+str(i)+"PVolHist_"
        for type in histogram_type:
            c = ROOT.TCanvas()
            h = f.Get(name+type)
            h.Draw("colz")
            if not omit_plots:
                c.Draw()
            if save_plots:
                c.SaveAs("Results/"+name+type+FORMAT)


@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    for file in in inputfiles:
        if save_plots:
            # Configure save directory
            folder = file.split("/")[-1].split(".")[0]
            os.makedirs(f"Pictures/{folder}", exist_ok=True)

            
        if file == "Results_Left_Right_Planes.root":
            left_right(file)







if __name__ == '__main__':
    main()