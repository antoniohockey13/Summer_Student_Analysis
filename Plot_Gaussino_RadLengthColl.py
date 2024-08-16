import ROOT
import sifca_utils
import click
import os


sifca_utils.plotting.set_sifca_style()

# ROOT configuration
save_plots = True
FORMAT = ".pdf"
omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(0)

# Name of histograms Scoring_Plane_XPVolHist_ + cml_int, cml_rad, p2p_int, p2p_rad, hit_map
histogram_type = ["cml_int", "cml_rad", "p2p_int", "p2p_rad", "hit_map"]

def left_right(file):
    """
    This function plot the rootfile with the results of the SP0, P0 SP1, P1, SP2
    And the P0 and P1 are displaced between them 
    """
    folder = file.split("/")[-1].split(".")[0]
    f = ROOT.TFile(file)
    dir ="GiGaMT/GiGaActionInitializer"
    d = f.Get(dir)
    tree_name = "RadLengthColl"
    tree = d.Get(tree_name)    
    for i in range(3):
        name = f"ScoringPlane_{str(i)}PVolHist_"
        for type in histogram_type:
            c = ROOT.TCanvas()
            h = tree.Get(name+type)
            h.Draw("colz")
            h.GetXaxis().SetTitle("X/m")
            h.GetYaxis().SetTitle("Y/m")
            if not omit_plots:
                input("Press enter to continue")
                c.Draw()
            if save_plots:
                c.SaveAs(f"Pictures/{folder}/{name}{type}{FORMAT}")

def two_mat(file):
    """
    This function plot the rootfile with the results of the SP0, P0 SP1
    When the P0 is divided in two materials, one in the left half and the other in the right half
    """
    folder = file.split("/")[-1].split(".")[0]
    f = ROOT.TFile(file)
    dir ="GiGaMT/GiGaActionInitializer"
    d = f.Get(dir)
    tree_name = "RadLengthColl"
    tree = d.Get(tree_name)    
    for i in range(2):
        name = "ScoringPlane_"+str(i)+"PVolHist_"
        for type in histogram_type:
            c = ROOT.TCanvas()
            h = tree.Get(name+type)
            h.Draw("colz")
            h.GetXaxis().SetTitle("X/m")
            h.GetYaxis().SetTitle("Y/m")
            if not omit_plots:
                input("Press enter to continue")
                c.Draw()
            if save_plots:
                c.SaveAs(f"Pictures/{folder}/{name}{type}{FORMAT}")



@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    for file in inputfiles:
        if save_plots:
            # Configure save directory
            folder = file.split("/")[-1].split(".")[0]
            os.makedirs(f"Pictures/{folder}", exist_ok=True)

        if file.split('/')[-1] == "Results_Left_Right_Planes.root":
            left_right(file)
        elif file.split('/')[-1] == "Results_Plane_2_Mat.root":
            two_mat(file)


if __name__ == '__main__':
    main()