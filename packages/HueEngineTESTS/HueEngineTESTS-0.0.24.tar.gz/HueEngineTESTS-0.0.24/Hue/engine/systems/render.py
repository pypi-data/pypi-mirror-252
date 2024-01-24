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
from Hue.utils.globals import _ENTITYMAP
from Hue.utils.profile import SystemHealth, ReportSystemImpact, ProfileSystem, SYSTIMES
from Hue.HueGame.HueGame import DebugInterface
from Hue.engine.components import DebugEntityCount
from .camera import Camera

class RenderingSystem:
    def __init__(self, window:pg.Surface, screen:pg.Surface) -> None:
        self._Debug = False
        self.window = window
        self.screen = screen
        self.camera = Camera()
        self.interface = None
        self.showColliders = True  
        self._preRenderLogic = self._
        self._postRenderLogic = self._
        self._clearColor = [60, 60, 60]
        self.spriteGroup = pg.sprite.Group()

    def _(self) -> None:
        0

    def SetPreRenderLogic(self, func) -> None:
        self._preRenderLogic = func
    
    def SetPostRenderLogic(self, func) -> None:
        self._postRenderLogic = func

    def ResetPreRenderLogic(self) -> None:
        self._preRenderLogic = self._
    
    def ResetPostRenderLogic(self) -> None:
        self._postRenderLogic = self._

    def SetInterface(self, interface:DebugInterface) -> None:
        self.interface = interface

    def ToggleDebugInterface(self):
        self._Debug = not self._Debug
    
    def ToggleShowColliders(self) -> None:
        self.showColliders = not self.showColliders
        if (self.showColliders):
            for entity in _ENTITYMAP.values():
                if ("ColliderComponent" in entity): 
                    self.spriteGroup.add(entity["ColliderComponent"])
        else:
            for entity in _ENTITYMAP.values():
                if ("ColliderComponent" in entity): 
                    self.spriteGroup.remove(entity["ColliderComponent"])

    @ProfileSystem('Rendering')
    def Update(self, dt:float=1.0) -> None:
        self.screen.fill(self._clearColor)
        self._preRenderLogic()
        self.spriteGroup.draw(self.screen)
        self._postRenderLogic()
        if (self.interface and self._Debug):
            self.interface.AddToInterface("~Hue Debug Interface~")
            self.interface.AddToInterface(DebugEntityCount())
            self.interface.VisualOutput()

        _VIEWPORTRECT = self.camera._GetViewRect()
        _VIEWPORTSURF = pg.Surface((_VIEWPORTRECT.width, _VIEWPORTRECT.height))
        _VIEWPORTSURF.blit(self.screen, (0,0), _VIEWPORTRECT)
        
        _SCALEDVIEWPORT = pg.transform.scale(_VIEWPORTSURF, (self.window.get_width(), self.window.get_height()))
        self.window.blit(_SCALEDVIEWPORT, (0,0))

        pg.display.flip()
