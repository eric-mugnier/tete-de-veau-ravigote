#!/usr/bin/env python3
"""
Couverture polar graphique - style Rivages/Noir
Tête de Veau Ravigote - Éric Mugnier
Format : 304 × 211 mm (4e couv 140 + dos 18 + 1ère couv 140 + fonds perdus 3+3)
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import mm
import io, os, textwrap

# ─── Constantes ───────────────────────────────────────────────────────────────
DPI = 300
MM = DPI / 25.4   # pixels par millimètre

def px(v_mm):
    """Convertit des millimètres en pixels (entier)."""
    return int(v_mm * MM)

# Dimensions totales
W = px(304)
H = px(211)

# Zones x (en pixels, origine haut-gauche)
BACK_X1  = px(3)
BACK_X2  = px(143)
SPINE_X1 = px(143)
SPINE_X2 = px(161)
FRONT_X1 = px(161)
FRONT_X2 = px(301)

# ─── Couleurs ─────────────────────────────────────────────────────────────────
BLACK     = (12, 12, 12)
WHITE     = (255, 255, 255)
BLOOD_RED = (160, 20, 20)    # rouge sang pour duotone haut
NEAR_BLK  = (18, 10, 8)     # presque noir pour duotone bas
GREY_LIGHT= (210, 210, 210)  # texte secondaire 4e de couverture
RED_SPINE = (180, 25, 25)    # filet rouge sur le dos

# ─── Polices ──────────────────────────────────────────────────────────────────
HN = '/System/Library/Fonts/HelveticaNeue.ttc'
FONT_REG   = (HN, 0)   # Regular
FONT_BOLD  = (HN, 1)   # Bold
FONT_COND  = (HN, 9)   # Condensed Black

def font(spec, size_mm):
    path, idx = spec
    return ImageFont.truetype(path, px(size_mm), index=idx)

# ─── Helper : dessin texte multiligne avec retour automatique ─────────────────
def draw_wrapped(draw, text, x, y, max_w_px, font_obj, fill, line_spacing_mm=1.5):
    """Dessine du texte avec retour à la ligne automatique (gauche aligné)."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = ' '.join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font_obj)
        if bbox[2] - bbox[0] > max_w_px and current:
            lines.append(' '.join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))

    lh = font_obj.size + px(line_spacing_mm)
    for line in lines:
        draw.text((x, y), line, fill=fill, font=font_obj)
        y += lh
    return y  # retourne la position y finale

# ─── Helper : texte vertical centré sur le dos ───────────────────────────────
def paste_vertical_text(img, text, font_obj, fill, center_x, center_y):
    """Crée un label vertical (bas → haut) et le colle sur img."""
    draw_tmp = ImageDraw.Draw(img)
    bbox = draw_tmp.textbbox((0, 0), text, font=font_obj)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = px(1)
    tmp = Image.new('RGBA', (tw + 2*pad, th + 2*pad), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((pad, pad), text, fill=fill, font=font_obj)
    rot = tmp.rotate(90, expand=True)
    x = center_x - rot.width  // 2
    y = center_y - rot.height // 2
    img.paste(rot, (x, y), rot)

# ══════════════════════════════════════════════════════════════════════════════
# 1. CANVAS DE BASE
# ══════════════════════════════════════════════════════════════════════════════
img = Image.new('RGB', (W, H), BLACK)
draw = ImageDraw.Draw(img)

# ══════════════════════════════════════════════════════════════════════════════
# 2. 1ÈRE DE COUVERTURE — photo + effets
# ══════════════════════════════════════════════════════════════════════════════
front_w = FRONT_X2 - FRONT_X1
front_h = H

photo = Image.open(
    '/Users/christophe.thiebaud/_Mugnier/tranche_tete_de_veau.jpg'
).convert('RGB')

# Redimensionner pour couvrir la zone (cover-fill)
pw, ph = photo.size
scale = max(front_w / pw, front_h / ph)
new_w, new_h = int(pw * scale), int(ph * scale)
photo_scaled = photo.resize((new_w, new_h), Image.LANCZOS)

# Recadrage centré
left = (new_w - front_w) // 2
top  = (new_h - front_h) // 2
photo_crop = photo_scaled.crop((left, top, left + front_w, top + front_h))

img.paste(photo_crop, (FRONT_X1, 0))

# Dégradé noir sur la moitié supérieure (pour que le texte blanc soit lisible)
overlay = Image.new('RGBA', (front_w, H), (0, 0, 0, 0))
ov_draw = ImageDraw.Draw(overlay)
gradient_h = px(120)  # 120 mm de dégradé en haut
for y in range(gradient_h):
    alpha = int(200 * (1 - y / gradient_h))
    ov_draw.line([(0, y), (front_w, y)], fill=(0, 0, 0, alpha))

img_rgba = img.convert('RGBA')
img_rgba.paste(overlay, (FRONT_X1, 0), overlay)
img = img_rgba.convert('RGB')
draw = ImageDraw.Draw(img)

# ══════════════════════════════════════════════════════════════════════════════
# 3. TEXTE SUR LA 1ÈRE DE COUVERTURE
# ══════════════════════════════════════════════════════════════════════════════

# ── Boîte auteur (blanc) ─────────────────────────────────────────────────────
BOX_MARGIN = px(6)     # depuis le bord gauche de la 1ère couv
BOX_TOP    = px(12)    # depuis le haut
BOX_PAD_X  = px(3)
BOX_PAD_Y  = px(2)

f_author_box = font(FONT_BOLD, 7.5)
author_text  = 'ÉRIC MUGNIER'
ab = draw.textbbox((0, 0), author_text, font=f_author_box)
box_w = ab[2] - ab[0] + 2 * BOX_PAD_X
box_h = ab[3] - ab[1] + 2 * BOX_PAD_Y

bx1 = FRONT_X1 + BOX_MARGIN
bx2 = bx1 + box_w
by1 = BOX_TOP
by2 = by1 + box_h
draw.rectangle([bx1, by1, bx2, by2], fill=WHITE)
draw.text((bx1 + BOX_PAD_X, by1 + BOX_PAD_Y), author_text, fill=BLACK, font=f_author_box)

# ── Titre principal (condensed black, blanc, très grand) ─────────────────────
title_x = FRONT_X1 + BOX_MARGIN
title_max_w = FRONT_X2 - FRONT_X1 - 2 * BOX_MARGIN  # largeur disponible

# Trouver la plus grande taille qui fait tenir chaque ligne
title_lines = ['TÊTE DE VEAU', 'RAVIGOTE']
title_size = 28.0
while title_size > 8:
    f_title = font(FONT_COND, title_size)
    max_w = max(
        draw.textbbox((0, 0), line, font=f_title)[2] for line in title_lines
    )
    if max_w <= title_max_w:
        break
    title_size -= 0.5

title_y = by2 + px(8)
for line in title_lines:
    draw.text((title_x, title_y), line, fill=WHITE, font=f_title)
    bb = draw.textbbox((title_x, title_y), line, font=f_title)
    title_y += (bb[3] - bb[1]) + px(2)

# ── Mention "roman" sous le titre ────────────────────────────────────────────
f_roman = font(FONT_REG, 6)
draw.text((title_x, title_y + px(6)), 'roman', fill=WHITE, font=f_roman)


# ══════════════════════════════════════════════════════════════════════════════
# 4. DOS
# ══════════════════════════════════════════════════════════════════════════════
# Fond déjà noir. Filets rouges sur les deux bords du dos.
draw.line([(SPINE_X1, 0), (SPINE_X1, H)], fill=RED_SPINE, width=px(0.4))
draw.line([(SPINE_X2, 0), (SPINE_X2, H)], fill=RED_SPINE, width=px(0.4))

spine_cx = (SPINE_X1 + SPINE_X2) // 2

# Auteur en haut du dos
paste_vertical_text(img, 'MUGNIER',
                    font(FONT_BOLD, 5), WHITE,
                    spine_cx, px(22))

# Titre vertical centré
paste_vertical_text(img, 'TÊTE DE VEAU RAVIGOTE',
                    font(FONT_BOLD, 5.5), WHITE,
                    spine_cx, H // 2)

# ══════════════════════════════════════════════════════════════════════════════
# 5. 4ÈME DE COUVERTURE
# ══════════════════════════════════════════════════════════════════════════════
# Fond noir (déjà en place). Texte blanc.
draw = ImageDraw.Draw(img)

BACK_PAD_X = px(10)
BACK_TEXT_W = BACK_X2 - BACK_X1 - 2 * BACK_PAD_X
TEXT_X = BACK_X1 + BACK_PAD_X

f_resume  = font(FONT_REG, 4.5)
f_bio     = font(FONT_REG, 4.0)
f_sep     = font(FONT_REG, 4.0)

resume = (
    "Quand le père Vidal disparaît dans des circonstances troubles "
    "et que le Brain Catcher sème la terreur, le commandant Beauvais "
    "se lance dans une enquête labyrinthique qui le mènera des caves "
    "de l'Église aux secrets les plus enfouis de la République. "
    "Entouré de Titus Beaugendre, son fidèle équipier, et d'une "
    "galerie de personnages hauts en couleur, Beauvais arpente une "
    "France contemporaine où l'absurde dispute à l'horreur."
)
bio = (
    "Éric Mugnier vit en France. "
    "Tête de veau ravigote est son premier roman."
)

y = px(14)
y = draw_wrapped(draw, resume, TEXT_X, y, BACK_TEXT_W, f_resume, WHITE, line_spacing_mm=1.8)

y += px(5)
draw_wrapped(draw, (
    "Roman-fleuve d'une ambition rare, Tête de veau ravigote mêle polar "
    "halluciné, satire sociale et méditation sur la violence. Éric Mugnier "
    "y déploie une prose incandescente, truculente et érudite, qui rappelle "
    "les grandes heures du roman noir français."
), TEXT_X, y, BACK_TEXT_W, f_resume, WHITE, line_spacing_mm=1.8)

# Filet séparateur
sep_y = H - px(32)
draw.line([(TEXT_X, sep_y), (BACK_X2 - BACK_PAD_X, sep_y)],
          fill=(100, 100, 100), width=px(0.25))

# Bio auteur
draw_wrapped(draw, bio, TEXT_X, sep_y + px(4), BACK_TEXT_W, f_bio, GREY_LIGHT,
             line_spacing_mm=1.5)

# ══════════════════════════════════════════════════════════════════════════════
# 6. GÉNÉRATION DU PDF via reportlab
# ══════════════════════════════════════════════════════════════════════════════
tmp_png = '/tmp/polar_couv.png'
img.save(tmp_png, dpi=(DPI, DPI))

pdf_path = '/Users/christophe.thiebaud/_Mugnier/tete_de_veau_ravigote_couverture_polar.pdf'
c = rl_canvas.Canvas(pdf_path, pagesize=(304 * mm, 211 * mm))
c.drawImage(tmp_png, 0, 0, width=304 * mm, height=211 * mm)
c.save()

print(f"✓ PDF généré : {pdf_path}")
print(f"  Dimensions image : {img.width}×{img.height} px ({img.width/MM:.1f}×{img.height/MM:.1f} mm)")
