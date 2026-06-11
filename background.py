# background.py
# Background starfield generation and coverage helpers

import random
from typing import List, Dict

def generate_deep_sky(area: int, count: int) -> List[Dict]:
    """Return a list of randomly placed background stars within +/-area."""
    stars = []
    for _ in range(count):
        x = random.randint(-area, area)
        y = random.randint(-area, area)
        size = random.choice([1, 1, 2, 2, 3])
        brightness = random.uniform(0.1, 0.7)
        v = int(brightness * 255)
        color = f"#{v:02x}{v:02x}{v:02x}"
        stars.append({"coords": (x, y), "size": size, "color": color, "brightness": brightness})
    return stars

def ensure_deep_sky_coverage(app, background_star_count: int, max_area: int = 200000):
    """
    Ensure the app.deep_sky_stars covers the visible world area.
    Regenerates only when required and updates app._background_area.
    """
    w = max(1, app.canvas.winfo_width())
    h = max(1, app.canvas.winfo_height())

    half_world_w = (w / 2) / max(app.zoom, 1e-6)
    half_world_h = (h / 2) / max(app.zoom, 1e-6)

    required_half_extent = int(max(half_world_w, half_world_h) * 1.6)
    current_area = getattr(app, "_background_area", None) or 0

    if required_half_extent > current_area:
        new_area = max(required_half_extent, max(1000, current_area * 2))
        new_area = min(new_area, max_area)
        app.deep_sky_stars = generate_deep_sky(new_area, background_star_count)
        app._background_area = new_area
