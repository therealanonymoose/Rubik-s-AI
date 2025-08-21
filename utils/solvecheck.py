# Method to check if a cube is solved

import pycuber as pc

def is_solved(cube: pc.Cube) -> bool:
    # Returns true if a cube is solved, regardless of orientation
    for face_name in ["U", "R", "F", "D", "L", "B"]:
        face = cube.get_face(face_name)
        center_color = str(face[1][1])
        for row in range(3):
            for col in range(3):
                if str(face[row][col]) != center_color:
                    return False
    return True

def check_solution(scramble: pc.Formula, solution: pc.Formula) -> bool:
    # Returns True if applying scramble and solution solves the cube in standard orientation

    cube = pc.Cube()
    cube(scramble)
    cube(solution)
    return cube == pc.Cube()