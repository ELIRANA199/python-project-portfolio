
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps


def load_image(path):
    try:
        image = Image.open(path)
        image.load()
        return image
    except (OSError, ValueError) as error:
        print(f"Cannot open image: {error}")
        return None


def save_image(image, output_path):
    try:
        image.save(output_path)
        print(f"Image saved successfully: {output_path}")
    except OSError as error:
        print(f"Could not save image: {error}")


def show_menu():
    print("\n===== IMAGE PROCESSING TOOL =====")
    print("1. Convert to Grayscale")
    print("2. Resize Image")
    print("3. Rotate Image")
    print("4. Apply Blur")
    print("5. Edge Detection")
    print("6. Flip Image")
    print("7. Exit")


def process_image(image, choice):
    if choice == "1":
        return ImageOps.grayscale(image)

    elif choice == "2":
        try:
            width = int(input("Enter new width: "))
            height = int(input("Enter new height: "))

            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive.")

            return image.resize((width, height))

        except ValueError as error:
            print(f"Invalid dimensions: {error}")
            return None

    elif choice == "3":
        try:
            angle = float(input("Enter rotation angle: "))
            return image.rotate(angle, expand=True)
        except ValueError:
            print("Please enter a valid number.")
            return None

    elif choice == "4":
        return image.filter(ImageFilter.GaussianBlur(radius=3))

    elif choice == "5":
        grayscale = ImageOps.grayscale(image)
        return grayscale.filter(ImageFilter.FIND_EDGES)

    elif choice == "6":
        return ImageOps.mirror(image)

    else:
        print("Invalid option.")
        return None


def main():
    print("Welcome to Image Processing Tool!")

    raw_path = input("Enter image path: ").strip().strip('"')
    image_path = Path(raw_path).expanduser()

    if not image_path.is_file():
        print("Image file not found.")
        return

    image = load_image(image_path)

    if image is None:
        return

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "7":
            print("Goodbye!")
            break

        result = process_image(image, choice)

        if result is None:
            continue

        output_name = (
            f"{image_path.stem}_edited_{choice}"
            f"{image_path.suffix}"
        )

        output_path = image_path.with_name(output_name)
        save_image(result, output_path)


if __name__ == "__main__":
    main()
