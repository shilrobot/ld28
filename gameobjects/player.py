from rect import Rect
from texturemanager import TextureManager
import pygame
from utils import drawRect, debugRect, sweepMovement, debugPoint
from gameobject import GameObject

WALK_SPEED = 300.0
ANIM_STAND = 0
ANIM_WALK = 1
GRAVITY_ACCEL = 1500
TERMINAL_VELOCITY = 1000
JUMP_VEL = 570

WALK_FRAME_TIME = 10/60.0

class Player(GameObject):
    def __init__(self, world):
        super(Player,self).__init__(world)
        self.texStand = TextureManager.get().load('player.png')
        self.texWalk1 = TextureManager.get().load('playerwalk1.png')
        self.texWalk2 = TextureManager.get().load('playerwalk2.png')
        self.buttonTex = TextureManager.get().load('TheButton.png')
        self.anim = ANIM_STAND
        self.animTime = 0
        self.faceRight = True
        self.vyLast = 0.0
        self.vy = 0.0
        world.player = self
        self.priority = GameObject.PRIORITY_PLAYER

    def spawn(self,spawn):
        super(Player,self).spawn(spawn)
        self.x = spawn.rect.centerX
        self.y = spawn.rect.bottom - 1

    def getRect(self,x,y):
        return Rect(x-8, y-60, 16,60)

    def getButtonActivationRect(self):
        if self.faceRight:
            return Rect(self.x-16, self.y-60, 32+16,60)
        else:
            return Rect(self.x-32,self.y-60,32+16,60)

    def setAnimation(self, anim):
        if self.anim == anim:
            return
        self.anim = anim
        self.animTime = 0

    def updateXMovement(self,delta):
        dx = 0
        moving = False

        if self.engine.key_down(pygame.K_LEFT) or self.engine.key_down(pygame.K_a):
            dx -= WALK_SPEED*delta
            self.faceRight = False
            moving = True
        if self.engine.key_down(pygame.K_RIGHT) or self.engine.key_down(pygame.K_d):
            dx += WALK_SPEED*delta
            self.faceRight = True
            moving = True

        self.move(dx,0)

        if moving:
            self.setAnimation(ANIM_WALK)
        else:
            self.setAnimation(ANIM_STAND)

    def updateJumping(self):
        if self.engine.key_pressed(pygame.K_SPACE):
            if self.vy >= 0 and self.canJump():
                self.vyLast = -JUMP_VEL
                self.vy = -JUMP_VEL

    def updateYMovement(self, delta):
        self.vy += GRAVITY_ACCEL*delta
        if self.vy > TERMINAL_VELOCITY:
            self.vy = TERMINAL_VELOCITY

        # trapezoidal integration
        newY = self.y + (self.vyLast + self.vy)*delta*0.5

        yCollision = self.move(0,newY - self.y)
        if yCollision:
            self.vy = 0

        self.vyLast = self.vy

    def updateAnimations(self, delta):
        if self.anim == ANIM_WALK:
            self.animTime += delta
            self.animTime = self.animTime % (WALK_FRAME_TIME*2)

    def updateButtonInteraction(self):
        button = self.getButton()
        if button is None:
            return
        if self.engine.key_pressed(pygame.K_e):
            if self.getButtonActivationRect().intersects(button.getRect()):
                button.activate()
        elif self.engine.key_pressed(pygame.K_q):
            if self.isHoldingButton():
                mount = self.world.findButtonMount(self.getButtonActivationRect())
                if mount is not None:
                    button.attachTo(mount)
                else:
                    self.dropButton()
            else:
                if self.getButtonActivationRect().intersects(button.getRect()):
                    button.becomeHeld()


    def update(self, delta):
        self.updateXMovement(delta)
        self.updateJumping()
        self.updateYMovement(delta)
        self.updateAnimations(delta)
        self.updateButtonInteraction()

    def canJump(self):
        return self.world.rectOverlaps(self.getRect(self.x, self.y+0.5))

    def move(self, dx, dy):
        collided, movedX, movedY = sweepMovement(self.world, self.getRect(self.x,self.y), dx, dy)
        self.x += movedX
        self.y += movedY
        return collided

    def getButtonLocation(self, frameTex):
        if frameTex == self.texStand:
            return (12,-25)
        elif frameTex == self.texWalk1:
            return (12,-34)
        elif frameTex == self.texWalk2:
            return (11,-24)
        else:
            return (0,0)

    def getButton(self):
        return self.world.goMgr.get('button')

    def isHoldingButton(self):
        button = self.getButton()
        return button is not None and button.isHeld()

    def buttonExists(self):
        return self.getButton() is not None

    def dropButton(self):
        if not self.isHoldingButton():
            return
        button = self.getButton()
        button.x = self.x + (12 if self.faceRight else -12)
        button.y = self.y - 25
        button.popOff()

    def draw(self):
        if self.anim == ANIM_STAND:
            tex = self.texStand
        elif self.anim == ANIM_WALK:
            if self.animTime < WALK_FRAME_TIME:
                tex = self.texWalk1
            else:
                tex = self.texWalk2

        drawRect(tex, self.x, self.y, anchorX=0.5, anchorY=1, flipX=not self.faceRight)

        if self.isHoldingButton():
            buttonDX, buttonDY = self.getButtonLocation(tex)
            if not self.faceRight:
                buttonDX = -buttonDX
            drawRect(self.buttonTex,
                        self.x+buttonDX,
                        self.y+buttonDY, 
                        anchorX=1,
                        anchorY=0.5,
                        flipX=self.faceRight)
