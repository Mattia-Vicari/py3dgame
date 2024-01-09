
class Body:
    def __init__(self, vertices, faces) -> None:
        self.v = vertices
        self.f = faces

    @classmethod
    def from_obj(cls, obj_file) -> 'Body':
        vertices = ...
        faces = ...

        return cls(vertices, faces)