import moderngl as GL
from . import zenbank, zenresource
from zenlite.core.globs import pg, np, glm
from zenlite.core.zenvx.zvxchunk import build_zvxmesh

class zvxchunk(zenresource):
    def __init__(self, id:int) -> None:
        super().__init__(id=id)
        self.voxels=None
        self.size:int=None
        self.area:int=None
        self.hsize:int=None
        self.volume:int=None
        self.nvoxels:int=None
        self.mesh_id:int=None
        self.vxsize:float=None
        self.location:list[float]=None

class zvxchunkbed(zenresource):
    def __init__(self, id:int) -> None:
        super().__init__(id=id)
        self.nvoxels:int=None
        self.nchunks:int=None
        self.area:float=None
        self.volume:float=None
        self.centery:float=None
        self.centerxz:float=None
        self.chunksize:float=None
        self.dimensions:glm.vec3=None
        self.chunk_ids:list[int]=None

ZVX_CHUNK_MAX:int=10_000
class zvxchunkbank(zenbank):
    class chunks:
        size:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        area:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        hsize:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        volume:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        nvoxels:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        mesh_id:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        vxsize:list[float]=[float for _ in range(ZVX_CHUNK_MAX)]
        voxels:list[np.ndarray]=[list for _ in range(ZVX_CHUNK_MAX)]
        location:list[list[float]]=[list for _ in range(ZVX_CHUNK_MAX)]

    class chunkbeds:
        area:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        centery:float=[float for _ in range(ZVX_CHUNK_MAX)]
        nvoxels:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        nchunks:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        volume:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        centerxz:float=[float for _ in range(ZVX_CHUNK_MAX)]
        chunksize:list[int]=[int for _ in range(ZVX_CHUNK_MAX)]
        vxsize:list[float]=[float for _ in range(ZVX_CHUNK_MAX)]
        chunk_ids:list[list[int]]=[list for _ in range(ZVX_CHUNK_MAX)]
        dimensions:list[glm.vec3]=[glm.vec3 for _ in range(ZVX_CHUNK_MAX)]

    def __init__(self, zenresources, *args, **kwargs):
        super().__init__(max=ZVX_CHUNK_MAX, *args, **kwargs)
        self.bedcount:int=0
        self.zenresources=zenresources

    def get_chunk(self, chunk_id:int) -> zvxchunk|zenresource|None:
        if chunk_id <= self.max and chunk_id != -1:
            c:zvxchunk=zvxchunk(chunk_id)
            c.size=self.chunks.size[chunk_id]
            c.area=self.chunks.area[chunk_id]
            c.hsize=self.chunks.hsize[chunk_id]
            c.vxsize=self.chunks.vxsize[chunk_id]
            c.voxels=self.chunks.voxels[chunk_id]
            c.volume=self.chunks.volume[chunk_id]
            c.nvoxels=self.chunks.nvoxels[chunk_id]
            c.mesh_id=self.chunks.mesh_id[chunk_id]
            return c
        else: return None
    
    def get_chunkbed(self, cbed_id:int) -> zvxchunkbed|zenresource|None:
        if cbed_id <= self.bedcount and cbed_id != -1:
            cbed:zvxchunkbed=zvxchunkbed(cbed_id)
            cbed.area=self.chunkbeds.area[cbed_id]
            cbed.vxsize=self.chunkbeds.vxsize[cbed_id]
            cbed.volume=self.chunkbeds.volume[cbed_id]
            cbed.nvoxels=self.chunkbeds.nvoxels[cbed_id]
            cbed.nchunks=self.chunkbeds.nchunks[cbed_id]
            cbed.centery=self.chunkbeds.centery[cbed_id]
            cbed.centerxz=self.chunkbeds.centerxz[cbed_id]
            cbed.chunk_ids=self.chunkbeds.chunk_ids[cbed_id]
            cbed.chunksize=self.chunkbeds.chunksize[cbed_id]
            cbed.dimensions=self.chunkbeds.dimensions[cbed_id]
            return cbed
        else: return None

    def make_chunkbed(self, w:int, h:int, d:int, chunksize:int=32, vxsize:float=1.0) -> int:
        cbarea:float=w*d
        cbvolume:float=cbarea*h
        if self.count+cbvolume <= self.max:
            cbed_id = self.bedcount
            self.chunkbeds.nvoxels[cbed_id]=0
            self.chunkbeds.area[cbed_id]=cbarea
            self.chunkbeds.chunk_ids[cbed_id]=[]
            self.chunkbeds.vxsize[cbed_id]=vxsize
            self.chunkbeds.volume[cbed_id]=cbvolume
            self.chunkbeds.nchunks[cbed_id]=cbvolume
            self.chunkbeds.chunksize[cbed_id]=chunksize
            self.chunkbeds.dimensions[cbed_id]=glm.vec3(w, h, d)
            self.chunkbeds.centery[cbed_id]=h*chunksize
            self.chunkbeds.centerxz[cbed_id]=w*chunksize
            
            self.bedcount+=1; self.chunkify(cbed_id); return cbed_id
    
    def rebuild_chunkbed(self, tgen_id:int, cbed_id:int) -> int:
        if cbed_id <= self.max and cbed_id != -1:
            for chunk_id in range(self.chunkbeds.nchunks[cbed_id]):
                self.rem_chunk(chunk_id=chunk_id)
                self.chunkbeds.chunk_ids[cbed_id].remove(chunk_id)
            self.chunkify(cbed_id, tgen_id)

    def rebuild_chunk(self, tgen_id:int, chunk_id:int) -> int:
        if chunk_id <= self.max and chunk_id != -1:
            size=self.chunks.size[chunk_id]
            vxsize=self.chunks.vxsize[chunk_id]
            location=self.chunks.location[chunk_id]
            self.rem_chunk(chunk_id)
            return self.make_chunk(tgen_id, location, size, vxsize)

    def chunkify(self, cbed_id:int, tgen_id:int=0) -> None:
        if cbed_id <= self.max and cbed_id != -1:
            for x in range(int(self.chunkbeds.dimensions[cbed_id].x)):
                for y in range(int(self.chunkbeds.dimensions[cbed_id].y)):
                    for z in range(int(self.chunkbeds.dimensions[cbed_id].z)):
                        chunk_local = glm.vec3(x,y,z)*self.chunkbeds.chunksize[cbed_id]
                        chunk_index = int(x+self.chunkbeds.dimensions[cbed_id].x*z+self.chunkbeds.area[cbed_id]*y)
                        chunk_id=self.make_chunk(
                            tgen_id,
                            location=chunk_local,
                            size=self.chunkbeds.chunksize[cbed_id],
                            vxsize=self.chunkbeds.vxsize[cbed_id],
                        )
                        self.chunkbeds.nvoxels[cbed_id]+=self.chunks.nvoxels[chunk_id]
                        self.chunkbeds.chunk_ids[cbed_id].insert(chunk_id, chunk_id)
                        chunk_mesh = self.zenresources.meshbank.get_mesh(chunk_id)
                        chunk_mesh.set_texture(self.zenresources, self.zenresources.textures["zenwhite"])
                        chunk_mesh.m_model=glm.translate(glm.vec3(x, y, z)*self.chunks.size[chunk_id]*self.chunks.vxsize[chunk_id])
                        self.zenresources.meshbank.set_mesh(chunk_mesh)

    def rem_chunk(self, chunk_id:int) -> None:
        if chunk_id <= self.max and chunk_id != -1:
            self.chunks.area.pop(chunk_id)
            self.chunks.size.pop(chunk_id)
            self.chunks.hsize.pop(chunk_id)
            self.chunks.vxsize.pop(chunk_id)
            self.chunks.volume.pop(chunk_id)
            self.chunks.voxels.pop(chunk_id)
            self.chunks.nvoxels.pop(chunk_id)
            self.chunks.location.pop(chunk_id)
            self.zenresources.meshbank.rem_mesh(self.chunks.mesh_id[chunk_id])
            self.count-=1; return None

    def make_chunk(self, tgen_id:int, location:list[float], size:int, vxsize:float) -> int:
        if self.count+1 <= self.max:
            chunk_id:int=self.count
            self.chunks.nvoxels[chunk_id]=0
            self.chunks.size[chunk_id]=size
            self.chunks.hsize[chunk_id]=size/2
            self.chunks.vxsize[chunk_id]=vxsize
            self.chunks.area[chunk_id]=size*size
            self.chunks.location[chunk_id]=location
            self.chunks.volume[chunk_id]=self.chunks.area[chunk_id]*size
            self.chunks.voxels[chunk_id]=np.zeros(self.chunks.volume[chunk_id], dtype="uint8")
            self.count+=1; self.voxelize(tgen_id, chunk_id); return chunk_id

    def simple_fill(self, chunk_id:int) -> None:
        """ simple zvx terrain generation (fills an entire chunk) """
        if chunk_id <= self.max and chunk_id != -1:
            for x in range(self.chunks.size[chunk_id]):
                for z in range(self.chunks.size[chunk_id]):
                    for y in range(self.chunks.size[chunk_id]):
                        self.chunks.voxels[chunk_id][x+self.chunks.size[chunk_id]*z+self.chunks.area[chunk_id]*y]=x+y+z

    def simple_noise(self, chunk_id:int) -> None:
        """ simple 3D noise terrain generation using the simplex wave function """
        if chunk_id <= self.max and chunk_id != -1:
            for x in range(self.chunks.size[chunk_id]):
                for z in range(self.chunks.size[chunk_id]):
                    for y in range(self.chunks.size[chunk_id]):
                        self.chunks.voxels[chunk_id][x+self.chunks.size[chunk_id]*z+self.chunks.area[chunk_id]*y]=(
                            x + y + z if int(glm.simplex(glm.vec3(x, y, z) * 0.1) + 1) else 0
                        )

    def simplexPB(self, chunk_id:int) -> None:
        """ 3D noise terrain generation using the simplex wave function based on voxel position """
        if chunk_id <= self.max and chunk_id != -1:
            localx, localy, localz = self.chunks.location[chunk_id]
            for x in range(self.chunks.size[chunk_id]):
                for z in range(self.chunks.size[chunk_id]):
                    relx = x + localx
                    relz = z + localz
                    relheight = int(glm.simplex(glm.vec2(relx, relz) * 0.01) * self.chunks.size[chunk_id]+self.chunks.size[chunk_id])
                    localheight = min(relheight - localy, self.chunks.size[chunk_id])
                    for y in range(int(localheight)):
                        rely = y + localy
                        self.chunks.voxels[chunk_id][x+self.chunks.size[chunk_id]*z+self.chunks.area[chunk_id]*y]=rely+1

    def voxelize(self, tgen_id:int, chunk_id:int) -> None:
        """
            voxels exist as a number from 0-255 where 0 is empty space
            rather than storing them in 3D arrays (glm.vec3(vx_x, vx_y, vx_z))
            they are stored in a 1D array which will be indexed using the following formula
            from 3D space to 1D array:  AREA=SIZE*SIZE
                                        INDEX=X+SIZE*Z+AREA*Y
        """
        if chunk_id <= self.max and chunk_id != -1:
            self.zenresources.zvxterrain.generate(chunk_id, self.chunks)
            self.chunks.nvoxels[chunk_id]=len(self.chunks.voxels[chunk_id]); self.build(chunk_id)
            if self.chunks.nvoxels[chunk_id] <= 0 or len(self.chunks.voxels[chunk_id]) <= 0:
                self.rem_chunk(chunk_id=chunk_id)

    def build(self, chunk_id:int) -> None:
        if chunk_id <= self.max and chunk_id != -1:
            self.chunks.mesh_id[chunk_id]=self.zenresources.meshbank.make_mesh(
                vertices=build_zvxmesh(
                    self.chunks.area[chunk_id],
                    self.chunks.size[chunk_id],
                    self.chunks.volume[chunk_id],
                    self.chunks.voxels[chunk_id],
                    sum(int(fmt[:1]) for fmt in '3u1 1u1 1u1'.split()),
                    self.chunks.vxsize[chunk_id],
                ),
                vformat='3u1 1u1 1u1',
                vattribs=('position', 'zvx_id', 'face_id'),
                # TODO: either make a chunk specific shader, or introduce shader conditionals
                shader_id=self.zenresources.shaders["default002"],
            )

