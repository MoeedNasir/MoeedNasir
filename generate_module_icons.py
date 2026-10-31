#!/usr/bin/env python3
"""Generate simple, original SVG icon tiles for Odoo modules (GitHub README assets)."""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "modules")
os.makedirs(OUT, exist_ok=True)

W = "white"
STROKE = f'stroke="{W}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"'


def gear(cx=120, cy=100, r_out=46, r_in=30):
    teeth = []
    for i in range(8):
        a = math.radians(i * 45)
        x = cx + (r_in + 6) * math.cos(a)
        y = cy + (r_in + 6) * math.sin(a)
        teeth.append(
            f'<rect x="{x - 9:.1f}" y="{y - 9:.1f}" width="18" height="18" rx="4" '
            f'fill="{W}" transform="rotate({i * 45} {x:.1f} {y:.1f})"/>'
        )
    return (
        "".join(teeth)
        + f'<circle cx="{cx}" cy="{cy}" r="{r_in}" fill="{W}"/>'
        + f'<circle cx="{cx}" cy="{cy}" r="11" fill="SITE_COLOR"/>'
    )


GLYPHS = {
    "sales": f'<polyline points="62,148 96,106 122,126 152,72 178,88" {STROKE}/>'
             '<circle cx="96" cy="106" r="6" fill="white"/><circle cx="152" cy="72" r="6" fill="white"/>'
             '<line x1="58" y1="158" x2="182" y2="158" stroke="white" stroke-width="7" stroke-linecap="round"/>',
    "crm": '<circle cx="120" cy="100" r="46" stroke="white" stroke-width="7" fill="none"/>'
           '<circle cx="120" cy="100" r="28" stroke="white" stroke-width="7" fill="none"/>'
           '<circle cx="120" cy="100" r="9" fill="white"/>',
    "purchase": f'<path d="M58 62 h24 l15 66 h72 l13 -48 H90" {STROKE}/>'
                '<circle cx="106" cy="152" r="9" fill="white"/><circle cx="164" cy="152" r="9" fill="white"/>',
    "inventory": '<polygon points="120,50 178,78 120,106 62,78" fill="white" opacity="0.95"/>'
                 '<polygon points="62,78 120,106 120,164 62,136" fill="white" opacity="0.65"/>'
                 '<polygon points="120,106 178,78 178,136 120,164" fill="white" opacity="0.8"/>',
    "accounting": '<rect x="80" y="48" width="80" height="118" rx="12" stroke="white" stroke-width="7" fill="none"/>'
                  '<rect x="94" y="62" width="52" height="20" rx="4" fill="white"/>'
                  + "".join(
                      f'<circle cx="{cx}" cy="{cy}" r="6" fill="white"/>'
                      for cy in (104, 126, 148) for cx in (98, 120, 142)
                  ),
    "manufacturing": "GEAR",
    "pos": '<path d="M84 50 h72 v104 l-12 -9 -12 9 -12 -9 -12 9 -12 -9 -8 6 z" fill="white" opacity="0.95"/>'
           '<line x1="98" y1="78" x2="142" y2="78" stroke="SITE_COLOR" stroke-width="7" stroke-linecap="round"/>'
           '<line x1="98" y1="100" x2="142" y2="100" stroke="SITE_COLOR" stroke-width="7" stroke-linecap="round"/>'
           '<line x1="98" y1="122" x2="128" y2="122" stroke="SITE_COLOR" stroke-width="7" stroke-linecap="round"/>',
    "hr": '<rect x="78" y="46" width="84" height="120" rx="12" stroke="white" stroke-width="7" fill="none"/>'
          '<circle cx="120" cy="84" r="17" stroke="white" stroke-width="7" fill="none"/>'
          '<path d="M96 132 q24 -18 48 0" stroke="white" stroke-width="7" fill="none" stroke-linecap="round"/>'
          '<line x1="98" y1="150" x2="142" y2="150" stroke="white" stroke-width="7" stroke-linecap="round"/>',
    "ecommerce": f'<path d="M76 84 h88 l-9 82 a8 8 0 0 1 -8 7 H93 a8 8 0 0 1 -8 -7 z" {STROKE}/>'
                 '<path d="M96 84 v-14 a24 24 0 0 1 48 0 v14" stroke="white" stroke-width="7" fill="none" stroke-linecap="round"/>',
    "website": '<circle cx="120" cy="100" r="54" stroke="white" stroke-width="7" fill="none"/>'
               '<ellipse cx="120" cy="100" rx="25" ry="54" stroke="white" stroke-width="6" fill="none"/>'
               '<line x1="66" y1="100" x2="174" y2="100" stroke="white" stroke-width="6"/>',
}

MODULES = [
    ("sales", "Sales", "#E46A11", "#F08A3C"),
    ("crm", "CRM", "#00A09D", "#2BB3A3"),
    ("purchase", "Purchase", "#875A7B", "#A47197"),
    ("inventory", "Inventory", "#1E9E75", "#38B98A"),
    ("accounting", "Accounting", "#2F5597", "#4A74B8"),
    ("manufacturing", "Manufacturing", "#546E7A", "#728994"),
    ("pos", "POS", "#C2185B", "#D93B78"),
    ("hr", "HR & Payroll", "#7B1FA2", "#9A3FC0"),
    ("ecommerce", "eCommerce", "#00838F", "#26A0AD"),
    ("website", "Website", "#3949AB", "#5A6BC2"),
]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="1" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="232" height="232" rx="48" fill="url(#g)"/>
  {glyph}
  <text x="120" y="212" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="{fs}" font-weight="bold" fill="white">{label}</text>
</svg>
"""

for slug, label, c1, c2 in MODULES:
    glyph = GLYPHS[slug]
    if glyph == "GEAR":
        glyph = gear().replace("SITE_COLOR", c1)
    glyph = glyph.replace("SITE_COLOR", c1)
    fs = 30 if len(label) <= 9 else (26 if len(label) <= 12 else 23)
    svg = TEMPLATE.format(c1=c1, c2=c2, glyph=glyph, fs=fs, label=label.replace("&", "&amp;"))
    with open(os.path.join(OUT, f"{slug}.svg"), "w") as f:
        f.write(svg)
    print("wrote", slug)
