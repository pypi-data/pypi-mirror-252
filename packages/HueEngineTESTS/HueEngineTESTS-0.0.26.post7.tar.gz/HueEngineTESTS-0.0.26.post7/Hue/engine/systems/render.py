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
from Hue.utils.globals import _ENTITY
from Hue.utils.profile import ProfileSystem
from Hue.HueGame.HueGame import DebugInterface
from Hue.engine.components import DebugEntityCount

class RenderingSystem:
    def __init__(self, window:pg.Surface, screen:pg.Surface) -> None:
        self._Debug = False
        self.window = window
        self.screen = screen
        self.camera = Camera()
        self.interface = None
        self.showColliders = True  
        self._preProcessingLogic = self._
        self._postProcessingLogic = self._
        self._clearColor = [60, 60, 60]
        self.spriteGroup = pg.sprite.Group()
        self._ACTIVE = []

    def _(self) -> None:
        0

    def SetPreProcessingLogic(self, func) -> None:
        self._preProcessingLogic = func
    
    def SetPostProcessingLogic(self, func) -> None:
        self._postProcessingLogic = func

    def ResetPreProcessingLogic(self) -> None:
        self._preProcessingLogic = self._
    
    def ResetPostProcessingLogic(self) -> None:
        self._postProcessingLogic = self._

    def SetInterface(self, interface:DebugInterface) -> None:
        self.interface = interface

    def ToggleDebugInterface(self):
        self._Debug = not self._Debug
    
    def ToggleShowColliders(self) -> None:
        self.showColliders = not self.showColliders
        if (self.showColliders):
            for entity in self._ACTIVE:
                if ("ColliderComponent" in entity): 
                    self.spriteGroup.add(entity["ColliderComponent"])
        else:
            for entity in self._ACTIVE:
                if ("ColliderComponent" in entity): 
                    self.spriteGroup.remove(entity["ColliderComponent"])

    @ProfileSystem('Rendering')
    def Update(self, entity:_ENTITY) -> None:
        self.screen.fill(self._clearColor)
        self._preProcessingLogic()
        if ("SpriteComponent" in entity):
            self.spriteGroup.add(entity["SpriteComponent"])
        self.spriteGroup.draw(self.screen)
        self._postProcessingLogic()
        if (self.interface and self._Debug):
            self.interface.AddToInterface("~Hue Debug Interface~")
            self.interface.AddToInterface(DebugEntityCount())
            self.interface.VisualOutput()
    
    def _CleanUp(self, entity):
        if ("SpriteComponent" in entity):
            self.spriteGroup.remove(entity["SpriteComponent"])

    def Blit(self, _VIEWPORTRECT:pg.Rect) -> None:
        _VIEWPORTSURF = pg.Surface((_VIEWPORTRECT.width, _VIEWPORTRECT.height))
        _VIEWPORTSURF.blit(self.screen, (0,0), _VIEWPORTRECT)

        _SCALEDVIEWPORT = pg.transform.scale(
            _VIEWPORTSURF,
            (self.window.get_width(), self.window.get_height())
        )

        self.window.blit(_SCALEDVIEWPORT, (0,0))
        pg.display.flip()
