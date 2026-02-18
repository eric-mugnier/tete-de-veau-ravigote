#!/usr/bin/env python3
"""
Couverture style Actes Noirs (Actes Sud)
Tête de Veau Ravigote — Éric Mugnier
Format : 304 × 211 mm (140 + 18 + 140 + 3+3 / 205 + 3+3)
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import mm
import math, textwrap

# ─── Dimensions ───────────────────────────────────────────────────────────────
DPI = 300
MM  = DPI / 25.4

def px(v_mm):
    return int(v_mm * MM)

W = px(304)
H = px(211)

BACK_X1  = px(3)
BACK_X2  = px(143)
SPINE_X1 = px(143)
SPINE_X2 = px(161)
FRONT_X1 = px(161)
FRONT_X2 = px(301)

# ─── Couleurs ─────────────────────────────────────────────────────────────────
BLACK    = (8, 8, 8)
WHITE    = (255, 255, 255)
RED      = (212, 32, 32)       # rouge Actes Noirs
GREY_OVL = (218, 213, 203)     # fond crème/gris chaud du médaillon

# ─── Polices ──────────────────────────────────────────────────────────────────
DIDOT = '/System/Library/Fonts/Supplemental/Didot.ttc'
HN    = '/System/Library/Fonts/HelveticaNeue.ttc'

def f_didot(size_mm, bold=False):
    return ImageFont.truetype(DIDOT, px(size_mm), index=2 if bold else 0)

def f_hn(size_mm, bold=False):
    return ImageFont.truetype(HN, px(size_mm), index=1 if bold else 0)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def center_x_text(draw, text, font, x1, x2):
    bb = draw.textbbox((0, 0), text, font=font)
    return x1 + (x2 - x1 - (bb[2] - bb[0])) // 2

def text_height(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def draw_wrapped_centered(draw, text, font, fill, x1, x2, y, line_gap_mm=1.5):
    words = text.split()
    lines, cur = [], []
    max_w = x2 - x1 - px(4)
    for w in words:
        test = ' '.join(cur + [w])
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] > max_w and cur:
            lines.append(' '.join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(' '.join(cur))
    lh = font.size + px(line_gap_mm)
    for line in lines:
        tx = center_x_text(draw, line, font, x1, x2)
        draw.text((tx, y), line, fill=fill, font=font)
        y += lh
    return y

def paste_vertical_text(img, text, font, fill, center_x, center_y):
    draw_tmp = ImageDraw.Draw(img)
    bb = draw_tmp.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = px(1)
    tmp = Image.new('RGBA', (tw + 2*pad, th + 2*pad), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((pad, pad), text, fill=fill, font=font)
    rot = tmp.rotate(90, expand=True)
    img.paste(rot, (center_x - rot.width//2, center_y - rot.height//2), rot)

def oval_medallion(photo_path, oval_w_mm, oval_h_mm, bg_color):
    ow, oh = px(oval_w_mm), px(oval_h_mm)
    result = Image.new('RGBA', (ow, oh), (0, 0, 0, 0))
    bg = Image.new('RGBA', (ow, oh), (0, 0, 0, 0))
    ImageDraw.Draw(bg).ellipse([0, 0, ow - 1, oh - 1], fill=bg_color + (255,))
    result.paste(bg, (0, 0), bg)
    photo = Image.open(photo_path).convert('RGB')
    pw, ph = photo.size
    scale = max(ow / pw, oh / ph)
    new_w, new_h = int(pw * scale), int(ph * scale)
    photo_r = photo.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - ow) // 2
    top  = (new_h - oh) // 2
    photo_c = photo_r.crop((left, top, left + ow, top + oh))
    mask = Image.new('L', (ow, oh), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, ow - 1, oh - 1], fill=255)
    result.paste(photo_c.convert('RGBA'), (0, 0), mask)
    return result

# ══════════════════════════════════════════════════════════════════════════════
# CANVAS
# ══════════════════════════════════════════════════════════════════════════════
img  = Image.new('RGB', (W, H), BLACK)
draw = ImageDraw.Draw(img)

BORDER = px(4)
PHOTO  = '/Users/christophe.thiebaud/_Mugnier/images/tranche_tete_de_veau.jpg'

# ══════════════════════════════════════════════════════════════════════════════
# 1ÈRE DE COUVERTURE
# ══════════════════════════════════════════════════════════════════════════════
FX1, FX2 = FRONT_X1, FRONT_X2

draw.rectangle([FX1, 0, FX2 - 1, H - 1], outline=RED, width=BORDER)

inner_x1 = FX1 + BORDER
inner_x2 = FX2 - BORDER
inner_y1 = BORDER

# Auteur (rouge, bold sans-serif)
f_auth = f_hn(7.5, bold=True)
auth_text = 'ÉRIC MUGNIER'
ax = center_x_text(draw, auth_text, f_auth, inner_x1, inner_x2)
ay = inner_y1 + px(5)
draw.text((ax, ay), auth_text, fill=RED, font=f_auth)
auth_bottom = ay + text_height(draw, auth_text, f_auth)

# Titre (blanc, Didot, auto-fit)
title_lines = ['TÊTE DE VEAU', 'RAVIGOTE']
avail_w = inner_x2 - inner_x1
title_size = 22.0
while title_size > 8:
    ft = f_didot(title_size)
    max_w = max(draw.textbbox((0, 0), l, font=ft)[2] for l in title_lines)
    if max_w <= avail_w:
        break
    title_size -= 0.5

ft = f_didot(title_size)
ty = auth_bottom + px(8)
for line in title_lines:
    tx = center_x_text(draw, line, ft, inner_x1, inner_x2)
    draw.text((tx, ty), line, fill=WHITE, font=ft)
    ty += text_height(draw, line, ft) + px(2)

# Médaillon ovale
OV_W, OV_H = 63.0, 80.0
medallion = oval_medallion(PHOTO, OV_W, OV_H, GREY_OVL)
ov_cx = (FX1 + FX2) // 2
ov_cy = int(0.64 * H)
ov_paste_x = ov_cx - medallion.width  // 2
ov_paste_y = ov_cy - medallion.height // 2
img_rgba = img.convert('RGBA')
img_rgba.paste(medallion, (ov_paste_x, ov_paste_y), medallion)
img = img_rgba.convert('RGB')
draw = ImageDraw.Draw(img)

# ══════════════════════════════════════════════════════════════════════════════
# DOS
# ══════════════════════════════════════════════════════════════════════════════
draw.line([(SPINE_X1, 0), (SPINE_X1, H)], fill=RED, width=BORDER)
draw.line([(SPINE_X2, 0), (SPINE_X2, H)], fill=RED, width=BORDER)
spine_cx = (SPINE_X1 + SPINE_X2) // 2
paste_vertical_text(img, 'ÉRIC MUGNIER  •  TÊTE DE VEAU RAVIGOTE',
                    f_hn(4.5), WHITE, spine_cx, H // 2)

# ══════════════════════════════════════════════════════════════════════════════
# 4ÈME DE COUVERTURE
# ══════════════════════════════════════════════════════════════════════════════
draw = ImageDraw.Draw(img)
draw.rectangle([BACK_X1, 0, BACK_X2 - 1, H - 1], outline=RED, width=BORDER)

bx1 = BACK_X1 + BORDER + px(4)
bx2 = BACK_X2 - BORDER - px(4)

f_txt = f_hn(4.2)
f_bio = f_hn(3.8)

by = BORDER + px(8)
by = draw_wrapped_centered(draw,
    "Quand le père Vidal disparaît dans des circonstances troubles "
    "et que le Brain Catcher sème la terreur, le commandant Beauvais "
    "se lance dans une enquête labyrinthique qui le mènera des caves "
    "de l'Église aux secrets les plus enfouis de la République. "
    "Entouré de Titus Beaugendre, son fidèle équipier, et d'une "
    "galerie de personnages hauts en couleur, Beauvais arpente une "
    "France contemporaine où l'absurde dispute à l'horreur.",
    f_txt, WHITE, bx1, bx2, by, 1.6)
by += px(5)
by = draw_wrapped_centered(draw,
    "Roman-fleuve d'une ambition rare, Tête de veau ravigote mêle polar "
    "halluciné, satire sociale et méditation sur la violence. Éric Mugnier "
    "y déploie une prose incandescente, truculente et érudite, qui rappelle "
    "les grandes heures du roman noir français.",
    f_txt, WHITE, bx1, bx2, by, 1.6)

sep_y = H - BORDER - px(20)
draw.line([(bx1, sep_y), (bx2, sep_y)], fill=(90, 90, 90), width=px(0.2))
draw_wrapped_centered(draw,
    "Éric Mugnier vit en France. "
    "Tête de veau ravigote est son premier roman.",
    f_bio, (180, 180, 180), bx1, bx2, sep_y + px(4), 1.4)

# ══════════════════════════════════════════════════════════════════════════════
# EXPORT PDF
# ══════════════════════════════════════════════════════════════════════════════
tmp_png  = '/tmp/actes_noirs_couv.png'
pdf_path = '/Users/christophe.thiebaud/_Mugnier/tete_de_veau_ravigote_couverture_actes_noirs.pdf'
img.save(tmp_png, dpi=(DPI, DPI))
c = rl_canvas.Canvas(pdf_path, pagesize=(304 * mm, 211 * mm))
c.drawImage(tmp_png, 0, 0, width=304 * mm, height=211 * mm)
c.save()
print(f"✓ PDF généré : {pdf_path}")
print(f"  Image : {img.width}×{img.height} px  ({img.width/MM:.1f}×{img.height/MM:.1f} mm)")
