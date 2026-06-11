# sky_viewer.py
# Main application file for Stellaris - Sky Viewer Pro
# Combines rendering, background generation, and astronomical data display

import tkinter as tk
from tkinter import font
import math

from astronomical_data import ASTRONOMICAL_DATA
from rendering import draw_glow
from background import generate_deep_sky, ensure_deep_sky_coverage

# Constants (zoom configuration and sensitivity)
ZOOM_INITIAL = 0.5
ZOOM_MIN     = 0.05
ZOOM_MAX     = 8.0
ZOOM_STEP    = 1.1

# Click detection radii (adjust the "clickable" area)
CLICK_RADIUS_STAR      = 1.8
CLICK_RADIUS_SATELLITE = 2.5

# Parameters for the starfield background
BACKGROUND_STAR_COUNT  = 4000
BACKGROUND_AREA        = 10000

class SkyViewerApp:
    def __init__(self, root):
        # Main application initialization and view state
        self.root = root
        self.root.title("Stellaris - Sky Viewer Pro")
        self.root.geometry("1200x750")
        self.root.configure(bg="#05050C")

        # Fonts used in the UI
        self.font_main       = font.Font(family="Helvetica Neue", size=11)
        self.font_title      = font.Font(family="Helvetica Neue", size=24, weight="bold")
        self.font_data_title = font.Font(family="Helvetica Neue", size=14, weight="bold")
        self.font_data_text  = font.Font(family="Helvetica Neue", size=10)

        # View state (zoom and offsets)
        self.zoom     = ZOOM_INITIAL
        self.offset_x = 0
        self.offset_y = 0

        # Mouse drag tracking
        self.last_drag_x = 0
        self.last_drag_y = 0

        # Current selection (object name and constellation if applicable)
        self.selected_object_name   = None
        self.selected_constellation = None

        # Generate and store background (random) stars
        self._background_area = BACKGROUND_AREA
        self.deep_sky_stars = generate_deep_sky(self._background_area, BACKGROUND_STAR_COUNT)

        # Create widgets and perform initial draw
        self.create_widgets()
        self.redraw()

    def create_widgets(self):
        # Canvas container (left side)
        canvas_frame = tk.Frame(self.root, bg="#05050C")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Main canvas where the sky is drawn
        self.canvas = tk.Canvas(canvas_frame, bg="#05050C", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Info panel (right side)
        self.info_frame = tk.Frame(self.root, bg="#111122", width=380, padx=20, pady=20)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_frame.pack_propagate(False)

        # App title
        tk.Label(self.info_frame, text="Stellaris", font=self.font_title, fg="white", bg="#111122").pack(anchor="w", pady=(0,10))

        # Introductory message (poetic + instructions)
        tk.Label(self.info_frame, text=("“Can you bind the chains of the Pleiades or loosen Orion’s belt?” — Job 38:31\n\n"
                                        "Use the scroll wheel to zoom and middle-click drag to pan.\n"
                                        "Discover planets, constellations, and hidden satellites."),
                 font=self.font_main, fg="#AAAAAA", bg="#111122", wraplength=340, justify="left").pack(anchor="w", pady=(0,20))

        # Container for astronomical data (fact + quote)
        data_container = tk.LabelFrame(self.info_frame, text="Astronomical Data", font=self.font_data_title, fg="#00CCFF",
                                       bg="#111122", bd=1, relief="solid", padx=10, pady=10)
        data_container.pack(fill=tk.BOTH, expand=True)

        # Label for the selected object's name
        self.object_name_label = tk.Label(data_container, text="No object selected", font=self.font_data_title, fg="#00CCFF", bg="#111122", anchor="w")
        self.object_name_label.pack(fill=tk.X, pady=(0,10))

        # Text area for the 'fact' (scientific information)
        self.fact_text = tk.Text(data_container, font=self.font_data_text, fg="white", bg="#111122", bd=0, wrap=tk.WORD, state=tk.DISABLED, height=8)
        self.fact_text.pack(fill=tk.BOTH, expand=False)

        # New: frame to visually separate the 'quote' from the 'fact'
        # Uses a LabelFrame with an inner Text for independent styling and control
        self.quote_frame = tk.LabelFrame(data_container, text="Quote", font=self.font_data_text, fg="#FFD580",
                                         bg="#111122", bd=0, relief="flat", padx=6, pady=6)
        self.quote_frame.pack(fill=tk.BOTH, expand=True, pady=(8,0))

        # Text area inside the quote frame (dark background for contrast)
        self.quote_text = tk.Text(self.quote_frame, font=self.font_data_text, fg="#FFEFD5", bg="#0F1016", bd=0, wrap=tk.WORD, state=tk.DISABLED, height=4)
        self.quote_text.pack(fill=tk.BOTH, expand=True)

        # Label to show cursor world coordinates (top-left)
        self.coord_label = tk.Label(self.root, text="", font=self.font_main, fg="#AAAAAA", bg="#05050C")
        self.coord_label.place(x=10, y=10)

        # Bindings: canvas events and keyboard shortcuts
        self.canvas.bind("<ButtonPress-1>",   self.on_click)        # left click -> selection
        self.canvas.bind("<ButtonPress-2>",   self.on_drag_start)  # middle click -> start drag
        self.canvas.bind("<B2-Motion>",       self.on_drag_move)   # drag with middle button
        self.canvas.bind("<MouseWheel>",      self.on_zoom)        # mouse wheel -> zoom
        self.canvas.bind("<Motion>",          self.on_mouse_move)  # mouse move -> update coords

        # Keyboard shortcuts for reset and center
        self.root.bind("r", lambda e: self.reset_view())
        self.root.bind("R", lambda e: self.reset_view())
        self.root.bind("c", lambda e: self.center_on_selected())
        self.root.bind("C", lambda e: self.center_on_selected())

    # Drawing helpers (uses rendering.draw_glow)
    def redraw(self):
        """Clear the canvas and redraw everything from scratch."""
        ensure_deep_sky_coverage(self, BACKGROUND_STAR_COUNT)  # ensure background has enough stars
        self.canvas.delete("all")
        self.draw_deep_sky()
        self.draw_deep_sky_objects()
        self.draw_satellites()
        self.draw_constellations()
        self.draw_planets()

    def draw_deep_sky(self):
        """Draw the randomly generated background stars."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        margin = 50
        for star in self.deep_sky_stars:
            sx, sy = self.world_to_screen(*star["coords"])
            if -margin < sx < w + margin and -margin < sy < h + margin:
                s = star["size"]
                self.canvas.create_oval(sx, sy, sx + s, sy + s, fill=star["color"], outline="")

    def draw_deep_sky_objects(self):
        """Draw deep-sky objects (galaxies, nebulae) with glow and label."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        margin = 100
        for name, data in ASTRONOMICAL_DATA.get("deep_sky", {}).items():
            sx, sy = self.world_to_screen(*data["coords"])
            if not (-margin < sx < w + margin and -margin < sy < h + margin):
                continue
            size = data["size"] * self.zoom
            brightness = data.get("brightness", min(1.0, data["size"] / 40))
            draw_glow(self.canvas, sx, sy, size, data["color"], brightness)
            half = size / 2
            self.canvas.create_oval(sx - half, sy - half, sx + half, sy + half, fill=data["color"], outline="#AAAAAA")
            self.canvas.create_text(sx + half + 8, sy, text=name, fill=data["color"], anchor="w", font=self.font_data_text)

    def draw_satellites(self):
        """Draw satellites (artificial objects). Highlight if selected."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        margin = 50
        for sat_name, sat_data in ASTRONOMICAL_DATA["satellites"].items():
            sx, sy = self.world_to_screen(*sat_data["coords"])
            if not (-margin < sx < w + margin and -margin < sy < h + margin):
                continue
            size   = sat_data["size"] * self.zoom
            brightness = sat_data.get("brightness", 0.5)
            draw_glow(self.canvas, sx, sy, size, sat_data["color"], brightness * 0.6)
            if sat_name == self.selected_object_name:
                # Highlight selected satellite with a larger circle
                r = size * 1.5
                self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill="#00FF88", outline="")
            half = size / 2
            self.canvas.create_oval(sx - half, sy - half, sx + half, sy + half, fill=sat_data["color"], outline="")

    def draw_constellations(self):
        """Draw constellation lines and their stars; show star names when the constellation is selected."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        margin = 80
        for const_name, const_data in ASTRONOMICAL_DATA["constellations"].items():
            is_selected = (const_name == self.selected_constellation)
            if is_selected:
                # Draw lines for the selected constellation
                for start_star, end_star in const_data["lines"]:
                    if start_star in const_data["stars"] and end_star in const_data["stars"]:
                        x1, y1 = self.world_to_screen(*const_data["stars"][start_star]["coords"])
                        x2, y2 = self.world_to_screen(*const_data["stars"][end_star]["coords"])
                        if (x1 < -margin and x2 < -margin) or (x1 > w + margin and x2 > w + margin):
                            continue
                        if (y1 < -margin and y2 < -margin) or (y1 > h + margin and y2 > h + margin):
                            continue
                        self.canvas.create_line(x1, y1, x2, y2, fill="#00CCFF", width=2, capstyle=tk.ROUND)
            # Draw each star in the constellation
            for star_name, star_data in const_data["stars"].items():
                sx, sy = self.world_to_screen(*star_data["coords"])
                if not (-margin < sx < w + margin and -margin < sy < h + margin):
                    continue
                size   = star_data["size"] * self.zoom
                brightness = star_data.get("brightness", min(1.0, star_data["size"] / 12))
                draw_glow(self.canvas, sx, sy, size, star_data["color"], brightness * 0.7)
                if star_name == self.selected_object_name:
                    # Highlight selected star
                    r = size * 1.5
                    self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill="#00CCFF", outline="")
                half = size / 2
                self.canvas.create_oval(sx - half, sy - half, sx + half, sy + half, fill=star_data["color"], outline="#AAAAAA")
                if is_selected:
                    # Show star name when the constellation is selected
                    self.canvas.create_text(sx + half + 5, sy, text=star_name, fill="white", anchor="w", font=self.font_data_text)

    def draw_planets(self):
        """Draw planets with glow and label; highlight if selected."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        margin = 100
        for planet_name, planet_data in ASTRONOMICAL_DATA["planets"].items():
            sx, sy = self.world_to_screen(*planet_data["coords"])
            if not (-margin < sx < w + margin and -margin < sy < h + margin):
                continue
            size   = planet_data["size"] * self.zoom
            brightness = planet_data.get("brightness", min(1.0, planet_data["size"] / 14))
            draw_glow(self.canvas, sx, sy, size, planet_data["color"], brightness)
            if planet_name == self.selected_object_name:
                # Highlight selected planet
                r = size * 1.5
                self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill="#CCFF00", outline="")
            half = size / 2
            self.canvas.create_oval(sx - half, sy - half, sx + half, sy + half, fill=planet_data["color"], outline="#AAAAAA")
            self.canvas.create_text(sx + half + 8, sy, text=planet_name, fill=planet_data["color"], anchor="w", font=self.font_data_text)

    # Coordinate helpers
    def world_to_screen(self, x, y):
        """Convert world coordinates to screen (canvas) coordinates."""
        cx = self.canvas.winfo_width()  / 2
        cy = self.canvas.winfo_height()  / 2
        sx = x * self.zoom + cx + self.offset_x
        sy = y * self.zoom + cy + self.offset_y
        return sx, sy

    def screen_to_world(self, sx, sy):
        """Convert screen (canvas) coordinates back to world coordinates (inverse)."""
        cx = self.canvas.winfo_width()  / 2
        cy = self.canvas.winfo_height()  / 2
        x  = (sx - cx - self.offset_x) / self.zoom
        y  = (sy - cy - self.offset_y) / self.zoom
        return x, y

    # Event handlers
    def on_click(self, event):
        """
        Handle user clicks. Detect collisions with planets, satellites,
        deep-sky objects and constellation stars. If an object is detected,
        call select_object passing the full dict so it can display fact and quote.
        """
        wx, wy = self.screen_to_world(event.x, event.y)
        # Planets
        for planet_name, planet_data in ASTRONOMICAL_DATA["planets"].items():
            px, py = planet_data["coords"]
            hit_r  = planet_data["size"] / self.zoom * CLICK_RADIUS_STAR
            if math.sqrt((wx - px) ** 2 + (wy - py) ** 2) < hit_r:
                # Pass the full dict so select_object can read 'fact' and 'quote'
                self.select_object(planet_name, None, planet_data, "#CCFF00")
                return
        # Satellites
        for sat_name, sat_data in ASTRONOMICAL_DATA["satellites"].items():
            sx, sy = sat_data["coords"]
            hit_r  = sat_data["size"] / self.zoom * CLICK_RADIUS_SATELLITE
            if math.sqrt((wx - sx) ** 2 + (wy - sy) ** 2) < hit_r:
                self.select_object(sat_name, None, sat_data, "#00FF88")
                return
        # Deep sky objects
        for ds_name, ds_data in ASTRONOMICAL_DATA.get("deep_sky", {}).items():
            dx, dy = ds_data["coords"]
            hit_r  = ds_data["size"] / self.zoom * CLICK_RADIUS_STAR
            if math.sqrt((wx - dx) ** 2 + (wy - dy) ** 2) < hit_r:
                self.select_object(ds_name, None, ds_data, "#FFFFFF")
                return
        # Constellation stars
        for const_name, const_data in ASTRONOMICAL_DATA["constellations"].items():
            for star_name, star_data in const_data["stars"].items():
                sx, sy = star_data["coords"]
                hit_r  = star_data["size"] / self.zoom * CLICK_RADIUS_STAR
                if math.sqrt((wx - sx) ** 2 + (wy - sy) ** 2) < hit_r:
                    self.select_object(star_name, const_name, star_data, "#00CCFF")
                    return
        # Nothing hit -> clear selection
        self.select_object(None, None, {"fact": "No object selected"}, "#00CCFF")

    def select_object(self, object_name, constellation_name, data, highlight_color):
        """
        Display information for the selected object.
        - object_name: name of the object (or None)
        - constellation_name: constellation name if applicable (or None)
        - data: dict containing at least 'fact' and optionally 'quote'
        - highlight_color: color used to highlight the title
        """
        self.selected_object_name   = object_name
        self.selected_constellation = constellation_name

        # Build the title shown in the UI
        if constellation_name and object_name:
            title = f"{constellation_name} > {object_name}"
        elif object_name:
            title = object_name
        else:
            title = "No object selected"

        self.object_name_label.config(text=title, fg=highlight_color)

        # Normalize data: accept legacy string or dict
        if isinstance(data, str):
            data_dict = {"fact": data}
        else:
            data_dict = data or {}

        fact = data_dict.get("fact", "")
        quote = data_dict.get("quote", None)

        # Update the fact text widget (scientific information)
        self.fact_text.config(state=tk.NORMAL)
        self.fact_text.delete("1.0", tk.END)
        if fact:
            self.fact_text.insert(tk.END, fact)
        self.fact_text.config(state=tk.DISABLED)

        # Update the quote text widget (separate box)
        self.quote_text.config(state=tk.NORMAL)
        self.quote_text.delete("1.0", tk.END)
        if quote:
            self.quote_text.insert(tk.END, quote)
        self.quote_text.config(state=tk.DISABLED)

        # Redraw to update highlights on the canvas
        self.redraw()

    def on_drag_start(self, event):
        # Save initial drag position
        self.last_drag_x = event.x
        self.last_drag_y = event.y

    def on_drag_move(self, event):
        # Compute displacement and update view offsets
        dx = event.x - self.last_drag_x
        dy = event.y - self.last_drag_y
        self.offset_x += dx
        self.offset_y += dy
        self.last_drag_x = event.x
        self.last_drag_y = event.y
        self.redraw()

    def on_zoom(self, event):
        """
        Handle zoom centered on the cursor position.
        Adjusts self.zoom and compensates offsets to keep the point under the cursor fixed.
        """
        zoom_factor = ZOOM_STEP if event.delta > 0 else 1 / ZOOM_STEP
        wx_before, wy_before = self.screen_to_world(event.x, event.y)
        self.zoom = max(ZOOM_MIN, min(self.zoom * zoom_factor, ZOOM_MAX))
        wx_after, wy_after = self.screen_to_world(event.x, event.y)
        # Compensate offset so the point under the cursor remains visually fixed
        self.offset_x += (wx_before - wx_after) * self.zoom
        self.offset_y += (wy_before - wy_after) * self.zoom

        # Redraw and then ensure background and selection visibility
        self.redraw()
        ensure_deep_sky_coverage(self, BACKGROUND_STAR_COUNT)
        self.ensure_selected_visible(margin=80)

    def on_mouse_move(self, event):
        # Show world coordinates under the cursor
        wx, wy = self.screen_to_world(event.x, event.y)
        self.coord_label.config(text=f"World: x={int(wx)}, y={int(wy)}")

    # Utilities
    def reset_view(self):
        """Reset zoom and offsets to initial values."""
        self.zoom = ZOOM_INITIAL
        self.offset_x = 0
        self.offset_y = 0
        self.redraw()

    def center_on_selected(self):
        """Center the view on the selected object (if any)."""
        name = self.selected_object_name
        if not name:
            return
        if name in ASTRONOMICAL_DATA["planets"]:
            x, y = ASTRONOMICAL_DATA["planets"][name]["coords"]
        elif name in ASTRONOMICAL_DATA["satellites"]:
            x, y = ASTRONOMICAL_DATA["satellites"][name]["coords"]
        elif name in ASTRONOMICAL_DATA.get("deep_sky", {}):
            x, y = ASTRONOMICAL_DATA["deep_sky"][name]["coords"]
        else:
            found = False
            for const_name, const_data in ASTRONOMICAL_DATA["constellations"].items():
                if name in const_data["stars"]:
                    x, y = const_data["stars"][name]["coords"]
                    found = True
                    break
            if not found:
                return
        cx = self.canvas.winfo_width() / 2
        cy = self.canvas.winfo_height() / 2
        self.offset_x = cx - x * self.zoom
        self.offset_y = cy - y * self.zoom
        self.redraw()

    def ensure_selected_visible(self, margin=80):
        """
        Ensure the selected object is within visible margins.
        If it's outside, adjust offsets to bring it into view.
        """
        name = self.selected_object_name
        if not name:
            return
        found = False
        if name in ASTRONOMICAL_DATA.get("planets", {}):
            wx, wy = ASTRONOMICAL_DATA["planets"][name]["coords"]
            found = True
        elif name in ASTRONOMICAL_DATA.get("satellites", {}):
            wx, wy = ASTRONOMICAL_DATA["satellites"][name]["coords"]
            found = True
        elif name in ASTRONOMICAL_DATA.get("deep_sky", {}):
            wx, wy = ASTRONOMICAL_DATA["deep_sky"][name]["coords"]
            found = True
        else:
            for const_name, const_data in ASTRONOMICAL_DATA.get("constellations", {}).items():
                if name in const_data["stars"]:
                    wx, wy = const_data["stars"][name]["coords"]
                    found = True
                    break
        if not found:
            return
        sx, sy = self.world_to_screen(wx, wy)
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        dx = 0
        dy = 0
        if sx < margin:
            dx = margin - sx
        elif sx > w - margin:
            dx = (w - margin) - sx
        if sy < margin:
            dy = margin - sy
        elif sy > h - margin:
            dy = (h - margin) - sy
        if dx != 0 or dy != 0:
            self.offset_x += dx
            self.offset_y += dy
            self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    app  = SkyViewerApp(root)
    root.mainloop()





