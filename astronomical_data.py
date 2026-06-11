# astronomical_data.py
# Extracted astronomical data for Stellaris - Sky Viewer Pro
# Contains constellations, planets, satellites and deep-sky objects.
# Each object may include: coords (x,y), size (visual base), color (hex), brightness (0.0-1.0), fact (string)

ASTRONOMICAL_DATA = {
    "constellations": {
        "Orion": {
            "stars": {
                "Betelgeuse": {"coords": (-1200, -800), "size": 10, "color": "#FF7A33", "brightness": 0.95,
                               "fact": "Red supergiant — one of the largest stars visible to the naked eye."},
                "Rigel": {"coords": (-1000, -420), "size": 10, "color": "#AEEFFF", "brightness": 0.95,
                          "fact": "Blue supergiant and the brightest star system in Orion."},
                "Bellatrix": {"coords": (-1250, -460), "size": 8, "color": "#DDEEFF", "brightness": 0.6,
                              "fact": "Known as the 'Amazon Star'. Marks Orion's left shoulder."},
                "Alnilam": {"coords": (-1100, -600), "size": 6, "color": "#FFFFFF", "brightness": 0.55,
                            "fact": "The central star of Orion's Belt. A blue supergiant ~2,000 light-years away."},
                "Alnitak": {"coords": (-1050, -580), "size": 6, "color": "#F0F8FF", "brightness": 0.5,
                           "fact": "Eastern star of Orion's Belt. A triple-star system."},
                "Mintaka": {"coords": (-1150, -620), "size": 6, "color": "#F8FBFF", "brightness": 0.5,
                            "fact": "Western star of Orion's Belt. Lies almost exactly on the celestial equator."},
            },
            "lines": [
                ("Betelgeuse", "Bellatrix"),
                ("Bellatrix",  "Rigel"),
                ("Rigel",      "Alnitak"),
                ("Alnitak",    "Mintaka"),
                ("Betelgeuse", "Mintaka"),
            ],
            "fact": "The giant hunter. One of the most recognizable constellations in the winter sky.",
        },

        "Ursa Major or Big Dipper": {
            "stars": {
                "Dubhe": {"coords": (1500, 1200), "size": 8, "color": "#FFF6CC", "brightness": 0.65,
                          "fact": "Outermost pointer star used to locate Polaris and true north."},
                "Merak": {"coords": (1550, 1350), "size": 8, "color": "#FFF6CC", "brightness": 0.6,
                         "fact": "A line through Merak and Dubhe leads directly to Polaris."},
                "Phecda": {"coords": (1700, 1300), "size": 6, "color": "#FFFFFF", "brightness": 0.45,
                           "fact": "Forms the base of the Big Dipper's bowl."},
                "Megrez": {"coords": (1750, 1150), "size": 6, "color": "#F7FBFF", "brightness": 0.4,
                          "fact": "Faintest of the seven main stars. Connects bowl to handle."},
                "Alioth": {"coords": (1900, 1050), "size": 6, "color": "#F7FBFF", "brightness": 0.5,
                          "fact": "Brightest star in Ursa Major. First star of the handle."},
                "Mizar": {"coords": (2050, 950), "size": 6, "color": "#F7FBFF", "brightness": 0.5,
                          "fact": "A quadruple star system. Splitting it from Alcor was a classic eyesight test."},
                "Alkaid": {"coords": (2200, 850), "size": 6, "color": "#F7FBFF", "brightness": 0.45,
                          "fact": "The tip of the Big Dipper's handle."},
            },
            "lines": [
                ("Dubhe",  "Merak"),
                ("Merak",  "Phecda"),
                ("Phecda", "Megrez"),
                ("Megrez", "Dubhe"),
                ("Megrez", "Alioth"),
                ("Alioth", "Mizar"),
                ("Mizar",  "Alkaid"),
            ],
            "fact": "One of the most recognizable asterisms in the northern hemisphere.",
        },

        "Scorpius": {
            "stars": {
                "Antares": {"coords": (3000, -2000), "size": 11, "color": "#FF3E1A", "brightness": 0.98,
                            "fact": "The heart of the scorpion. A red supergiant often confused with Mars."},
                "Graffias": {"coords": (2800, -2200), "size": 7, "color": "#FFFFFF", "brightness": 0.45,
                             "fact": "A multiple star system forming the scorpion's claws."},
                "Dschubba": {"coords": (2900, -2100), "size": 7, "color": "#FFFFFF", "brightness": 0.45,
                             "fact": "Marks the crown of the scorpion."},
                "Shaula": {"coords": (3300, -1600), "size": 8, "color": "#AEEFFF", "brightness": 0.7,
                           "fact": "The scorpion's stinger. One of the brightest stars in the night sky."},
                "Sargas": {"coords": (3200, -1750), "size": 7, "color": "#FFF6CC", "brightness": 0.55,
                          "fact": "Located in the lower curve of the scorpion's tail."},
            },
            "lines": [
                ("Graffias", "Dschubba"),
                ("Dschubba", "Antares"),
                ("Antares",  "Sargas"),
                ("Sargas",   "Shaula"),
            ],
            "fact": "A bright zodiacal constellation best seen from the southern hemisphere in summer.",
        },

        # New constellations with adjusted positions and sizes
        "Leo": {
            "stars": {
                "Regulus": {"coords": (520, 1580), "size": 9, "color": "#FFF8D6", "brightness": 0.8,
                            "fact": "Bright star at Leo's heart."},
                "Denebola": {"coords": (760, 1480), "size": 7, "color": "#F6F9FF", "brightness": 0.55,
                             "fact": "Tail of the lion."},
                "Algieba": {"coords": (640, 1450), "size": 7, "color": "#FFF6E0", "brightness": 0.5,
                            "fact": "A binary star in Leo."},
            },
            "lines": [("Regulus", "Algieba"), ("Algieba", "Denebola")],
            "fact": "Leo, the lion; a prominent zodiacal constellation.",
        },

        "Cassiopeia": {
            "stars": {
                "Schedar": {"coords": (-1980, 1780), "size": 8, "color": "#FFDDBB", "brightness": 0.7,
                           "fact": "One of the brightest in Cassiopeia."},
                "Caph": {"coords": (-1830, 1700), "size": 6, "color": "#FFFFFF", "brightness": 0.45,
                         "fact": "Part of the W asterism."},
                "Ruchbah": {"coords": (-1680, 1780), "size": 6, "color": "#F7FBFF", "brightness": 0.45,
                            "fact": "Another W point."},
            },
            "lines": [("Schedar", "Caph"), ("Caph", "Ruchbah")],
            "fact": "Cassiopeia forms a distinctive W shape in the northern sky.",
        },

        "Gemini": {
            "stars": {
                "Castor": {"coords": (320, 420), "size": 7, "color": "#DFF7FF", "brightness": 0.6,
                          "fact": "One of the twin stars."},
                "Pollux": {"coords": (480, 360), "size": 9, "color": "#FFF6CC", "brightness": 0.8,
                          "fact": "The brighter twin."},
            },
            "lines": [("Castor", "Pollux")],
            "fact": "Gemini, the twins; easy to spot near Orion in winter.",
        },

        "Cruz del Sur": {
            "stars": {
                "Acrux": {"coords": (-3450, 2180), "size": 9, "color": "#FFF6CC", "brightness": 0.9,
                         "fact": "Brightest star of the Southern Cross."},
                "Becrux": {"coords": (-3350, 2100), "size": 7, "color": "#FFFFFF", "brightness": 0.6,
                          "fact": "Part of the cross."},
                "Gacrux": {"coords": (-3250, 2180), "size": 7, "color": "#FFFFFF", "brightness": 0.55,
                          "fact": "Top of the cross."},
            },
            "lines": [("Acrux", "Becrux"), ("Becrux", "Gacrux")],
            "fact": "La Cruz del Sur, visible desde latitudes del sur.",
        },
    },

    "planets": {
        "Jupiter": {"coords": (-2500, 1500), "size": 14, "color": "#FFD24D", "brightness": 0.98,
                    "fact": "The solar system's largest planet. Acts as a gravitational shield for the inner planets."},
        "Mars": {"coords": (820, -1180), "size": 9, "color": "#FF4C1A", "brightness": 0.85,
                 "fact": "Home to Olympus Mons, the tallest volcano in the solar system.",
                 "quote": "Ray Bradbury — 'Mars is heaven.'"},
        "Saturn": {"coords": (4020, 2980), "size": 12, "color": "#EEDDAA", "brightness": 0.9,
                   "fact": "Famous for its ring system made of ice and rock.",
                   "quote": "Galileo Galilei — 'Saturn has ears.'"},
        "Venus": {"coords": (1250, 920), "size": 11, "color": "#FFF7D9", "brightness": 0.95,
                  "fact": "Second planet; dense atmosphere and extreme greenhouse effect."},
        "Mercury": {"coords": (980, 820), "size": 6, "color": "#CFCFCF", "brightness": 0.6,
                    "fact": "Closest planet to the Sun; small and heavily cratered."},
        "Uranus": {"coords": (4180, -980), "size": 10, "color": "#CFEFFF", "brightness": 0.55,
                  "fact": "Ice giant with a pronounced axial tilt."},
        "Neptune": {"coords": (4420, -1180), "size": 10, "color": "#2F66FF", "brightness": 0.55,
                    "fact": "Farthest classical planet; deep blue due to methane in its atmosphere."},
    },

    "satellites": {
        "International Space Station (ISS)": {"coords": (-500, 300), "size": 5, "color": "#FFFFFF", "brightness": 0.95,
                                              "fact": "[ARTIFICIAL OBJECT] The largest human structure in space, orbiting at ~400 km altitude.",
                                              "quote": "Chris Hadfield — 'The more you look out, the more you realize how small we are.'"},
        "Hubble Space Telescope": {"coords": (2500, 500), "size": 4, "color": "#FFFFFF", "brightness": 0.75,
                                   "fact": "[ARTIFICIAL OBJECT] Launched in 1990. Has contributed to over 1.5 million scientific observations.",
                                   "quote": "Edwin Hubble — 'Equipped with his five senses, man explores the universe around him and calls the adventure Science.'"},
        "Starlink Satellite": {"coords": (100, -800), "size": 4, "color": "#FFFFFF", "brightness": 0.6,
                               "fact": "[ARTIFICIAL OBJECT] Part of SpaceX's megaconstellation providing global broadband internet.",
                               "quote": "Elon Musk — 'When something is important enough, you do it even if the odds are not in your favor.'"},
    },

    "deep_sky": {
        "Andromeda Galaxy (M31)": {"coords": (3520, -520), "size": 48, "color": "#E6E9FF", "brightness": 0.65,
                                   "fact": "Andromeda (M31): spiral galaxy ~2.5 million light-years away.",
                                   "quote": "Edwin Hubble — 'Equipped with his five senses, man explores the universe around him and calls the adventure Science.'"},
        "Orion Nebula (M42)": {"coords": (-1125, -655), "size": 22, "color": "#8FB8FF", "brightness": 0.78,
                               "fact": "Orion Nebula: a bright emission nebula and stellar nursery."},
        "Pleiades (M45)": {"coords": (-1310, -710), "size": 16, "color": "#FFFFFF", "brightness": 0.6,
                           "fact": "Pleiades: an open star cluster also known as the Seven Sisters.",
                           "quote": "Alfred Lord Tennyson — 'Many a night I saw the Pleiads, rising thro’ the mellow shade.'"},
        "Centaurus A": {"coords": (-3200, 2000), "size": 20, "color": "#FFD700", "brightness": 0.6,
                        "fact": "Centaurus A: a nearby elliptical galaxy with a prominent dust lane."},
        "Sombrero Galaxy (M104)": {"coords": (4200, 300), "size": 18, "color": "#E6E9FF", "brightness": 0.55,
                                   "fact": "Sombrero Galaxy (M104): a spiral galaxy with a bright nucleus and large central bulge."},
        "Whirlpool Galaxy (M51)": {"coords": (1200, 2000), "size": 24, "color": "#E6E9FF", "brightness": 0.6,
                                   "fact": "Whirlpool Galaxy (M51): a classic spiral galaxy interacting with a smaller companion."},
        # Ancient star Methuselah (HD 140283)
        "HD 140283": {"coords": (250, 1850), "size": 7, "color": "#FFF9E6", "brightness": 0.7,
                                        "fact": "Extremely old subgiant star (~14 billion years). Known as 'Methuselah Star'.",
                                        "quote": "Stephen Hawking — 'To confine our attention to terrestrial matters would be to limit the human spirit.'"},
    },}

