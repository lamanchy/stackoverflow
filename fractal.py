from PIL import Image, ImageDraw

size = (1000, 1000)

image = Image.open("/home/lamanchy/Downloads/aaa.jpg", "r")
image = Image.new("RGBA", size, (255, 255, 255, 255))

size = image.size

draw = ImageDraw.Draw(image)


def non_repeating(i):
    if i % 3 == 0: return 0
    if i % 3 == 1: return 1
    return non_repeating(i // 3)


def draw_line(pos):
    pos = [(p[0] * size[0], p[1] * size[1]) for p in pos]
    print(pos)
    draw.line(pos, fill="black")


def get_ksqr(pos, height):
    width = height / 2
    base = [pos, (pos[0] - width / 2, pos[1] + height / 2), (pos[0], pos[1] + height), (pos[0] + width / 2, pos[1] + height / 2)]
    base += [base[0]]
    return base


i = 0
def draw_fractal(pos, height, first=False):
    if height*size[1] < 1: return
    global i
    if not first: draw_line(get_ksqr(pos, height))
    i += 1
    width = height / 2
    draw_fractal((pos[0], pos[1] + height / 10), height / 5)
    draw_fractal((pos[0], pos[1] + 2 * height / 5), height / 5)
    draw_fractal((pos[0] - width/5, pos[1] + height / 5), height / 2.5)
    draw_fractal((pos[0] + width/5, pos[1] + height / 5), height / 2.5)
    draw_fractal((pos[0], pos[1] + 3 * height / 5), height / 2.5)


draw_fractal((0.5, 0.0), 1.0, True)

image.show()




