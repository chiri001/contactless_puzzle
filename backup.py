from PIL import Image
import matplotlib.pyplot as plt
import random
import cv2
import pyautogui
from multiprocessing import Process
import random
import time

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

def slice_image(image_path, num_slices):
    # Open the image
    original_image = Image.open(image_path)
    
    # Get the size of the image
    width, height = original_image.size

    # Calculate the size of each square
    slice_size = min(width, height) // num_slices

    # Create a list of indices to shuffle
    indices = list(range(num_slices**2))
    random.shuffle(indices)

    # Create a new figure for plotting
    fig, axes = plt.subplots(num_slices, num_slices, figsize=(8, 7))

    for index, ax in zip(indices, axes.flatten()):
        # Calculate the row and column for the current index
        i = index // num_slices
        j = index % num_slices

        # Calculate the coordinates for slicing
        left = j * slice_size
        upper = i * slice_size
        right = left + slice_size
        lower = upper + slice_size

        # Crop the image to get a square slice
        slice_image = original_image.crop((left, upper, right, lower))

        # Display the slice
        ax.imshow(slice_image)
        ax.axis('off')  # Turn off axis labels for better visualization

    plt.savefig("sliced_image.png", bbox_inches='tight', pad_inches=0.1)

def highlight_puzzle_piece(mouse_pos, num_slices):
    width, height = plt.figaspect(num_slices)
    slice_width = mouse_pos[0] // (width / num_slices)
    slice_height = mouse_pos[1] // (height / num_slices)

    # Calculate the index of the puzzle piece under the mouse cursor
    piece_index = int(slice_height * num_slices + slice_width)

    # Highlight the corresponding puzzle piece in the saved image
    image = Image.open("sliced_image.png")
    width, height = image.size
    slice_size = min(width, height) // num_slices

    i, j = piece_index // num_slices, piece_index % num_slices
    left, upper = j * slice_size, i * slice_size
    right, lower = left + slice_size, upper + slice_size

    highlighted_piece = image.crop((left, upper, right, lower))

    # Display the highlighted puzzle piece
    plt.figure()
    plt.imshow(highlighted_piece)
    plt.axis('off')
    plt.show()
    plt.pause(0.01)  # Pause for a short duration to allow for updating the display


if __name__ == "__main__":
    image_path = "dog.jpg"
    num_slices = 5

    cursor_process = Process(target=find_and_move_to_face)
    image_process = Process(target=slice_image, args=(image_path, num_slices))

    #start process
    
    image_process.start()
    cursor_process.start()

    
    image_process.join()
    cursor_process.join()

    while True:
        mouse_pos = pyautogui.position()
        highlight_puzzle_piece(mouse_pos, num_slices)

    # # Load the pre-trained face detection model
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # # Start the video capture
    # video_capture = cv2.VideoCapture(0)

    # face_queue = queue.Queue()
    # face_thread = threading.Thread(target=find_faces, args=(face_cascade, video_capture, face_queue))
    # face_thread.start()

    # display_frames_and_move_cursor(face_queue)
    # slice_image(image_path, num_slices)

    # face_thread.join()
