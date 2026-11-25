from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import math

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height

BG_DARK = RGBColor(0x0B, 0x1D, 0x0E)
BG_MID = RGBColor(0x11, 0x2B, 0x16)
GREEN_DARK = RGBColor(0x0D, 0x47, 0x15)
GREEN_ACCENT = RGBColor(0x1B, 0x8A, 0x2B)
GREEN_LIGHT = RGBColor(0x4C, 0xAF, 0x50)
GOLD = RGBColor(0xD4, 0xA0, 0x1E)
GOLD_LIGHT = RGBColor(0xF0, 0xC8, 0x4D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFF_WHITE = RGBColor(0xE8, 0xE8, 0xE0)
LIGHT_GRAY = RGBColor(0xB0, 0xB0, 0xB0)
SEMI_DARK = RGBColor(0x1A, 0x1A, 0x1A)

def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

NS_A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'

def _set_shape_alpha(shape, alpha_pct):
    from lxml import etree
    sp = shape._element
    spPr = sp.find(f'{NS_A}spPr')
    if spPr is None:
        return
    solidFill = spPr.find(f'{NS_A}solidFill')
    if solidFill is None:
        return
    srgb = solidFill.find(f'{NS_A}srgbClr')
    if srgb is not None:
        alpha_elem = etree.SubElement(srgb, f'{NS_A}alpha')
        alpha_elem.set('val', str(int(alpha_pct * 1000)))

def add_rect(slide, left, top, width, height, fill_color, alpha=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    if alpha is not None:
        _set_shape_alpha(shape, alpha)
    return shape

def add_circle(slide, left, top, size, fill_color, alpha=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    if alpha is not None:
        _set_shape_alpha(shape, alpha)
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, color=WHITE,
                 bold=False, italic=False, alignment=PP_ALIGN.LEFT, font_name="Calibri",
                 anchor=MSO_ANCHOR.TOP, line_spacing=None):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = font_name
    p.alignment = alignment
    tf.auto_size = None
    if line_spacing:
        p.line_spacing = Pt(line_spacing)
    return txBox

def add_text_multiline(slide, left, top, width, height, lines, font_size=18, color=WHITE,
                       bold=False, italic=False, alignment=PP_ALIGN.LEFT, font_name="Calibri",
                       line_spacing=None, bullet=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        if isinstance(line, dict):
            p.text = line.get("text", "")
            p.font.size = Pt(line.get("size", font_size))
            p.font.color.rgb = line.get("color", color)
            p.font.bold = line.get("bold", bold)
            p.font.italic = line.get("italic", italic)
            p.font.name = line.get("font", font_name)
            p.alignment = line.get("align", alignment)
            if line.get("spacing"):
                p.line_spacing = Pt(line["spacing"])
            else:
                if line_spacing:
                    p.line_spacing = Pt(line_spacing)
        else:
            p.text = line
            p.font.size = Pt(font_size)
            p.font.color.rgb = color
            p.font.bold = bold
            p.font.italic = italic
            p.font.name = font_name
            p.alignment = alignment
            if line_spacing:
                p.line_spacing = Pt(line_spacing)
    return txBox

def add_field_lines(slide):
    for i in range(18):
        y = int(Inches(0.4167) * i)
        add_rect(slide, 0, y, W, Inches(0.015), GREEN_DARK, alpha=25)
    lines_v = 12
    spacing = W // lines_v
    for i in range(lines_v + 1):
        x = int(spacing * i)
        add_rect(slide, x, 0, Inches(0.015), H, GREEN_DARK, alpha=25)

def add_penalty_spot(slide, x, y, size=Inches(0.08), color=WHITE, alpha=40):
    add_circle(slide, x - size // 2, y - size // 2, size, color, alpha)

def add_center_circle(slide, cx, cy, radius=Inches(1.5), color=GREEN_LIGHT, alpha=20):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        cx - radius, cy - radius, radius * 2, radius * 2)
    shape.fill.background()
    shape.line.color.rgb = color
    shape.line.width = Pt(1.5)
    from lxml import etree
    ln = shape.line._ln
    solidFill = ln.find(f'{NS_A}solidFill')
    if solidFill is not None:
        srgb = solidFill.find(f'{NS_A}srgbClr')
        if srgb is not None:
            alpha_elem = etree.SubElement(srgb, f'{NS_A}alpha')
            alpha_elem.set('val', str(int(alpha * 1000)))

def add_goal_shape(slide, left, top, width, height, color=WHITE, alpha=25):
    add_rect(slide, left, top, width, Inches(0.03), color, alpha)
    add_rect(slide, left, top, Inches(0.03), height, color, alpha)
    add_rect(slide, left + width - Inches(0.03), top, Inches(0.03), height, color, alpha)

def add_net_pattern(slide, left, top, width, height, color=WHITE, alpha=10):
    for i in range(0, int(width), Inches(0.2)):
        add_rect(slide, left + i, top, Inches(0.01), height, color, alpha)
    for i in range(0, int(height), Inches(0.15)):
        add_rect(slide, left, top + i, width, Inches(0.01), color, alpha)

def add_bottom_bar(slide, color=GOLD, height=Inches(0.06)):
    add_rect(slide, 0, H - height, W, height, color, alpha=70)

def add_top_accent(slide, color=GOLD, height=Inches(0.04)):
    add_rect(slide, 0, 0, W, height, color, alpha=70)

def add_slide_number(slide, num, total=19):
    add_text_box(slide, W - Inches(1.5), H - Inches(0.5), Inches(1.3), Inches(0.4),
                 f"{num} / {total}", font_size=10, color=LIGHT_GRAY,
                 alignment=PP_ALIGN.RIGHT, font_name="Calibri Light")

def add_decorative_corners(slide, color=GOLD, size=Inches(0.6), thickness=Pt(2), alpha=50):
    positions = [
        (Inches(0.3), Inches(0.3), 'top_left'),
        (W - Inches(0.3) - size, Inches(0.3), 'top_right'),
        (Inches(0.3), H - Inches(0.3) - size, 'bottom_left'),
        (W - Inches(0.3) - size, H - Inches(0.3) - size, 'bottom_right'),
    ]
    for x, y, pos in positions:
        h_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, size, Inches(0.025))
        h_line.fill.solid()
        h_line.fill.fore_color.rgb = color
        h_line.line.fill.background()
        v_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.025), size)
        v_line.fill.solid()
        v_line.fill.fore_color.rgb = color
        v_line.line.fill.background()

        _set_shape_alpha(h_line, alpha)
        _set_shape_alpha(v_line, alpha)

        if 'right' in pos:
            h_line.left = W - Inches(0.3) - size
            v_line.left = W - Inches(0.3) - Inches(0.025)
        if 'bottom' in pos:
            h_line.top = H - Inches(0.3) - Inches(0.025)
            v_line.top = H - Inches(0.3) - size


# ======== SLIDE 1: Title ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)
add_center_circle(slide, W // 2, H // 2, Inches(2.0), GREEN_LIGHT, 15)
add_penalty_spot(slide, W // 2, H // 2, Inches(0.15), GOLD, 60)

add_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(0.04), GOLD, 60)

add_text_box(slide, Inches(1.5), Inches(2.0), Inches(10.3), Inches(2.0),
             "CARLOS ROA", font_size=72, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER, font_name="Calibri Light")

add_rect(slide, Inches(4.5), Inches(3.9), Inches(4.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.5), Inches(4.1), Inches(10.3), Inches(1.2),
             "Le gardien qui a choisi la foi avant le ballon",
             font_size=26, color=GOLD_LIGHT, italic=True,
             alignment=PP_ALIGN.CENTER, font_name="Calibri Light")

add_rect(slide, Inches(1.5), Inches(5.5), Inches(10.3), Inches(0.04), GOLD, 60)

add_decorative_corners(slide, GOLD, Inches(0.5), alpha=40)
add_bottom_bar(slide)
add_slide_number(slide, 1)

# ======== SLIDE 2: Parcours overview ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)
add_top_accent(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0),
             "DU RACING CLUB AUX SOMMETS D'EUROPE",
             font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.8), Inches(1.2), Inches(11.7), Inches(0.5),
             "1988 - 2006", font_size=22, color=GOLD, alignment=PP_ALIGN.CENTER,
             font_name="Calibri Light")

add_rect(slide, Inches(5.5), Inches(1.8), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.5), Inches(2.2), Inches(10.3), Inches(1.5),
             "Dix-huit ans de carrière, deux pays, cinq clubs — le parcours d'un gardien\nqui traversera l'Atlantique pour atteindre l'élite européenne, avant d'y renoncer par conviction.",
             font_size=17, color=OFF_WHITE, italic=True, alignment=PP_ALIGN.CENTER,
             line_spacing=24)

clubs = [
    ("Racing Club", "1988-1993", Inches(1.2)),
    ("Lanús", "1994-1997", Inches(3.8)),
    ("RCD Mallorca", "1997-2002", Inches(6.4)),
    ("Albacete", "2002-2004", Inches(9.0)),
    ("Olimpo", "2005-2006", Inches(11.2)),
]
y_club = Inches(4.0)
for name, years, x in clubs:
    add_circle(slide, x, y_club, Inches(0.18), GREEN_ACCENT, 80)
    add_text_box(slide, x - Inches(0.5), y_club + Inches(0.3), Inches(1.8), Inches(0.4),
                 name, font_size=14, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x - Inches(0.5), y_club + Inches(0.6), Inches(1.8), Inches(0.3),
                 years, font_size=11, color=GOLD_LIGHT, alignment=PP_ALIGN.CENTER)

for i in range(len(clubs) - 1):
    x1 = clubs[i][2] + Inches(0.18)
    x2 = clubs[i + 1][2]
    add_rect(slide, x1, y_club + Inches(0.07), x2 - x1, Inches(0.03), GREEN_LIGHT, 30)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 2)

# ======== SLIDE 3: Racing Club ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(8.0), Inches(0.8),
             "RACING CLUB", font_size=44, color=WHITE, bold=True)
add_text_box(slide, Inches(1.0), Inches(1.3), Inches(3.0), Inches(0.5),
             "1988 - 1993", font_size=20, color=GOLD, font_name="Calibri Light")

add_rect(slide, Inches(1.0), Inches(2.0), Inches(4.0), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(2.4), Inches(7.0), Inches(2.5),
             "Ses débuts professionnels.\n\nC'est à Avellaneda, dans l'un des clubs historiques du football argentin, que Carlos Roa fait ses premiers pas entre les perches au plus haut niveau.",
             font_size=18, color=OFF_WHITE, line_spacing=26)

add_goal_shape(slide, Inches(8.5), Inches(1.5), Inches(4.0), Inches(3.5), WHITE, 20)
add_net_pattern(slide, Inches(8.7), Inches(1.7), Inches(3.6), Inches(3.1), WHITE, 8)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 3)

# ======== SLIDE 4: Lanús ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_MID)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(8.0), Inches(0.8),
             "LANÚS", font_size=44, color=WHITE, bold=True)
add_text_box(slide, Inches(1.0), Inches(1.3), Inches(3.0), Inches(0.5),
             "1994 - 1997", font_size=20, color=GOLD, font_name="Calibri Light")

add_rect(slide, Inches(1.0), Inches(2.0), Inches(4.0), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(2.4), Inches(6.5), Inches(2.0),
             "Un premier sommet continental : Roa remporte avec Lanús la Copa CONMEBOL 1996, son premier grand titre international et la confirmation de son talent.",
             font_size=18, color=OFF_WHITE, line_spacing=26)

add_rect(slide, Inches(8.0), Inches(3.5), Inches(4.5), Inches(2.0), GREEN_DARK, 70)
add_rect(slide, Inches(8.0), Inches(3.5), Inches(0.06), Inches(2.0), GOLD, 80)

add_text_box(slide, Inches(8.4), Inches(3.7), Inches(3.8), Inches(0.5),
             "1996", font_size=36, color=GOLD_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(8.4), Inches(4.4), Inches(3.8), Inches(0.8),
             "Vainqueur de la\nCopa CONMEBOL", font_size=18, color=WHITE,
             alignment=PP_ALIGN.CENTER, bold=True, line_spacing=24)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 4)

# ======== SLIDE 5: RCD Mallorca ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(10.0), Inches(0.8),
             "RCD MALLORCA", font_size=44, color=WHITE, bold=True)
add_text_box(slide, Inches(1.0), Inches(1.3), Inches(3.0), Inches(0.5),
             "1997 - 2002", font_size=20, color=GOLD, font_name="Calibri Light")

add_rect(slide, Inches(1.0), Inches(2.0), Inches(4.0), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(2.4), Inches(7.5), Inches(2.5),
             "L'apogée de sa carrière européenne.\n\nEn Liga espagnole, Roa devient l'un des gardiens les plus respectés du continent — un statut qui attirera bientôt l'attention des plus grands clubs d'Europe.",
             font_size=18, color=OFF_WHITE, line_spacing=26)

add_rect(slide, Inches(9.0), Inches(2.5), Inches(3.5), Inches(3.5), GREEN_DARK, 50)
add_circle(slide, Inches(9.7), Inches(2.8), Inches(2.0), GREEN_ACCENT, 15)
add_penalty_spot(slide, Inches(10.7), Inches(3.8), Inches(0.2), GOLD, 70)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 5)

# ======== SLIDE 6: Albacete ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_MID)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(10.0), Inches(0.8),
             "ALBACETE BALOMPIÉ", font_size=44, color=WHITE, bold=True)
add_text_box(slide, Inches(1.0), Inches(1.3), Inches(3.0), Inches(0.5),
             "2002 - 2004", font_size=20, color=GOLD, font_name="Calibri Light")

add_rect(slide, Inches(1.0), Inches(2.0), Inches(4.0), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(2.4), Inches(7.5), Inches(2.5),
             "Un retour en Liga après une montée, et le début d'une reconstruction personnelle autant que sportive — la carrière de Roa va bientôt être bouleversée par une nouvelle épreuve.",
             font_size=18, color=OFF_WHITE, line_spacing=26)

add_goal_shape(slide, Inches(8.5), Inches(1.5), Inches(4.0), Inches(3.5), WHITE, 15)
add_net_pattern(slide, Inches(8.7), Inches(1.7), Inches(3.6), Inches(3.1), WHITE, 6)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 6)

# ======== SLIDE 7: Olimpo ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(10.0), Inches(0.8),
             "OLIMPO", font_size=44, color=WHITE, bold=True)
add_text_box(slide, Inches(1.0), Inches(1.3), Inches(3.0), Inches(0.5),
             "2005 - 2006", font_size=20, color=GOLD, font_name="Calibri Light")

add_rect(slide, Inches(1.0), Inches(2.0), Inches(4.0), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(2.4), Inches(7.5), Inches(2.5),
             "Le dernier club avant la retraite.\n\nRoa referme la boucle dans son pays natal, mettant un terme à une carrière de dix-huit ans marquée par la foi autant que par le talent.",
             font_size=18, color=OFF_WHITE, line_spacing=26)

add_rect(slide, Inches(9.0), Inches(4.5), Inches(3.5), Inches(1.5), GREEN_DARK, 50)
add_text_box(slide, Inches(9.2), Inches(4.7), Inches(3.1), Inches(1.1),
             "18 ans de carrière\n2 pays - 5 clubs",
             font_size=16, color=GOLD_LIGHT, bold=True, alignment=PP_ALIGN.CENTER,
             line_spacing=22)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 7)

# ======== SLIDE 8: Végétarien ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_MID)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide, GREEN_LIGHT, Inches(0.04))

add_text_box(slide, Inches(1.0), Inches(0.5), Inches(11.0), Inches(0.8),
             "UN VÉGÉTARIEN STRICT", font_size=40, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.0), Inches(1.2), Inches(11.0), Inches(0.5),
             "Un temple, pas une machine", font_size=20, color=GOLD_LIGHT,
             italic=True, alignment=PP_ALIGN.CENTER, font_name="Calibri Light")

add_rect(slide, Inches(5.5), Inches(1.8), Inches(2.3), Inches(0.03), GOLD, 50)

items_veg = [
    "L'Église adventiste met l'accent sur une santé globale :\nle corps y est considéré comme un temple à respecter.",
    "Le « régime d'Éden » : une alimentation végétale\ninspirée du jardin d'Éden biblique.",
    "Roa évitait strictement viande, produits laitiers\net aliments transformés.",
    "Ses coéquipiers lui donnèrent un surnom affectueux :\n« El Lechuga » (la Laitue)"
]
y_pos = Inches(2.2)
for i, item in enumerate(items_veg):
    color_bar = GREEN_LIGHT if i > 0 else GOLD
    add_rect(slide, Inches(1.5), y_pos, Inches(0.08), Inches(0.8), color_bar, 70)
    add_text_box(slide, Inches(1.9), y_pos, Inches(10.0), Inches(0.9),
                 item, font_size=16, color=OFF_WHITE, line_spacing=22)
    y_pos += Inches(1.2)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 8)

# ======== SLIDE 9: Forme au sommet ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(11.0), Inches(0.8),
             "LA FORME AU SOMMET", font_size=40, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(1.4), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.5),
             "Malgré les exigences physiques du football professionnel européen,\nRoa a conservé une condition physique optimale grâce à ce mode de vie.",
             font_size=18, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=26)

add_rect(slide, Inches(3.5), Inches(3.5), Inches(6.3), Inches(2.5), GREEN_DARK, 60)
add_rect(slide, Inches(3.5), Inches(3.5), Inches(6.3), Inches(0.06), GOLD, 80)

add_text_box(slide, Inches(3.8), Inches(3.8), Inches(5.7), Inches(0.7),
             "TROPHÉE ZAMORA", font_size=32, color=GOLD_LIGHT, bold=True,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(3.8), Inches(4.6), Inches(5.7), Inches(1.0),
             "Meilleur gardien de but d'Espagne",
             font_size=20, color=WHITE, alignment=PP_ALIGN.CENTER,
             font_name="Calibri Light")

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 9)

# ======== SLIDE 10: Héros de Saint-Étienne ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.5), Inches(11.0), Inches(0.8),
             "LE HÉROS DE SAINT-ÉTIENNE", font_size=40, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(1.3), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(1.6), Inches(11.0), Inches(1.2),
             "Roa ne disputera qu'une seule Coupe du Monde de sa carrière.\nTitulaire incontesté de l'Argentine, il garde ses cages inviolées durant\ntoute la phase de groupes, face au Japon, à la Jamaïque et à la Croatie.",
             font_size=16, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=24)

items_cdm = [
    "En huitièmes de finale contre l'Angleterre, le match se termine 2-2 après prolongation.",
    "Lors de la séance de tirs au but, il repousse les tentatives de Paul Ince et David Batty.",
    "L'Argentine se qualifie 4-3, et Roa devient une légende instantanée dans son pays."
]
y = Inches(3.2)
for item in items_cdm:
    add_rect(slide, Inches(1.5), y + Inches(0.05), Inches(0.08), Inches(0.08), GREEN_ACCENT, 80)
    add_text_box(slide, Inches(1.9), y, Inches(8.5), Inches(0.5),
                 item, font_size=15, color=OFF_WHITE, line_spacing=20)
    y += Inches(0.55)

add_rect(slide, Inches(9.5), Inches(3.0), Inches(3.3), Inches(2.8), GREEN_DARK, 60)
add_rect(slide, Inches(9.5), Inches(3.0), Inches(3.3), Inches(0.06), GOLD, 80)
add_text_box(slide, Inches(9.7), Inches(3.3), Inches(2.9), Inches(1.0),
             "4 - 3", font_size=48, color=GOLD_LIGHT, bold=True,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(9.7), Inches(4.4), Inches(2.9), Inches(1.0),
             "Tirs au but\nArgentine bat l'Angleterre",
             font_size=13, color=WHITE, alignment=PP_ALIGN.CENTER, line_spacing=18)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 10)

# ======== SLIDE 11: Le but de trop ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_MID)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(11.0), Inches(0.8),
             "LE BUT DE TROP", font_size=40, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(1.4), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(1.8), Inches(7.0), Inches(1.0),
             "En quarts de finale, l'Argentine affronte les Pays-Bas.\nAprès un but pour chaque équipe, le score reste bloqué à 1-1 jusqu'à la 90e minute.",
             font_size=16, color=OFF_WHITE, line_spacing=24)

items_but = [
    "Dennis Bergkamp contrôle un long ballon et fusille Roa\nd'une frappe devenue légendaire : 2-1, l'Argentine est éliminée.",
    "Roa retourne en Argentine, son unique Mondial déjà terminé —\nl'année suivante, il quitte le football pour sa foi\net ne rejouera plus jamais de Coupe du Monde."
]
y = Inches(3.2)
for item in items_but:
    add_rect(slide, Inches(1.5), y + Inches(0.05), Inches(0.08), Inches(0.08), GREEN_ACCENT, 80)
    add_text_box(slide, Inches(1.9), y, Inches(7.5), Inches(0.8),
                 item, font_size=15, color=OFF_WHITE, line_spacing=20)
    y += Inches(0.9)

add_rect(slide, Inches(9.5), Inches(3.0), Inches(3.3), Inches(2.8), GREEN_DARK, 60)
add_rect(slide, Inches(9.5), Inches(3.0), Inches(3.3), Inches(0.06), RGBColor(0xC0, 0x39, 0x2B), 80)
add_text_box(slide, Inches(9.7), Inches(3.3), Inches(2.9), Inches(1.0),
             "1 - 2", font_size=48, color=RGBColor(0xE7, 0x4C, 0x3C), bold=True,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(9.7), Inches(4.4), Inches(2.9), Inches(1.0),
             "Pays-Bas élimine\nl'Argentine",
             font_size=13, color=WHITE, alignment=PP_ALIGN.CENTER, line_spacing=18)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 11)

# ======== SLIDE 12: Héroïque même dans la défaite ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.5), Inches(11.0), Inches(0.8),
             "HÉROÏQUE, MÊME DANS LA DÉFAITE",
             font_size=36, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.0), Inches(1.3), Inches(3.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(1.7), Inches(11.0), Inches(1.2),
             "En finale de la Coupe du Roi face au FC Barcelone, le Mallorca de Roa termine\nà dix contre onze après deux exclusions, mais tient bon jusqu'aux tirs au but.",
             font_size=16, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=24)

items_roi = [
    "Roa repousse trois penaltys — dont ceux de Rivaldo et Figo —\net va même marquer le sien.",
    "Malgré cette performance individuelle exceptionnelle,\nle Mallorca s'incline 5-4."
]
y = Inches(3.2)
for item in items_roi:
    add_rect(slide, Inches(1.5), y + Inches(0.05), Inches(0.08), Inches(0.08), GREEN_ACCENT, 80)
    add_text_box(slide, Inches(1.9), y, Inches(7.5), Inches(0.8),
                 item, font_size=15, color=OFF_WHITE, line_spacing=20)
    y += Inches(0.9)

add_rect(slide, Inches(9.5), Inches(3.0), Inches(3.3), Inches(2.8), GREEN_DARK, 60)
add_rect(slide, Inches(9.5), Inches(3.0), Inches(3.3), Inches(0.06), RGBColor(0xC0, 0x39, 0x2B), 80)
add_text_box(slide, Inches(9.7), Inches(3.3), Inches(2.9), Inches(1.0),
             "5 - 4", font_size=48, color=RGBColor(0xE7, 0x4C, 0x3C), bold=True,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(9.7), Inches(4.4), Inches(2.9), Inches(1.0),
             "FC Barcelone bat\nMallorca",
             font_size=13, color=WHITE, alignment=PP_ALIGN.CENTER, line_spacing=18)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 12)

# ======== SLIDE 13: Prophétie de l'an 2000 ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_MID)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(11.0), Inches(0.8),
             "LA PROPHÉTIE DE L'AN 2000",
             font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(1.4), Inches(2.3), Inches(0.03), GOLD, 50)

items_prophecy = [
    "En 1999, Roa était l'un des gardiens les plus convoités d'Europe —\nManchester United voulait qu'il succède à Peter Schmeichel.",
    "Convaincu par les prophéties bibliques sur la fin des temps, il croyait\nque le passage à l'an 2000 marquerait l'Apocalypse et le retour du Christ.",
    "Persuadé que l'argent et le football perdraient bientôt tout leur sens,\nil renonça à un contrat de plusieurs millions."
]
y = Inches(2.2)
for i, item in enumerate(items_prophecy):
    add_rect(slide, Inches(1.5), y + Inches(0.05), Inches(0.08), Inches(0.08), GOLD if i == 0 else GREEN_ACCENT, 80)
    add_text_box(slide, Inches(1.9), y, Inches(10.0), Inches(0.8),
                 item, font_size=16, color=OFF_WHITE, line_spacing=22)
    y += Inches(1.1)

add_rect(slide, Inches(9.0), Inches(0.5), Inches(3.8), Inches(1.2), GREEN_DARK, 50)
add_rect(slide, Inches(9.0), Inches(0.5), Inches(3.8), Inches(0.05), GOLD, 70)
add_text_box(slide, Inches(9.2), Inches(0.7), Inches(3.4), Inches(0.9),
             "Manchester United\nPETER SCHMEICHEL", font_size=13, color=GOLD_LIGHT,
             alignment=PP_ALIGN.CENTER, bold=True, line_spacing=18)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 13)

# ======== SLIDE 14: Se préparer, puis revenir ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(11.0), Inches(0.8),
             "SE PRÉPARER, PUIS REVENIR",
             font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(1.4), Inches(2.3), Inches(0.03), GOLD, 50)

items_revenir = [
    "Il installa sa famille dans un village isolé de la province\nde Córdoba, en Argentine, pour prier et se préparer.",
    "L'an 2000 arriva — et le monde ne prit pas fin.",
    "Roa revint alors sereinement au football professionnel."
]
y = Inches(2.0)
for item in items_revenir:
    add_rect(slide, Inches(1.5), y + Inches(0.05), Inches(0.08), Inches(0.08), GREEN_ACCENT, 80)
    add_text_box(slide, Inches(1.9), y, Inches(10.0), Inches(0.6),
                 item, font_size=16, color=OFF_WHITE, line_spacing=22)
    y += Inches(0.8)

add_rect(slide, Inches(1.5), Inches(4.5), Inches(10.3), Inches(2.0), GREEN_DARK, 50)
add_rect(slide, Inches(1.5), Inches(4.5), Inches(0.06), Inches(2.0), GOLD, 70)

add_text_box(slide, Inches(1.9), Inches(4.6), Inches(9.5), Inches(0.4),
             "SES MOTS, DES ANNÉES PLUS TARD", font_size=14, color=GOLD,
             bold=True, font_name="Calibri Light")

add_text_box(slide, Inches(1.9), Inches(5.1), Inches(9.5), Inches(1.2),
             "« Sur le plan spirituel, c'était la bonne décision.\nMais sur le plan sportif, il reconnaîtra avoir quitté le football\nau sommet de sa carrière. »",
             font_size=17, color=OFF_WHITE, italic=True, line_spacing=24)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 14)

# ======== SLIDE 15: Sabbat ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_MID)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.5), Inches(11.0), Inches(0.8),
             "FIDÈLE AU QUATRIÈME COMMANDEMENT",
             font_size=36, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.0), Inches(1.3), Inches(3.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(1.7), Inches(11.0), Inches(1.2),
             "De retour au RCD Mallorca en 2000, sa pratique religieuse posa un défi logistique\ninédit pour son club : les adventistes observent le sabbat du vendredi au coucher du\nsoleil jusqu'au samedi au coucher du soleil, période durant laquelle le travail séculier\n— et la compétition sportive — sont mis de côté.",
             font_size=15, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=22)

add_rect(slide, Inches(2.5), Inches(3.4), Inches(8.3), Inches(1.2), GREEN_DARK, 60)
add_rect(slide, Inches(2.5), Inches(3.4), Inches(0.06), Inches(1.2), GOLD, 80)

add_text_box(slide, Inches(2.9), Inches(3.5), Inches(7.5), Inches(1.0),
             "« Je ne jouerai jamais un match le samedi. »",
             font_size=22, color=GOLD_LIGHT, italic=True, alignment=PP_ALIGN.CENTER,
             font_name="Calibri Light")

add_text_box(slide, Inches(1.0), Inches(5.0), Inches(11.0), Inches(1.2),
             "La Liga programmant souvent ses grandes rencontres le samedi soir,\nRoa acceptait de se mettre lui-même sur le banc — quitte à perdre\nsa place de titulaire et ses primes.",
             font_size=16, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=24)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 15)

# ======== SLIDE 16: Cancer ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)

add_rect(slide, 0, 0, Inches(0.15), H, GREEN_ACCENT, 60)
add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.6), Inches(11.0), Inches(0.8),
             "UNE AUTRE ÉPREUVE",
             font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(1.4), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.0), Inches(1.8), Inches(11.0), Inches(1.0),
             "En pleine reconstruction de sa carrière à Albacete, Roa reçoit un diagnostic\nde cancer des testicules. Lui qui n'avait jamais bu ni fumé peine à comprendre\nce nouveau coup du sort.",
             font_size=16, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=24)

items_cancer = [
    "Une année entière est consacrée à la chimiothérapie et à la rééducation.",
    "Il guérit, revient au jeu, puis termine sa carrière en Argentine\navec le club Olimpo en 2006."
]
y = Inches(3.4)
for item in items_cancer:
    add_rect(slide, Inches(1.5), y + Inches(0.05), Inches(0.08), Inches(0.08), GREEN_ACCENT, 80)
    add_text_box(slide, Inches(1.9), y, Inches(10.0), Inches(0.7),
                 item, font_size=16, color=OFF_WHITE, line_spacing=22)
    y += Inches(0.8)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 16)

# ======== SLIDE 17: Question ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_MID)
add_field_lines(slide)
add_center_circle(slide, W // 2, H // 2, Inches(2.5), GREEN_LIGHT, 10)

add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.8), Inches(11.0), Inches(1.5),
             "Qu'est-ce que je suis prêt\nà mettre de côté pour ma foi ?",
             font_size=38, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER,
             line_spacing=48)

add_rect(slide, Inches(5.5), Inches(2.4), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.5), Inches(2.8), Inches(10.3), Inches(1.2),
             "Malgré ses regrets sportifs assumés, Carlos Roa a choisi, à répétition —\nla prophétie de l'an 2000, le sabbat, la maladie — de faire passer\nsa foi avant sa réussite terrestre.",
             font_size=16, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=24)

concepts = [
    ("SOBRIÉTÉ", Inches(2.0)),
    ("FIDÉLITÉ AU SABBAT", Inches(5.5)),
    ("PRIORITÉS", Inches(9.5)),
]
for label, x in concepts:
    add_rect(slide, x, Inches(4.5), Inches(2.8), Inches(1.5), GREEN_DARK, 60)
    add_rect(slide, x, Inches(4.5), Inches(2.8), Inches(0.06), GOLD, 70)
    add_text_box(slide, x, Inches(4.8), Inches(2.8), Inches(1.0),
                 label, font_size=16, color=GOLD_LIGHT, bold=True,
                 alignment=PP_ALIGN.CENTER)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 17)

# ======== SLIDE 18: Le monde offrit ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)
add_center_circle(slide, W // 2, H // 2 - Inches(0.5), Inches(3.0), GREEN_LIGHT, 8)

add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.5), Inches(11.0), Inches(0.8),
             "LE MONDE OFFRIT DES MILLIONS.",
             font_size=38, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.0), Inches(1.2), Inches(11.0), Inches(0.5),
             "DIEU DEMANDAIT UN JOUR.",
             font_size=24, color=GOLD_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(1.8), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.5), Inches(2.1), Inches(10.3), Inches(1.5),
             "Carlos Roa a compris quelque chose que le football ne pouvait jamais enseigner :\nla vraie grandeur ne se mesure pas en trophées, mais en fidélité.\nChaque samedi, en posant son maillot, il a témoigné que Dieu passe avant le monde.",
             font_size=16, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=24)

add_rect(slide, Inches(2.5), Inches(3.8), Inches(8.3), Inches(1.2), GREEN_DARK, 60)
add_rect(slide, Inches(2.5), Inches(3.8), Inches(0.06), Inches(1.2), GOLD, 80)

add_text_box(slide, Inches(2.9), Inches(3.9), Inches(7.5), Inches(1.0),
             "« Souviens-toi du jour du sabbat, pour le sanctifier. »\nExode 20:8",
             font_size=18, color=GOLD_LIGHT, italic=True, alignment=PP_ALIGN.CENTER,
             line_spacing=26, font_name="Calibri Light")

add_text_box(slide, Inches(1.5), Inches(5.3), Inches(10.3), Inches(1.0),
             "Aujourd'hui, Dieu te fait la même question : m'auras-tu pour sacré ?",
             font_size=20, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_bottom_bar(slide)
add_decorative_corners(slide, GOLD, Inches(0.4), alpha=30)
add_slide_number(slide, 18)

# ======== SLIDE 19: Conclusion ========
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_field_lines(slide)
add_center_circle(slide, W // 2, H // 2, Inches(2.5), GREEN_LIGHT, 10)
add_penalty_spot(slide, W // 2, H // 2, Inches(0.2), GOLD, 60)

add_top_accent(slide)

add_text_box(slide, Inches(1.0), Inches(0.5), Inches(11.0), Inches(1.0),
             "IL A TOUT QUITTÉ POUR DIEU.",
             font_size=38, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.0), Inches(1.3), Inches(11.0), Inches(0.6),
             "ET DIEU NE L'A JAMAIS ABANDONNÉ.",
             font_size=28, color=GOLD_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)

add_rect(slide, Inches(5.5), Inches(2.0), Inches(2.3), Inches(0.03), GOLD, 50)

add_text_box(slide, Inches(1.5), Inches(2.3), Inches(10.3), Inches(1.0),
             "Carlos Roa n'a jamais regretté sa décision. Le sacrifice pour la foi\nn'est jamais une perte — c'est un investissement pour l'éternité.",
             font_size=17, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=24)

add_rect(slide, Inches(2.5), Inches(3.5), Inches(8.3), Inches(1.5), GREEN_DARK, 50)
add_rect(slide, Inches(2.5), Inches(3.5), Inches(0.06), Inches(1.5), GOLD, 70)

add_text_box(slide, Inches(2.9), Inches(3.6), Inches(7.5), Inches(1.3),
             "« Ce que tu semes pour Dieu,\ntu le moissonneras pour l'éternité. »\nGalates 6:7-9",
             font_size=18, color=GOLD_LIGHT, italic=True, alignment=PP_ALIGN.CENTER,
             line_spacing=26, font_name="Calibri Light")

add_text_box(slide, Inches(1.5), Inches(5.3), Inches(10.3), Inches(0.8),
             "Le sabbat n'est pas une perte.\nC'est la preuve que Dieu est plus grand que tout ce que le monde peut offrir.",
             font_size=16, color=OFF_WHITE, alignment=PP_ALIGN.CENTER, line_spacing=22)

tags = ["GRÂCE", "TÉMOIGNAGE", "SABBAT", "ESPÉRANCE"]
tag_width = Inches(2.2)
total_tags_w = len(tags) * tag_width + (len(tags) - 1) * Inches(0.3)
start_x = (W - total_tags_w) // 2
for i, tag in enumerate(tags):
    x = start_x + i * (tag_width + Inches(0.3))
    add_rect(slide, x, Inches(6.3), tag_width, Inches(0.5), GREEN_DARK, 60)
    add_rect(slide, x, Inches(6.3), tag_width, Inches(0.04), GOLD, 70)
    add_text_box(slide, x, Inches(6.35), tag_width, Inches(0.4),
                 tag, font_size=12, color=GOLD_LIGHT, bold=True,
                 alignment=PP_ALIGN.CENTER)

add_bottom_bar(slide, GOLD, Inches(0.08))
add_decorative_corners(slide, GOLD, Inches(0.5), alpha=40)
add_slide_number(slide, 19)

output_path = r"G:\SDA\Toriteny Ankizy\Carlos_Roa_Presentation.pptx"
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
