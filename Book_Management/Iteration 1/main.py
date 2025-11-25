if __name__ == "__main__":
    from ui.ui import Console
    from controller.service import ServiceBook
    from repo.repo import RepoBook

    repo = RepoBook()
    service = ServiceBook(repo)
    ui = Console(service)
    ui.run_console()