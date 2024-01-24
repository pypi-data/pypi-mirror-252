#  Hue Engine ©️
#  2023-2024 Setoichi Yumaden <setoichi.dev@gmail.com>
#
#  This software is provided 'as-is', without any express or implied
#  warranty.  In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     appreciated but is not required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.

import pygame as pg
from .camera import Camera
from .physics import PhysicsSystem
from .render import RenderingSystem
from Hue.utils.globals import _ENTITYMAP

class Systems():
    def __init__(self, winX:int=800, winY:int=600, _WINFLAGS:tuple|list=[]):
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode((winX, winY), *_WINFLAGS)
        self.screen = pg.Surface((self.window.get_width(), self.window.get_height()))
        self.camera = Camera(self.window.get_width()/2, self.window.get_height()/2)
        self.renderSystem = RenderingSystem(self.window, self.screen)
        self.physicsSystem = PhysicsSystem()
        self._ACTIVE = []

    def CalculateActiveEntities(self) -> pg.Rect:
        _VIEWPORTRECT = self.camera._GetViewRect()
        self._ACTIVE = [print(entity) if "SpriteComponent" in entity and _VIEWPORTRECT.colliderect(entity["SpriteComponent"].rect) else self.renderSystem._CleanUp(entity) for entity in _ENTITYMAP.values()]
        self.renderSystem._ACTIVE = self._ACTIVE.copy()
        print( "SYSTEMS _ACTIVE", self._ACTIVE )
        print( "RENDER SYSTEMS _ACTIVE", self.renderSystem._ACTIVE )
        return _VIEWPORTRECT

    def Run(self, dt:float) -> None:
        _VIEWPORTRECT = self.CalculateActiveEntities()
        for entity in self._ACTIVE:
            self.physicsSystem.update(entity, dt)
            self.renderSystem.update(entity)
        self.renderSystem.Blit(_VIEWPORTRECT)
        

