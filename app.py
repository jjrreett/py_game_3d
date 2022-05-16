# from object_3d import Object3D, get_object_from_file, create_axes
# from camera import Camera
# from projection import Projection
# import pygame as pg
import numpy as np


# def create_objects(self):
#     self.objects.append(create_axes(self))
#     # self.objects.append(get_object_from_file(self, 'resources/t_34_obj.obj'))
#     # self.object.rotate_y(-math.pi / 4)
#     # self.objects.append(get_object_from_file(self, 'resources/test.obj'))
#
#
# def draw(self):
#     self.screen.fill(pg.Color('darkslategray'))
#     for object in self.objects:
#         object.draw()
#
#
# def run(self):
#     while True:
#         self.draw()
#         self.camera.control()
#         [exit() for i in pg.event.get() if i.type == pg.QUIT]
#         pg.display.set_caption(str(self.clock.get_fps()))
#         pg.display.flip()
#         self.clock.tick(self.FPS)

def Vec3(x, y, z):
    return np.array([x, y, z])


def Vec4(x, y, z):
    return np.array([x, y, z, 1])


class Window:
    def __init__(self):
        self.ASPECT_RATIO = 2.
        self.WIDTH = 1200
        self.HEIGHT = self.WIDTH // self.ASPECT_RATIO
        self.RES = self.WIDTH, self.HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2

        self.FPS = 60

        # pg.init()
        # self.screen = pg.display.set_mode(self.RES)
        # self.clock = pg.time.Clock()
        self.scene = Scene()

        self.scene.add_object(Object('test', Vec4(0, 1, 1), []))
        self.scene.camera.translate(Vec3(0, 0, 1))
        self.scene.camera.yaw_camera(np.pi/2)

    def render(self):
        self.scene.render()


class Scene():
    def __init__(self):
        self.camera = Camera()
        self.objects = {}

    def render(self):
        # calculate all raw objects movement within scene
        inverse_camera_matrix = self.camera.get_inverse_camera_matrix()
        for name, object in self.objects.items():
            object.calculate_points(inverse_camera_matrix)
            print(object.points)
        # rotate entire scene such that camera is at 0,0,0 and axis align
        # project all points onto screen
        # draw
        pass

    def add_object(self, object):
        self.objects[object.name] = object


class Object:
    def __init__(self, name, points, lines):
        self.name = name
        self._points = points  # n x 4 ndarray
        self.points = points
        self.lines = lines  # list[list[ints]]
        self.movement_matrix = np.identity(4)

    def calculate_points(self, inverse_camera_matrix):
        self.points = self.movement_matrix @ self._points
        self.points = inverse_camera_matrix @ self.points


class Camera():
    def __init__(self):
        self.pos = np.zeros((3))
        self.alpha = 0  # yaw angle (about z, how much x/y moves) z' = z
        self.beta = 0  # pitch angle (about y', how much x'/z' moves) y'' = y'
        self.gamma = 0  # roll angle (about x'', how much y''/z'' moves) x''' = x''
        self.calculate_movement_matrix()

    def translate(self, vector):
        self.pos += vector

    def yaw_camera(self, angle):
        self.alpha += angle

    def pitch_camera(self, angle):
        self.beta += angle

    def roll_camera(self, angle):
        self.gamma += angle

    def calculate_movement_matrix(self):
        a = self.alpha
        b = self.beta
        y = self.gamma
        p, q, r = self.pos[0], self.pos[1], self.pos[2]
        r1 = np.array([
            [np.cos(a), -np.sin(a), 0, 0],
            [np.sin(a), np.cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        r2 = np.array([
            [np.cos(b), 0, np.sin(b), 0],
            [0, 1, 0, 0],
            [-np.sin(b), 0, np.cos(b), 0],
            [0, 0, 0, 1],
        ])
        r3 = np.array([
            [1, 0, 0, 0],
            [0, np.cos(y), -np.sin(y), 0],
            [0, np.sin(y), np.cos(y), 0],
            [0, 0, 0, 1],
        ])
        t0 = np.array([
            [1, 0, 0, p],
            [0, 1, 0, q],
            [0, 0, 1, r],
            [0, 0, 0, 1],
        ])
        mm = np.identity(4)
        mm = r1 @ mm
        mm = r2 @ mm
        mm = r3 @ mm
        mm = t0 @ mm
        self.movement_matrix = mm

    def get_inverse_camera_matrix(self):
        self.calculate_movement_matrix()
        return np.linalg.inv(self.movement_matrix)


if __name__ == '__main__':
    window = Window()
    window.render()
