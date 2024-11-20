# Ausschneiden einzelner Zähne aus Mesh, grob aus Jeanines Code zusammengetragen und etwas angepasst

import numpy as np
from stl import mesh
import math
import os

# Globale Parameter (um Anpassbarkeit zu gewährleisten)
total_teeth = 19  # Anzahl der Zähne
inner_radius = 10  # Innenradius der Zähne (hier nur Bsp.)
outer_radius = 15  # Außenradius der Zähne (ebenfalls nur Bsp.)
output_folder = "extracted_teeth"  # Ordnername für die Ausgabe

# Schritt 1: STL-Datei einlesen
input_file = '/mnt/data/CrownGearHigh.stl'  # Eingabedatei (.stl)
gear_mesh = mesh.Mesh.from_file(input_file) # Nur testweise

# !NUR WENN MITTELPUNKT NICHT VORGEGEBEN! SONST: center = np.array([x_mittelpunkt, y_mittelpunkt, z_mittelpunkt]) ->evtl. [0,0,0]
# Schritt 2: Mittelpunkt des Zahnrads berechnen
# Zentrum des Zahnrades ist Mittelwert aller Punkte ist.
vertices = gear_mesh.vectors.reshape(-1, 3)  # Alle Eckpunkte der Dreiecke
center = np.mean(vertices, axis=0)  # Mittelpunkt des Zahnrades

# Schritt 3: Winkel für jeden Zahn berechnen
# Kreis in gleichmäßige Winkelbereiche unterteilen
angles = np.linspace(0, 2 * np.pi, total_teeth + 1)[:-1]  # angles ist Feld mit bspw. angles[1]= Startwinkel Zahn 1


# Schritt 4: Funktion zum Extrahieren eines Zahnes !Hier ggf. lokale Variablen einführen, um Verwirrung zu vermeiden!
def extract_tooth(mesh_data, tooth_idx, total_teeth, center, angles, inner_radius, outer_radius):
    """
    Extrahiert die Dreiecke, die innerhalb des Zahnbereichs (Winkel) und des Radiusbereichs liegen.
    """
    start_angle = angles[tooth_idx]
    end_angle = angles[(tooth_idx + 1) % total_teeth]

    # Liste für die neuen Dreiecke des Zahnes
    new_triangles = []

    for triangle in mesh_data.vectors:
        # Mittelpunkt des Dreiecks berechnen
        triangle_center = np.mean(triangle, axis=0)
        vector = triangle_center - center  # Vektor vom Zentrum zum Dreiecksmittelpunkt

        # Berechnung des Radius und Winkels
        radius = np.linalg.norm(vector[:2])  # Abstand vom Zentrum (nur XY-Ebene)
        angle = math.atan2(vector[1], vector[0])  # Winkel im Bogenmaß

        # Korrigieren des Winkels in den Bereich [0, 2π]
        if angle < 0:
            angle += 2 * np.pi

        # Prüfen, ob das Dreieck im Zahnwinkelbereich und zwischen Innen- und Außenradius liegt
        if start_angle <= angle < end_angle and inner_radius <= radius <= outer_radius:
            new_triangles.append(triangle)

    # Neues Mesh erstellen
    new_mesh = mesh.Mesh(np.zeros(len(new_triangles), dtype=mesh.Mesh.dtype))
    for i, triangle in enumerate(new_triangles):
        new_mesh.vectors[i] = triangle

    return new_mesh


# Schritt 5: Ordner für die Ausgabe erstellen
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Schritt 6: Jeden Zahn extrahieren und speichern
for i in range(total_teeth):
    tooth_mesh = extract_tooth(gear_mesh, i, total_teeth, center, angles, inner_radius, outer_radius)
    output_file = os.path.join(output_folder, f"tooth_{i + 1}.stl")
    tooth_mesh.save(output_file)
    print(f"Zahn {i + 1} gespeichert in {output_file}")

print("Test. Syntax des Schneideabschnitt stimmt")
