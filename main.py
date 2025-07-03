import arcade
import arcade.gui
import random

from data import *
import game

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = f"Irisis v0.1"

GRAPH_WIDTH = 100
GRAPH_HEIGHT = 60

arcade.enable_timings()

global CURRENT_SCENE, TELEPORT_SCENE
CURRENT_SCENE, TELEPORT_SCENE = 0, 1

arcade.load_font("assets/精品點陣體-Bold_1.9.ttf")
# Fusion Pixel 10px Proportional zh_hans
arcade.load_font("assets/fusion-pixel-10px-proportional-zh_hans.otf")
# BoutiqueBitmap9x9 1.9

class MainMenuView(arcade.View):
    mouse_x, mouse_y = -100, -100

    def __init__(self):
        super().__init__()
        arcade.resources.load_kenney_fonts()
        self.background_color = (17, 10, 25)

        # fps指示图
        self.perf_graph_list = arcade.SpriteList()
        row_y = self.height - GRAPH_HEIGHT / 2
        starting_x = GRAPH_WIDTH / 2
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS")
        graph.position = starting_x, row_y
        self.perf_graph_list.append(graph)

        # 游戏标题
        self.cached_text = []
        title_color = arcade.color.WHITE
        self.cached_text.append(arcade.Text("Irisis", 60, 200, title_color, 96, font_name="Kenney Pixel"))
        self.cached_text.append(arcade.Text("v0.1", 60, 160, title_color, 24, font_name="Kenney Mini Square"))

        # 关门动画定义
        def close_door(s):
            self.door_left = 200 
            self.door_right = 800
            self.door_speed = 60
            self.door_start = s
            self.door_prog = 0
        close_door(False)
        
        # 按钮
        self.manager = arcade.gui.UIManager()
        self.manager.enable() 

        button_first = arcade.gui.UIFlatButton(text="first", height=36, width=160, style=DEFAULT_BUTTON_STYLE)
        @button_first.event("on_click")
        def _(event):
            close_door(True)

        button_about = arcade.gui.UIFlatButton(text="关于", height=36, width=160, style=DEFAULT_BUTTON_STYLE)
        @button_about.event("on_click")
        def _(event): self.window.show_view(game.GameView())

        button_exit = arcade.gui.UIFlatButton(text="退出程序", height=36, width=160, style=DEFAULT_BUTTON_STYLE)
        @button_exit.event("on_click")
        def _(event): self.window.close()

        self.b_box = arcade.gui.UIBoxLayout()
        self.b_box.add(arcade.gui.UIBoxLayout(children=[button_first, button_about, button_exit], space_between=10, vertical=False))
        self.manager.add(
            arcade.gui.UIAnchorLayout(
                x = -320,
                y = -250,
                width = 200,
                height = 400,
                children=self.b_box
            )
        )
    
    def setup(self):
        self.mouse_particle = arcade.SpriteList()
        arcade.schedule(self.spawn_mouse_particle, 0.08)

    def spawn_mouse_particle(self, delta_time):
        size = random.randint(100, 150)
        c = arcade.SpriteSolidColor(size, size, color=arcade.color.QUEEN_PINK)
        c.center_x = self.mouse_x + random.randint(-30, 30)
        c.center_y = self.mouse_y + random.randint(-30, 30)
        c.change_angle = random.uniform(-2, 2)
        c.change_y = 0.2
        c.alpha = random.randint(10, 20)
        self.mouse_particle.append(c)

    def reset(self):
        pass

    def on_draw(self):
        self.clear()

        for i in self.cached_text: i.draw() # 文字
        self.perf_graph_list.draw() # fps图
        self.manager.draw() # ui
        self.mouse_particle.draw() # 鼠标粒子

        # 关门动画
        if self.door_start:
            r1 = arcade.Rect(
                left = self.door_left,
                right = 0,
                bottom = 0,
                top = self.height,
                width = 900,
                height = self.height * 2,
                x = self.door_left - 800,
                y = self.height / 2
            )
            r2 = arcade.Rect(
                left = self.door_right,
                right = 0,
                bottom = 0,
                top = self.height,
                width = 900,
                height = self.height * 2,
                x = self.door_right+ 1410,
                y = self.height / 2
            )
            arcade.draw_rect_filled(r1, arcade.color.BLACK, 33)
            arcade.draw_rect_filled(r2, arcade.color.DARK_CYAN, 33)


    def on_update(self, delta_time):
        # 鼠标粒子动画
        for cube in self.mouse_particle:
            cube.change_y -= 0.1
            cube.center_y += cube.change_y
            cube.angle += cube.change_angle
            cube.alpha -= 0.5
            if cube.alpha <= 0 or cube.center_y < -50:
                cube.remove_from_sprite_lists()
        self.mouse_particle.update()

        # 关门动画
        if self.door_start:
            pr = 1800
            if 0 <= self.door_prog < pr:
                self.door_prog += self.door_speed
            elif self.door_prog >= pr:
                self.door_start = False
            self.door_left += self.door_speed * (pr - self.door_prog) / pr
            self.door_right -= self.door_speed * (pr - self.door_prog) / pr


    def on_hide_view(self):
        self.manager.disable()
        self.manager.clear()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse_x, self.mouse_y = x, y


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    main_menu = MainMenuView()
    game_view = game.GameView()
    
    global CURRENT_SCENE, TELEPORT_SCENE

    if CURRENT_SCENE != TELEPORT_SCENE:
        if TELEPORT_SCENE == 1:
            current = main_menu
            main_menu.setup()
        elif TELEPORT_SCENE == 2:
            current = game_view
            game_view.reset()
        CURRENT_SCENE = TELEPORT_SCENE
        
    window.show_view(current)
    arcade.run()

if __name__ == "__main__":
    main()