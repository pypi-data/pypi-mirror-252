"""Help goes here"""
import os
import re
import sys
import json
# import yaml
import subprocess
import threading
import time
import datetime

from .ui import Colors, Icons
from .spinner import Spinner
from .repo import Repo


class Repos:

    def __init__(self, root):
        self.root = root
        self.repos = {}


    def insideRepo(self) -> bool:
        self.repo = Repo(self.root)
        self.repo.load()
        return self.repo.git

    def findNames(self, patterns: str) -> list[str]:
        found = set()

        for pattern in patterns.split(","):
            if not "*" in pattern and not "?" in pattern:
                pattern = f"*{pattern}*"

            # print(f"Before: {pattern}")
            pattern = pattern.replace("?", ".")
            pattern = pattern.replace("*", ".*")
            # print(f"After:  {pattern}")
            regex = re.compile(pattern)
            # print(f"Regex:  {regex}")
            for _, repo in self.repos.items():
                if regex.match(repo.name):
                    found.add(repo.name)

        return list(found)


    def list(self):
        names = []
        for name in os.listdir(self.root):
            if name == "." or name == "..":
                continue

            dir = os.path.join(self.root, name)
            if os.path.isdir(dir):
                names.append(name)

        sort = sorted(names)
        for name in sort:
            dir = os.path.join(self.root, name)
            repo = Repo(dir)
            self.repos[name] = repo


    def configs(self):
        self.list()

        for _, repo in self.repos.items():
            repo.configs()
            # print(f"REPO {repo.dir}: {configs}")


    def archived(self):
        dirs   = []
        topDir = f"{self.root}/.archived"
        for name in os.listdir(topDir):
            fullDir = os.path.join(topDir, name)
            if os.path.isdir(fullDir):
                dirs.append(name)

        sort = sorted(dirs)
        print("\n".join(sort))


    def saveAll(self):
        self.load()
        threads = []
        for _, repo in self.repos.items():
            if not repo.git:
                # print(f"Directory {repo.name} is not a repo.")
                continue

            if not repo.config:
                # print(f"Repo {repo.name} doesn't have config.")
                continue

            # print(f"repo: {repo}")
            if not repo.config.get("save", False):
                # print(f"Repo {repo.name} is not configured to save.")
                continue

            if repo.changes < 1 and repo.ahead < 1 and repo.behind < 1:
                print(f"{Colors.GRAY}Repo {repo.name} is clean.{Colors.RESET}")
                continue

            thread = threading.Thread(
                target=self.saveRepo,
                args=(repo,)
            )
            threads.append(thread)

        # print(threads); exit(88)
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


    def showConfigs(self, showEmpty: bool = False):
        self.load()
        maxLen = 0
        for _, repo in self.repos.items():

            if not repo.config:
                if showEmpty:
                    if len(repo.name) > maxLen:
                        maxLen = len(repo.name)
                continue

            if len(repo.name) > maxLen:
                maxLen = len(repo.name)

        for _, repo in self.repos.items():
            self.listConfigs(maxLen, repo, showEmpty)


    def listConfigs(self, maxLen: int, repo: Repo, showEmpty: bool = False):
        if not repo.config:
            if showEmpty:
                print(f"    {repo.name:{maxLen}}   {Colors.GRAY}(empty){Colors.RESET}")
            return

        print(f"    {repo.name:{maxLen + 2}}", end="")
        for key, val in repo.config.items():
            color = self.getColor(val)
            print(f" {Colors.DIMMED}{key}:{Colors.RESET}", end="")
            print(f"\033[{color}m{val}{Colors.RESET}", end="")
        print()


    def showConfig(self, names):
        maxLen = 0
        for name in names:
            if len(name) > maxLen:
                maxLen = len(name)

        for name in names:
            repoDir = f"{self.root}/{name}"
            repo = Repo(repoDir)
            repo.load()

            self.listConfigs(maxLen, repo, True)


    def getConfig(self, names, key):
        maxLen = 0
        for name in names:
            if len(name) > maxLen:
                maxLen = len(name)

        for name in names:
            repoDir = f"{self.root}/{name}"
            repo = Repo(repoDir)
            repo.load()

            if not repo.config:
                print(f"    {Colors.GRAY}{repo.name:{maxLen}}   (empty){Colors.RESET}")
                return

            value = repo.config.get(key)
            if not value:
                print(f"    {Colors.GRAY}{repo.name:{maxLen}}   {key}:(none){Colors.RESET}")
                return

            color = self.getColor(value)
            print(f"    {repo.name:{maxLen}}   {Colors.DIMMED}{key}:{Colors.RESET}\033[{color}m{value}{Colors.RESET}")


    def setConfig(self, name, key, value):
        repoDir = f"{self.root}/{name}"
        repo = Repo(repoDir)
        repo.load()

        if not repo.config:
            repo.config = {}

        if value == "null":
            del repo.config[key]
        else:
            repo.config[key] = self.getRaw(value)

        print(f"- SAVING {repo.name}: \033[33;1m{repo.config}\033[0m")
        repo.saveConfig()


    def getRaw(self, value: str):
        lower = value.lower()
        if lower in ["true", "false"]:
            return True if lower == "true" else False

        if value.isdigit():
            return int(value)


        try:
            if str(float(value)) == value:
                return float(value)
        except ValueError:
            pass

        return value


    def getColor(self, value):
        if type(value) is bool:
            if value:
                return "32;1"
            else:
                return "38;5;201"

        if type(value) in [int, float]:
            return "32;1"

        # return True
        # return 1.23
        # return 123
        # return "123"

        return "33;1"


    def save(self, name):
        repoDir = f"{self.root}/{name}"
        repo = Repo(repoDir)
        repo.load()
        self.saveRepo(repo)


    def saveRepo(self, repo):
        print(f"Saving {Colors.YELLOW}{repo.name}{Colors.RESET}... ")

        try:
            if repo.changes > 0:
                repo.run(f"git add --all")
                repo.run(f"git commit --message 'Saving it all'")

            repo.run(f"git push {repo.remote} HEAD")
            print(f"Saved {Colors.GREEN}{repo.name}{Colors.RESET}")

        except Exception as e:
            print(f"\033[31mError: {e}\033[0m")


    def pull(self, repo):
        if not self.save(name):
            print(f"{Colors.GRAY}Pulling {repo.name}... Skipped{Colors.RESET}", flush=True)
            return

        print(f"Pushing repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        repo = Repo(repoDir)
        isOn = repo.run("git config repos.push")

        if isOn == "true":
            repo.run("git push origin HEAD")
            print(f"{Colors.GREEN}Pushed{Colors.RESET}")
        else:
            print(f"{Colors.GRAY}Skipped{Colors.RESET}")


    def enable(self, name, feature):
        print(f"Enabling {feature} in repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        repo = Repo(repoDir)
        isOn = repo.run(f"git config repos.{feature}")

        if isOn == "true":
            print(f"{Colors.GRAY}Skipped{Colors.RESET}")
        else:
            repo.run(f"git config repos.{feature} true")
            print(f"{Colors.GREEN}Enabled{Colors.RESET}")


    def archive(self, name):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        print(f"Archiving repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        archivedDir = f"{self.root}/.archived/{name}@{now}"

        if os.path.isdir(archivedDir):
            print(f" {Colors.GRAY}Skipped{Colors.RESET}")
            return

        if not os.path.isdir(repoDir):
            print(f" {Colors.RED}Fail{Colors.RESET}")
            exit(f"Error: Repo {name} is not an active repo.")

        os.system(f"mkdir -p {self.root}/_archived")
        os.system(f"mv {repoDir} {archivedDir}")
        print(f" {Colors.YELLOW}Archived{Colors.RESET} into {archivedDir}")


    def restore(self, name):
        print(f"Restoring repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        archDir = f"{self.root}/.archived/{name}"

        if os.path.isdir(repoDir):
            print(f" {Colors.GRAY}Skipped{Colors.RESET}")
            return

        if not os.path.isdir(archDir):
            print(f" {Colors.RED}Fail{Colors.RESET}")
            exit(f"Error: Repo {name} is not an archived repo.")

        os.system(f"mv {self.root}/_archived/{name} {self.root}/{name}")
        print(f" {Colors.GREEN}Restored{Colors.RESET}")


    def flip(self, name):
        print(f"Flipping repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        archDir = f"{self.root}/.archived/{name}"
        if os.path.isdir(repoDir):
            os.system(f"mkdir -p {self.root}/.archived")
            os.system(f"mv {self.root}/{name} {self.root}/.archived/{name}")
            print(f" {Colors.YELLOW}Archived{Colors.RESET}")
            return

        if os.path.isdir(archDir):
            os.system(f"mv {self.root}/_archived/{name} {self.root}/{name}")
            print(f" {Colors.GREEN}Restored{Colors.RESET}")
            return

        print(f" {Colors.RED}Fail{Colors.RESET}")
        exit(f"Error: Repo {name} is neither an active nor an archived repo.")


    def calcPads(self, repos):
        self.pads = {
            "changes"  : 0,
            "ahead"    : 0,
            "behind"   : 0,
            "name"     : 0,
            "branch"   : 0,
            "branches" : 0,
            "remotes"  : 0,
        }

        for _, repo in self.repos.items():
            self.checkLen("name", repo.name)

            if not repo.git:
                repo.name = repo.name + "/"
                continue

            self.checkLen("branch", repo.branch)
            self.checkLen("branches", repo.branches)
            self.checkLen("remotes", repo.remotes)
            self.checkLen("changes", repo.changes)
            self.checkLen("ahead", repo.ahead)
            self.checkLen("behind", repo.behind)


    def checkLen(self, name, value, isText: bool = False) -> int:
        if type(value) is str:
            length = len(value)
        elif type(value) is int:
            length = len(str(value))
        elif type(value) is list:
            length = len(str(len(value)))
        else:
            raise Exception("What happened here?")

        if length > self.pads[name]:
            self.pads[name] = length


    def text(self, showClean: bool = False):
        # sep = " │ "
        sep = "   "

        # print(f"{sep}{Colors.GRAY}Repos in {Colors.GREEN}{self.root}{Colors.RESET}\n")

        self.calcPads(self.repos)
        self.total = {
            "dir":      0,
            "solo":     0,
            "detached": 0,
            "clean":    0,
            "changed":  0,
            "ahead":    0,
            "behind":   0,
        }

        statusPad  = 9
        statusPad += self.pads["changes"]
        statusPad += self.pads["behind"]
        statusPad += self.pads["ahead"]
        # statusPad += 1
        ### DOING
        # statusPad += self.pads['branches']
        # statusPad += self.pads['remotes']

        branchPad  = 8 # 3 for branches pad, 3 for remotes pad and 2 for icon
        # branchPad += self.pads['branches']
        # branchPad += self.pads['remotes']
        branchPad += self.pads["branch"]

        # print(self.pads)
        # header  = f"{Colors.GRAY}{sep}"
        # header += f"{self.pad('STATUS', statusPad, False)}{sep}"
        # header += f"{self.pad('NAME', self.pads['name'], False)}{sep}"
        # header += f"{self.pad('', self.pads['branches'], True)} "
        # header += f"{self.pad('⬆', self.pads['remotes'], True)}  "
        # header += f"{self.pad('BRANCH', branchPad, False)}"
        # header += f"{Colors.RESET}"
        # print(header)

        # dashes  = f"{Colors.GRAY}{sep}"
        # dashes += f"{'═' * statusPad}{sep}"
        # dashes += f"{'═' * (self.pads['name'])}{sep}"
        # # 3 because: 1 space between branches and remotes and 2 for branch:
        # # branches_remotes__branch
        # dashes += f"{'═' * (self.pads['branches'] + self.pads['remotes'] + 3)}"
        # # 2 because: 1 for icon, 1 for space
        # dashes += f"{'═' * (self.pads['branch'] + 2)}"
        # dashes += f"{Colors.RESET}"
        # print(dashes)

        # print(self.pads)
        ### We separate branches_remotes info from branch info
        header  = f"{Colors.GRAY}{sep}"
        header += f"{self.pad('STATUS', statusPad, False)}{sep}"
        header += f"{self.pad('NAME', self.pads['name'], False)}{sep}"
        header += f"{self.pad('', self.pads['branches'], True)} "
        header += f"{self.pad('⬆', self.pads['remotes'], True)}{sep}"
        header += f"{self.pad('BRANCH', branchPad, False)}"
        header += f"{Colors.RESET}"
        print(header)

        dashes  = f"{Colors.GRAY}{sep}"
        dashes += f"{'═' * statusPad}{sep}"
        dashes += f"{'═' * (self.pads['name'])}{sep}"
        # 1 because: 1 space between branches and remotes
        dashes += f"{'═' * (self.pads['branches'] + self.pads['remotes'] + 1)}{sep}"
        # 2 because: 1 for icon, 1 for space
        dashes += f"{'═' * (self.pads['branch'] + 2)}"
        dashes += f"{Colors.RESET}"
        print(dashes)

        # print(f"  {Colors.GRAY}{self.pad('STATUS', statusPad, False)}    {self.pad('NAME', self.pads['name'], False)}    {self.pad('BRANCH', self.pads['branch'], False)}{Colors.RESET}")
        # print(f"  {Colors.GRAY}{'─' * statusPad}    {'─' * (self.pads['name'])}    {'─' * (self.pads['branch'] + 2)}{Colors.RESET}")

        count = 0
        for _, repo in self.repos.items():
            count += 1
            if not repo.git:
                self.total["dir"] += 1
                if not showClean:
                    continue

            elif repo.changes < 1 and repo.ahead < 1 and repo.behind < 1:
                self.total["clean"] += 1
                if len(repo.remotes) > 0 and repo.remote:
                    if not showClean:
                        # print(f"Repo {Colors.GREEN}{repo.name}{Colors.RESET} is clean.")
                        continue

            # Assume all are clean (gray)
            changes = f"{Colors.GRAY}{Icons.DOT}{Colors.RESET}"
            ahead   = f"{Colors.GRAY}{Icons.DOT}{Colors.RESET}"
            behind  = f"{Colors.GRAY}{Icons.DOT}{Colors.RESET}"

            # Flag the file change count with yellow
            if repo.changes > 0:
                changes = f"{Colors.YELLOW}{repo.changes}{Icons.DIFF}{Colors.RESET}"

            # Flag the number of commits ahead with green (should be
                # orange to match the `prompt-git` colours)
            if repo.ahead > 0:
                ahead = f"{Colors.GREEN}{repo.ahead}{Icons.UP}{Colors.RESET}"

            # Flag the number of commits behind with purple
            if repo.behind > 0:
                behind = f"{Colors.PURPLE}{repo.behind}{Icons.DOWN}{Colors.RESET}"

            # If not a repo we stop here the git lineage
            if not repo.git:
                # self.total["dir"] += 1
                color   = Colors.BLUE
                changes = ""
                ahead   = ""
                behind  = ""

            # If it has no remotes, it will not have any upstreams and
            # flag it with a red flag
            elif len(repo.remotes) < 1:
                self.total["solo"] += 1
                color = Colors.RED
                ahead = ""
                behind = f"{Colors.RED}{Icons.FLAG}{Colors.RESET}"

            # If it has remotes but no upstreams flag it with an orange
            # flag
            elif repo.upstream is None:
                self.total["detached"] += 1
                color = Colors.ORANGE
                ahead = f"{Colors.ORANGE}{Icons.FLAG}{Colors.RESET}"
                behind = f"{Colors.ORANGE}{Icons.FLAG}{Colors.RESET}"

            # Now we change the repo name line color depending on local
            # status. In order of priority: uncommited changes get
            # flagged yellow straight away. As this is the top concern
            # to fix.
            if repo.changes > 0:
                self.total["changed"] += 1
                color = Colors.YELLOW

            # Behind beats ahead because we need to pull first so it
            # can go from:
            # - yellow (changes) to
            # - purple (behind) to
            # - green (ahead) to
            # - gray (clean)
            elif repo.behind > 0:
                self.total["behind"] += 1
                color = Colors.PURPLE

            # If it has unpushed changes (ahead) we show it too
            elif repo.ahead > 0:
                self.total["ahead"] += 1
                color = Colors.GREEN

            # Clean repos get grayed out
            elif repo.changes + repo.ahead + repo.behind == 0:
                if repo.git:
                    # self.total["clean"] += 1
                    if repo.upstream:
                        color = Colors.GRAY

            else:
                print(repo)
                raise Exception("WTF happened here?")

            ### Handle the branch counters colors

            # For a single branch repo we gray dot it as it's the most
            # common scenario
            if len(repo.branches) == 1:
                branches = f"{Colors.GRAY}{Icons.DOT}{Colors.RESET}"

            # For a multiple branches repo we show the count in gray
            elif len(repo.branches) > 1:
                branches = f"{Colors.GRAY}{str(len(repo.branches))}{Colors.RESET}"

            # Somehow it has no branches: a dir
            else:
                branches = " "

            # For a single remote repo we gray dot it as it's common
            if len(repo.remotes) == 1:
                remotes = f"{Colors.GRAY}{Icons.DOT}{Colors.RESET}"

            # For a multiple remotes repo we show the count in gray
            elif len(repo.remotes) > 1:
                remotes = f"{Colors.GRAY}{str(len(repo.remotes))}{Colors.RESET}"

            # Somehow it has no remote: a dir ?
            elif repo.git:
                remotes = f"{Colors.RED}{Icons.FLAG}{Colors.RESET}"

            else:
                # remotes = "?"
                # remotes = f"{Colors.GRAY} {Colors.RESET}"
                remotes = f"{Colors.BLUE} {Colors.RESET}"

            # statusLine = self.padStatus(changes, behind, ahead)
            # nameLine   = f"{color}{self.pad(repo.name, self.pads['name'], False)}"
            # remoteLine = self.padRemotes(branches, remotes)
            # branchLine = f"{color}{repo.icon} {repo.branch}"

            # print(f"{sep}{statusLine}{sep}{nameLine}{sep}{remoteLine}  {branchLine}{Colors.RESET}")

            statusLine = self.padStatus(changes, behind, ahead)
            nameLine   = f"{color}{self.pad(repo.name, self.pads['name'], False)}"
            remoteLine = self.padRemotes(branches, remotes)
            branchLine = f"{color}{repo.icon} {repo.branch}"

            print(f"{sep}{statusLine}{sep}{Colors.GRAY}{count:3}{Colors.RESET} {nameLine}{sep}{remoteLine}{sep}{branchLine}{Colors.RESET}")

        # self.stats()

        millis = round(self.finish - self.started)
        report = f"\033[38;5;242m({len(self.repos)} dirs in {millis} ms)"
        print(f"\n    {report}")

    ### DOING
    def padStatus(self, changes: str, behind: str, ahead: str) -> str:
        extra = 3
        text  = ""
        text += self.pad(changes,   self.pads['changes']    + extra)
        text += self.pad(behind,    self.pads['behind']     + extra)
        text += self.pad(ahead,     self.pads['ahead']      + extra)

        return text

    # def padStatusOld(self, changes: str, behind: str, ahead: str, branches: str, remotes: str) -> str:
    #     extra = 3
    #     text  = ""
    #     text += self.pad(changes,   self.pads['changes']    + extra)
    #     text += self.pad(behind,    self.pads['behind']     + extra)
    #     text += self.pad(ahead,     self.pads['ahead']      + extra)
    #     text += self.pad(branches,  self.pads['branches']   + extra)
    #     text += self.pad(remotes,   self.pads['remotes']    + extra)

    #     return text

    def padRemotes(self, branches: str, remotes: str) -> str:
        text  = ""
        text += self.pad(branches,      self.pads['branches'])
        text += self.pad(" " + remotes, self.pads['remotes'])

        return text

    # def test(self):
    #     pad = 6
    #     tests = {
    #         "\033[38;5;220mBlah\033[0m": "--\033[38;5;220mBlah\033[0m",
    #         "\033[1mBla\033[0m": "---\033[1mBla\033[0m",
    #         "B": "-----B",
    #     }
    #     for text, expected in tests.items():
    #         returned = self.pad(text, pad)
    #         if returned != expected:
    #             print(f"Failed test on '{text}': expected '{expected}' vs returned '{returned}'.")
    #             exit(1)

    #     exit()


    def pad(self, text: str, pad: int, right: bool = True) -> str:
        # print(f"==> {len(text)}")
        # 1. '\033[38;5;220mBlah\033[0m'
        # 2. '\033[1mBlah\033[0m'
        # 3. 'Blah'
        fill = " "
        tag = "\033["
        if tag in text:
            pos = text.find(tag)
            end = text.find("m", pos)
            plain = text[end+1:]
            plain = plain.replace(f"{tag}0m", "")
            # print(f"==> PLAIN_TEXT: {plain}")
            pad = pad + len(text) - len(plain)
            # print(f"==> NEW PAD: {pad}")

        if right:
            return text.rjust(pad, fill)
        return text.ljust(pad, fill)


    def stats(self):
        report = ""
        report += self.addStat("dir", "directories")
        report += self.addStat("solo", f"without a remote {Colors.RED}{Icons.FLAG}{Colors.PALE}")
        report += self.addStat("detached", f"without upstream {Colors.ORANGE}{Icons.FLAG}{Colors.PALE}")
        report += self.addStat("changed", f"changed")
        report += self.addStat("behind", f"behind")
        report += self.addStat("ahead", f"ahead")
        report += self.addStat("clean", f"clean")
        print(f"{Colors.PALE}{report}{Colors.RESET}")

        # if self.total["dir"]:
        #     report += f"\n{self.total['dir']:9} directories"
        # if self.total["solo"]:
        #     report += f"\n{self.total['solo']:9} without a remote {Colors.RED}{Icons.FLAG}{Colors.PALE}"
        # if self.total["detached"]:
        #     # report += f"\n{self.total['detached']:9} without upstream {Colors.ORANGE}⚑{Colors.PALE}"
        #     report += f"\n{self.total['detached']:9} without upstream {Colors.ORANGE}{Icons.FLAG}{Colors.PALE}"
        # if self.total["changed"]:
        #     report += f"\n{self.total['changed']:9} changed"
        # if self.total["behind"]:
        #     report += f"\n{self.total['behind']:9} behind"
        # if self.total["ahead"]:
        #     report += f"\n{self.total['ahead']:9} ahead"
        # if self.total["clean"]:
        #     report += f"\n{self.total['clean']:9} clean"


    def addStat(self, name, message):
        if self.total[name]:
            return f"\n{self.total[name]:9} {message}"

        return ""


    # @yaspin(text=f"Loading from root...", color="green")
    # @spinner
    def load(self):
        # if self.loaded:
        #     return
        self.started = time.time()*1000
        self.list()
        threads = []

        showSpinner = os.environ.get("REPOS_SPINNER")
        if showSpinner != "false":
            spinner = threading.Thread(
                target=Spinner.start,
                # args=(f" Loading from \033[32;1m{self.root}\033[0m...",)
                args=(f" Loading repos...",)
            )
            spinner.start()

        for _, repo in self.repos.items():
            thread = threading.Thread(target=repo.load)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if showSpinner != "false":
            Spinner.stop()
        Spinner.show()

        self.finish = time.time()*1000
        millis = round(self.finish - self.started)
        report = f"\033[38;5;242m({len(self.repos)} dirs in {millis} ms)"
        print(f"    Repos inside \033[32;1m{self.root}\033[0m\n")
        self.loaded = True


    def show(self, name: str):
        repo = self.repos[name]
        print(repo)


    def export(self, format: str):
        self.load()
        data = {
            "repos": {}
        }
        for dir, repo in self.repos.items():
            data["repos"][dir] = repo.dict()

        if format == "json":
            print(json.dumps(data, indent=2))
            return

        # if format == "yaml":
        #     print(yaml.dump(data, indent=2))
        #     return
