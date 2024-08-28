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
histogram_type = ["cml_int", "cml_rad", "p2p_int", "p2p_rad"]
hit_map = "hit_map"
@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    """
    This function plot the rootfile with the results of the SP0, P0 SP1 when the uniform particlegun is used
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
            # Plot and store the hit map
            c = ROOT.TCanvas()
            c.SetRightMargin(0.2)  
            h_hit_map = tree.Get(name+hit_map)
            h_hit_map.Draw("colz")
            h_hit_map.GetXaxis().SetTitle("X/mm")
            h_hit_map.GetYaxis().SetTitle("Y/mm")
            if not omit_plots:
                input("Press enter to continue")
                c.Draw()
            if save_plots:
                c.SaveAs(f"Pictures/{folder}/{name}{hit_map}{FORMAT}")

            # Loop over the histogram types
            for type in histogram_type:
                c = ROOT.TCanvas()
                c.SetRightMargin(0.2)  
                h = tree.Get(name+type)
                h.Draw("colz")
                # Divide histogram by hit map
                h.Divide(h_hit_map)
                h.GetXaxis().SetTitle("X/mm")
                h.GetYaxis().SetTitle("Y/mm")               
                if not omit_plots:
                    input("Press enter to continue")
                    c.Draw()
                if save_plots:
                    c.SaveAs(f"Pictures/{folder}/{name}{type}{FORMAT}")



if __name__ == '__main__':
    main()