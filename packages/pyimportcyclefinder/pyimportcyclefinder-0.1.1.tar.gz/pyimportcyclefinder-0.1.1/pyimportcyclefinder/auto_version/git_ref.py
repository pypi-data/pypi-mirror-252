import copy
from functools import partial, partialmethod
from typing import Any, Callable, ClassVar, Optional, Set, Tuple
import sys

from packaging import version
from pyimportcyclefinder.auto_version.git import Git
from urlpath import URL
old_print = print
try:
    import rich
    import rich.pretty

    rich.pretty.install()
    print = rich.print
except ModuleNotFoundError:
    print = old_print


class GitRef:
    _tag_path: ClassVar[URL] = URL("refs") / 'tags'
    _local_branch_base_path: ClassVar[URL] = URL("refs") / 'heads'
    _remote_branch_base_path: ClassVar[URL] = URL("refs") / 'remotes' / 'origin'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            str(
                {
                    "hash": str(self.object_git_hash),
                    "full_branch_name": str(self.full_local_branch_name),
                    "remote_name": str(self.full_remote_branch_name),
                    "tag": str(self.tag_name),
                    "verbose": str(self.verbose)
                }
            )
        )

    def __rich_repr__(self):
        yield (
            "hash",
            None if self.object_git_hash is None else str(self.object_git_hash)
        )
        yield (
            "remote",
            None if self.full_remote_branch_name is None else str(self.full_remote_branch_name)
        )
        yield (
            "branch",
            None if self.full_local_branch_name is None else str(self.full_local_branch_name)
        )
        yield "tag", None if self.tag_name is None else str(self.tag_name)
        yield "verbose", self.verbose

    def _determine_tag(self):
        errlvl, points_at = Git.Tag.points_at(self.object_git_hash, return_errorcode=True)
        if len(points_at.strip()) > 0:
            use_tag = points_at.split("\n")
        else:
            errlvl, merged = Git.Tag.merged(self.object_git_hash, return_errorcode=True)
            use_tag = merged.split("\n")
        parsed_versions = sorted([version.parse(x) for x in use_tag])
        # print(parsed_versions)
        self.tag_name = self.__class__._tag_path / f"v{str(parsed_versions[-1])}"

    def _determine_branch(self):
        errlvl, points_at = Git.Branch.points_at(self.object_git_hash, return_errorcode=True)
        detached_head_text = None
        starred_branch = None

        def clean_branch_response(text: str):
            lines = text.split("\n")
            kept = []
            for line in lines:
                if line.startswith("* (HEAD detached"):
                    detached_head_text = line[2:].strip()
                elif line.startswith("* "):
                    starred_branch = line[2:].strip()
                    kept.append(starred_branch)
                else:
                    kept.append(line.strip())
            return kept
        if len(points_at.strip()) > 0:
            use_branch = points_at
            kept_branch = clean_branch_response(use_branch)
        else:
            errlvl, use_branch = Git.Branch.contains(self.object_git_hash, return_errorcode=True)
            if errlvl:
                print(use_branch, file=sys.stderr)
            kept_branch = clean_branch_response(use_branch)
        if len(kept_branch) == 0:
            # print(self)
            kept_branch.append("main")  # if there are not any branches, this was probably a tag ref
            # raise ValueError(
            #         "Cannot determine branch, probably a dangling commit"
            # )
        # rich.print(kept_branch)
        if "main" in kept_branch:
            self.full_remote_branch_name = self.__class__._remote_branch_base_path / "main"
            self.full_local_branch_name = self.__class__._local_branch_base_path / "main"
        elif len(kept_branch) == 1:
            bn = list(kept_branch)[0]
            self.full_remote_branch_name = self.__class__._remote_branch_base_path / bn
            self.full_local_branch_name = self.__class__._local_branch_base_path / bn
        elif len(kept_branch) > 1:
            raise ValueError(f"what do?: {kept_branch}")

    def __init__(self, ref_info: Tuple[str, str], verbose=True):
        self.verbose = verbose
        errlvl, self.object_git_hash = Git.RevParse.object(ref_info[0], return_errorcode=True)
        self.object_ref_type = ref_info[1]
        self.tag_name = None  # type: Optional[URL]
        self.full_local_branch_name = None  # type: Optional[URL]
        self.full_remote_branch_name = None  # type: Optional[URL]
        if self.object_ref_type == "tag":
            errlvl, points_at_output = Git.Tag.points_at(
                self.object_git_hash,
                return_errorcode=True
            )
            self.tag_name = (
                    self.__class__._tag_path / points_at_output

            )
            self._determine_branch()
        elif self.object_ref_type == "branch":
            errlvl, points_at_output = Git.Branch.points_at(
                self.object_git_hash,
                include_remotes=False,
                include_local=True,
                return_errorcode=True
            )
            self.full_local_branch_name = (
                    self.__class__._local_branch_base_path /
                    points_at_output[2:]
            )
            self.full_remote_branch_name = (
                    self.__class__._remote_branch_base_path /
                    self.full_local_branch_name.name
            )
            self._determine_tag()
        elif self.object_ref_type == 'remote':
            errlvl, points_at_output = Git.Branch.points_at(
                    self.object_git_hash,
                    include_remotes=True,
                    include_local=False,
                    return_errorcode=True
            )
            self.full_remote_branch_name = (
                    self.__class__._remote_branch_base_path /
                    URL(points_at_output[2:]).name
            )
            self.full_local_branch_name = (
                    self.__class__._local_branch_base_path /
                    self.full_remote_branch_name.name
            )
            self._determine_tag()
        else:
            raise RuntimeError("unknown ref type: ", self.object_ref_type, "for ref:", self.object_git_hash)


if __name__ == "__main__":
    gr = GitRef(("HEAD", "branch"))
    print(gr.full_remote_branch_name)
