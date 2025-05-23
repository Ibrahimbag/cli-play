from blessed import Terminal
import cv2
from sys import argv, exit
from time import sleep
from ffpyplayer.player import MediaPlayer
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
        cap = cv2.VideoCapture(file_path)
        player = MediaPlayer(file_path)

        if not cap.isOpened():
            exit("Error: Could not open video.")

        while self.term.inkey(timeout=0) != "q":
            success, image = cap.read()
            if not success:
                break

            height, width = self.term.height, self.term.width
            image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

            output = []
            for y in range(height):
                for x in range(width):
                    b, g, r = image[y, x]
                    output.append(
                        self.term.move(y, x) + self.term.on_color_rgb(r, g, b) + " "
                    )

            print("".join(output))

            fps = 1 / cap.get(cv2.CAP_PROP_FPS)
            audio_frame, val = player.get_frame()
            if val != "eof" and audio_frame is not None:
                _, pts = audio_frame
                delay = fps - (player.get_pts() - pts)
                sleep(max(0, delay))
            else:
                sleep(fps)

        cap.release()

    def __show_picture(self, file_path):
        image = cv2.imread(file_path)
        if image is None:
            exit("Could not read the image")

        old_height, old_width = 0, 0
        while self.term.inkey(timeout=0) != "q":
            height, width = self.term.height, self.term.width
            if height != old_height or width != old_width:
                image = cv2.imread(file_path)
                image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

            output = []
            for y in range(height):
                for x in range(width):
                    b, g, r = image[y, x]
                    output.append(
                        self.term.move(y, x) + self.term.on_color_rgb(r, g, b) + " "
                    )

            if height != old_height or width != old_width:
                print("".join(output))
                old_height, old_width = height, width

            sleep(1)


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
