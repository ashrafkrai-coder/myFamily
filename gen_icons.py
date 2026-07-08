from PIL import Image, ImageDraw, ImageFont

C1 = (99, 102, 241)   # indigo
C2 = (236, 72, 153)   # pink


def gradient(W):
    img = Image.new('RGBA', (W, W))
    px = img.load()
    for y in range(W):
        for x in range(W):
            t = (x + y) / (2 * W)
            r = int(C1[0] + (C2[0] - C1[0]) * t)
            g = int(C1[1] + (C2[1] - C1[1]) * t)
            b = int(C1[2] + (C2[2] - C1[2]) * t)
            px[x, y] = (r, g, b, 255)
    return img


def rounded_mask(W, radius):
    m = Image.new('L', (W, W), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, W - 1, W - 1], radius=radius, fill=255)
    return m


def coin(draw, cx, cy, R, font, text):
    # white coin
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(255, 255, 255, 255))
    # inner subtle ring
    draw.ellipse([cx - R * 0.82, cy - R * 0.82, cx + R * 0.82, cy + R * 0.82],
                 outline=(99, 102, 241, 60), width=max(2, int(R * 0.04)))
    # RM text in primary color, centered
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    tw, th = r - l, b - t
    draw.text((cx - tw / 2 - l, cy - th / 2 - t), text, font=font, fill=C1)


def make(size, frac, maskable, out):
    W = size
    bg = gradient(W)
    cx = cy = W // 2
    R = int(W * frac / 2)
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', int(R * 1.05))
    except Exception:
        font = ImageFont.load_default()
    coin(ImageDraw.Draw(bg), cx, cy, R, font, 'RM')
    if not maskable:
        bg.putalpha(rounded_mask(W, int(W * 0.22)))
    bg.save(out)
    print('saved', out)


make(192, 0.62, False, 'icon-192.png')
make(512, 0.62, False, 'icon-512.png')
make(512, 0.46, True, 'icon-maskable-512.png')
