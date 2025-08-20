# Converts a PyCuber cube into a 6x3x3 int array
import pycuber as pc
import json

# Load color mapping from JSON
with open("ref/color_mapping.json", "r") as f:
    COLOR_IDS = json.load(f)

def encode_cube(cube: pc.Cube) -> list:
    #Encode PyCuber cube state into 6x3x3 int array
    state = []
    for face_name in ["U", "R", "F", "D", "L", "B"]:
        face = cube.get_face(face_name)
        face_array = [[],[],[]]
        for row in range(3):
            for col in range(3):
                sticker = face[row][col]
                # Convert sticker color letter to int
                face_array[row].append(COLOR_IDS[str(sticker).strip("[]")])
        state.append(face_array)
    return state
