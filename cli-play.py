from blessed import Terminal
import cv2
from sys import argv, exit
from time import sleep
from ffpyplayer.player import MediaPlayer


class cli_play:
    def __init__(self):
        self.term = Terminal()

    def play_video(self, file_name):
        cap = cv2.VideoCapture(file_name)
        player = MediaPlayer(file_name)

        if not cap.isOpened():
            print("Error: Could not open video.")
            exit(3)

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


def main():
    try:
        file_name = argv[1]
    except IndexError:
        print(f"Usage: {argv[0]} [FILE_NAME]")
        exit(1)

    app = cli_play()
    with app.term.fullscreen(), app.term.cbreak(), app.term.hidden_cursor():
        app.play_video(file_name)


if __name__ == "__main__":
    main()
