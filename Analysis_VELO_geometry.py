import ROOT
import sifca_utils
import click
import os


sifca_utils.plotting.set_sifca_style()

# ROOT configuration
plot_log = False
limit_z = False
projection = False
omit_plots = True
save_plots = True
FORMAT = ".pdf"
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(0)
histogram_type = ["cml_int", "cml_rad", "p2p_int", "p2p_rad", "hit_map"]
plane_names = ["EndVelo"]

@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    """
    Plot the VELO LHCb scan
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

        # Loop over the scoring planes
        for i in plane_names:
            name = f"ScoringPlane_{i}PVolHist_"
            for type in histogram_type:
                name = f"ScoringPlane_{i}PVolHist_"
                c = ROOT.TCanvas()
                c.SetRightMargin(0.2) 
                h = tree.Get(name+type)
                h.Draw("colz")
                # Limit range in z of the plot
                if limit_z and type != "hit_map":
                    h.GetZaxis().SetRangeUser(0, 60)
                if plot_log:
                    c.SetLogz()
                # h.GetXaxis().SetTitle("#eta")
                # h.GetYaxis().SetTitle("#phi")
                h.GetXaxis().SetTitle("X/mm")
                h.GetYaxis().SetTitle("Y/mm")
                h.GetZaxis().SetTitle("X/X0 (%)")
                h.GetZaxis().SetTitleOffset(1.2)
                if not omit_plots:
                    input("Press enter to continue")
                    c.Draw()
                if save_plots:
                    if plot_log:
                        name = f"{name}log"
                    if limit_z:
                        name = f"{name}zlimited"
                    c.SaveAs(f"Pictures/{folder}/{name}{type}{FORMAT}")

if __name__ == '__main__':
    main()
