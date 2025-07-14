import arcade as a
from data import *
import os

class Map():
    def __init__(self):
        self.blocks = {}
    
    def do(self, x, y, type):
        if x not in self.blocks:
            self.blocks[x] = {}
        self.blocks[x][y] = type
    
    def get(self, x, y) -> int | None:
        if x in self.blocks and y in self.blocks[x]:
            return self.blocks[x][y]
        return None
    
    def fill(self, x1, y1, x2, y2, type):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.do(x, y, type)

    def draw(self):
        sprite_list = arcade.SpriteList(use_spatial_hash=True)
        for x in self.blocks:
            for y in self.blocks[x]:
                block = self.blocks[x][y]
                draw_x, draw_y = x * 64, y * 64
                img = BLOCK_IMG[block]
                if img is not None:
                    tex = a.Texture(img)
                    block_sprite = arcade.BasicSprite(tex, center_x=draw_x, center_y=draw_y)
                    sprite_list.append(block_sprite)
        sprite_list.draw()

class GameView(a.View):
    def __init__(self):
        super().__init__()
        self.debug = False # 调试模式开关
        self.background_color = a.color.BLACK # 背景颜色

        # fps指示图
        self.perf_graph_list = arcade.SpriteList()
        row_y = self.height - GRAPH_HEIGHT / 2
        starting_x = GRAPH_WIDTH / 2
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS", update_rate=0.05, axis_color=arcade.color.CYBER_GRAPE, grid_color=arcade.color.CYBER_GRAPE, data_line_color=arcade.color.PINK_LACE)
        graph.position = starting_x, row_y
        self.perf_graph_list.append(graph)

        # ui
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.blackout = 255 # 不透明度

        self.player_x = 0 # 玩家x坐标
        self.player_y = 0 # 玩家y坐标

        # 地图
        self.map = Map()
        self.map.fill(-10, -10, 10, 10, 1)

        # 相机
        vp = arcade.Rect(
            left = 0,
            right = 0,
            bottom = 0,
            top = 0,
            width = 1280,
            height = 720,
            x = 0,
            y = 0
        )
        self.ui_camera = arcade.Camera2D(viewport=vp)
        self.game_camera = arcade.Camera2D(viewport=vp)

    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.game_camera.use() # 以下绘制游戏元素

        self.map.draw()

        self.ui_camera.use() # 以下绘制UI元素

        self.perf_graph_list.draw() # fps图
        
        arcade.draw_text(f"playerxy={self.player_x},{self.player_y}", 10, self.height-75, arcade.color.WHITE, 12, font_name="Kenney Mini Square")

        # 入场动画
        blackout_r = arcade.Rect(
            left = 0,
            right = 0,
            bottom = 0,
            top = 0,
            width = self.width,
            height = self.height,
            x = self.width / 2,
            y = self.height / 2
        )
        if self.blackout >= 0: arcade.draw_rect_filled(blackout_r, (64, 41, 66, self.blackout))
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.game_camera.zoom += scroll_y * 0.05
        self.game_camera.zoom = max(0.5, min(self.game_camera.zoom, 2.0))

    def on_update(self, delta_time):
        if self.blackout > 0:
            def bd(): self.blackout -= 1
            arcade.schedule(lambda _: bd(), 0.01)

        if self.debug:
            arcade.print_timings()
            os.system("cls" if os.name == "nt" else "clear")
    
    def on_hide_view(self):
        self.manager.disable()
        self.manager.clear()