import pygame
import random

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

                    print(f"Swapped pieces at indices {indecies}")


    pygame.quit()

if __name__ == "__main__":
    main("dog.jpg", 4)  # Ensure the image path is correct
