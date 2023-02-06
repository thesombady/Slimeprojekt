import os
from PIL import Image
def simulation():
        frames = []
        imgs = os.listdir("images")
        for i in imgs:
            new_frame = Image.open(f"images\\{i}")
            frames.append(new_frame)
        frames[0].save("slime.gif", format='GIF', append_images=frames[1:], save_all=True, duration=round(len(imgs) / 100), loop=0)
        """
        for img in imgs:
            os.remove("images\\{}".format(img))
        """

simulation()