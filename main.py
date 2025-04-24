from src.db.database_manager import create_player, get_player, get_player_by_tg_id, add_image


def main():
    image_path = r"C:\Users\Ksenia\PycharmProjects\pythonProject8\Digital_transformation\src\правила1.png"

    add_image(image_path, "правила1")


if __name__ == "__main__":
    main()
