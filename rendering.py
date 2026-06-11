# rendering.py
# Drawing helpers: color blending and glow rendering (dependency-free)

def blend_color_to_bg(hex_color, alpha, bg=(5, 5, 12)):
    """Blend a hex color toward the background by alpha (0..1)."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    br = int(r * alpha + bg[0] * (1 - alpha))
    bgc = int(g * alpha + bg[1] * (1 - alpha))
    bb = int(b * alpha + bg[2] * (1 - alpha))
    return f"#{br:02x}{bgc:02x}{bb:02x}"

def draw_glow(canvas, sx, sy, size, color, brightness):
    """
    Draw a soft glow using concentric ovals on the provided canvas.
    Keeps implementation simple and dependency-free for course scope.
    """
    rings = max(3, int(3 + brightness * 5))
    for i in range(rings, 0, -1):
        factor = i / rings
        r = size * (1 + factor * 2.2)
        alpha = factor * brightness * 0.6
        glow_color = blend_color_to_bg(color, alpha)
        canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill=glow_color, outline="")
