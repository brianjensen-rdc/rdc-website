#!/usr/bin/env python3
"""One-time media curation for rdc-website (run by .github/workflows/curate-media.yml).

1. Copies the images the live reddoorcollaborative.com uses (matched by
   Squarespace asset ID) out of asset-library/ into src/media/, with readable
   names. Videos used by the case study pages go to public/media/video/.
2. Repoints the case study pages from raw.githubusercontent.com links to the
   copied files (images as Astro imports, videos via BASE_URL).
3. Removes asset-library/ from the repo (it stays in git history).
"""
import os, re, shutil, subprocess, sys, urllib.parse

A = "asset-library/"
# (source file in asset-library/, destination)
LIVE = [
    ("RDC_InfinityChart_NoLabels_Light.png", "src/media/home/infinity-chart.png"),
    ("images_Microsoft logo_gray.png", "src/media/clients/microsoft.png"),
    ("images_Salesforce logo_gray.png", "src/media/clients/salesforce.png"),
    ("images_Databricks logo_gray.png", "src/media/clients/databricks.png"),
    ("images_Procraft logo_gray.png", "src/media/clients/procraft.png"),
    ("images_Meta logo_gray.png", "src/media/clients/meta.png"),
    ("images_icon_redcolor.png", "src/media/about/icon-red.png"),
    ("images_icon_doorsymbol.png", "src/media/about/icon-door.png"),
    ("images_icon_collaboratereason.png", "src/media/about/icon-collaborative.png"),
    ("images_diverse-team.png", "src/media/about/diverse-team.png"),
    ("Chris_headshot.png", "src/media/team/chris-telfer.png"),
    ("Jenny_headshot.png", "src/media/team/jenny-telfer.png"),
    ("Brian_headshot.png", "src/media/team/brian-jensen.png"),
    ("Amy_headshot.png", "src/media/team/amy-metzler.png"),
    ("Erin.jpg", "src/media/team/erin-genest.jpg"),
    ("Najwa_headshot.png", "src/media/team/najwa-yosof.png"),
    ("nathan_headshot.png", "src/media/team/nathan-smith.png"),
    ("Joy_headshot.png", "src/media/team/joy-baer.png"),
    ("justine.jpg", "src/media/team/justine-brown.jpg"),
    ("images_icon_collaborate.png", "src/media/services/icon-collaborate.png"),
    ("images_icon_create.png", "src/media/services/icon-create.png"),
    ("images_icon_scale.png", "src/media/services/icon-scale.png"),
    ("images_embedded-consulting.png", "src/media/services/embedded-consulting.png"),
    ("images_project-based-consulting.png", "src/media/services/project-based-consulting.png"),
    ("images_managed-services (1).png", "src/media/services/managed-services.png"),
    ("images_editorial.png", "src/media/services/editorial.png"),
    ("images_visual-design.png", "src/media/services/visual-design.png"),
    ("images_video-motion.png", "src/media/services/video-motion.png"),
    ("unified.png", "src/media/careers/values.png"),
    ("images_remote-work (1).png", "src/media/careers/remote-work.png"),
    ("images_minority-business-badge.png", "src/media/careers/minority-business-badge.png"),
    ("thumbnails_azure-essentials-campaign.png", "src/media/work/azure-essentials.png"),
    ("thumbnails_visual-studio-ide-campaign__1.png", "src/media/work/vss-benefits.png"),
    ("thumbnails_procraft-courses-campaign.png", "src/media/work/procraft.png"),
    ("thumbnails_FinOps-Sustnblty-ebook.png", "src/media/work/finops-ebook.png"),
    ("thumbnails_azure-socials.png", "src/media/work/azure-social.png"),
    ("vssVideo17_gif_v1.gif", "src/media/work/vss-video.gif"),
    ("thumbnails_databricks-lakehouse-ebook__1.png", "src/media/work/databricks-ebook.png"),
    ("rdcSocials_gif_v1.gif", "src/media/work/rdc-social.gif"),
    ("AzureEssentials_gif_v1.gif", "src/media/work/azure-essentials-show.gif"),
]
# Used by the case study pages; not yet verified against the live case study pages.
CASE = [
    ("Azura Essentials-Dark_640x320.png", "src/media/case-studies/azure-essentials/lockup-dark.png"),
    ("Azura Essentials-Light_640x320.png", "src/media/case-studies/azure-essentials/lockup-light.png"),
    ("Azure Essentials_thumbnail.png", "src/media/case-studies/azure-essentials/thumbnail.png"),
    ("AzureEssentialsVideo-OpeningFrame.png", "src/media/case-studies/azure-essentials/video-opening-frame.png"),
    ("Event style guide_AzureEssentialsTechAccelerator.png", "src/media/case-studies/azure-essentials/event-style-guide.png"),
    ("Azura Essentials_email banner 1.png", "src/media/case-studies/azure-essentials/email-banner-1.png"),
    ("Azura Essentials_email banner 2.png", "src/media/case-studies/azure-essentials/email-banner-2.png"),
    ("VSS Twitter Banner.png", "src/media/case-studies/vss-benefits/twitter-banner.png"),
    ("Q4_VSS Social_Ad2_VSLive.png", "src/media/case-studies/vss-benefits/social-ad-vslive.png"),
    ("MICROSOCF VSS (A4 SIZE) FA (DIGITAL)_Page_1.png", "src/media/case-studies/vss-benefits/benefits-flyer.png"),
    ("ProCraft_BrandingGuidelines 1_Page_01.png", "src/media/case-studies/procraft/brand-guidelines-01.png"),
    ("ProCraft_BrandingGuidelines 1_Page_05 (1).png", "src/media/case-studies/procraft/brand-guidelines-05.png"),
    ("ProCraft_BrandingGuidelines 1_Page_09 (1).png", "src/media/case-studies/procraft/brand-guidelines-09.png"),
    ("AzureEssentials_Intro-2024_v03-00.mp4", "public/media/video/azure-essentials-intro.mp4"),
    ("Azure Essentials \u2013 Customer Presentation_2024_final-portfolioedit.mp4", "public/media/video/azure-essentials-customer-presentation.mp4"),
]

# Byte-identical duplicates in the archive that the case study pages link to.
ALIASES = {
    "thumbnails_visual-studio-ide-campaign.png": "thumbnails_visual-studio-ide-campaign__1.png",
}

def main():
    dest_for = {}
    for src, dst in LIVE + CASE:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(A + src, dst)  # raises if a source file is missing
        dest_for.setdefault(src, dst)
    print(f"copied {len(LIVE)} live-site files and {len(CASE)} case study files")

    raw = re.compile(r"'https://raw\.githubusercontent\.com/brianjensen-rdc/rdc-website/main/asset-library/([^']+)'")
    for page in ["src/pages/case-study-azure-essentials.astro",
                 "src/pages/case-study-vss-benefits.astro",
                 "src/pages/case-study-procraft.astro"]:
        s = open(page, encoding="utf-8").read()
        imports, names = [], {}
        def repl(m):
            src = urllib.parse.unquote(m.group(1))
            dst = dest_for[ALIASES.get(src, src)]
            if dst.startswith("public/"):
                return "`${import.meta.env.BASE_URL}" + dst[len("public/"):] + "`"
            if dst not in names:
                names[dst] = f"media{len(names) + 1}"
                imports.append(f"import {names[dst]} from '../{dst[len('src/'):]}';")
            return f"{names[dst]}.src"
        s, n = raw.subn(repl, s)
        if raw.search(s):
            sys.exit(f"unreplaced link left in {page}")
        # Add the imports right after the opening frontmatter fence.
        assert s.startswith("---\n"), page
        s = "---\n" + "\n".join(imports) + "\n" + s[4:]
        # Update the old provenance comment.
        s = re.sub(r"// Served straight from this repo's asset-library/ archive.*?\n(?=\S)(?!//)",
                   "", s, count=1, flags=re.S)
        open(page, "w", encoding="utf-8").write(s)
        print(f"{page}: {n} links repointed, {len(imports)} imports added")

    shutil.rmtree("asset-library")
    print("removed asset-library/")

if __name__ == "__main__":
    main()
