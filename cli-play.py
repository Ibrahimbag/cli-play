from blessed import Terminal
import cv2
from sys import argv, exit
from time import sleep
from ffpyplayer.player import MediaPlayer


def play_video(term):
    cap = cv2.VideoCapture(argv[1])
    player = MediaPlayer(argv[1])

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit(3)

    while term.inkey(timeout=0) != "q":
        success, image = cap.read()
        if not success:
            break

        height, width = term.height, term.width
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

        output = []
        for y in range(height):
            for x in range(width):
                b, g, r = image[y, x]
                output.append(term.move(y, x) + term.on_color_rgb(r, g, b) + " ")

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
        argv[1]
    except IndexError:
        print(f"Usage: {argv[0]} [FILE_NAME]")
        exit(1)

    term = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        play_video(term)


if __name__ == "__main__":
    main()
