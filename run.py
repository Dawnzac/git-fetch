import os
import shutil
from git import Repo
from pathlib import Path


WINGET_REPO_URL = "https://github.com/microsoft/winget-pkgs.git"
LOCAL_WINGET_REPO_PATH = "./wingetclone"  
YOUR_REPO_URL = "https://github.com/Dawnzac/git-fetch.git"
LOCAL_YOUR_REPO_PATH = "./wingetclone" 
APPS_TO_FETCH = ["Google.Chrome", "Mozilla.Firefox", "Microsoft.Edge"] 


def clone_or_pull_repo(repo_url, local_path):
    """Clone the repository if not already present; otherwise, pull latest changes."""
    if not os.path.exists(local_path):
        print(f"Cloning repository: {repo_url}")
        Repo.clone_from(repo_url, local_path)
    else:
        print(f"Pulling latest changes from: {repo_url}")
        repo = Repo(local_path)
        repo.git.pull()


def fetch_latest_apps(apps, source_repo_path, dest_repo_path):
    """Fetch the latest versions of specific applications."""
    for app in apps:
        app_path = Path(source_repo_path) / "manifests" / app[0].lower() / app
        if app_path.exists():
            dest_path = Path(dest_repo_path) / "manifests" / app[0].lower() / app
            print(f"Copying {app} to personal repo...")
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(app_path, dest_path)
        else:
            print(f"Application {app} not found in Winget repository.")


def commit_and_push_changes(repo_path, commit_message):
    """Commit and push changes to the personal repository."""
    repo = Repo(repo_path)
    if repo.is_dirty(untracked_files=True):
        print("Committing and pushing changes...")
        repo.git.add(A=True)
        repo.index.commit(commit_message)
        repo.git.push()
    else:
        print("No changes to commit.")


def main():
    
    clone_or_pull_repo(WINGET_REPO_URL, LOCAL_WINGET_REPO_PATH)
  
    clone_or_pull_repo(YOUR_REPO_URL, LOCAL_YOUR_REPO_PATH)

    fetch_latest_apps(APPS_TO_FETCH, LOCAL_WINGET_REPO_PATH, LOCAL_YOUR_REPO_PATH)
   
    commit_and_push_changes(LOCAL_YOUR_REPO_PATH, "Update apps from Winget community repo")


if __name__ == "__main__":
    main()
