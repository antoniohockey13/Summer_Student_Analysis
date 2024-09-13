import ROOT
import sifca_utils
import click
import os


sifca_utils.plotting.set_sifca_style()

# ROOT configuration
save_plots = True
FORMAT = ".pdf"
omit_plots = True
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(0)
histogram_type = ["hit_map", "cml_int", "cml_rad", "p2p_int", "p2p_rad"]

@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    """
    This function plot the rootfile with the results of the SP0, P0 SP1 when the grid particlegun is used
    """
    for file in inputfiles:
        #Save plots
        if save_plots:
            # Configure save directory
            folder = file.split("/")[-1].split(".")[0]
            os.makedirs(f"Pictures/{folder}", exist_ok=True)
        # Draw and analyse the root file
        # Get the histograms folder
        f = ROOT.TFile(file)
        dir ="GiGaMT/GiGaActionInitializer"
        d = f.Get(dir)
        tree_name = "RadLengthColl"
        tree = d.Get(tree_name)    
        # Loop over the two scoring planes
        for i in range(2):
            name = "ScoringPlane_"+str(i)+"PVolHist_"
            # Loop over the histogram types
            for type in histogram_type:
                c = ROOT.TCanvas()
                c.SetRightMargin(0.2)  
                h = tree.Get(name+type)
                h.Draw("colz")
                # Divide histogram by hit map
                h.GetXaxis().SetTitle("X/mm")
                h.GetYaxis().SetTitle("Y/mm")
                h.GetZaxis().SetTitle("X/X0 (%)")
                # Move Z axis label to the right
                h.GetZaxis().SetTitleOffset(1.2)
                # Write z axis in math mode
                if not omit_plots:
                    input("Press enter to continue")
                    c.Draw()
                if save_plots:
                    c.SaveAs(f"Pictures/{folder}/{name}{type}{FORMAT}")



if __name__ == '__main__':
    main()