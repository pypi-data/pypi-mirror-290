import os
import re
import colorama
import git
import shutil
import hashlib
from files3 import files
from git.cmd import Git
from git.exc import InvalidGitRepositoryError
from stcube.core import *
import tempfile

test_url = "https://gitee.com/eagle-s_baby/stcube_libmos"


def get_url_name(_url) -> str:
    """
    获取url的名称，获取到的name可以作为文件夹名
    :param _url: 传入的URL
    :return: 返回一个字符串，作为文件夹名
    """

    # 统一\/\/为/
    clean_url = re.sub(r'\\', '/', _url)

    # 取倒数第二个/后的内容(去最后两个非空的内容)
    _splits = [s for s in clean_url.split('/') if s]

    if not _splits:
        return ''

    if len(_splits) >= 3:
        clean_url = _splits[-2] + '_' + _splits[-1]
    else:
        clean_url = _splits[-1]

    # 去除路径中的-
    clean_url = re.sub(r'-', '', clean_url)

    # 去除路径中的斜杠
    clean_url = re.sub(r'/', '_', clean_url)

    # 去除路径中的点
    clean_url = re.sub(r'\.', '_', clean_url)

    # 替换一些特殊字符，使其更安全作为文件夹名
    clean_url = re.sub(r'[^\w\-_\.]', '', clean_url)

    return clean_url


def get_full_url(_url) -> str:
    if not _url.startswith('http://') or not _url.startswith('https://'):
        return 'https://' + _url

def is_subpath(a, b):
    """
    判断 a 是否是 b 的子路径
    """
    # 规范化路径，消除路径中的 '.' 和 '..'
    a = os.path.normpath(a)
    b = os.path.normpath(b)

    # 将路径分割成部分
    a_parts = a.split(os.sep)
    b_parts = b.split(os.sep)

    # 检查 a 的路径部分是否是 b 的前缀
    return a_parts[:len(b_parts)] == b_parts


class _ULGitRepoBase:
    URL_REPO = {}

    @classmethod
    def save(cls):
        HOME_F._GIT_REPO = cls.URL_REPO

    @classmethod
    def load(cls):
        if HOME_F.has('_GIT_REPO'):
            cls.URL_REPO = HOME_F._GIT_REPO

    @staticmethod
    def available(repo_url:str):
        try:
            # 使用 GitPython 执行 git ls-remote 命令
            git = Git()
            output = git.execute(['git', 'ls-remote', repo_url])

            # 如果命令执行成功，输出将包含仓库信息
            print("Success check url. " if setting.language == 'en' else "repo url验证通过。")
            return True

        except Exception as e:
            # 如果命令执行失败，打印错误信息
            print(f"Failed check url: {e}" if setting.language == 'en' else f"repo url验证失败: {e}")
            return False

    @staticmethod
    def different(repo: git.Repo, branch:str=None) -> bool:
        """
        检查仓库是否有不同
        * print diff
        """
        local_branch = repo.active_branch if branch is None else repo.branches[branch]
        remote_branch = local_branch.tracking_branch()

        if remote_branch is None:
            print(f"no remote branch for {local_branch}")
            return False

        diff = repo.git.diff(f"{remote_branch.name}..{local_branch.name}")
        if diff:
            print(diff)
            return True
        else:
            print("no diff")
            return False


class ULGitRepo(_ULGitRepoBase):
    """
    用于连接到适用于STCube
    """
    _FIRST = True

    @property
    def uflag(self):
        return self._need_update_flag

    def __init__(self, target_url, u: bool = False, specific_dir: str = None):
        """
        :param target_url: 仓库地址
        :param u: 是否更新
        """
        self.target_url = target_url
        self._need_update_flag = False
        self.repo_dir = None

        if self.__class__._FIRST:
            self.load()
            self.__class__._FIRST = False

        self.initial(specific_dir, u)

    def initial(self, custom_dir: str = None, u: bool = False):
        if not u and self.target_url in self.URL_REPO and os.path.exists(self.URL_REPO[self.target_url]) and (custom_dir is None or custom_dir == self.URL_REPO[self.target_url]):
            self.repo_dir = (self.URL_REPO[self.target_url] if self.repo_dir is None else self.repo_dir) if custom_dir is None else custom_dir
            self.repo = git.Repo(self.repo_dir)
        else:
            self.repo_dir = (tempfile.mkdtemp() if self.repo_dir is None else self.repo_dir) if custom_dir is None else custom_dir

            if os.path.exists(self.repo_dir):
                try:
                    self.repo = git.Repo(self.repo_dir)
                except InvalidGitRepositoryError:
                    try:
                        shutil.rmtree(self.repo_dir)
                        self.repo = git.Repo.clone_from(self.target_url, self.repo_dir)
                    except PermissionError as err:
                        print(f"Can not remove .local files. PermissionError: {self.repo_dir}" if setting.language == 'en' else f"无法删除 .local 文件夹。PermissionError: {self.repo_dir}")
                        raise err
            else:
                self.repo = git.Repo.clone_from(self.target_url, self.repo_dir)
            self.URL_REPO[self.target_url] = self.repo_dir
            self.save()

    def add(self, *files, update:bool=False):
        new_paths = []
        files = [os.path.abspath(f) for f in files]
        for f in files:
            fnametype = os.path.basename(f)
            repo_this = os.path.join(self.repo_dir, fnametype)
            if not is_subpath(f, self.repo_dir):
                if os.path.isdir(f):
                    if not os.path.exists(repo_this):
                        shutil.copytree(f, repo_this)
                    elif update:
                        shutil.rmtree(repo_this)
                        shutil.copytree(f, repo_this)
                elif os.path.isfile(f):
                    if not os.path.exists(repo_this):
                        shutil.copy(f, repo_this)
                    elif update:
                        os.remove(repo_this)
                        shutil.copy(f, repo_this)
                else:
                    print(f"file {f} not found")
                    continue
            new_paths.append(repo_this)
        if not new_paths:
            return
        self.repo.index.add(new_paths)
        self._need_update_flag = True

    def remove(self, *files):
        if not files:
            return
        for f in files:
            fnametype = os.path.basename(f)
            repo_this = os.path.join(self.repo_dir, fnametype)
            if os.path.exists(repo_this):
                if os.path.isdir(repo_this):
                    shutil.rmtree(repo_this)
                else:
                    os.remove(repo_this)
        self.repo.index.remove(files)
        self._need_update_flag = True


    def push(self, info="user update"):
        if not self._need_update_flag:
            return
        self.repo.index.commit(info)
        remote = self.repo.remote('origin')
        remote.push('master')

    def clone(self, target_dir, u: bool = False):
        if u:
            self.initial(target_dir, u)
        else:
            shutil.copytree(self.repo_dir, target_dir)

    def refresh(self):
        self.initial(u=True)

    def checkout(self, branch='master'):
        git = Git(self.repo_dir)
        output = git.execute(['git', 'checkout', branch, '.'])

    def __repl__(self):
        return f"STCubeModuleRepo({self.target_url})|{self.repo_dir}"

    def __str__(self):
        txt = f"STCubeModuleRepo:\n  url:   {self.target_url}\n  local: {self.repo_dir}\n  files:\n"
        for file in self:
            txt += f"    {file}\n"

        return txt + '\n'

    def __iter__(self):
        return iter(os.listdir(self.repo_dir))


class STCubeModuleRepo(ULGitRepo):
    pass


class FRepo(Functional):
    key = "r|repo"
    doc_zh = """
    * 只适用于用于STCUBE的仓库
    * 只能管理体积较小的MODS(不能管理Library)
    > 用于同步你的'MODS'到指定url的仓库
    > 可以访问他人的仓库，将其克隆到本地
        .exp: 打开本地仓库管理文件夹
        # ----------- 您的仓库 -------------
        .url: 设置你的上传同步git仓库地址
        .push: 手动上传MODS更新到仓库
        .pull: 手动拉取同步到本地
        # ----------- 他人的仓库 ------------
        .visit: 访问他人仓库，并克隆到本地作为备选方案
    """
    doc = """
    * Only for the repository used for STCUBE
    * Can only manage small MODS (cannot manage Library)
    > Synchronize your 'MODS' to the repository with the specified url
    > You can access other people's repositories and clone them locally
        .exp: Open the local repository management folder
        # ----------- Your repository -------------
        .url: Set the address of your upload synchronization git repository
        .push: Manually upload MODS updates to the repository
        .pull: Manually pull synchronization to local
        # ----------- Other people's repositories ------------
        .visit: Access the other's repository, clone it locally as a backup plan    
    """
    sys = Functional.sys + ['compare_mods_repo']
    def loading(self):
        self._url = None if not HOME_F.has('REPO_URL') else HOME_F.REPO_URL

        if not os.path.exists(REPO_DIR):
            os.makedirs(REPO_DIR)

        if self._url:
            if not os.path.exists(LOCAL_REPO):
                os.mkdir(LOCAL_REPO)
            self.local_repo = STCubeModuleRepo(test_url, specific_dir=LOCAL_REPO)
        else:
            self.local_repo = None

        # get component:module
        module = self.ce.get('m|mod')
        if not module:
            raise Exception("\n\nSystem Error: \n\tComponent<FModule> not found. "
                            if setting.language == 'en' else
                            "\n\n系统错误: \n\t组件<FModule>未找到。")
        self.module = module

    def exp(self):
        os.startfile(REPO_DIR)

    def url(self, url=None):
        _url = input('input url: ' if setting.language == 'en' else '输入url: ') if url is None else url
        _url = get_full_url(_url)
        # check url available
        if ULGitRepo.available(_url):
            self._url = _url
            HOME_F.REPO_URL = self._url
            if self._url:
                if not os.path.exists(LOCAL_REPO):
                    os.mkdir(LOCAL_REPO)
                print("Cloning from git. Please wait..." if setting.language == 'en' else "正在从git克隆，请稍等...", end='')
                self.local_repo = STCubeModuleRepo(url, specific_dir=LOCAL_REPO)
                print("\rdone." if setting.language == 'en' else "\r完成")

            else:
                self.local_repo = None
        else:
            print("cancel for invalid url" if setting.language == 'en' else "无效的url，操作取消")

    def compare_mods_repo(self) -> tuple[list, list, list]:
        """

        :return: diff from mods, diff from local, diff fhash between same-mod
        """
        _all_mods = set(self.module.scan_rmods(MODS_DIR, True))
        _local_mods = set(self.module.scan_rmods(LOCAL_REPO, True))


        # Get the difference of _all_mods and _local_mods
        cross_mods = _all_mods & _local_mods
        _diff_of_all = _all_mods - cross_mods
        _diff_of_local = _local_mods - cross_mods

        # update (hash compare)
        _updates = []
        for _mod in cross_mods:
            with open(os.path.join(MODS_DIR, _mod), 'rb') as f:
                _hash1 = hashlib.md5(f.read()).hexdigest()
            with open(os.path.join(LOCAL_REPO, _mod), 'rb') as f:
                _hash2 = hashlib.md5(f.read()).hexdigest()
            if _hash1 != _hash2:
                self.local_repo.add(os.path.join(MODS_DIR, _mod), update=True)
                _updates.append(_mod)


        return _diff_of_all, _diff_of_local, _updates

    def push(self):
        _diff_of_all, _diff_of_local, _updates = self.compare_mods_repo()

        # remove of _diff_of_local
        for _mod in _diff_of_local:
            self.local_repo.remove(os.path.join(LOCAL_REPO, _mod))

        # add of _diff_of_all
        for _mod in _diff_of_all:
            self.local_repo.add(os.path.join(MODS_DIR, _mod))

        # get a tempdir
        tempdir = tempfile.mkdtemp()
        _infos = HOME_F.MODS_INFO if HOME_F.has('MODS_INFO') else {}
        _tmp_f = files(tempdir)
        _tmp_f.mods_info = _infos
        _tmp_f = None
        self.local_repo.add(os.path.join(tempdir, 'mods_info.inst'))

        # Create show info
        txt = "//// ----  Summery  ---- ////\n"
        txt += f"These files will be Added: {', '.join(_diff_of_all)}\n" if _diff_of_all else ""
        txt += f"These files will be Updated: {', '.join(_updates)}\n" if _updates else ""
        txt += f"These files will be Removed: {', '.join(_diff_of_local)}\n" if _diff_of_local else ""
        print(txt, end='')

        if not self.local_repo.uflag:
            print("no update" if setting.language == 'en' else "没有更新")
            return

        # Create commit info
        info = "stcube update:\n"
        info += f"Added: {', '.join(_diff_of_all)}\n" if _diff_of_all else ""
        info += f"Updated: {', '.join(_updates)}\n" if _updates else ""
        info += f"Removed: {', '.join(_diff_of_local)}\n" if _diff_of_local else ""

        print("pushing..." if setting.language == 'en' else "正在上传...", end='')
        self.local_repo.push(info)
        print("\rdone." if setting.language == 'en' else "\r完成")

    def pull(self, update=True):
        if update:
            self.local_repo.refresh()

        # Checkout master LOCAL_REPO
        self.local_repo.checkout()

        _diff_of_all, _diff_of_local, _updates = self.compare_mods_repo()

        # move file in _diff_of_local and _updates from LOCAL_REPO to MODS_DIR
        for _mod in _diff_of_local:
            shutil.copy(os.path.join(LOCAL_REPO, _mod), os.path.join(MODS_DIR, _mod))
        for _mod in _updates:
            shutil.copy(os.path.join(LOCAL_REPO, _mod), os.path.join(MODS_DIR, _mod))

        # Create show info
        txt = "//// ----  Summery  ---- ////\n"
        txt += f"These files will be Added: {', '.join(_diff_of_local)}\n" if _diff_of_local else ""
        txt += f"These files will be Updated: {', '.join(_updates)}\n" if _updates else ""
        print(txt, end='')

        # update mods info
        _tmp_f = files(LOCAL_REPO)
        if _tmp_f.has('mods_info'):
            _infos = _tmp_f.mods_info
            HOME_F.MODS_INFO = _infos

        if not _diff_of_local and not _updates:
            print(f"no update{'(update)' if update else ''}." if setting.language == 'en' else f"无需更新{'(update)' if update else ''}")
            return

        print(f"done{'(update)' if update else ''}." if setting.language == 'en' else f"完成{'(update)' if update else ''}")


    def visit(self):
        _url = input("input visit url: " if setting.language == 'en' else "输入访问url: ")
        _url = get_full_url(_url)
        if not STCubeModuleRepo.available(_url):
            print(f"Invalid url: {_url}" if setting.language == 'en' else f"无效url: {_url}")

        print(f"Visiting... url={_url}" if setting.language == 'en' else f"访问中...  url={_url}")
        rname = get_url_name(_url)

        # 检查是否已经存在
        if os.path.exists(os.path.join(REPO_DIR, rname)):
            r = STCubeModuleRepo(_url, specific_dir=os.path.join(REPO_DIR, rname), u=True)
            r.checkout()
            print(f"done. update backend plan:{rname}" if setting.language == 'en' else f"完成。备用选项:{rname}已更新")
        else:
            os.mkdir(os.path.join(REPO_DIR, rname))
            STCubeModuleRepo(_url, specific_dir=os.path.join(REPO_DIR, rname))

            print(f"done. create backend plan:{rname}" if setting.language == 'en' else f"完成。备用选项:{rname}已创建")



    def get_collection(self):
        ...

    def __call__(self):
        print("Gitee Repo Manager" if setting.language == 'en' else "Gitee仓库管理")
        if self._url:
            print(f"* Bind to the repo: {colorama.Fore.BLUE + self._url + colorama.Fore.RESET}" if setting.language == 'en' else f"* 已绑定到仓库: {colorama.Fore.BLUE + self._url + colorama.Fore.RESET}")
        else:
            print(f"* No repo binded" if setting.language == 'en' else f"* 未绑定任何仓库")
        if self.local_repo:
            print(f"* Local repo: {colorama.Fore.BLUE + self.local_repo.repo_dir + colorama.Fore.RESET}" if setting.language == 'en' else f"* 本地仓库: {colorama.Fore.BLUE + self.local_repo.repo_dir + colorama.Fore.RESET}")
        else:
            print(f"* No local repo" if setting.language == 'en' else f"* 未创建本地仓库")


if __name__ == '__main__':
    print(
        get_url_name(test_url),
        hash(get_url_name(test_url)),
        hash(test_url)
    )
