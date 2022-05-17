# from object_3d import Object3D, get_object_from_file, create_axes
# from camera import Camera
# from projection import Projection
# import pygame as pg
import numpy as np
import pygame as pg


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
    return np.array([[x], [y], [z]])


def Homogenious_Vec3(x, y, z):
    return np.array([[x], [y], [z], [1]])


def scale_homogenious_vec3(array):
    return array / array[3]


BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 100)
RED = (255, 0, 0, 100)
GREEN = (0, 255, 0, 100)
BLUE = (0, 0, 255, 100)
EMPTY = pg.Color(0, 0, 0, 0)


class Window:
    def __init__(self):
        self.ASPECT_RATIO = 2.0
        self.WIDTH = 1200
        self.HEIGHT = self.WIDTH // self.ASPECT_RATIO
        self.RES = self.WIDTH, self.HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2

        self.FPS = 60

        # pg.init()
        # self.screen = pg.display.set_mode(self.RES)
        # self.clock = pg.time.Clock()
        self.scene = Scene()

        self.scene.add_Camera()

        self.scene.add_object(PointObject(0, 1, 1, name="a"))
        self.scene.add_object(PointObject(0, 2, 1, name="b"))
        self.scene.add_object(PointObject(1, 2, 1, name="c"))
        self.scene.add_object(PointObject(1, 1, 1, name="d"))

        self.scene.add_object(PointObject(0, 1, 2, name="e"))
        self.scene.add_object(PointObject(0, 2, 2, name="f"))
        self.scene.add_object(PointObject(1, 2, 2, name="g"))
        self.scene.add_object(PointObject(1, 1, 2, name="h"))

        self.scene.camera.translate(Vec3(0, -5, 1.5))
        self.scene.camera.yaw(np.pi / 2)

        self.screen = pg.display.set_mode(self.RES)
        self.surface = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)

        self.event_handlers = []
        self.clock = pg.time.Clock()

    def attach_event_handler(self, handler):
        self.event_handlers.append(handler)

    def handle_events(self):
        for event in pg.event.get():
            for handler in self.event_handlers:
                handler(event)

    def render(self):
        self.scene.render()

    def draw(self):

        self.screen.fill(pg.Color("darkslategray"))
        self.surface.fill(EMPTY)
        for name, object in self.scene.objects.items():
            pg.draw.circle(
                self.surface,
                WHITE,
                (
                    object.points_screen_floats[0][0] * self.WIDTH,
                    object.points_screen_floats[1][0] * self.HEIGHT,
                ),
                10,
            )

        self.screen.blit(self.surface, (0, 0))
        pg.display.flip()

    def run(self):
        while True:
            self.draw()
            self.handle_events()
            pg.display.set_caption(str(int(self.clock.get_fps())))
            self.clock.tick(self.FPS)


class Scene:
    def __init__(self):
        self.objects: list[Object3D] = {}

    def add_Camera(self, fov=np.pi / 6, AR=2):
        self.camera = Camera(fov=fov, AR=AR)

    def render(self):
        # apply individual object movments and recalculate transformation matrix
        # for name, object in self.objects.items():
        #     object.calculate_transformation_matrix()

        self.rotate_scene_into_camera_view()

        # project all points onto screen
        # draw

    def rotate_scene_into_camera_view(self):
        # rotate entire scene such that camera is at 0,0,0 and axis align
        self.camera.calculate_transformation_matrix()
        inverse_camera_matrix = self.camera.get_inverse_transformation_matrix()
        camera_projection_matrix = self.camera.projection_matrix

        for name, object in self.objects.items():
            object.calculate_points_in_camera_space(inverse_camera_matrix)
            object.calculate_points_projected(camera_projection_matrix)
            object.points_on_plane = scale_homogenious_vec3(object.points_projected)
            object.points_screen_floats = (
                self.camera.convert_projected_points_to_screen_floats(
                    object.points_on_plane
                )
            )
            # print(object.points_screen_floats)

    def add_object(self, object):
        self.objects[object.name] = object


class Object:
    def __init__(self):
        self.pos = Vec3(0.0, 0.0, 0.0)
        self.alpha = 0  # yaw angle (about z, how much x/y moves) z' = z
        self.beta = 0  # pitch angle (about y', how much x'/z' moves) y'' = y'
        self.gamma = 0  # roll angle (about x'', how much y''/z'' moves) x''' = x''
        self.calculate_transformation_matrix()

    def translate(self, vector):
        self.pos += vector

    def yaw(self, angle):
        self.alpha += angle

    def pitch(self, angle):
        self.beta += angle

    def roll(self, angle):
        self.gamma += angle

    def calculate_transformation_matrix(self):
        a = self.alpha
        b = self.beta
        y = self.gamma
        p, q, r = self.pos[0, 0], self.pos[1, 0], self.pos[2, 0]
        r1 = np.array(
            [
                [np.cos(a), -np.sin(a), 0, 0],
                [np.sin(a), np.cos(a), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        r2 = np.array(
            [
                [np.cos(b), 0, np.sin(b), 0],
                [0, 1, 0, 0],
                [-np.sin(b), 0, np.cos(b), 0],
                [0, 0, 0, 1],
            ]
        )
        r3 = np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(y), -np.sin(y), 0],
                [0, np.sin(y), np.cos(y), 0],
                [0, 0, 0, 1],
            ]
        )
        t0 = np.array(
            [
                [1, 0, 0, p],
                [0, 1, 0, q],
                [0, 0, 1, r],
                [0, 0, 0, 1],
            ]
        )
        self.transformation_matrix = t0 @ r3 @ r2 @ r1

    def get_inverse_transformation_matrix(self):
        return np.linalg.inv(self.transformation_matrix)


class Camera(Object):
    def __init__(self, fov=np.pi / 6, AR=2):
        super().__init__()

        self.FOV = fov
        self.AR = AR
        self.WIDTH = 2 * np.sin(self.FOV / 2) / 1
        self.HEIGHT = self.WIDTH / self.AR

        self.projection_matrix = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0]]
        )

    def convert_projected_points_to_screen_floats(self, points):
        points = points[1:3, :]
        points = points / np.array([[self.WIDTH], [-self.HEIGHT]]) + np.array(
            [[0.5], [0.5]]
        )
        return points


class Object3D(Object):
    def __init__(self, name, points, lines):
        super().__init__()
        self.name = name
        self._points_raw = points  # n x 4 ndarray
        self.points_on_plane = points
        self.points_screen_floats = points
        self.lines = lines  # list[list[ints]]

    def calculate_points_in_camera_space(self, inverse_camera_transformation_matrix):
        self.points_camera_space = (
            inverse_camera_transformation_matrix
            @ self.transformation_matrix
            @ self._points_raw
        )

    def calculate_points_projected(self, camera_projection_matrx):
        self.points_projected = camera_projection_matrx @ self.points_camera_space


class PointObject(Object3D):
    def __init__(self, x, y, z, name=""):
        super().__init__(name, Homogenious_Vec3(x, y, z), [])


def handle_quit(event):
    if event.type == pg.QUIT:
        exit()


if __name__ == "__main__":
    window = Window()
    window.attach_event_handler(handle_quit)
    window.run()
