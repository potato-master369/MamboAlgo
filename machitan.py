from PIL import Image
import sys
import io
def mamboify(n, outf):
    r = []
    with Image.open("mambo.jpg") as f:
        print(f.mode)
        p = f.convert("L").load()
        w, h = f.size
        
        for x in range(w):
            for y in range(h):
                r.append({
                    "X": x,
                    "Y": y,
                    "p": p[x, y],
                })
    r.sort(key=lambda px: px["p"])
    r2 = []

    with Image.open(io.BytesIO(n.read())).resize((512, 512), Image.Resampling.LANCZOS) as f:
        f.save("static/original.png")
        print(f.mode)
        c = f.convert("RGB")
        p = f.convert("L").load()
        w, h = f.size
        
        for x in range(w):
            for y in range(h):
                red, g, b = c.getpixel((x, y))
                r2.append({
                    "X": x,
                    "Y": y,
                    "p": p[x, y],
                    "red": red,
                    "g": g,
                    "b": b
                })

    r2.sort(key=lambda px: px["p"])

    out = Image.new(mode='RGB', size=(512, 512))

    for i in range(len(r)):
        out.putpixel((r[i]["X"], r[i]["Y"]), (r2[i]["red"], r2[i]["g"], r2[i]["b"]))

    out.save(fp=f"static/{outf}")
    print(f"Saved as static/{outf}!")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        mamboify(sys.argv[1], "out.jpg")
    elif len(sys.argv) == 3:
        mamboify(sys.argv[1], sys.argv[2])
    else:
        print("ERROR: expected python machitan.py [OPT: INPUT FILE] [OPT: OUTPUT FILE]")