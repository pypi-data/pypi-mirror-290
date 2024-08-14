from ..globs import glm
from ..resource.zvxchunk import zvxchunk

class zvxterraingen:
    def __init__(self, noise_function, scale=0.01, height_scale=64):
        self.scale=scale
        self.height_scale=height_scale
        self.noise_function=noise_function

    def generate(self, chunk_id: int, chunks:list) -> None:
        """ Generate terrain using the provided noise function """
        if chunk_id <= chunks.max and chunk_id != -1:
            localx, localy, localz = chunks.location[chunk_id]
            for x in range(chunks.size[chunk_id]):
                for z in range(chunks.size[chunk_id]):
                    relx = x + localx
                    relz = z + localz
                    noise_value = self.noise_function(glm.vec2(relx, relz) * self.scale)
                    relheight = int(noise_value * self.height_scale)
                    localheight = min(relheight - localy, chunks.size[chunk_id])
                    for y in range(int(localheight)):
                        rely = y + localy
                        chunks.voxels[chunk_id][x + chunks.size[chunk_id] * z + chunks.area[chunk_id] * y] = rely + 1


""" TERRAIN GENERATION ALGORITHMS """
def simplexGL(vec:glm.vec2) -> glm.vec2: return glm.simplex(vec)
    
