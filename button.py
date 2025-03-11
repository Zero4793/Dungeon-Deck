import pygame

class Button:
	def __init__(self, core, pos, dim, text, color):
		self.core = core
		self.dim = dim
		self.pos = pos
		self.text = text
		self.color = color
		self.hover = False
		self.active = False


	def process(self):
		mx,my = pygame.mouse.get_pos()
		px,py = self.pos
		dx,dy = self.dim

		if px < mx < px+dx and py < my < py+dy:
			if self.core.mouseTarget is None:
				self.hover = True
			if pygame.mouse.get_pressed()[0] and not self.core.mouseTarget:
				self.core.mouseTarget = self
			if not pygame.mouse.get_pressed()[0] and self.core.mouseTarget is self:
				self.core.mouseTarget = None
				self.active = True
		else:
			self.hover = False
			if not pygame.mouse.get_pressed()[0] and self.core.mouseTarget is self:
				self.core.mouseTarget = None


	def display(self, screen):
		px,py = self.pos
		dx,dy = self.dim
		if self.color:
			col = self.color[3] if self.active else self.color[2] if self.held() else self.color[1] if self.hover else self.color[0] #never seen this annotation before, was confued at first
			pygame.draw.rect(screen, col, (px,py,dx,dy))
		if self.text:
			text = self.text[3] if self.active else self.text[2] if self.held() else self.text[1] if self.hover else self.text[0]
			font = pygame.font.Font(None, 32)
			text = font.render(text, True, (0,0,0))
			screen.blit(text, (px+dx/2-text.get_width()/2, py+dy/2-text.get_height()/2))


	def held(self) -> bool:
		return self.core.mouseTarget is self