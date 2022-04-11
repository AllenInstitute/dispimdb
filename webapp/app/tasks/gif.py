import os
import sys

from PIL import Image

default_config = {
    "scope": "ispim1"
    "size_x": 512,
    "size_y": 512,
    "ds_factor": 4
}

def print_dir_contents(gif_path, row_positions):
    for pos in row_positions:
        pos_path = os.path.join(gif_path, pos)
        gifs = os.listdir(pos_path)

        for gif in gifs:
            im = Image.open(os.path.join(pos_path, gif))
            im = im.convert(mode="L")

            print(gif)
            print(im.size)
            print(im.mode)

gif_path = "/home/samk/acstorage/practice/gifs"
col_positions = os.listdir(gif_path)

#num_columns = len(col_positions)
#num_rows = len(os.listdir(os.path.join(gif_path, col_positions[0])))
num_columns = 8
num_rows = 8
size = (512, 512)
num_frames = 10
ds_factor = 4

overview_size = (int(num_rows * (size[0] / ds_factor)), int(num_columns * (size[1] / ds_factor)))
print(overview_size)

overview_frames = []

for k in range(num_frames):
    frame = Image.new("L", overview_size)

    for j in range(len(col_positions)):
        pos_path = os.path.join(gif_path, col_positions[j])
        gifs = os.listdir(pos_path)
        gifs.sort()

        for i in range(len(gifs)):
            print(gifs[i])
            im = Image.open(os.path.join(pos_path, gifs[i]))
            im.seek(im.tell() + k)
            im = im.resize((int(size[0] / ds_factor), int(size[1] / ds_factor)))
            frame.paste(im, (im.size[0] * i, im.size[1] * j))
    
    overview_frames.append(frame)

print(len(overview_frames))
overview_frames[0].save("/home/samk/acstorage/practice/overview.gif",
                        save_all=True,
                        append_images=overview_frames[1:],
                        duration=50,
                        loop=0)