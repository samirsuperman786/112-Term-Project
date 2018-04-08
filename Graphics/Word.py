class Word(object):
	def __init__(self, x, y, radius, text):
		self.x = x
		self.y = y
		self.text = text
		self.radius = radius

	def draw(self, canvas, data):
		canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x + self.radius, self.y + self.radius, fill = "blue")
		canvas.create_text(self.x, self.y, text = self.text, fill = "black", font = "Helvetica 30 bold")

	def move(self, direction):
		(deltaX, deltaY) = direction
		self.x +=deltaX
		self.y +=deltaY