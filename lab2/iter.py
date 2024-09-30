import simple_draw as sd

sd.resolution = (1920, 1080)
#sd.resolution = (900, 600)

n = 10
start = 'F++F++F++F++'
start_p = sd.get_point(600, 500)
angle = 0

for i in range(n):
    start = start.replace('F', '-F++F-')

for k in start:
    if k == '+':
        angle -= 45
    elif k == '-':
        angle += 45
    else:
        v = sd.get_vector(start_point=start_p, angle=angle, length=3)
        v.draw()

        start_p = v.end_point

sd.pause()
