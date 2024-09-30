import simple_draw as sd

sd.resolution = (1920, 1080)
start_p = sd.get_point(600, 300)
n = 2
angle = 0


def fractal(n, x1, y1, x2, y2):
    if n == 0:  
        sd.line(sd.Point(x1, y1), sd.Point(x2, y2), width=1)
    else:  
        x3 = (x1 + x2) / 2 + (y2 - y1) / 2
        y3 = (y1 + y2) / 2 - (x2 - x1) / 2

        fractal(n - 1, x1, y1, x3, y3)
        fractal(n - 1, x3, y3, x2, y2)

fractal(n, 900, 500, 700, 500)

sd.pause()