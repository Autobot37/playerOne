file_path = "DOOM1.WAD"
print("lets fucking doom")
import math
import struct
import time

DOOM_RES = DOOM_W, DOOM_H = 320, 200

SCALE = 3.0
WIN_RES = WIDTH, HEIGHT = int(DOOM_W * SCALE), int(DOOM_H * SCALE)
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

import pygame as pg
from pygame.math import Vector2 as vec2


class Linedef:

  def __init__(self):
    self.startvertex = None
    self.endvertex = None
    self.flags = None
    self.linetype = None
    self.sectortag = None
    self.rightsidedef = None
    self.leftsidedef = None


class Node:

  class BBox:

    #2'H' * 12 + 2 * 2H = 28bytes
    __slots__ = ['top', 'bottom', 'left', 'right']

  __slots__ = [
      'x_partition', 'y_partition', 'dx_partition', 'dy_partition', 'bbox',
      'front_child_id', 'back_child_id'
  ]

  def __init__(self):
    self.bbox = {"front": self.BBox(), "back": self.BBox()}


class SubSector:
  __slots__ = ['seg_count', 'first_seg_id']


class Seg:
  __slots__ = [
      'start_vertex_id',
      'end_vertex_id',
      'angle',
      'linedef_id',
      'direction',
      'offset',
  ]


class Thing:
  __slots__ = ['pos', 'angle', 'type', 'flags']


class WADReader:

  def __init__(self, file_path):
    self.wad_file = open(file_path, 'rb')
    self.header = self.read_header()
    self.directory = self.read_directory()

  def read_bytes(self, offset, num_bytes, byte_format):
    self.wad_file.seek(offset)
    buffer = self.wad_file.read(num_bytes)
    return struct.unpack(byte_format, buffer)

  def read_string(self, offset, num_bytes):
    return ''.join(
        b.decode('ascii') for b in self.read_bytes(
            offset, num_bytes, byte_format='c' * num_bytes)).upper()

  def read1byte(self, offset, byte_format='B'):
    return self.read_bytes(offset, 1, byte_format)[0]

  def read2byte(self, offset, byte_format='H'):
    return self.read_bytes(offset, 2, byte_format)[0]

  def read4byte(self, offset, byte_format='i'):
    return self.read_bytes(offset, 4, byte_format)[0]

  def read_header(self):
    return {
        "wad_type": self.read_string(0, 4),
        "lump_count": self.read4byte(4),
        "init_offset": self.read4byte(8)
    }

  def read_vertex(self, offset):
    x = self.read2byte(offset, byte_format='h')
    y = self.read2byte(offset + 2, byte_format='h')
    return vec2(x, y)

  def read_linedef(self, offset):
    linedef = Linedef()
    #foramt is 'H' 14 bytes
    read = self.read2byte
    linedef.startvertex = read(offset)
    linedef.endvertex = read(offset + 2)
    linedef.flags = read(offset + 4)
    linedef.linetype = read(offset + 6)
    linedef.sectortag = read(offset + 8)
    linedef.rightsidedef = read(offset + 10)
    linedef.leftsidedef = read(offset + 12)
    return linedef

  def read_nodes(self, offset):
    node = Node()
    read = self.read2byte
    node.x_partition = read(offset, 'h')
    node.y_partition = read(offset + 2, 'h')
    node.dx_partition = read(offset + 4, 'h')
    node.dy_partition = read(offset + 6, 'h')
    node.bbox['front'].top = read(offset + 8, 'h')
    node.bbox['front'].bottom = read(offset + 10, 'h')
    node.bbox['front'].left = read(offset + 12, 'h')
    node.bbox['front'].right = read(offset + 14, 'h')
    node.bbox['back'].top = read(offset + 16, 'h')
    node.bbox['back'].bottom = read(offset + 18, 'h')
    node.bbox['back'].left = read(offset + 20, 'h')
    node.bbox['back'].right = read(offset + 22, 'h')

    node.front_child_id = read(offset + 24, 'H')
    node.back_child_id = read(offset + 26, 'H')

    return node

  def read_sub_sector(self, offset):
    read = self.read2byte
    sec = SubSector()
    sec.seg_count = read(offset, 'h')
    sec.first_seg_id = read(offset + 2, 'h')
    return sec

  def read_segment(self, offset):
    read = self.read2byte
    seg = Seg()

    seg.start_vertex_id = read(offset, 'h')
    seg.end_vertex_id = read(offset + 2, 'h')
    seg.angle = read(offset + 4, 'h')
    seg.linedef_id = read(offset + 6, 'h')
    seg.direction = read(offset + 8, 'h')
    seg.offset = read(offset + 10, 'h')
    return seg

  def read_thing(self, offset):
    thing = Thing()
    read = self.read2byte

    x = read(offset, 'h')
    y = read(offset + 2, 'h')
    thing.pos = vec2(x, y)
    thing.angle = read(offset + 4, 'h')
    thing.type = read(offset + 6, 'h')
    thing.flags = read(offset + 8, 'h')
    return thing

  def read_directory(self):
    directory = []
    for i in range(self.header["lump_count"]):
      offset = self.header["init_offset"] + i * 16
      lump_info = {
          "lump_offset": self.read4byte(offset),
          "lump_size": self.read4byte(offset + 4),
          "lump_name": self.read_string(offset + 8, num_bytes=4)
      }
      directory.append(lump_info)
    return directory

  def close(self):
    self.wad_file.close()


from enum import Enum


class LUMP_INDICES(Enum):
  THINGS = 1
  LINEDEFS = 2
  SIDEDEFS = 3
  VERTEXES = 4
  SEGS = 5
  SSECTORS = 6
  NODES = 7
  SECTORS = 8
  REJECT = 9
  BLOCKMAP = 10


class WADData:

  def __init__(self, map_name):
    self.reader = WADReader(file_path)
    self.LUMP_INDICES = LUMP_INDICES
    self.map_index = self.get_lump_index(map_name)
    self.vertexes = self.get_lump_data(reader=self.reader.read_vertex,
                                       lump_index=self.map_index +
                                       self.LUMP_INDICES.VERTEXES.value,
                                       num_bytes=4)
    self.linedefs = self.get_lump_data(reader=self.reader.read_linedef,
                                       lump_index=self.map_index +
                                       self.LUMP_INDICES.LINEDEFS.value,
                                       num_bytes=14)
    self.nodes = self.get_lump_data(reader=self.reader.read_nodes,
                                    lump_index=self.map_index +
                                    self.LUMP_INDICES.NODES.value,
                                    num_bytes=28)
    self.sub_sectors = self.get_lump_data(reader=self.reader.read_sub_sector,
                                          lump_index=self.map_index +
                                          self.LUMP_INDICES.SSECTORS.value,
                                          num_bytes=4)
    self.segments = self.get_lump_data(reader=self.reader.read_segment,
                                       lump_index=self.map_index +
                                       self.LUMP_INDICES.SEGS.value,
                                       num_bytes=12)
    self.things = self.get_lump_data(reader=self.reader.read_thing,
                                     lump_index=self.map_index +
                                     self.LUMP_INDICES.THINGS.value,
                                     num_bytes=10)
    self.reader.close()

  def get_lump_index(self, lump_name):
    for index, lump_info in enumerate(self.reader.directory):
      if lump_name in lump_info["lump_name"]:
        return index
    print("No Lump Found")
    return None

  def get_lump_data(self, reader, lump_index, num_bytes, header_length=0):
    lump_info = self.reader.directory[lump_index]
    count = lump_info["lump_size"] // num_bytes
    data = []
    for i in range(count):
      offset = lump_info["lump_offset"] + i * num_bytes + header_length
      data.append(reader(offset))
    return data

  @staticmethod
  def print_attrs(obj):
    print()
    for attr in obj.__slots__:
      print(eval(f"obj.{attr}", end=' '))


class Player:

  def __init__(self, engine):
    self.engine = engine
    self.thing = engine.wad_data.things[0]
    self.pos = self.thing.pos
    self.angle = self.thing.angle

  def update(self):
    pass


import random


class MapRender:

  def __init__(self, engine):
    self.engine = engine
    self.wad_data = engine.wad_data
    self.vertexes = self.wad_data.vertexes
    self.linedefs = self.wad_data.linedefs
    self.x_min, self.x_max, self.y_min, self.y_max = self.get_maps_bounds()
    self.vertexes = [
        vec2(self.remap_x(v.x), self.remap_y(v.y)) for v in self.vertexes
    ]
    assert (len(self.vertexes) == len(self.wad_data.vertexes))

  def draw(self):
    #self.draw_linedefs()
    #self.draw_vertexes()
    #self.draw_player_pos()
    self.engine.bsp.draw()

  def get_color(self, seed=0):
    random.seed(seed)
    rnd = random.randrange
    rng = 100, 256
    return rnd(*rng), rnd(*rng), rnd(*rng)

  def draw_seg(self, seg, subsector_id):
    if seg.start_vertex_id < len(self.vertexes):
      v1 = self.vertexes[seg.start_vertex_id]
    else:
      v1 = self.vertexes[0]

    if seg.end_vertex_id < len(self.vertexes):
      v2 = self.vertexes[seg.end_vertex_id]
    else:
      v2 = self.vertexes[0]

    pg.draw.line(self.engine.screen, self.get_color(subsector_id), v1, v2, 4)
    pg.display.flip()
    pg.time.wait(10)

  def draw_bbox(self, bbox, color):
    x, y = self.remap_x(bbox.left), self.remap_y(bbox.top)
    w, h = self.remap_x(bbox.right) - x, self.remap_y(bbox.bottom) - y
    pg.draw.rect(self.engine.screen, color, (x, y, w, h), 2)
    

  def draw_node(self, node_id):
    node = self.engine.wad_data.nodes[node_id]
    bbox_front = node.bbox["front"]
    bbox_back = node.bbox["back"]
    self.draw_bbox(bbox_front, color='green')
    self.draw_bbox(bbox_back, color='red')

    pg.display.flip()
    pg.time.wait(25)
    

  def draw_player_pos(self):
    pos = self.engine.player.pos
    x = self.remap_x(pos.x)
    y = self.remap_y(pos.y)
    pg.draw.circle(self.engine.screen, 'orange', (x, y), 8)

  def draw_linedefs(self):
    for line in self.linedefs:
      p1 = self.vertexes[line.startvertex]
      p2 = self.vertexes[line.endvertex]
      pg.draw.line(self.engine.screen, 'orange', p1, p2, 3)

  def draw_vertexes(self):
    for v in self.vertexes:
      pg.draw.circle(self.engine.screen, 'white', (v.x, v.y), 4)

  def get_maps_bounds(self):
    x = ([a.x for a in self.vertexes])
    y = ([a.y for a in self.vertexes])
    return min(x), max(x), min(y), max(y)

  def remap_x(self, n, out_min=30, out_max=WIDTH - 30):
    return (max(self.x_min, min(n, self.x_max)) - self.x_min) * (
        out_max - out_min) / (self.x_max - self.x_min) + out_min

  def remap_y(self, n, out_min=30, out_max=HEIGHT - 30):
    return HEIGHT - (max(self.y_min, min(n, self.y_max)) - self.y_min) * (
        out_max - out_min) / (self.y_max - self.y_min) - out_min


import sys


class BSP:
  SUB_SECTOR_IDENTIFIER = 0x8000

  def __init__(self, engine):
    self.engine = engine
    self.nodes = engine.wad_data.nodes
    self.player = engine.player
    self.sub_sectors = engine.wad_data.sub_sectors
    self.segs = engine.wad_data.segments
    self.root_node_id = len(self.nodes) - 1

  def draw(self):
    self.render_bsp_node(self.root_node_id)
    #self.render_sub_sector(len(self.sub_sectors)-1)

  def render_sub_sector(self, id):
    sub_sector = self.sub_sectors[id]
    for i in range(sub_sector.seg_count):
      seg = self.segs[sub_sector.first_seg_id + i]
      self.engine.map_renderer.draw_seg(seg, id)

  def render_bsp_node(self, node_id):
    print(node_id, end="\n")
    if node_id >= self.SUB_SECTOR_IDENTIFIER:
      sub_sector_id = node_id - self.SUB_SECTOR_IDENTIFIER
      #self.render_sub_sector(sub_sector_id)
      return None
      

    node = self.nodes[node_id]
    self.engine.map_renderer.draw_node(node_id)
    is_on_back = self.is_on_back_side(node)
    if is_on_back:
      self.render_bsp_node(node.back_child_id)
      self.render_bsp_node(node.front_child_id)
    else:
      self.render_bsp_node(node.front_child_id)
      self.render_bsp_node(node.back_child_id)
    

  def is_on_back_side(self, node):
    dx = self.player.pos.x - node.x_partition
    dy = self.player.pos.y - node.y_partition
    return dx * node.dy_partition - dy * node.dx_partition <= 0


class Engine:

  def __init__(self):
    self.screen = pg.display.set_mode(WIN_RES)
    self.clock = pg.time.Clock()
    self.running = True
    self.dt = 1 / 60
    self.on_init()

  def on_init(self):
    self.wad_data = WADData(map_name='E1M3')
    self.map_renderer = MapRender(self)
    self.player = Player(self)
    self.bsp = BSP(self)

  def update(self):
    self.player.update()
    self.dt = self.clock.tick()
    pg.display.set_caption(f'{self.clock.get_fps()}')

  def draw(self):
    self.screen.fill('black')
    self.map_renderer.draw()
    pg.display.flip()

  def check_events(self):
    for e in pg.event.get():
      if e.type == pg.QUIT:
        self.running = False

  def run(self):
    while self.running:
      self.check_events()
      self.update()
      self.draw()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
  doom = Engine()
  doom.run()
