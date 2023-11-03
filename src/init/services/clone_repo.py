import subprocess
import os

def clone_repository(username, repo_name, token_user):
        try:
            current_directory = os.getcwd()
            file_name = 'Dockerfile'
            repos_folder = os.path.join(current_directory, 'deployment', repo_name)
            print(f"token_user: {token_user}")
            print(f"username: {username}")
            print(f"repo_name: {repo_name}")
            clone_url = f"https://{token_user}@github.com/{username}/{repo_name}.git"
            file_path = os.path.join(repos_folder, file_name)
            subprocess.run(["git", "clone", clone_url, repos_folder], check=True)
            with open('./docker/dockerfile', 'r') as firstfile, open(file_path, 'a') as secondfile:
                for line in firstfile:
                    secondfile.write(line)
            print(repos_folder)
            return repos_folder
        except subprocess.CalledProcessError as e:
            print(f"Subprocess error: {e}")
            return None  
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
