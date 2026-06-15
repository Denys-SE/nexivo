from __future__ import annotations

import math
import random
from pathlib import Path


OUT_DIR = Path("assets")
OUT_FILE = OUT_DIR / "earth-logistics-background.svg"
WIDTH = 1920
HEIGHT = 1080
CX = 1260
CY = 500
R = 455


def project(lat: float, lon: float, rotation: float = -30.0) -> tuple[float, float]:
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon + rotation)
    x = CX + R * math.cos(lat_rad) * math.sin(lon_rad)
    y = CY - R * math.sin(lat_rad) * 0.86
    return x, y


def points_path(points: list[tuple[float, float]], close: bool = True) -> str:
    projected = [project(lat, lon) for lon, lat in points]
    commands = [f"M {projected[0][0]:.1f} {projected[0][1]:.1f}"]
    commands.extend(f"L {x:.1f} {y:.1f}" for x, y in projected[1:])
    if close:
        commands.append("Z")
    return " ".join(commands)


def route_path(start: tuple[float, float], end: tuple[float, float], lift: float) -> str:
    sx, sy = project(start[0], start[1])
    ex, ey = project(end[0], end[1])
    mx = (sx + ex) / 2
    my = (sy + ey) / 2 - lift
    return f"M {sx:.1f} {sy:.1f} Q {mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}"


def make_ship(route_id: str, delay: float, scale: float = 1.0) -> str:
    colors = ["#2563eb", "#16a34a", "#f8fafc", "#0891b2", "#60a5fa", "#f59e0b", "#ef4444"]
    containers = []
    for row in range(4):
        for col in range(10):
            color = colors[(row + col) % len(colors)]
            x = -39 + col * 8
            y = -30 - row * 5
            containers.append(
                f'<rect x="{x}" y="{y}" width="6.5" height="4" rx="0.5" fill="{color}" opacity="0.96"/>'
            )
    containers_svg = "\n".join(containers)
    return f"""
      <g class="cargo-ship" transform="scale({scale})" opacity="0.98">
        <path class="ship-wake" d="M -86 18 C -62 6, -34 5, -10 11"/>
        <path class="ship-wake soft" d="M -96 28 C -66 14, -38 15, -14 21"/>
        <path d="M -58 14 L 46 14 L 68 -5 L -37 -23 Z" fill="#edf4fb" stroke="#06101d" stroke-width="2.4"/>
        <path d="M -48 14 L 41 14" stroke="#7dd3fc" stroke-width="2.5"/>
        <path d="M 25 -31 L 45 -27 L 49 -10 L 21 -13 Z" fill="#dbeafe" stroke="#06101d" stroke-width="1.4"/>
        <rect x="31" y="-38" width="11" height="8" rx="1" fill="#93c5fd" stroke="#06101d" stroke-width="1"/>
        {containers_svg}
        <animateMotion dur="24s" begin="{delay}s" repeatCount="indefinite" rotate="auto">
          <mpath href="#{route_id}"/>
        </animateMotion>
      </g>
    """


def main() -> None:
    random.seed(42)
    OUT_DIR.mkdir(exist_ok=True)

    stars = []
    for _ in range(260):
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)
        r = random.uniform(0.45, 1.8)
        opacity = random.uniform(0.22, 0.9)
        stars.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#dbeafe" opacity="{opacity:.2f}"/>'
        )

    land_polygons = [
        [(-168, 72), (-150, 71), (-138, 70), (-122, 60), (-116, 56), (-125, 42), (-118, 35), (-104, 27), (-100, 24), (-91, 18), (-82, 27), (-76, 37), (-66, 48), (-52, 59), (-63, 67), (-80, 72)],
        [(-82, 13), (-70, 8), (-62, -2), (-60, -12), (-66, -32), (-72, -52), (-64, -56), (-55, -55), (-46, -38), (-42, -24), (-50, 2)],
        [(-11, 36), (-6, 51), (4, 55), (18, 58), (35, 58), (49, 54), (60, 50), (73, 52), (84, 56), (96, 56), (112, 51), (133, 48), (145, 41), (150, 28), (139, 22), (121, 18), (111, 21), (104, 16), (92, 22), (82, 15), (72, 6), (58, 8), (47, 20), (36, 18), (33, 4), (22, 7), (8, 8), (1, 18), (-8, 26)],
        [(-18, 32), (-4, 34), (9, 31), (22, 25), (30, 14), (35, 2), (38, -8), (34, -20), (28, -34), (16, -35), (8, -24), (6, -10), (-2, 2), (-6, 8)],
        [(44, 12), (58, 16), (78, 8), (88, 1), (92, -10), (84, -21), (76, -30), (62, -31), (50, -25), (42, -4)],
        [(112, -11), (124, -8), (140, -10), (154, -12), (150, -28), (150, -38), (132, -40), (118, -40), (110, -24)],
        [(-52, 72), (-36, 76), (-20, 75), (-4, 73), (12, 70), (10, 62), (-12, 60), (-32, 60)],
        [(-180, -62), (-110, -70), (-35, -66), (45, -72), (128, -66), (180, -70), (180, -82), (-180, -82)],
        [(-8, 58), (2, 60), (9, 56), (7, 50), (-4, 51)],
        [(136, 45), (142, 43), (146, 38), (142, 32), (135, 34), (130, 39)],
        [(104, 4), (114, 5), (121, -1), (118, -8), (108, -7), (101, -1)],
        [(120, 24), (123, 25), (122, 21), (119, 20)],
        [(79, 9), (82, 7), (81, 5), (78, 6)],
        [(43, -12), (50, -16), (49, -24), (43, -25), (40, -18)],
    ]

    country_lines = [
        [(-10, 35), (5, 43), (20, 44), (36, 47), (48, 42), (61, 44), (78, 47), (94, 45), (108, 42), (132, 35)],
        [(32, 28), (46, 20), (63, 17), (78, 24), (98, 21), (116, 28), (128, 42)],
        [(-5, 12), (15, 8), (32, 2), (48, -6), (62, -18), (76, -26), (89, -12)],
        [(-76, 48), (-102, 38), (-115, 28), (-96, 18), (-78, 24)],
        [(-70, -8), (-64, -22), (-70, -38), (-58, -50)],
        [(15, 60), (28, 50), (35, 40), (22, 31), (10, 36)],
        [(88, 8), (101, 0), (108, -12), (121, -19), (135, -25)],
        [(73, 36), (80, 30), (90, 28), (100, 32), (109, 29)],
        [(96, 42), (105, 36), (116, 34), (125, 40)],
        [(24, 38), (30, 33), (36, 31), (42, 36)],
        [(2, 48), (12, 46), (22, 44), (30, 47)],
    ]

    ports = {
        "Shanghai": (31.2, 121.5),
        "Shenzhen": (22.5, 114.1),
        "Ningbo": (29.9, 121.6),
        "Qingdao": (36.1, 120.4),
        "Xiamen": (24.5, 118.1),
        "Tianjin": (39.1, 117.2),
        "Rotterdam": (51.9, 4.5),
        "Hamburg": (53.5, 10.0),
        "Constanta": (44.2, 28.6),
        "Gdansk": (54.4, 18.6),
        "Piraeus": (37.9, 23.6),
        "Antwerp": (51.2, 4.4),
        "Singapore": (1.3, 103.8),
        "Dubai": (25.2, 55.3),
        "Suez": (30.6, 32.3),
        "Valencia": (39.5, -0.3),
        "Barcelona": (41.3, 2.2),
        "Marseille": (43.3, 5.4),
        "Genoa": (44.4, 8.9),
        "Trieste": (45.6, 13.8),
    }

    routes = [
        ("route-1", "Shanghai", "Rotterdam", 190),
        ("route-2", "Shenzhen", "Constanta", 155),
        ("route-3", "Ningbo", "Hamburg", 210),
        ("route-4", "Qingdao", "Gdansk", 235),
        ("route-5", "Shanghai", "Piraeus", 130),
        ("route-6", "Shenzhen", "Antwerp", 205),
        ("route-7", "Xiamen", "Marseille", 175),
        ("route-8", "Tianjin", "Barcelona", 220),
        ("route-9", "Shenzhen", "Singapore", 70),
        ("route-10", "Singapore", "Dubai", 100),
        ("route-11", "Dubai", "Suez", 75),
        ("route-12", "Suez", "Valencia", 115),
        ("route-13", "Suez", "Genoa", 95),
        ("route-14", "Shanghai", "Trieste", 150),
    ]

    land_svg = "\n".join(
        f'<path class="continent" d="{points_path(poly)}"/>' for poly in land_polygons
    )
    borders_svg = "\n".join(
        f'<path class="country-border" d="{points_path(line, close=False)}"/>' for line in country_lines
    )
    ports_svg = "\n".join(
        f'<circle class="port {"china-port" if name in {"Shanghai", "Shenzhen", "Ningbo", "Qingdao"} else ""}" cx="{project(lat, lon)[0]:.1f}" cy="{project(lat, lon)[1]:.1f}" r="{5 if name in {"Shanghai", "Shenzhen", "Ningbo", "Qingdao"} else 3.6}"/>'
        for name, (lat, lon) in ports.items()
    )
    route_defs = "\n".join(
        f'<path id="{rid}" d="{route_path(ports[start], ports[end], lift)}"/>'
        for rid, start, end, lift in routes
    )
    route_lines = "\n".join(
        f'<use href="#{rid}" class="trade-route" style="animation-delay:{i * -0.55}s"/>'
        for i, (rid, *_rest) in enumerate(routes)
    )
    ships = "\n".join(
        make_ship(rid, delay=-i * 1.85, scale=0.58 + (i % 4) * 0.07)
        for i, (rid, *_rest) in enumerate(routes)
    )

    cloud_bands = []
    for i, lat in enumerate(range(-52, 64, 12)):
        points = []
        for lon in range(-180, 181, 8):
            wave = lat + math.sin(math.radians(lon * 2 + i * 21)) * 2.7
            points.append((lon, wave))
        cloud_bands.append(f'<path class="cloud-band" d="{points_path(points, close=False)}"/>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Animated Earth logistics background">
  <defs>
    <radialGradient id="ocean" cx="38%" cy="28%" r="68%">
      <stop offset="0%" stop-color="#67b7ef"/>
      <stop offset="28%" stop-color="#1769aa"/>
      <stop offset="58%" stop-color="#063b78"/>
      <stop offset="84%" stop-color="#031c44"/>
      <stop offset="100%" stop-color="#020817"/>
    </radialGradient>
    <linearGradient id="land" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e5c17b"/>
      <stop offset="28%" stop-color="#387c39"/>
      <stop offset="55%" stop-color="#b18a55"/>
      <stop offset="78%" stop-color="#235f38"/>
      <stop offset="100%" stop-color="#7f633c"/>
    </linearGradient>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="globeClip">
      <circle cx="{CX}" cy="{CY}" r="{R}"/>
    </clipPath>
    {route_defs}
  </defs>

  <style>
    .stars {{ transform-origin: center; animation: driftStars 58s linear infinite; }}
    .earth {{ transform-origin: {CX}px {CY}px; animation: breathe 10s ease-in-out infinite; }}
    .surface {{ transform-origin: {CX}px {CY}px; animation: surfaceDrift 34s ease-in-out infinite alternate; }}
    .continent {{ fill: url(#land); stroke: rgba(255,255,255,.58); stroke-width: 1.12; }}
    .country-border {{ fill: none; stroke: rgba(255,255,255,.5); stroke-width: .82; }}
    .cloud-band {{ fill: none; stroke: rgba(255,255,255,.18); stroke-width: 4.8; stroke-linecap: round; animation: cloudMove 17s ease-in-out infinite alternate; }}
    .trade-route {{ fill: none; stroke: rgba(103,232,249,.56); stroke-width: 1.55; filter: url(#softGlow); stroke-dasharray: 8 18; animation: routePulse 6s ease-in-out infinite; }}
    .port {{ fill: #2dd4bf; filter: url(#softGlow); }}
    .china-port {{ fill: #60a5fa; }}
    .cargo-ship {{ filter: drop-shadow(0 6px 12px rgba(0,0,0,.45)); }}
    .ship-wake {{ fill: none; stroke: rgba(191,219,254,.38); stroke-width: 2.2; stroke-linecap: round; }}
    .ship-wake.soft {{ stroke: rgba(103,232,249,.18); stroke-width: 1.5; }}
    @keyframes driftStars {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-32px); }} }}
    @keyframes breathe {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.012); }} }}
    @keyframes surfaceDrift {{ from {{ transform: translateX(18px) scale(1.002); }} to {{ transform: translateX(-28px) scale(1.008); }} }}
    @keyframes cloudMove {{ from {{ transform: translateX(-26px); opacity: .42; }} to {{ transform: translateX(34px); opacity: .72; }} }}
    @keyframes routePulse {{ 0%,100% {{ opacity: .48; }} 50% {{ opacity: .9; }} }}
  </style>

  <rect width="100%" height="100%" fill="#020711"/>
  <g class="stars">{''.join(stars)}</g>

  <circle cx="{CX}" cy="{CY}" r="{R + 38}" fill="none" stroke="rgba(96,165,250,.42)" stroke-width="20" filter="url(#softGlow)"/>
  <g class="earth">
    <circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#ocean)" stroke="rgba(147,197,253,.72)" stroke-width="2.2"/>
    <g clip-path="url(#globeClip)">
      <g class="surface">
        <g opacity=".18">
          {''.join(f'<ellipse cx="{CX}" cy="{CY - R * .78 + j * R * .13:.1f}" rx="{R * (.82 - abs(7-j)*.018):.1f}" ry="{R * .028:.1f}" fill="none" stroke="#bae6fd" stroke-width="1"/>' for j in range(15))}
        </g>
        {land_svg}
        {borders_svg}
        <g opacity=".76">{''.join(cloud_bands)}</g>
        <path d="M {CX - R} {CY - R * .74} C {CX - R * .4} {CY - R * .9}, {CX + R * .4} {CY - R * .9}, {CX + R} {CY - R * .72}" fill="none" stroke="rgba(248,250,252,.34)" stroke-width="10"/>
        <path d="M {CX - R} {CY + R * .75} C {CX - R * .4} {CY + R * .88}, {CX + R * .45} {CY + R * .88}, {CX + R} {CY + R * .74}" fill="none" stroke="rgba(248,250,252,.2)" stroke-width="8"/>
        {route_lines}
        {ports_svg}
        {ships}
      </g>
    </g>
    <circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="rgba(125,211,252,.42)" stroke-width="3"/>
    <circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#shade)"/>
  </g>

  <defs>
    <radialGradient id="shade" cx="34%" cy="24%" r="76%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".08"/>
      <stop offset="48%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity=".52"/>
    </radialGradient>
  </defs>

  <rect width="100%" height="100%" fill="url(#readability)"/>
  <defs>
    <linearGradient id="readability" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#040a14" stop-opacity=".86"/>
      <stop offset="40%" stop-color="#040a14" stop-opacity=".48"/>
      <stop offset="76%" stop-color="#040a14" stop-opacity=".12"/>
      <stop offset="100%" stop-color="#040a14" stop-opacity=".34"/>
    </linearGradient>
  </defs>
</svg>
"""

    OUT_FILE.write_text(svg, encoding="utf-8")
    print(f"Generated {OUT_FILE}")


if __name__ == "__main__":
    main()
