import ROOT
import sifca_utils
import click
import os


sifca_utils.plotting.set_sifca_style()

# ROOT configuration
projection = False
save_plots = True
FORMAT = ".pdf"
omit_plots = True
z_limited = True
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(0)
histogram_type = ["cml_int", "cml_rad", "p2p_int", "p2p_rad", "hit_map"]
plane_names = [
    "EndVelo",
    "EndRich1", 
    "AfterTT", 
    "AfterMagnet", 
    "AfterOTPlane1", 
    "AfterOTPlane2", 
    "AfterOTPlane3", 
    "AfterRich2", 
    "AfterSpd", 
    "AfterECAL", 
    "AfterM2",
    "AfterM2Filter",
    "EoD",
    ]

limit_z = {
    "EndVelo" :       {"min" : 0, "max" : 60},
    "EndRich1" :      {"min" : 0, "max" : 40},
    "AfterTT" :       {"min" : 0, "max" : 70},
    "AfterMagnet" :   {"min" : 0, "max" : 150},
    "AfterOTPlane1" : {"min" : 0, "max" : 100},
    "AfterOTPlane2" : {"min" : 0, "max" : 100},
    "AfterOTPlane3" : {"min" : 0, "max" : 100},
    "AfterRich2" :    {"min" : 0, "max" : 700},
    "AfterSpd" :      {"min" : 0, "max" : 6},
    "AfterECAL" :     {"min" : 0, "max" : 2500},
    "AfterM2" :       {"min" : 0, "max" : 10000},
    "AfterM2Filter" : {"min" : 0, "max" : 60}, 
    "EoD" :           {"min" : 3000, "max" : 5000}, 
}

@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    """
    Plot the full LHCb scans
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
                c = ROOT.TCanvas()
                c.SetRightMargin(0.25) 
                h = tree.Get(name+type)
                h.Draw("colz")
                # h.GetXaxis().SetTitle("#eta")
                # h.GetYaxis().SetTitle("#phi")
                h.GetXaxis().SetTitle("X/mm")
                h.GetYaxis().SetTitle("Y/mm")
                h.GetZaxis().SetTitle("X/X0 (%)")
                # Move Z axis label to the right
                h.GetZaxis().SetTitleOffset(1.5)
                if not omit_plots:
                    input("Press enter to continue")
                    c.Draw()
                if save_plots:
                    c.SaveAs(f"Pictures/{folder}/{name}{type}{FORMAT}")
                # Delete canvas
                c.Close()

                # Limit range in z of the plot
                if z_limited and type != "hit_map":
                    c = ROOT.TCanvas()
                    c.SetRightMargin(0.2) 
                    h.GetZaxis().SetRangeUser(limit_z[i]["min"], limit_z[i]["max"])
                    h = tree.Get(name+type)
                    h.Draw("colz")
                        # h.GetXaxis().SetTitle("#eta")
                        # h.GetYaxis().SetTitle("#phi")
                    h.GetXaxis().SetTitle("X/mm")
                    h.GetYaxis().SetTitle("Y/mm")
                    h.GetZaxis().SetTitle("X/X0 (%)")
                    # Move Z axis label to the right
                    h.GetZaxis().SetTitleOffset(1.5)

                    if not omit_plots:
                        input("Press enter to continue")
                        c.Draw()
                    if save_plots:
                        c.SaveAs(f"Pictures/{folder}/{name}_zlimited_{type}{FORMAT}")
                    # Delete canvas
                    c.Close()
                # Project over x-axis
                if projection:
                    c_proj = ROOT.TCanvas("c_proj")
                    h_proj = tree.Get(name+type)
                    h_proj.ProjectionX("Normalise").Draw()
                    h_proj.GetYaxis().SetTitle("Entries")
                    if not omit_plots:
                        input("Press enter to continue")
                        c_proj.Draw()
                    if save_plots:
                        c_proj.SaveAs(f"Pictures/{folder}/{name}_projX_{type}{FORMAT}")
                    # Delete canvas
                    c_proj.Close()


if __name__ == '__main__':
    main()
