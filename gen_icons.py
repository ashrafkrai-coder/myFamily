from PIL import Image, ImageDraw

PHOTO = 'abah-cek.jpg'

def gradient(W):
    img = Image.new('RGBA', (W, W))
    px = img.load()
    c1 = (99, 102, 241)
    c2 = (236, 72, 153)
    for y in range(W):
        for x in range(W):
            t = (x + y) / (2 * W)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            px[x, y] = (r, g, b, 255)
    return img

def circle_photo(diam):
    im = Image.open(PHOTO).convert('RGB')
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    im = im.resize((diam, diam), Image.LANCZOS)
    mask = Image.new('L', (diam, diam), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diam - 1, diam - 1), fill=255)
    return im, mask

def make(size, frac, out):
    W = size
    bg = gradient(W)
    diam = int(W * frac)
    photo, mask = circle_photo(diam)
    ring = Image.new('RGBA', (diam + 18, diam + 18), (255, 255, 255, 255))
    pos = ((W - (diam + 18)) // 2, (W - (diam + 18)) // 2)
    bg.paste(ring, pos)
    bg.paste(photo, (pos[0] + 9, pos[1] + 9), mask)
    bg.save(out)
    print('saved', out)

make(192, 0.72, 'icon-192.png')
make(512, 0.72, 'icon-512.png')
make(512, 0.56, 'icon-maskable-512.png')
