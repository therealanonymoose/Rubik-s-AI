# Converts a PyCuber cube into a 6x3x3 int array
import pycuber as pc
import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load color mapping from JSON
with open(os.path.join(BASE_DIR, "ref", "color_mapping.json"), "r") as f:
    COLOR_IDS = json.load(f)

def orient_cube(cube: pc.Cube) -> pc.Cube:
    # Reorient the cube to the yellow top and green front
    oriented = cube.copy()

    yellow_pos = next(f for f in "URFDLB" if str(oriented.get_face(f)[1][1]).strip("[]") == "y")
    rot_up = {
        "U": "",   "D": "x2",
        "F": "x'", "B": "x",
        "L": "z",  "R": "z'"
    }[yellow_pos]
    oriented(rot_up)

    green_pos = next(f for f in "URFDLB" if str(oriented.get_face(f)[1][1]).strip("[]") == "g")
    rot_front = {
        "F": "",  "R": "y", 
        "B": "y2",  "L": "y'"
    }[green_pos]
    oriented(rot_front)

    return oriented

def encode_cube_array(cube: pc.Cube) -> list[list[list[int]]]:
    #Encode PyCuber cube state into 6x3x3 int array
    cube = orient_cube(cube)
    state = []
    for face_name in ["U", "R", "F", "D", "L", "B"]:
        face = cube.get_face(face_name)
        face_array = [[], [], []]
        for row in range(3):
            for col in range(3):
                sticker = str(face[row][col]).strip("[]")
                # Convert sticker color letter to int
                face_array[row].append(COLOR_IDS[sticker])
        state.append(face_array)
    return state

def encode_cube_vector(cube: pc.Cube) -> list[int]:
    #Encode PyCuber cube state into 324 element array representation of a one hot vector
    cube = orient_cube(cube)
    state = []
    for face_name in ["U", "R", "F", "D", "L", "B"]:
        face = cube.get_face(face_name)
        for row in range(3):
            for col in range(3):
                sticker: str = str(face[row][col]).strip("[]")
                # Convert sticker color letter to one hot vector
                one_hot = [0] * 6
                one_hot[COLOR_IDS[sticker]] = 1
                state.extend(one_hot)
    return state

if __name__ == "__main__":
    cube = pc.Cube()
    print(encode_cube_vector(cube))
    print(encode_cube_array(cube))