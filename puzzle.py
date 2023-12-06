import pygame
import random
import cv2
import pyautogui
from multiprocessing import Process


def find_and_move_to_face():
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
 
    # Start the video capture
    video_capture = cv2.VideoCapture(0)
 
    while True:
        # Read a frame from the video capture
        ret, frame = video_capture.read()
 
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
 
        # Iterate over the detected faces
        for (x, y, w, h) in faces:
            # Get the center position of the face
            face_center_x = x + w // 2
            face_center_y = y + h // 2
 
            # Move the cursor to the center of the face
            pyautogui.moveTo(face_center_x, face_center_y)
 
        # Display the frame with face detection
        #cv2.imshow('Face Detection', frame)
 
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    # Release the video capture and close the window
    video_capture.release()
    cv2.destroyAllWindows()


def load_and_scale_image(image_path, max_width, max_height):
    image = pygame.image.load(image_path)
    image_width, image_height = image.get_size()

    # Scale the image if it's larger than the screen
    if image_width > max_width or image_height > max_height:
        scaling_factor = min(max_width / image_width, max_height / image_height)
        new_size = (int(image_width * scaling_factor), int(image_height * scaling_factor))
        image = pygame.transform.scale(image, new_size)

    return image

def slice_image(image, num_pieces):
    image_width, image_height = image.get_size()
    piece_width = image_width // num_pieces
    piece_height = image_height // num_pieces

    pieces = []
    for i in range(num_pieces):
        for j in range(num_pieces):
            rect = pygame.Rect(j * piece_width, i * piece_height, piece_width, piece_height)
            piece = image.subsurface(rect)
            pieces.append(piece)

    return pieces

def main(image_path, num_pieces):
    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puzzle Game")

    # Load and scale the image
    image = load_and_scale_image(image_path, screen_width, screen_height)
    # Slice the image
    pieces = slice_image(image, num_pieces)

    orig = pieces.copy()

    # Shuffle the pieces
    random.shuffle(pieces)

    # Display the pieces
    piece_width, piece_height = pieces[0].get_size()
    for i, piece in enumerate(pieces):
        x = (i % num_pieces) * piece_width
        y = (i // num_pieces) * piece_height
        screen.blit(piece, (x, y))

    pygame.display.flip()

    running = True
    indecies = []  # Move these outside the event loop
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            complete = True
            for i in range (len(pieces)):
                if pieces[i] != orig[i]:
                    complete = False
            if complete:
                print("You did it")
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get current mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculate the index of the puzzle piece the mouse is over
                column = mouse_x // piece_width
                row = mouse_y // piece_height
                piece_index = row * num_pieces + column
                indecies.append(piece_index)
                count += 1

                if count == 2:
                    pieces[indecies[0]], pieces[indecies[1]] = pieces[indecies[1]], pieces[indecies[0]]
                    count = 0

                    for i, piece in enumerate(pieces):
                        x = (i % num_pieces) * piece_width
                        y = (i // num_pieces) * piece_height
                        screen.blit(piece, (x, y))

                    pygame.display.flip()
                    indecies = []


    pygame.quit()


if __name__ == "__main__":
    image_path = "dog.jpg"
    num_slices = 5

    cursor_process = Process(target=find_and_move_to_face)
    image_process = Process(target=main, args=(image_path, num_slices))

    #start process
    
    image_process.start()
    cursor_process.start()

    
    image_process.join()
    cursor_process.join()
