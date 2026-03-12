"""
generate_paper_figures.py
─────────────────────────────────────────────────────────────────────────────
Generates two IEEE-style paper figures for the RDHEI method:

  Fig 1  —  Framework of the proposed method
             (Image Owner / Data-Hider / Receiver)

  Fig 2  —  Auxiliary bitstream structure LA
             (showing our simplified header vs base-paper LR)

Output files  (saved in same folder as this script):
  fig1_framework.png  /  fig1_framework.pdf
  fig2_bitstream.png  /  fig2_bitstream.pdf

Requirements:  matplotlib  (pip install matplotlib)
─────────────────────────────────────────────────────────────────────────────
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ── output directory = folder containing this script ─────────
OUT = os.path.dirname(os.path.abspath(__file__))

# ── colour palette ────────────────────────────────────────────
SALMON  = "#F5A88C"   # image-owner / recovered image boxes
GREEN   = "#7CBF7C"   # shared / embedding / extraction boxes
YELLOW  = "#E8D460"   # encryption / key boxes
BLUE    = "#7AADD4"   # receiver processing boxes
BG      = "#FFFFFF"   # background
BDR     = "#1a1a1a"   # box border
DASH_C  = "#555555"   # dashed-region border
TXT     = "#1a1a1a"   # default text


# ═════════════════════════════════════════════════════════════════════════════
#  SHARED DRAWING HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def solid_box(ax, x, y, w, h, text, fc,
              fontsize=9.0, bold=False, lw=1.2):
    """Rounded solid box with centred text."""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.14",
        facecolor=fc, edgecolor=BDR, linewidth=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, text,
            ha="center", va="center",
            fontsize=fontsize,
            fontweight="bold" if bold else "normal",
            multialignment="center",
            zorder=4, color=TXT)


def dashed_region(ax, x, y, w, h, label="", fontsize=10.5):
    """Dashed boundary box with italic bold label at bottom-left."""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.18",
        facecolor="none", edgecolor=DASH_C,
        linestyle="--", linewidth=1.6, zorder=1))
    if label:
        ax.text(x + 0.22, y + 0.24, label,
                fontsize=fontsize,
                fontstyle="italic", fontweight="bold",
                color=DASH_C, zorder=2)


def arrow(ax, x0, y0, x1, y1,
          color=BDR, lw=1.15, mutation_scale=12):
    """Single arrowhead from (x0,y0) → (x1,y1)."""
    ax.annotate("",
                xy=(x1, y1), xytext=(x0, y0),
                zorder=6,
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=color, lw=lw,
                    mutation_scale=mutation_scale))


def line(ax, points, color=BDR, lw=1.15):
    """Polyline through list of (x, y) tuples."""
    ax.plot([p[0] for p in points],
            [p[1] for p in points],
            color=color, lw=lw, zorder=5)


def label(ax, x, y, text,
          fontsize=8.5, ha="center", va="center",
          italic=True, bold=False, color="#333333"):
    """Floating text label."""
    ax.text(x, y, text,
            ha=ha, va=va,
            fontsize=fontsize,
            fontstyle="italic" if italic else "normal",
            fontweight="bold" if bold else "normal",
            color=color, zorder=7)


# ═════════════════════════════════════════════════════════════════════════════
#  FIGURE 1  —  Framework
#
#  Layout (coordinate space  0–20  wide,  0–13  tall):
#
#   y 8.5 – 12.5   IMAGE OWNER   (left)     DATA-HIDER  (right)
#   y 0.5 –  7.5   RECEIVER      (full width)
#
# ═════════════════════════════════════════════════════════════════════════════

def draw_framework():
    fig, ax = plt.subplots(figsize=(20, 13))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13)
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)
    ax.axis("off")

    # ── dashed regions ────────────────────────────────────────
    dashed_region(ax,  0.30,  6.80, 13.00, 5.80, "Image Owner",   fontsize=10.5)
    dashed_region(ax, 13.50,  6.80,  6.10, 5.80, "Data-Hider",    fontsize=10.5)
    dashed_region(ax,  0.30,  0.40, 19.30, 6.00, "Receiver",      fontsize=10.5)

    # ══ IMAGE OWNER ══════════════════════════════════════════

    # --- left cluster: 3 stacked salmon boxes ---
    BW, BH = 3.20, 1.00          # box width / height
    CX = 0.70                    # cluster left edge
    BOX_Y = [10.90, 9.65, 8.40]  # top, mid, bottom

    solid_box(ax, CX, BOX_Y[0], BW, BH,
              "LOCO-I Prediction\n(Compute Residuals)", SALMON)
    solid_box(ax, CX, BOX_Y[1], BW, BH,
              "Count Zero-Planes $z_k$\n(per 4×4 block)", SALMON)
    solid_box(ax, CX, BOX_Y[2], BW, BH,
              "Block Compression\n(Plane / Residual mode)", SALMON)

    # dashed border around cluster
    ax.add_patch(FancyBboxPatch(
        (CX - 0.18, BOX_Y[2] - 0.22), BW + 0.36, 3.64,
        boxstyle="round,pad=0.10",
        facecolor="none", edgecolor=SALMON,
        linestyle="--", linewidth=1.4, zorder=2))
    label(ax, CX + BW / 2, 12.06,
          "Bit-plane Compression",
          fontsize=9.0, color="#A03800")

    # --- encryption box (centre) ---
    EX, EY, EW, EH = 5.20, 9.20, 2.80, 1.60
    solid_box(ax, EX, EY, EW, EH,
              "Encryption\n(XOR Keystream\n$\\mathcal{K}_e$)", YELLOW)

    # Ke arrow & label
    label(ax, EX + EW / 2, EY - 0.42, "$\\mathcal{K}_e$",
          fontsize=13, color="#666666")
    arrow(ax, EX + EW / 2, EY - 0.22, EX + EW / 2, EY)

    # --- aux-embed cluster (right of encryption) ---
    AX, AW, AH = 9.00, 3.50, 1.05
    solid_box(ax, AX, 10.80, AW, AH,
              "Auxiliary Information\nEmbedding (LSBs)", GREEN)
    solid_box(ax, AX, 9.40, AW, AH,
              "Bitstream:  3-bit $z_k$\n+ compressed bits", GREEN)

    # dashed border around aux cluster
    ax.add_patch(FancyBboxPatch(
        (AX - 0.18, 9.22), AW + 0.36, 2.78,
        boxstyle="round,pad=0.10",
        facecolor="none", edgecolor=GREEN,
        linestyle="--", linewidth=1.4, zorder=2))

    # --- Original image label + arrow ---
    label(ax, 0.12, 11.45, "Original\nimage $\\mathcal{I}$",
          fontsize=9.5, ha="left", color=TXT)
    arrow(ax, 0.52, 11.40, CX, 11.40)

    # cluster → encryption
    arrow(ax, CX + BW, 9.90, EX, 9.90)
    label(ax, (CX + BW + EX) / 2, 10.12,
          "$N_{czb},\\ z_k$", fontsize=8.5)

    # cluster → aux bitstream (path goes over the top)
    line(ax, [(CX + BW, 11.40), (8.60, 11.40), (8.60, 11.32)])
    arrow(ax, 8.60, 11.32, AX, 11.32)
    label(ax, (CX + BW + AX) / 2 + 0.4, 11.58,
          "aux bitstream", fontsize=8.5)

    # encryption → aux embed (horizontal)
    arrow(ax, EX + EW, 9.90, AX, 9.90)

    # If exits owner
    arrow(ax, AX + AW, 10.38, 13.50, 10.38)
    label(ax, 13.28, 10.60, "$\\mathcal{I}_f$", fontsize=11)

    # ══ DATA-HIDER ═══════════════════════════════════════════

    DX = 13.70   # data-hider left edge

    solid_box(ax, DX, 11.10, 5.50, 1.05,
              "Auxiliary Information Extraction", GREEN)
    solid_box(ax, DX,  8.80, 5.50, 1.05,
              "Data Hiding  (LSB Embedding)", GREEN)

    # hat{N}: aux extract → data hiding
    arrow(ax, DX + 5.50 / 2, 11.10, DX + 5.50 / 2, 9.85)
    label(ax, DX + 5.50 / 2 + 0.28, 10.47,
          "$\\hat{N}$", fontsize=11)

    # secret data + Kd
    label(ax, DX + 5.50 / 2, 8.52,
          "Secret data $+\\ \\mathcal{K}_d$", fontsize=8.5, color="#444")
    arrow(ax, DX + 5.50 / 2, 8.72, DX + 5.50 / 2, 8.80)

    # Im exits right → down into receiver
    line(ax, [(DX + 5.50, 9.32), (19.52, 9.32), (19.52, 3.60)])
    arrow(ax, 19.52, 3.60, 19.30, 3.60)
    label(ax, 19.72, 9.32, "$\\mathcal{I}_m$",
          fontsize=11, ha="left", color=TXT)

    # ══ RECEIVER ═════════════════════════════════════════════
    #
    #   Right col  : Aux Info Extraction  |  Block Arrangement
    #   Middle col : Image Recovery       |  Reconstruct Residuals
    #   Left col   : Data Extraction      |  Recovered Image
    #
    # Row tops:  upper=4.80   lower=2.90

    RBW = 4.40   # receiver box width
    RBH = 1.10   # receiver box height
    RY1 = 4.60   # upper row y
    RY2 = 2.90   # lower row y

    # right col  (x ≈ 14.5)
    RCX = 14.40
    solid_box(ax, RCX, RY1, RBW, RBH,
              "Auxiliary Information\nExtraction", GREEN)
    solid_box(ax, RCX, RY2, RBW, RBH,
              "Block Arrangement &\nBit-plane Swapping", BLUE)

    # middle col  (x ≈ 9.2)
    MCX = 9.00
    solid_box(ax, MCX, RY1, RBW, RBH,
              "Image Recovery\n(Invert LOCO-I)", BLUE)
    solid_box(ax, MCX, RY2, RBW, RBH,
              "Reconstruct Residuals\nfrom $z_k$, compressed bits", BLUE)

    # left col  (x ≈ 1.0)
    LCX = 1.00
    solid_box(ax, LCX, RY1, RBW, RBH,
              "Data Extraction\n(Payload bits)", BLUE)
    solid_box(ax, LCX, RY2, RBW, RBH,
              "Recovered Image $\\mathcal{I}$\n(PSNR = ∞,   SSIM = 1)",
              SALMON, bold=True, fontsize=9.0)

    # Im → aux extract (enter from right)
    arrow(ax, 19.30, 3.60, 19.30, 5.15)
    line(ax, [(19.30, 5.15), (18.80, 5.15)])
    arrow(ax, 18.80, 5.15, RCX + RBW, 5.15)
    label(ax, 19.55, 4.35, "$\\mathcal{I}_m$", fontsize=10)

    # aux extract → block arrangement (down)
    arrow(ax, RCX + RBW / 2, RY1, RCX + RBW / 2, RY2 + RBH)
    label(ax, RCX + RBW / 2 + 0.35, (RY1 + RY2 + RBH) / 2,
          "$LR_e$", fontsize=10)

    # aux extract → image recovery (hat N, horizontal path at top)
    line(ax, [(RCX, RY1 + RBH / 2 + 0.15),
              (MCX + RBW, RY1 + RBH / 2 + 0.15)])
    arrow(ax, MCX + RBW, RY1 + RBH / 2 + 0.15,
               MCX + RBW, RY1 + RBH / 2)
    label(ax, (RCX + MCX + RBW) / 2,
          RY1 + RBH / 2 + 0.38,
          "$\\hat{N}$", fontsize=11)

    # block arrangement → reconstruct residuals (left)
    arrow(ax, RCX, RY2 + RBH / 2, MCX + RBW, RY2 + RBH / 2)
    label(ax, (RCX + MCX + RBW) / 2, RY2 + RBH / 2 + 0.22,
          "$z_k$, compressed bits", fontsize=8.5)

    # reconstruct residuals → image recovery (up)
    arrow(ax, MCX + RBW / 2, RY2 + RBH, MCX + RBW / 2, RY1)
    label(ax, MCX + RBW / 2 + 0.36, (RY1 + RY2 + RBH) / 2,
          "residuals", fontsize=8.5)

    # image recovery → data extraction (hat N, long leftward path)
    line(ax, [(MCX, RY1 + RBH / 2),
              (LCX + RBW, RY1 + RBH / 2)])
    arrow(ax, LCX + RBW, RY1 + RBH / 2,
               LCX + RBW, RY1 + RBH / 2)
    ax.annotate("",
                xy=(LCX + RBW, RY1 + RBH / 2),
                xytext=(MCX, RY1 + RBH / 2),
                zorder=6,
                arrowprops=dict(
                    arrowstyle="-|>", color=BDR,
                    lw=1.15, mutation_scale=12))
    label(ax, (MCX + LCX + RBW) / 2, RY1 + RBH / 2 + 0.25,
          "$\\hat{N}$", fontsize=11)

    # image recovery → recovered image (down then left)
    line(ax, [(MCX + RBW / 2, RY1),
              (MCX + RBW / 2, RY2 + RBH + 0.18),
              (LCX + RBW, RY2 + RBH + 0.18)])
    ax.annotate("",
                xy=(LCX + RBW, RY2 + RBH + 0.18),
                xytext=(MCX + RBW / 2, RY2 + RBH + 0.18),
                zorder=6,
                arrowprops=dict(
                    arrowstyle="-|>", color=BDR,
                    lw=1.15, mutation_scale=12))
    label(ax, (MCX + LCX + RBW) / 2, RY2 + RBH + 0.42,
          "reconstructed $\\mathcal{I}$", fontsize=8.5)

    # data extraction → recovered image (down)
    arrow(ax, LCX + RBW / 2, RY1, LCX + RBW / 2, RY2 + RBH)

    # secret data (enters from left)
    label(ax, 0.22, RY1 + RBH / 2, "Secret\ndata",
          fontsize=9.5, ha="left", color=TXT)
    arrow(ax, 0.80, RY1 + RBH / 2, LCX, RY1 + RBH / 2)

    # key labels
    label(ax, MCX + RBW / 2, RY1 - 0.38, "$\\mathcal{K}_e$",
          fontsize=13, color="#666666")
    label(ax, LCX + RBW / 2, RY2 - 0.38, "$\\mathcal{K}_d$",
          fontsize=13, color="#666666")

    # ── figure caption ────────────────────────────────────────
    label(ax, 10.0, 0.18,
          "Fig. 1.   Framework of the proposed RDHEI method.",
          fontsize=11, color=TXT)

    # ── save ─────────────────────────────────────────────────
    fig.tight_layout(pad=0.2)
    for ext, dpi in [("png", 220), ("pdf", 300)]:
        fig.savefig(os.path.join(OUT, f"fig1_framework.{ext}"),
                    dpi=dpi, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓  fig1_framework.png / .pdf  saved")


# ═════════════════════════════════════════════════════════════════════════════
#  FIGURE 2  —  Auxiliary Bitstream Structure LA
#
#  Top row    :  base-paper LR  (for comparison / reference)
#  Bottom row :  our LA         (simplified)
#  Dashed connecting lines show the correspondence.
#
# ═════════════════════════════════════════════════════════════════════════════

def draw_bitstream():
    fig, ax = plt.subplots(figsize=(18, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)
    ax.axis("off")

    def seg_row(y, row_h, segments, colors, fontsize=9.0):
        """
        Draw a segmented horizontal bar.
        segments = [(label, relative_weight), ...]
        Returns list of (x_left, x_right) for each segment.
        """
        total = sum(s[1] for s in segments)
        x = 0.0
        coords = []
        for (lbl, w), col in zip(segments, colors):
            rw = w / total
            ax.add_patch(FancyBboxPatch(
                (x, y), rw, row_h,
                boxstyle="square,pad=0",
                facecolor=col, edgecolor=BDR,
                linewidth=0.9, zorder=3))
            ax.text(x + rw / 2, y + row_h / 2, lbl,
                    ha="center", va="center",
                    fontsize=fontsize, zorder=4,
                    multialignment="center", color=TXT)
            coords.append((x, x + rw))
            x += rw
        return coords

    def measure_brace(x0, x1, y, text, fontsize=8.0, above=True):
        """Double-headed arrow with centred label."""
        ax.annotate("",
                    xy=(x0, y), xytext=(x1, y),
                    arrowprops=dict(
                        arrowstyle="<->", color="#555555", lw=0.9))
        dy = 0.030 if above else -0.030
        va = "bottom" if above else "top"
        ax.text((x0 + x1) / 2, y + dy, text,
                ha="center", va=va,
                fontsize=fontsize, color="#444444",
                fontstyle="italic")

    # ── top row: base-paper LR ────────────────────────────────
    TOP_Y  = 0.66
    TOP_H  = 0.16

    top = seg_row(TOP_Y, TOP_H,
        [("$H$",             2.0),
         ("$N'_{czb}$",      2.0),
         ("$Map$",           3.5),
         ("$Inf$",           3.5),
         ("Sign map $L_{sign}$", 8.0),
         ("$\\mathcal{I}(1,1)$", 1.5)],
        [GREEN, GREEN, YELLOW, YELLOW, SALMON, SALMON],
        fontsize=9.5)

    # row title
    ax.text(0.50, 0.91,
            "$LR$   (base paper — shown for comparison)",
            ha="center", fontsize=9.5,
            fontstyle="italic", color="#888888")

    # measurement braces above
    measure_brace(top[0][0], top[1][1], 0.88,
                  "32 bits", fontsize=8.5)
    measure_brace(top[4][0], top[4][1], 0.88,
                  "$(mn-1)$ bits", fontsize=8.5)
    measure_brace(top[5][0], top[5][1], 0.88,
                  "8 bits", fontsize=8.5)

    # encryption arrow
    mid_x = (top[2][0] + top[3][1]) / 2
    ax.annotate("Encrypted by $\\mathcal{K}_e$",
                xy=(mid_x, TOP_Y),
                xytext=(mid_x, TOP_Y - 0.14),
                fontsize=9.0, ha="center",
                arrowprops=dict(
                    arrowstyle="-|>", color="#555555", lw=1.0),
                color="#333333")
    ax.text(mid_x - 0.018, TOP_Y - 0.07,
            "$LR$", fontsize=10, ha="center",
            fontstyle="italic", color="#333333")

    # ── bottom row: our LA ────────────────────────────────────
    LA_Y = 0.28
    LA_H = 0.18

    la = seg_row(LA_Y, LA_H,
        [("3-bit $z_k$ header\n(per block)",                      4.0),
         ("Compressed data\n(plane bits / residual bits)",         10.0),
         ("Length $\\ell_b(LR_e)$\n$\\lceil\\log_2(8mn)\\rceil$ bits", 3.0),
         ("Encrypted bitstream $LR_e$",                           10.0)],
        [YELLOW, SALMON, GREEN, GREEN],
        fontsize=9.5)

    # LA: label to the left
    ax.text(-0.012, LA_Y + LA_H / 2,
            "$LA:$",
            fontsize=15, ha="right", va="center",
            fontweight="bold", color=TXT)

    # measurement braces below
    measure_brace(la[0][0], la[0][1],
                  LA_Y - 0.06,
                  "$3 \\cdot \\lceil m/t \\rceil \\lceil n/t \\rceil$ bits",
                  fontsize=8.5, above=False)

    measure_brace(la[0][0], la[1][1],
                  LA_Y - 0.13,
                  "Our auxiliary bitstream  (replaces complex headers)",
                  fontsize=8.5, above=False)

    # ── dashed correspondence lines ───────────────────────────
    correspondence = [
        (top[0][0],  la[0][0]),   # left edge aligns
        (top[1][1],  la[1][1]),   # after N'czb aligns with after compressed data
        (top[2][0],  la[3][0]),   # Map start → LRe start
        (top[3][1],  la[3][1]),   # Inf end   → LRe end
    ]
    for tx, bx in correspondence:
        ax.plot([tx, bx], [TOP_Y, LA_Y + LA_H],
                color="#bbbbbb", lw=0.8,
                linestyle="--", zorder=1)

    # ── contribution callout box ──────────────────────────────
    ax.text(0.50, 0.09,
            "Our contribution:  eliminates  $Map$,  $Inf$,  $N'_{czb}$,  "
            "sign map,  and Huffman encoding\n"
            "→  replaced by a single  3-bit $z_k$  per block",
            ha="center", va="center",
            fontsize=9.5, color="#1a3a7a",
            multialignment="center",
            bbox=dict(boxstyle="round,pad=0.45",
                      facecolor="#dce8ff",
                      edgecolor="#5577bb",
                      linewidth=1.0))

    # ── figure caption ────────────────────────────────────────
    ax.text(0.50, 0.01,
            "Fig. 2.   Auxiliary bitstream structure $LA$.",
            ha="center", fontsize=10.5,
            fontstyle="italic", color=TXT)

    # ── save ─────────────────────────────────────────────────
    fig.tight_layout(pad=0.3)
    for ext, dpi in [("png", 220), ("pdf", 300)]:
        fig.savefig(os.path.join(OUT, f"fig2_bitstream.{ext}"),
                    dpi=dpi, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓  fig2_bitstream.png / .pdf  saved")


# ═════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    draw_framework()
    draw_bitstream()
    print("\nAll figures generated successfully.")