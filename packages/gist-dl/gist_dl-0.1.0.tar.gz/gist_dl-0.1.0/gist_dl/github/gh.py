import requests
import typer


class GithubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.user_agent = "Gist CLI"
        self.gist_memory = {}
        self.file_memory = {}

    def map_gist(self, gist):
        """
        This function maps a gist id to a normal int id in memory so user can easily select a gist
        """
        existing_length = len(self.gist_memory)
        self.gist_memory[gist["id"]] = existing_length + 1


    def map_file(self, file):
        """
        This function maps a file id to a normal int id in memory so user can easily select a file
        """
        existing_length = len(self.file_memory)
        self.file_memory[file] = existing_length + 1

    def get_user_gists(self, username, page=1):
        """
        grabs the gists of a user from github
        """
        typer.echo("Getting gists...")
        url = self.base_url + "/users/" + username + "/gists?page=" + str(page)
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=headers)
        # pprint(response.json())
        return response.json()

    def get_gist(self, gist_id):
        """
        grabs a specific gist from github
        """
        url = self.base_url + "/gists/" + gist_id
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_gist_file(self, gist_id, filename):
        url = self.base_url + "/gists/" + gist_id
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=headers)
        response = response.json()
        for file in response["files"]:
            if file == filename:
                return response["files"][file]["raw_url"]
        return None

    def download_file(self, url, path):
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=headers)
        with open(path, "w") as f:
            f.write(response.text)
        return True

    def get_gist_files(self, gist_id):
        url = self.base_url + "/gists/" + gist_id
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=headers)
        response = response.json()
        files = []
        for file in response["files"]:
            files.append(file)
        return files

    def get_gist_file_content(self, gist_id, filename):
        url = self.base_url + "/gists/" + gist_id
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=headers)
        response = response.json()
        for file in response["files"]:
            if file == filename:
                return response["files"][file]["content"]
        return None
