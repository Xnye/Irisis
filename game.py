import arcade as a
from data import *
import os
import random
import pyglet

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
                draw_x, draw_y = x * 32, y * 32
                tex = BLOCK_TEX[block]
                block_sprite = arcade.BasicSprite(BLOCK_TEX[block], center_x=draw_x, center_y=draw_y)
                sprite_list.append(block_sprite) # todo: camera之外的不绘制
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

        # 玩家状态
        self.player_x = 0
        self.player_y = 0
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.acc_x = 0
        self.acc_y = 0

        # 地图
        self.map = Map()
        self.map.do(0, 0, 0)
        for i in range(100): self.map.do(random.randint(-80,80), random.randint(-80,80), 1)
        for i in range(100): self.map.do(random.randint(-80,80), random.randint(-80,80), 2)

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
        self.cam_x = self.player_x
        self.cam_y = self.player_y
        self.ui_camera = arcade.Camera2D(viewport=vp)
        self.game_camera = arcade.Camera2D(viewport=vp)

    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.game_camera.use() # 以下绘制游戏元素

        game_sl = arcade.SpriteList(use_spatial_hash=True)
        self.map.draw()
        game_sl.append(arcade.BasicSprite(BLOCK_TEX[-1], center_x=self.player_x, center_y=self.player_y))
        game_sl.draw()

        self.ui_camera.use() # 以下绘制UI元素

        self.perf_graph_list.draw() # fps图
        
        arcade.draw_text(f"playerxy={round(self.player_x)},{round(self.player_y)}", 10, self.height-75, arcade.color.WHITE, 12, font_name="Kenney Mini Square")
        arcade.draw_text(f"accxy={round(self.acc_x)},{round(self.acc_y)}", 10, self.height-90, arcade.color.WHITE, 12, font_name="Kenney Mini Square")

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

    def on_key_press(self, key, modifiers):
        if key == a.key.W or key == a.key.UP:
            self.up_pressed = True
        elif key == a.key.S or key == a.key.DOWN:
            self.down_pressed = True
        elif key == a.key.A or key == a.key.LEFT:
            self.left_pressed = True
        elif key == a.key.D or key == a.key.RIGHT:
            self.right_pressed = True
        elif key == a.key.ESCAPE:
            self.window.close()

    def on_key_release(self, key, modifiers):
        if key == a.key.W or key == a.key.UP:
            self.up_pressed = False
        elif key == a.key.S or key == a.key.DOWN:
            self.down_pressed = False
        elif key == a.key.A or key == a.key.LEFT:
            self.left_pressed = False
        elif key == a.key.D or key == a.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        # 转场
        if self.blackout > 0:
            def bd(): self.blackout -= 1
            arcade.schedule(lambda _: bd(), 0.01)
        
        # 玩家移动
        max_speed = 6
        acc_acc = 0.5
        stop_acc = 1
        if self.up_pressed:
            self.acc_y = min(max_speed, self.acc_y + acc_acc)
        if self.down_pressed:
            self.acc_y = max(-max_speed, self.acc_y - acc_acc)
        if not self.up_pressed and not self.down_pressed:
            self.acc_y = max(0, self.acc_y - stop_acc) if self.acc_y > 0 else min(0, self.acc_y + stop_acc)
        if self.right_pressed:
            self.acc_x = min(max_speed, self.acc_x + acc_acc)
        if self.left_pressed:
            self.acc_x = max(-max_speed, self.acc_x - acc_acc)
        if not self.right_pressed and not self.left_pressed:
            self.acc_x = max(0, self.acc_x - stop_acc) if self.acc_x > 0 else min(0, self.acc_x + stop_acc)
        self.player_x += self.acc_x
        self.player_y += self.acc_y

        # 相机跟随
        self.cam_x += (self.player_x - self.cam_x) * 0.03
        self.cam_y += (self.player_y - self.cam_y) * 0.03
        self.game_camera.position = (self.cam_x, self.cam_y)

        # 调试
        if self.debug:
            arcade.print_timings()
            os.system("cls" if os.name == "nt" else "clear")
    
    def on_hide_view(self):
        self.manager.disable()
        self.manager.clear()