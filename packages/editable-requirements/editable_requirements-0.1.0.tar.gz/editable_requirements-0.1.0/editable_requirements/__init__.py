from pathlib import Path
from typing import List

import cattrs
import git
import tomlkit
from attrs import define, field
from cattrs.preconf.json import JsonConverter
from cattrs.preconf.tomlkit import TomlkitConverter
from loguru import logger as log

from git import Repo, Remote


def load_pyproject(folder: str | Path):
    folder = Path(folder)

    pyproj_file = folder / "pyproject.toml"

    data = tomlkit.load(open(pyproj_file))
    return data


def find_git_path(path):
    path = Path(path)

    while not (path / ".git").exists():
        if path == Path("/"):
            return None
        path = path.parent

    return path


@define
class GitRemote:
    name: str = field()
    urls: List[str] = field(converter=lambda x: [str(url) for url in x])


@define
class GitRepo:
    localpath: Path = field(converter=Path)
    remotes: List[GitRemote] = field(factory=list)
    current_sha: str  = field(default=None)


def find_editables(data):
    out = []
    deps = data["tool"]["poetry"]["dependencies"]
    for k, v in deps.items():
        if isinstance(v, str):
            pass
        elif "path" in v.keys():
            path = v["path"]
            print(path)
            path = find_git_path(path)

            if path:
                print(f"Found path {path}")
                repo = Repo(path)

                r = GitRepo(path)
                sha = repo.head.object.hexsha
                r.current_sha = sha

                for remote in repo.remotes:
                    rem = GitRemote(remote.name, remote.urls)

                    r.remotes.append(rem)

                out.append(r)
    return out



# c = TomlkitConverter()
c = JsonConverter()


def generate_requirements(folder):
    data = load_pyproject(folder)

    if not data:
        log.warning

    out = find_editables(data)
    # repos = c.unstructure(out, List[GitRepo])

    outfile = folder / "local_repositories.json"
    with open(outfile, "w") as f:
        f.write(c.dumps(out, List[GitRepo], indent=2))




def rebuild_editables(folder , checkout_folder=None, pretend=False):
    folder = Path(folder)
    with open(folder /'local_repositories.json',  'r') as f:
        infile = f.read()
        data =c.loads(infile, List[GitRepo])

    output_location = Path(checkout_folder)
    print(f'Repos will be checked out at {output_location}')
    
    if not pretend:
        output_location.mkdir(exist_ok=True, parents=True)

    for repo in data:

        if output_location:
            newpath = output_location / repo.localpath.name
        else: 
            newpath = repo.localpath # same as in the file


        print(f'{repo.localpath} will be checked out at {newpath}')
        
        git_url = repo.remotes[0].urls[0]
        if not pretend:
            try:
                r = Repo.clone_from(git_url, newpath)
            except git.exc.GitCommandError as e:
                r = Repo(newpath)

        if not pretend:
            for remote in repo.remotes:
                print(f'Checking remote {remote} is already setup')
                for url in remote.urls:
                    if remote.name not in r.remotes:
                        print('to be added')
                        remote = r.create_remote(name=remote.name, url=url)
                    else:
                        print('already there')
                        remote = r.remote(remote.name)

                    if url not in remote.urls:
                        remote.add_url(url)
            try:
                r.git.checkout(repo.current_sha)
            except git.exc.GitCommandError as e:
                for remote in r.remotes:
                    print(f"Fetching from remote: {remote.name}")
                    remote.fetch()
                    
                r.git.checkout(repo.current_sha)
            print(f'Commit reset to {repo.current_sha}')
            # Optionally, set HEAD to this commit
            r.head.reset(commit=repo.current_sha, index=True, working_tree=True)
            