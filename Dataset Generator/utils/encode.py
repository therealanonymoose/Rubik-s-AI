# Converts a PyCuber cube into a 6x3x3 int array
import pycuber as pc
import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load color mapping from JSON
with open(os.path.join(BASE_DIR, "ref", "color_mapping.json"), "r") as f:
    COLOR_IDS: dict[str, int] = json.load(f)

def encode_cube(cube: pc.Cube) -> list[list[list[int]]]:
    #Encode PyCuber cube state into 6x3x3 int array
    state: list[list[list[int]]] = []
    for face_name in ["U", "D", "F", "B", "L", "R"]:
        face: pc.Face = cube.get_face(face_name)
        face_array: list[list[int]] = [[], [], []]
        for row in range(3):
            for col in range(3):
                sticker: str = str(face[row][col]).strip("[]")
                # Convert sticker color letter to int
                face_array[row].append(COLOR_IDS[sticker])
        state.append(face_array)
    return state
