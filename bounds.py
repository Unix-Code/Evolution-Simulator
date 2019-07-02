class ScreenBounds:
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"
    ALL_BOUNDS = [RIGHT, LEFT, TOP, BOTTOM]

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def bounds_collided(self, obj):
        collisions = [obj.rect.x + obj.rect.width + obj.velocity.x > self.width,
                      obj.rect.x + obj.velocity.x < 0,
                      obj.rect.y + obj.velocity.y < 0,
                      obj.rect.y + obj.rect.height + obj.velocity.y > self.height]
        return [bound for bound, collided in zip(ScreenBounds.ALL_BOUNDS, collisions) if collided]

    def bounds(self):
        return self.width, self.height
