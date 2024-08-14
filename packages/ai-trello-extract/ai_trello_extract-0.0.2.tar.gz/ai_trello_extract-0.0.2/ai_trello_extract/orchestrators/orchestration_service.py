import json
import os

from ai_trello_extract.formatters.generate_markdown import generate_markdown
from ai_trello_extract.services.trello_service import TrelloService


class OrchestrationService:
    def __init__(self, trello_service: TrelloService):
        """
        Initializes the OrchestrationService with a TrelloService instance.

        Args:
            trello_service (TrelloService): The service to interact with Trello API.
        """
        self.trello_service = trello_service

    def write_board_markdown_to_file(self, board_name: str, directory: str) -> str:
        """
        Generates markdown for a Trello board and writes it to a file.

        Args:
            board_name (str): The name of the Trello board.
            directory (str): The directory where the file will be saved.

        Returns:
            str: The path to the file where the markdown was written.
        """
        markdown_content = self.get_board_markdown(board_name)
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(directory, f"{board_name} Status Trello Board.txt")
        with open(file_path, "w") as file:
            file.write(markdown_content)  # Write the markdown content to the file
        return file_path

    def get_board_markdown(self, board_name: str) -> str:
        """
        Retrieves the markdown representation of a Trello board.

        Args:
            board_name (str): The name of the Trello board.

        Returns:
            str: The markdown content of the board.
        """
        board = self.trello_service.get_board_by_name(board_name)
        return generate_markdown(self.trello_service.extract_cards_info(board))

    def write_board_json_to_file(self, board_name: str, directory: str) -> str:
        """
        Retrieves the JSON representation of a Trello board and writes it to a file.

        Args:
            board_name (str): The name of the Trello board.
            directory (str): The directory where the file will be saved.

        Returns:
            str: The path to the file where the JSON was written.
        """
        board_json = self.get_board_json(board_name)

        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(directory, f"{board_name} Trello.json")
        with open(file_path, "w") as file:
            json.dump(board_json, file, indent=2)  # Write the JSON content to the file

        return file_path

    def get_board_json(self, board_name: str):
        """
        Retrieves the JSON representation of a Trello board.

        Args:
            board_name (str): The name of the Trello board.

        Returns:
            dict: The JSON content of the board.
        """
        board = self.trello_service.get_board_by_name(board_name)
        categorized_lists = self.trello_service.extract_cards_info(board)
        return categorized_lists.to_dict()
