# Method to check if a cube is solved

import pycuber as pc

def is_solved(cube: pc.Cube) -> bool:
    # Returns True if a cube is solved, regardless of orientation
    for face_name in ["U", "D", "F", "B", "L", "R"]:
        face: pc.Face = cube.get_face(face_name)
        center_color: str = str(face[1][1])
        for row in range(3):
            for col in range(3):
                if str(face[row][col]) != center_color:
                    return False
    return True

def is_valid_solution(scramble: pc.Formula, solution: pc.Formula) -> bool:
    # Returns True if applying scramble and solution solves the cube in standard orientation
    cube = pc.Cube()
    cube(scramble)
    cube(solution)
    return is_solved(cube)
