import typer
from gist_dl.github.gh import GithubClient


class Gist:
    def __init__(self):
        pass

    def greeting(self):
        typer.echo("Welcome to Gist CLI")
        typer.echo("Usage:")

        typer.echo("Listing all gists of a user")
        typer.echo("gist <username>")
        typer.echo("Example: gist fauzaanu")

    def get_command(self):
        return typer.prompt("Enter a command: ")

    def list_all_gists(self, username):
        client = GithubClient()
        page = 1
        while True:
            gists = client.get_user_gists(username, page=page)
            if len(gists) == 0:
                break
            for gist in gists:
                client.map_gist(gist)
                typer.echo(
                    f"{client.gist_memory[gist['id']]}: {gist['description']}"
                )
            page += 1
        typer.echo("Select a gist by typing the number")
        gist_number = typer.prompt("Enter a gist number: ")
        gist_id = None
        for key, value in client.gist_memory.items():
            if value == int(gist_number):
                gist_id = key
                break
        if gist_id is None:
            typer.echo("Invalid gist number")
            return
        files = client.get_gist_files(gist_id)
        for file in files:
            print(file)
            client.map_file(file)
            typer.echo(
                f"{client.file_memory[file]}: {file}"
            )

        filenum = typer.prompt("Enter a file number: ")
        filename = None
        for key, value in client.file_memory.items():
            if value == int(filenum):
                filename = key
                break

        url = client.get_gist_file(gist_id, filename)
        if url is None:
            typer.echo("Invalid filename")
            return
        typer.echo("Downloading file...")
        client.download_file(url, filename)
        typer.echo("File downloaded")

    def process_command(self, command):
        if command[0] == "gist":

            if len(command) == 2:
                username = command[1]
                self.list_all_gists(username)

            # elif len(command) == 3:
            # TODO: implement this
            #     username = command[1]
            #     filename = command[2]
            #     self.list_specific_gist(username, filename)
            # This comment is for the people on twitter who said not to write TODOs in code comments
            else:
                typer.echo("Invalid command")
