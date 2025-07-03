import arcade as a
import arcade.gui

class GameView(a.View):
    def __init__(self):
        super().__init__()
        self.background_color = a.color.LICORICE
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.perf_graph_list = a.SpriteList()
        self.mouse_particle = a.SpriteList()

    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.perf_graph_list.draw()
        self.mouse_particle.draw()
    
    def on_hide_view(self):
        self.manager.disable()
        self.manager.clear()