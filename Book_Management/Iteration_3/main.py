"""
Main entry point for the Book Management System application.

This module initializes all repositories, services, and the UI, then starts the application.
It follows the layered architecture pattern with repositories, services, and UI layers.
"""

from repo.repo_book import RepoBook
from repo.repo_client import RepoClient
from repo.repo_rental import RepoRental
from controller.service_book import ServiceBook
from controller.service_client import ServiceClient
from controller.service_rental import ServiceRental

from ui.ui import Console

if __name__ == "__main__":
    # 1. Initialize Repositories (The storage)
    book_repo = RepoBook()
    client_repo = RepoClient()
    rental_repo = RepoRental()

    # 2. Initialize Services (The logic, injected with repos)
    book_service = ServiceBook(book_repo)
    client_service = ServiceClient(client_repo)
    rental_service = ServiceRental(rental_repo, book_repo, client_repo)

    # 3. Initialize UI (The menu, injected with services)
    console = Console(book_service, client_service, rental_service)

    # 4. Start the Application
    console.run_console()