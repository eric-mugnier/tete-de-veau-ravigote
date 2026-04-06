#!/usr/bin/env python3
"""
lighten_bg.py  —  lighten image backgrounds via macOS Vision person-segmentation.

No heavy ML deps — uses the native Vision framework bundled with macOS.
Mask quality is improved with a guided filter (edge-aware refinement using
the original image's colour structure) and optional Gaussian softening.

Install once:
    pip install pyobjc-framework-Vision pyobjc-framework-Quartz
                pyobjc-framework-Cocoa pillow numpy scipy

Usage:
    python figures/lighten_bg.py            # LIGHTEN=0.55, REFINE=True (defaults)
    python figures/lighten_bg.py 0.4        # custom lightening factor 0–1
                                            # 0 = no change · 1 = pure white bg
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

# ── config ────────────────────────────────────────────────────────────────────
### IMG_DIR = Path(__file__).parent.parent / "iconography/acte_09/scene_16/actresses"
IMG_DIR = Path(__file__).parent.parent / "iconography/acte_09/scene_16/"

### IMAGES = [
###     "_1960_scarlett-johansson.jpg",
###     "_2020_leven-rambin.jpg",
###     "_2060_amanda-seyfried.jpg",
###     "_2070_sydney-sweeney.jpg",
### ]

IMAGES = [
    "_2110_hérodote.jpg",
    "_2120_scythes.jpg",
]

LIGHTEN      = float(sys.argv[1]) if len(sys.argv) > 1 else 0.4
GUIDED_R     = 50     # guided-filter radius (px) — larger = smoother boundary
GUIDED_EPS   = 0.1   # guided-filter regularisation — larger = less edge-snapping
EDGE_BLUR    = 2.0    # Gaussian blur (px) applied to mask after guided filter


# ── guided filter (pure numpy/scipy, no OpenCV needed) ───────────────────────
def _box2d(arr: np.ndarray, r: int) -> np.ndarray:
    """Fast mean filter over a (2r+1)×(2r+1) window — pure numpy, no scipy."""
    d = 2 * r + 1
    H, W = arr.shape

    # rows: prepend a zero row so c[i+d] - c[i] gives the box sum at row i
    padded = np.pad(arr, ((r, r), (0, 0)), mode="reflect")   # (H+2r, W)
    c = np.zeros((H + 2 * r + 1, W), dtype=np.float64)
    c[1:] = np.cumsum(padded, axis=0)
    out = c[d : d + H] - c[:H]                               # (H, W)

    # cols: same trick
    padded2 = np.pad(out, ((0, 0), (r, r)), mode="reflect")  # (H, W+2r)
    c2 = np.zeros((H, W + 2 * r + 1), dtype=np.float64)
    c2[:, 1:] = np.cumsum(padded2, axis=1)
    out2 = c2[:, d : d + W] - c2[:, :W]                      # (H, W)

    return out2 / (d * d)


def guided_filter(guide_rgb: np.ndarray, mask: np.ndarray,
                  radius: int = 20, eps: float = 0.01) -> np.ndarray:
    """
    Edge-aware refinement: snaps the mask boundary to colour edges in the
    original image, greatly reducing fringing and missed fine details.

    guide_rgb : float32 H×W×3, range [0,1]
    mask      : float32 H×W,   range [0,1]
    returns   : float32 H×W,   range [0,1]
    """
    box = lambda x: _box2d(x.astype(np.float64), radius)

    # luminance guide
    g = (0.299 * guide_rgb[:, :, 0]
       + 0.587 * guide_rgb[:, :, 1]
       + 0.114 * guide_rgb[:, :, 2]).astype(np.float64)
    p = mask.astype(np.float64)

    mean_g  = box(g)
    mean_p  = box(p)
    mean_gp = box(g * p)
    mean_gg = box(g * g)

    cov_gp = mean_gp - mean_g * mean_p
    var_g  = mean_gg - mean_g * mean_g

    a = cov_gp / (var_g + eps)
    b = mean_p - a * mean_g

    refined = box(a) * g + box(b)
    return np.clip(refined, 0.0, 1.0).astype(np.float32)


# ── mask via macOS Vision ─────────────────────────────────────────────────────
def person_mask(img_path: Path) -> np.ndarray:
    """Return float32 array (H×W), 1.0 = person, 0.0 = background."""
    import io
    try:
        from Foundation import NSURL
        from Vision import VNGeneratePersonSegmentationRequest, VNImageRequestHandler
        from Quartz import CIImage, CIContext
        from AppKit import NSBitmapImageRep
    except ImportError as exc:
        raise SystemExit(
            f"\n  Missing PyObjC framework: {exc}\n"
            "  Install with:\n"
            "      pip install pyobjc-framework-Vision pyobjc-framework-Quartz"
            " pyobjc-framework-Cocoa\n"
        )

    url = NSURL.fileURLWithPath_(str(img_path.resolve()))

    request = VNGeneratePersonSegmentationRequest.alloc().initWithCompletionHandler_(None)
    request.setQualityLevel_(2)          # 0=Fast 1=Balanced 2=Accurate

    handler = VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    ok, err = handler.performRequests_error_([request], None)
    if not ok:
        raise RuntimeError(f"Vision segmentation failed: {err}")

    pb = request.results()[0].pixelBuffer()

    # CVPixelBuffer → CIImage → CGImage → NSBitmapImageRep → PNG bytes → PIL
    ci  = CIImage.imageWithCVPixelBuffer_(pb)
    ctx = CIContext.contextWithOptions_(None)
    cg  = ctx.createCGImage_fromRect_(ci, ci.extent())
    rep = NSBitmapImageRep.alloc().initWithCGImage_(cg)
    png = rep.representationUsingType_properties_(4, None)  # NSBitmapImageFileTypePNG

    mask_img = Image.open(io.BytesIO(bytes(png))).convert("L")
    return np.array(mask_img).astype(np.float32) / 255.0


# ── processing ────────────────────────────────────────────────────────────────
def process(src: Path, factor: float) -> Path:
    print(f"  {src.name} …", end=" ", flush=True)

    orig  = Image.open(src).convert("RGB")
    W, H  = orig.size

    raw_mask = person_mask(src)

    # 1. resize Vision mask to match source image (Vision returns a smaller buffer)
    if raw_mask.shape != (H, W):
        m = Image.fromarray((raw_mask * 255).astype(np.uint8), mode="L")
        raw_mask = np.array(m.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255.0

    orig_arr = np.array(orig).astype(np.float32) / 255.0

    # 2. guided filter: snap mask edges to image colour boundaries
    mask = guided_filter(orig_arr, raw_mask, radius=GUIDED_R, eps=GUIDED_EPS)

    # 3. gentle Gaussian blur to soften any remaining hard transitions
    if EDGE_BLUR > 0:
        from PIL import ImageFilter
        m_img = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
        m_img = m_img.filter(ImageFilter.GaussianBlur(radius=EDGE_BLUR))
        mask  = np.array(m_img).astype(np.float32) / 255.0

    # 4. blend: background pixels → white, subject pixels → original
    white  = np.ones_like(orig_arr)
    bg     = (1.0 - mask[:, :, np.newaxis]) * factor
    result = orig_arr + bg * (white - orig_arr)
    result = np.clip(result * 255, 0, 255).astype(np.uint8)

    dst = src.parent / (src.stem + "_lb.jpg")
    Image.fromarray(result).save(dst, quality=95)
    print(f"→ {dst.name}")
    return dst


# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Lightening factor: {LIGHTEN:.0%}  ·  guided-filter r={GUIDED_R}"
          f"  ·  edge blur={EDGE_BLUR}px\n")
    for name in IMAGES:
        src = IMG_DIR / name
        if not src.exists():
            print(f"  ✗ not found: {src}")
            continue
        process(src, LIGHTEN)
    print("\nDone.")
