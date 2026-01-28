from blessed import Terminal
from sys import argv, exit
from time import sleep
from ffpyplayer.player import MediaPlayer
from ffpyplayer.pic import SWScale, ImageLoader
import numpy as np
from pymediainfo import MediaInfo


class cli_play:
    def __init__(self):
        self.term = Terminal()

    def run(self, file_path):
        try:
            file_info = MediaInfo.parse(file_path)
        except:
            exit("file not found")

        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            for track in file_info.tracks:
                if track.track_type == "Video":
                    self.__play_video(file_path)
                elif track.track_type == "Image":
                    self.__show_picture(file_path)

    def __play_video(self, file_path):
        player = MediaPlayer(file_path)
        sws = None
        prev_height, prev_width = 0, 0

        while self.term.inkey(timeout=0) != "q":
            height, width = self.term.height, self.term.width

            frame, val = player.get_frame()

            if val == "eof":
                break
            if frame is None:
                sleep(0.01)
                continue

            img, _ = frame

            if sws is None or width != prev_width or height != prev_height:
                x, y = img.get_size()
                sws = SWScale(x, y, img.get_pixel_format(), ow=width, oh=height)
                prev_width, prev_height = width, height

            scaled_image = sws.scale(img)

            image_buffer = scaled_image.to_bytearray()[0]

            pixel_array = np.frombuffer(image_buffer, dtype=np.uint8)

            rgb_image = pixel_array.reshape((height, width, 3))

            output = []
            for y in range(height):
                for x in range(width):
                    r, g, b = rgb_image[y, x]
                    output.append(
                        self.term.move(y, x) + self.term.on_color_rgb(r, g, b) + " "
                    )

            print("".join(output))

            sleep(val)

        player.close_player()

    def __show_picture(self, file_path):
        loader = ImageLoader(file_path)
        frame = loader.next_frame()[0]

        src_w, src_h = frame.get_size()
        pix_fmt = frame.get_pixel_format()
        ofmt = "rgb24"

        prev_height, prev_width = 0, 0

        sws = None
        rgb_image = None

        output = []

        while self.term.inkey(timeout=0) != "q":
            height, width = self.term.height, self.term.width

            if sws == None or height != prev_height or width != prev_width:
                sws = SWScale(src_w, src_h, pix_fmt, ofmt=ofmt, ow=width, oh=height)
                scaled_frame = sws.scale(frame)

                frame_buffer = scaled_frame.to_bytearray()[0]

                pixel_array = np.frombuffer(frame_buffer, dtype=np.uint8)
                rgb_image = pixel_array.reshape((height, width, 3))

                prev_height, prev_width = height, width

                for y in range(height):
                    for x in range(width):
                        r, g, b = rgb_image[y, x]
                        output.append(
                            self.term.move(y, x) + self.term.on_color_rgb(r, g, b) + " "
                        )

                print("".join(output))

            sleep(0.5)


def main():
    try:
        file_path = argv[1]
    except IndexError:
        print(f"Usage: {argv[0]} [file_path]")
        exit(1)

    app = cli_play()
    app.run(file_path)


if __name__ == "__main__":
    main()
