from woodoku.utils import get_all_shapes_from_file
from config import CONFIG_FILE


def main() -> None:
    for shape in get_all_shapes_from_file(CONFIG_FILE):
        print(shape)


if __name__ == "__main__":
    main()
