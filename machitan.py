from PIL import Image
import sys
import io
import numpy as np
import subprocess
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
    if type(n) == str:
        with Image.open(n).resize((512, 512), Image.Resampling.LANCZOS) as f:
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
    else:
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

    
    old_C = np.array([[p["X"], p["Y"]] for p in r2], dtype=np.float32)
    new_C = np.array([[p["X"], p["Y"]] for p in r], dtype=np.float32)
    colors = np.array([[p["red"], p["g"], p["b"]] for p in r2], dtype=np.uint8)
    delta = new_C - old_C
    for i in range(65):
        # Linear interpolation factor
        t = i / 64
        # Compute all positions in one go
        positions = (old_C + t * delta).astype(int)

        # Create blank frame as NumPy array
        frame_array = np.zeros(((512, 512)[1], (512, 512)[0], 3), dtype=np.uint8)

        # Clip positions to canvas bounds
        mask = (
            (positions[:,0] >= 0) & (positions[:,0] < (512, 512)[0]) &
            (positions[:,1] >= 0) & (positions[:,1] < (512, 512)[1])
        )
        valid_positions = positions[mask]
        valid_colors = colors[mask]

        # Assign colors in bulk
        frame_array[valid_positions[:,1], valid_positions[:,0]] = valid_colors

        # Convert back to PIL and save
        frame = Image.fromarray(frame_array, "RGB")
        frame.save(f"animation/{i}.png")

    out.save(fp=f"static/{outf}")
    subprocess.run([
        "ffmpeg",
        "-framerate", "6.4",
        "-i", "animation/%d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "static/anim.mp4",
        "-y"
    ])

    print(f"Saved as static/{outf}!")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        mamboify(sys.argv[1], "out.jpg")
    elif len(sys.argv) == 3:
        mamboify(sys.argv[1], sys.argv[2])
    else:
        print("ERROR: expected python machitan.py [OPT: INPUT FILE] [OPT: OUTPUT FILE]")