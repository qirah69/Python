from repo.repo_book import RepoBook
from repo.repo_client import RepoClient
from controller.service_book import ServiceBook
from controller.service_client import ServiceClient
from ui.ui import Console

if __name__ == "__main__":
    # 1. Initialize Repositories (The storage)
    book_repo = RepoBook()
    client_repo = RepoClient()

    # 2. Initialize Services (The logic, injected with repos)
    book_service = ServiceBook(book_repo)
    client_service = ServiceClient(client_repo)

    # 3. Initialize UI (The menu, injected with services)
    console = Console(book_service, client_service)

    # 4. Start the Application
    console.run_console()