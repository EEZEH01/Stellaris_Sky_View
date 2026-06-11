# Stellaris - Sky Viewer Pro

Stellaris - Sky Viewer Pro is an interactive, graphical astronomical exploration tool developed as a final project for Stanford University's Code in Place program. This application utilizes Python's tkinter library to create a dynamic, zoomable, and pannable star map, allowing users to investigate constellations, planets, and artificial satellites.

## How to run
- Ensure you have Python installed on your system.
- Copy the code into a file named stellaris.py.
- Run the application via terminal or command prompt:

                python sky_viewer.py

- Files required in the same folder: sky_viewer.py, astronomical_data.py, rendering.py, background.py

## Controls
- Left-click drag  : pan the sky
- Mouse wheel      : zoom in / out
- Click any object : see its astronomical data
- Search bar       : jump to any named star, planet, or satellite

## Included elements

Constellations  
Orion; Ursa Major; Scorpius; Leo; Cassiopeia; Gemini; Cruz del Sur

Stars (by name, within constellations)  
Betelgeuse; Rigel; Bellatrix; Alnilam; Alnitak; Mintaka;
Dubhe; Merak; Phecda; Megrez; Alioth; Mizar; Alkaid;
Antares; Graffias; Dschubba; Shaula; Sargas;
Regulus; Denebola; Algieba;
Schedar; Caph; Ruchbah;
Castor; Pollux;
Acrux; Becrux; Gacrux

Planets  
Jupiter; Mars; Saturn; Venus; Mercury; Uranus; Neptune

Satellites (artificial)  
International Space Station (ISS); Hubble Space Telescope; Starlink Satellite

Deep-sky objects  
Andromeda Galaxy (M31); Orion Nebula (M42); Pleiades (M45)


## Notes
- Labels and detailed info appear when selecting objects.
- To add or adjust objects, modify astronomical_data.py and restart the app.

Thanks CiP Team!!