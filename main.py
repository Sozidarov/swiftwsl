import os
import sys
import subprocess
import shutil
from datetime import datetime
import platform
import getpass
import glob
import stat
import time
import zipfile
import tarfile
import hashlib
import psutil  
from pystyle import *

class LinuxEmulator:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = getpass.getuser()
        self.hostname = platform.node()
        self.home_dir = os.path.expanduser("~")
        self.env_vars = {
            "PATH": os.environ.get("PATH", ""),
            "USER": self.user,
            "HOME": self.home_dir,
            "SHELL": "python_wsl"
        }
        self.aliases = {
            "ll": "ls -l",
            "la": "ls -a",
            "l": "ls -la"
        }
        self.history = []
        self.history_file = os.path.join(self.home_dir, ".python_wsl_history")
        self.load_history()

    def neofetch(self, args):
        try:
            
            neofetch_file = os.path.join(os.path.dirname(__file__), "neofetch.txt")
            
            if os.path.exists(neofetch_file):
                
                with open(neofetch_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    
                    content = content.replace("{host}", platform.node())
                    content = content.replace("{kernel}", platform.release())
                    content = content.replace("{shell_version}", f"{sys.version_info.major}.{sys.version_info.minor}")
                    content = content.replace("{cpu}", platform.processor())
                    content = content.replace("{memory}", str(psutil.virtual_memory().total // (1024**3)))
                    
                    from pystyle import Colorate, Colors
                    print(Colorate.Horizontal(Colors.red_to_white, content))
            else:
                
                self._default_neofetch()
        except Exception as e:
            print(f"neofetch error: {str(e)}")
            self._default_neofetch()
    
    def _default_neofetch(self):
        
        from pyfiglet import Figlet
        from pystyle import Colors, Colorate
        
        f = Figlet(font='slant')
        ascii_art = f.renderText('Python WSL')
        
        info = f"""
    {Colorate.Horizontal(Colors.red_to_white, ascii_art)}
    {Colorate.Horizontal(Colors.red_to_white, "══════════════════════════════════════════════════")}
    
    {Colorate.Horizontal(Colors.red_to_white, f"OS: Python WSL Emulator")}
    {Colorate.Horizontal(Colors.red_to_white, f"Host: {platform.node()}")}
    {Colorate.Horizontal(Colors.red_to_white, f"Kernel: {platform.release()}")}
    {Colorate.Horizontal(Colors.red_to_white, f"Shell: Python WSL {sys.version_info.major}.{sys.version_info.minor}")}
    {Colorate.Horizontal(Colors.red_to_white, f"CPU: {platform.processor()}")}
    {Colorate.Horizontal(Colors.red_to_white, f"Memory: {psutil.virtual_memory().total // (1024**3)}GB")}
    """
        print(info)  
        
    def load_history(self):
        try:
            with open(self.history_file, "r") as f:
                self.history = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            pass
            
    def save_history(self):
        with open(self.history_file, "w") as f:
            for cmd in self.history[-1000:]:  
                f.write(cmd + "\n")
    
    def get_prompt(self):
        from pystyle import Colors, Colorate
        path = self.current_dir.replace(self.home_dir, "~") if self.current_dir.startswith(self.home_dir) else self.current_dir
        prompt_text = f"{self.user}@{self.hostname}:{path}$ "
        return Colorate.Horizontal(Colors.red_to_white, prompt_text)
    
    def parse_command(self, cmd):
        if not cmd.strip():
            return
        
        
        for alias, expansion in self.aliases.items():
            if cmd.split()[0] == alias:
                cmd = expansion + cmd[len(alias):]
        
        
        parts = cmd.split()
        command = parts[0]
        args = parts[1:]
        
        
        self.history.append(cmd)
        
        
        try:
            if command == "cd":
                self.cd(args)
            elif command == "ls":
                self.ls(args)
            elif command == "pwd":
                self.pwd()
            elif command == "echo":
                self.echo(args)
            elif command == "cat":
                self.cat(args)
            elif command == "mkdir":
                self.mkdir(args)
            elif command == "rm":
                self.rm(args)
            elif command == "cp":
                self.cp(args)
            elif command == "mv":
                self.mv(args)
            elif command == "touch":
                self.touch(args)
            elif command == "grep":
                self.grep(args)
            elif command == "find":
                self.find(args)
            elif command == "chmod":
                self.chmod(args)
            elif command == "chown":
                print("chown: изменение владельца не поддерживается в эмуляторе")
            elif command == "ps":
                self.ps()
            elif command == "kill":
                self.kill(args)
            elif command == "df":
                self.df()
            elif command == "du":
                self.du(args)
            elif command == "uname":
                self.uname(args)
            elif command == "whoami":
                self.whoami()
            elif command == "date":
                self.date()
            elif command == "history":
                self.show_history()
            elif command == "clear":
                self.clear()
            elif command == "exit":
                self.save_history()
                print("Выход из Python WSL эмулятора")
                sys.exit(0)
            elif command == "help":
                self.help()
            elif command == "alias":
                self.handle_alias(args)
            elif command == "env":
                self.show_env()
            elif command == "export":
                self.export_var(args)
            elif command == "zip":
                self.zip(args)
            elif command == "unzip":
                self.unzip(args)
            elif command == "tar":
                self.tar(args)
            elif command == "md5sum":
                self.md5sum(args)
            elif command == "sha1sum":
                self.sha1sum(args)
            elif command == "head":
                self.head(args)
            elif command == "tail":
                self.tail(args)
            elif command == "diff":
                self.diff(args)
            elif command == "sort":
                self.sort(args)
            elif command == "wc":
                self.wc(args)
            elif command == "ssh":
                print("ssh: подключение к удаленному серверу не поддерживается в эмуляторе")
            elif command == "scp":
                print("scp: копирование файлов между серверами не поддерживается в эмуляторе")
            elif command == "wget":
                print("wget: загрузка файлов из интернета не поддерживается в эмуляторе")
            elif command == "curl":
                print("curl: отправка HTTP запросов не поддерживается в эмуляторе")
            elif command == "ping":
                print("ping: проверка соединения с сервером не поддерживается в эмуляторе")
            elif command == "ifconfig":
                print("ifconfig: информация о сетевых интерфейсах не поддерживается в эмуляторе")
            elif command == "sudo":
                print("sudo: выполнение команд с правами root не поддерживается в эмуляторе")
            elif command == "neofetch":
                self.neofetch(args)    
            else:
                
                try:
                    subprocess.run(cmd, shell=True, cwd=self.current_dir)
                except FileNotFoundError:
                    print(f"{command}: команда не найдена")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def cd(self, args):
        if not args:
            new_dir = self.home_dir
        else:
            new_dir = args[0]
            if new_dir == "-":
                if hasattr(self, "prev_dir"):
                    new_dir = self.prev_dir
                else:
                    print("cd: предыдущая директория не задана")
                    return
            elif new_dir.startswith("~"):
                new_dir = os.path.join(self.home_dir, new_dir[2:])
        
        try:
            self.prev_dir = self.current_dir
            new_dir = os.path.abspath(os.path.join(self.current_dir, new_dir))
            os.chdir(new_dir)
            self.current_dir = new_dir
        except FileNotFoundError:
            print(f"cd: {new_dir}: Нет такой директории")
        except NotADirectoryError:
            print(f"cd: {new_dir}: Не директория")
        except PermissionError:
            print(f"cd: {new_dir}: Отказано в доступе")
    
    def ls(self, args):
        show_all = False
        long_format = False
        human_readable = False
        reverse_sort = False
        sort_by_time = False
        
        # Парсинг аргументов
        paths = []
        for arg in args:
            if arg.startswith("-"):
                if "a" in arg:
                    show_all = True
                if "l" in arg:
                    long_format = True
                if "h" in arg:
                    human_readable = True
                if "r" in arg:
                    reverse_sort = True
                if "t" in arg:
                    sort_by_time = True
            else:
                paths.append(arg)
        
        if not paths:
            paths = ["."]
        
        for path in paths:
            if len(paths) > 1:
                print(f"{path}:")
            
            full_path = os.path.join(self.current_dir, path) if not os.path.isabs(path) else path
            
            try:
                items = os.listdir(full_path)
                
                
                if not show_all:
                    items = [item for item in items if not item.startswith(".")]
                
                
                if sort_by_time:
                    items.sort(key=lambda x: os.path.getmtime(os.path.join(full_path, x)), reverse=not reverse_sort)
                else:
                    items.sort(reverse=reverse_sort)
                
                if long_format:
                    self._print_long_format(items, full_path, human_readable)
                else:
                    
                    cols = 3
                    max_len = max(len(item) for item in items) if items else 0
                    col_width = max_len + 2
                    terminal_width = shutil.get_terminal_size().columns
                    cols = max(1, terminal_width // col_width)
                    
                    for i, item in enumerate(items):
                        end = "\n" if (i + 1) % cols == 0 else ""
                        print(item.ljust(col_width), end=end)
                    if items and i % cols != cols - 1:
                        print()
            except FileNotFoundError:
                print(f"ls: невозможно получить доступ к '{path}': Нет такого файла или директории")
            except NotADirectoryError:
                print(f"ls: '{path}': Не директория")
            except PermissionError:
                print(f"ls: невозможно получить доступ к '{path}': Отказано в доступе")
            
            if len(paths) > 1 and path != paths[-1]:
                print()
    
    def _print_long_format(self, items, path, human_readable):
        total = 0
        items_with_stats = []
        
        for item in items:
            full_path = os.path.join(path, item)
            try:
                stat_info = os.stat(full_path)
                items_with_stats.append((item, stat_info))
                total += stat_info.st_blocks // 2  
            except Exception:
                items_with_stats.append((item, None))
        
        print(f"итого {total}")
        
        for item, stat_info in items_with_stats:
            if stat_info is None:
                print(f"?--------- ? ? ? ? ? {item}")
                continue
                
            
            mode = stat_info.st_mode
            permissions = [
                'd' if stat.S_ISDIR(mode) else '-',
                'r' if mode & stat.S_IRUSR else '-',
                'w' if mode & stat.S_IWUSR else '-',
                'x' if mode & stat.S_IXUSR else '-',
                'r' if mode & stat.S_IRGRP else '-',
                'w' if mode & stat.S_IWGRP else '-',
                'x' if mode & stat.S_IXGRP else '-',
                'r' if mode & stat.S_IROTH else '-',
                'w' if mode & stat.S_IWOTH else '-',
                'x' if mode & stat.S_IXOTH else '-'
            ]
            perm_str = ''.join(permissions)
            
            
            nlinks = stat_info.st_nlink
            
            
            try:
                import pwd
                owner = pwd.getpwuid(stat_info.st_uid).pw_name
                group = pwd.getpwuid(stat_info.st_gid).pw_name
            except (ImportError, KeyError):
                owner = str(stat_info.st_uid)
                group = str(stat_info.st_gid)
            
            
            size = stat_info.st_size
            if human_readable:
                for unit in ['', 'K', 'M', 'G', 'T', 'P']:
                    if size < 1024:
                        size_str = f"{size:.1f}{unit}"
                        break
                    size /= 1024
                else:
                    size_str = f"{size:.1f}P"
            else:
                size_str = str(size)
            
            
            mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime('%b %d %H:%M')
            
            print(f"{perm_str} {nlinks:>2} {owner} {group} {size_str:>8} {mtime} {item}")
    
    def pwd(self):
        print(self.current_dir)
    
    def echo(self, args):
        
        processed_args = []
        for arg in args:
            if arg.startswith("$"):
                var_name = arg[1:]
                processed_args.append(self.env_vars.get(var_name, ""))
            else:
                processed_args.append(arg)
        print(' '.join(processed_args))
    
    def cat(self, args):
        if not args:
            print("cat: требуется указать файл(ы)")
            return
        
        for filename in args:
            try:
                with open(os.path.join(self.current_dir, filename), 'r') as f:
                    print(f.read(), end='')
            except FileNotFoundError:
                print(f"cat: {filename}: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"cat: {filename}: Это директория")
            except PermissionError:
                print(f"cat: {filename}: Отказано в доступе")
    
    def mkdir(self, args):
        if not args:
            print("mkdir: требуется операнд")
            return
        
        parents = False
        paths = []
        
        for arg in args:
            if arg == "-p":
                parents = True
            else:
                paths.append(arg)
        
        for path in paths:
            full_path = os.path.join(self.current_dir, path) if not os.path.isabs(path) else path
            try:
                if parents:
                    os.makedirs(full_path, exist_ok=True)
                else:
                    os.mkdir(full_path)
            except FileExistsError:
                print(f"mkdir: невозможно создать директорию '{path}': Файл существует")
            except FileNotFoundError:
                print(f"mkdir: невозможно создать директорию '{path}': Нет такой директории")
            except PermissionError:
                print(f"mkdir: невозможно создать директорию '{path}': Отказано в доступе")
    
    def rm(self, args):
        if not args:
            print("rm: требуется операнд")
            return
        
        recursive = False
        force = False
        paths = []
        
        for arg in args:
            if arg == "-r" or arg == "-R":
                recursive = True
            elif arg == "-f":
                force = True
            else:
                paths.append(arg)
        
        for path in paths:
            full_path = os.path.join(self.current_dir, path) if not os.path.isabs(path) else path
            try:
                if os.path.isdir(full_path) and not recursive:
                    print(f"rm: невозможно удалить '{path}': Это директория")
                    continue
                
                if recursive:
                    shutil.rmtree(full_path)
                else:
                    os.remove(full_path)
            except FileNotFoundError:
                if not force:
                    print(f"rm: невозможно удалить '{path}': Нет такого файла или директории")
            except PermissionError:
                print(f"rm: невозможно удалить '{path}': Отказано в доступе")
    
    def cp(self, args):
        if len(args) < 2:
            print("cp: требуется как минимум два операнда")
            return
        
        recursive = False
        sources = args[:-1]
        dest = args[-1]
        
        if "-r" in sources or "-R" in sources:
            recursive = True
            sources = [s for s in sources if s not in ("-r", "-R")]
        
        for src in sources:
            src_path = os.path.join(self.current_dir, src) if not os.path.isabs(src) else src
            dest_path = os.path.join(self.current_dir, dest) if not os.path.isabs(dest) else dest
            
            
            if os.path.isdir(dest_path):
                dest_path = os.path.join(dest_path, os.path.basename(src_path))
            
            try:
                if os.path.isdir(src_path) and not recursive:
                    print(f"cp: -r не указан; пропущена директория '{src}'")
                    continue
                
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)
            except FileNotFoundError:
                print(f"cp: невозможно открыть '{src}': Нет такого файла или директории")
            except PermissionError:
                print(f"cp: невозможно создать '{dest}': Отказано в доступе")
            except shutil.SameFileError:
                print(f"cp: '{src}' и '{dest}' это один и тот же файл")
    
    def mv(self, args):
        if len(args) < 2:
            print("mv: требуется как минимум два операнда")
            return
        
        sources = args[:-1]
        dest = args[-1]
        
        for src in sources:
            src_path = os.path.join(self.current_dir, src) if not os.path.isabs(src) else src
            dest_path = os.path.join(self.current_dir, dest) if not os.path.isabs(dest) else dest
            
            
            if os.path.isdir(dest_path):
                dest_path = os.path.join(dest_path, os.path.basename(src_path))
            
            try:
                shutil.move(src_path, dest_path)
            except FileNotFoundError:
                print(f"mv: невозможно открыть '{src}': Нет такого файла или директории")
            except PermissionError:
                print(f"mv: невозможно создать '{dest}': Отказано в доступе")
            except shutil.SameFileError:
                print(f"mv: '{src}' и '{dest}' это один и тот же файл")
    
    def touch(self, args):
        if not args:
            print("touch: требуется операнд")
            return
        
        for filename in args:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'a'):
                    os.utime(full_path, None)
            except IsADirectoryError:
                print(f"touch: {filename}: Это директория")
            except PermissionError:
                print(f"touch: {filename}: Отказано в доступе")
    
    def grep(self, args):
        if len(args) < 1:
            print("grep: требуется шаблон")
            return
        
        pattern = args[0]
        files = args[1:] if len(args) > 1 else []
        ignore_case = False
        count_only = False
        line_numbers = False
        invert_match = False
        
        
        if pattern.startswith("-"):
            if "-i" in pattern:
                ignore_case = True
                pattern = args[1]
                files = args[2:] if len(args) > 2 else []
            elif "-c" in pattern:
                count_only = True
                pattern = args[1]
                files = args[2:] if len(args) > 2 else []
            elif "-n" in pattern:
                line_numbers = True
                pattern = args[1]
                files = args[2:] if len(args) > 2 else []
            elif "-v" in pattern:
                invert_match = True
                pattern = args[1]
                files = args[2:] if len(args) > 2 else []
        
        if ignore_case:
            pattern = pattern.lower()
        
        if not files:
            
            print("grep: чтение из stdin не реализовано в эмуляторе")
            return
        
        for filename in files:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'r') as f:
                    lines = f.readlines()
                
                match_count = 0
                for i, line in enumerate(lines, 1):
                    line_to_check = line.lower() if ignore_case else line
                    match = pattern in line_to_check
                    
                    if (match and not invert_match) or (not match and invert_match):
                        match_count += 1
                        if not count_only:
                            prefix = f"{filename}:" if len(files) > 1 else ""
                            if line_numbers:
                                prefix += f"{i}:"
                            print(f"{prefix}{line.rstrip()}")
                
                if count_only:
                    prefix = f"{filename}:" if len(files) > 1 else ""
                    print(f"{prefix}{match_count}")
            
            except FileNotFoundError:
                print(f"grep: {filename}: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"grep: {filename}: Это директория")
            except PermissionError:
                print(f"grep: {filename}: Отказано в доступе")
    
    def find(self, args):
        if not args:
            print("find: требуется путь")
            return
        
        path = args[0]
        name = None
        file_type = None
        
        
        i = 1
        while i < len(args):
            if args[i] == "-name" and i + 1 < len(args):
                name = args[i+1]
                i += 2
            elif args[i] == "-type" and i + 1 < len(args):
                file_type = args[i+1]
                i += 2
            else:
                i += 1
        
        full_path = os.path.join(self.current_dir, path) if not os.path.isabs(path) else path
        
        try:
            for root, dirs, files in os.walk(full_path):
                for item in dirs + files:
                    item_path = os.path.join(root, item)
                    
                    # Проверка имени
                    if name is not None:
                        if not fnmatch.fnmatch(item, name):
                            continue
                    
                    # Проверка типа
                    if file_type is not None:
                        if file_type == "f" and not os.path.isfile(item_path):
                            continue
                        if file_type == "d" and not os.path.isdir(item_path):
                            continue
                    
                    print(item_path)
        except FileNotFoundError:
            print(f"find: '{path}': Нет такого файла или директории")
        except PermissionError:
            print(f"find: '{path}': Отказано в доступе")
    
    def chmod(self, args):
        if len(args) < 2:
            print("chmod: требуется режим и файл")
            return
        
        mode = args[0]
        files = args[1:]
        
        try:
            
            if mode.startswith("+"):
                
                for filename in files:
                    full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
                    current_mode = os.stat(full_path).st_mode
                    if "x" in mode:
                        os.chmod(full_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            else:
                
                octal_mode = int(mode, 8)
                for filename in files:
                    full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
                    os.chmod(full_path, octal_mode)
        except FileNotFoundError:
            print(f"chmod: невозможно получить доступ к '{filename}': Нет такого файла или директории")
        except PermissionError:
            print(f"chmod: изменить права доступа для '{filename}': Отказано в доступе")
        except ValueError:
            print(f"chmod: неверный режим: '{mode}'")
    
    def ps(self):
        try:
            
            print("  PID TTY          TIME CMD")
            print(f"{os.getpid():>5} ?        00:00:00 python_wsl")
        except Exception as e:
            print(f"ps: ошибка: {str(e)}")
    
    def kill(self, args):
        if not args:
            print("kill: требуется аргумент")
            return
        
        for pid_str in args:
            try:
                pid = int(pid_str)
                if pid == os.getpid():
                    print("kill: невозможно убить процесс эмулятора")
                else:
                    print(f"kill: ({pid}) - Нет такого процесса")
            except ValueError:
                print(f"kill: неверный аргумент: {pid_str}")
    
    def df(self):
        try:
            print("Файл.система    Размер Использовано  Доступно Использовано% Cмонтировано в")
            for part in psutil.disk_partitions(all=False):
                usage = psutil.disk_usage(part.mountpoint)
                print(f"{part.device:<15} {usage.total // (1024*1024):>6}G "
                      f"{usage.used // (1024*1024):>10}G {usage.free // (1024*1024):>8}G "
                      f"{usage.percent:>11}% {part.mountpoint}")
        except NameError:
            print("df: для работы этой команды требуется установить модуль psutil")
        except Exception as e:
            print(f"df: ошибка: {str(e)}")
    
    def du(self, args):
        if not args:
            args = ["."]
        
        human_readable = False
        paths = []
        
        for arg in args:
            if arg == "-h":
                human_readable = True
            else:
                paths.append(arg)
        
        for path in paths:
            full_path = os.path.join(self.current_dir, path) if not os.path.isabs(path) else path
            try:
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(full_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        try:
                            total_size += os.path.getsize(fp)
                        except OSError:
                            pass
                
                if human_readable:
                    size_str = self._human_size(total_size)
                else:
                    size_str = str(total_size // 1024)  
                
                print(f"{size_str}\t{path}")
            except FileNotFoundError:
                print(f"du: невозможно получить доступ к '{path}': Нет такого файла или директории")
            except PermissionError:
                print(f"du: невозможно прочитать директорию '{path}': Отказано в доступе")
    
    def _human_size(self, size):
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}P"
    
    def uname(self, args):
        a = False
        s = False
        n = False
        r = False
        v = False
        m = False
        
        for arg in args:
            if arg == "-a":
                a = True
            elif arg == "-s":
                s = True
            elif arg == "-n":
                n = True
            elif arg == "-r":
                r = True
            elif arg == "-v":
                v = True
            elif arg == "-m":
                m = True
        
        if not any([a, s, n, r, v, m]):
            s = True  
        
        info = []
        if a or s:
            info.append("Linux")
        if a or n:
            info.append(self.hostname)
        if a or r:
            info.append("5.10.16.3-microsoft-standard-WSL2")
        if a or v:
            info.append("#1 SMP Fri Apr 2 22:23:49 UTC 2021")
        if a or m:
            info.append(platform.machine())
        
        print(' '.join(info))
    
    def whoami(self):
        print(self.user)
    
    def date(self):
        print(datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y"))
    
    def show_history(self):
        for i, cmd in enumerate(self.history[-20:], 1):  
            print(f"{i:>5}  {cmd}")
    
    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def help(self):
        print("Доступные команды:")
        print("  cd [директория] - сменить директорию")
        print("  ls [опции] [файлы] - список файлов")
        print("  pwd - показать текущую директорию")
        print("  echo [текст] - вывести текст")
        print("  cat [файлы] - вывести содержимое файлов")
        print("  mkdir [опции] директории - создать директории")
        print("  rm [опции] файлы - удалить файлы")
        print("  cp [опции] источник назначение - копировать файлы")
        print("  mv [опции] источник назначение - переместить/переименовать файлы")
        print("  touch файлы - создать файлы или обновить время модификации")
        print("  grep [опции] шаблон [файлы] - поиск текста в файлах")
        print("  find [путь] [опции] - поиск файлов")
        print("  chmod [режим] файлы - изменить права доступа")
        print("  ps - список процессов")
        print("  kill [PID] - завершить процесс")
        print("  df - информация о файловых системах")
        print("  du [опции] [файлы] - использование диска")
        print("  uname [опции] - информация о системе")
        print("  whoami - текущий пользователь")
        print("  date - текущая дата и время")
        print("  history - история команд")
        print("  clear - очистить экран")
        print("  exit - выйти из эмулятора")
        print("  help - эта справка")
        print("\nЭто упрощенный эмулятор Linux команд. Не все опции и команды поддерживаются.")
    
    def handle_alias(self, args):
        if not args:
            # Показать все алиасы
            for alias, cmd in self.aliases.items():
                print(f"alias {alias}='{cmd}'")
            return
        
        
        for arg in args:
            if "=" in arg:
                alias, cmd = arg.split("=", 1)
                if cmd.startswith("'") and cmd.endswith("'"):
                    cmd = cmd[1:-1]
                elif cmd.startswith('"') and cmd.endswith('"'):
                    cmd = cmd[1:-1]
                self.aliases[alias] = cmd
            else:
                
                if arg in self.aliases:
                    print(f"alias {arg}='{self.aliases[arg]}'")
                else:
                    print(f"-bash: alias: {arg}: не найден")
    
    def show_env(self):
        for var, value in self.env_vars.items():
            print(f"{var}={value}")
    
    def export_var(self, args):
        if not args:
            self.show_env()
            return
        
        for arg in args:
            if "=" in arg:
                var, value = arg.split("=", 1)
                self.env_vars[var] = value
    
    def zip(self, args):
        if len(args) < 2:
            print("zip: требуется архив и файлы")
            return
        
        zip_name = args[0]
        files = args[1:]
        
        try:
            with zipfile.ZipFile(os.path.join(self.current_dir, zip_name), 'w') as zipf:
                for file in files:
                    full_path = os.path.join(self.current_dir, file) if not os.path.isabs(file) else file
                    if os.path.isdir(full_path):
                        for root, dirs, files_in_dir in os.walk(full_path):
                            for f in files_in_dir:
                                file_path = os.path.join(root, f)
                                arcname = os.path.relpath(file_path, start=os.path.dirname(full_path))
                                zipf.write(file_path, arcname=os.path.join(os.path.basename(full_path), arcname))
                    else:
                        zipf.write(full_path, arcname=os.path.basename(full_path))
        except Exception as e:
            print(f"zip: ошибка: {str(e)}")
    
    def unzip(self, args):
        if not args:
            print("unzip: требуется архив")
            return
        
        zip_name = args[0]
        extract_to = None
        if len(args) > 1 and args[1] == "-d":
            if len(args) > 2:
                extract_to = args[2]
            else:
                print("unzip: требуется путь после -d")
                return
        
        try:
            with zipfile.ZipFile(os.path.join(self.current_dir, zip_name), 'r') as zipf:
                if extract_to:
                    extract_path = os.path.join(self.current_dir, extract_to) if not os.path.isabs(extract_to) else extract_to
                    zipf.extractall(extract_path)
                else:
                    zipf.extractall(self.current_dir)
        except Exception as e:
            print(f"unzip: ошибка: {str(e)}")
    
    def tar(self, args):
        if len(args) < 2:
            print("tar: требуется опции и файлы")
            return
        
        mode = None
        archive_name = None
        files = []
        
        
        if args[0].startswith("-"):
            opts = args[0][1:]
            if "c" in opts:
                mode = "create"
            elif "x" in opts:
                mode = "extract"
            elif "t" in opts:
                mode = "list"
            
            if "z" in opts:
                compression = "gz"
            elif "j" in opts:
                compression = "bz2"
            else:
                compression = None
            
            if "f" in opts and len(args) > 1:
                archive_name = args[1]
                files = args[2:]
            else:
                print("tar: требуется имя архива после -f")
                return
        else:
            print("tar: неверные опции")
            return
        
        if not mode:
            print("tar: требуется режим (c/x/t)")
            return
        
        try:
            full_archive_path = os.path.join(self.current_dir, archive_name) if not os.path.isabs(archive_name) else archive_name
            
            if mode == "create":
                with tarfile.open(full_archive_path, f"w:{compression}" if compression else "w") as tarf:
                    for file in files:
                        full_path = os.path.join(self.current_dir, file) if not os.path.isabs(file) else file
                        tarf.add(full_path, arcname=os.path.basename(full_path))
            elif mode == "extract":
                with tarfile.open(full_archive_path, f"r:{compression}" if compression else "r") as tarf:
                    tarf.extractall(self.current_dir)
            elif mode == "list":
                with tarfile.open(full_archive_path, f"r:{compression}" if compression else "r") as tarf:
                    tarf.list()
        except Exception as e:
            print(f"tar: ошибка: {str(e)}")
    
    def md5sum(self, args):
        if not args:
            print("md5sum: требуется файл(ы)")
            return
        
        for filename in args:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'rb') as f:
                    md5_hash = hashlib.md5()
                    for chunk in iter(lambda: f.read(4096), b""):
                        md5_hash.update(chunk)
                    print(f"{md5_hash.hexdigest()}  {filename}")
            except FileNotFoundError:
                print(f"md5sum: {filename}: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"md5sum: {filename}: Это директория")
            except PermissionError:
                print(f"md5sum: {filename}: Отказано в доступе")
    
    def sha1sum(self, args):
        if not args:
            print("sha1sum: требуется файл(ы)")
            return
        
        for filename in args:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'rb') as f:
                    sha1_hash = hashlib.sha1()
                    for chunk in iter(lambda: f.read(4096), b""):
                        sha1_hash.update(chunk)
                    print(f"{sha1_hash.hexdigest()}  {filename}")
            except FileNotFoundError:
                print(f"sha1sum: {filename}: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"sha1sum: {filename}: Это директория")
            except PermissionError:
                print(f"sha1sum: {filename}: Отказано в доступе")
    
    def head(self, args):
        lines = 10
        files = []
        
        
        i = 0
        while i < len(args):
            if args[i] == "-n" and i + 1 < len(args):
                try:
                    lines = int(args[i+1])
                    i += 2
                except ValueError:
                    print(f"head: неверное количество строк: {args[i+1]}")
                    return
            else:
                files.append(args[i])
                i += 1
        
        if not files:
            print("head: требуется файл(ы)")
            return
        
        for filename in files:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'r') as f:
                    if len(files) > 1:
                        print(f"==> {filename} <==")
                    
                    for i, line in enumerate(f):
                        if i >= lines:
                            break
                        print(line.rstrip())
                    
                    if len(files) > 1 and filename != files[-1]:
                        print()
            except FileNotFoundError:
                print(f"head: невозможно открыть '{filename}' для чтения: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"head: ошибка чтения '{filename}': Это директория")
            except PermissionError:
                print(f"head: невозможно открыть '{filename}' для чтения: Отказано в доступе")
    
    def tail(self, args):
        lines = 10
        files = []
        follow = False
        
        
        i = 0
        while i < len(args):
            if args[i] == "-n" and i + 1 < len(args):
                try:
                    lines = int(args[i+1])
                    i += 2
                except ValueError:
                    print(f"tail: неверное количество строк: {args[i+1]}")
                    return
            elif args[i] == "-f":
                follow = True
                i += 1
            else:
                files.append(args[i])
                i += 1
        
        if not files:
            print("tail: требуется файл(ы)")
            return
        
        for filename in files:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'r') as f:
                    if len(files) > 1:
                        print(f"==> {filename} <==")
                    
                    # Читаем последние N строк
                    all_lines = f.readlines()
                    start = max(0, len(all_lines) - lines)
                    for line in all_lines[start:]:
                        print(line.rstrip())
                    
                    if follow:
                        print("\nРежим слежения (-f) не полностью поддерживается в эмуляторе. Нажмите Ctrl+C для выхода.")
                        try:
                            while True:
                                new_lines = f.readlines()
                                for line in new_lines:
                                    print(line.rstrip())
                                time.sleep(1)
                        except KeyboardInterrupt:
                            pass
                    
                    if len(files) > 1 and filename != files[-1]:
                        print()
            except FileNotFoundError:
                print(f"tail: невозможно открыть '{filename}' для чтения: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"tail: ошибка чтения '{filename}': Это директория")
            except PermissionError:
                print(f"tail: невозможно открыть '{filename}' для чтения: Отказано в доступе")
    
    def diff(self, args):
        if len(args) != 2:
            print("diff: требуется два файла для сравнения")
            return
        
        file1, file2 = args
        full_path1 = os.path.join(self.current_dir, file1) if not os.path.isabs(file1) else file1
        full_path2 = os.path.join(self.current_dir, file2) if not os.path.isabs(file2) else file2
        
        try:
            with open(full_path1, 'r') as f1, open(full_path2, 'r') as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
                
                for i, (line1, line2) in enumerate(zip(lines1, lines2)):
                    if line1 != line2:
                        print(f"{i+1}c{i+1}")
                        print(f"< {line1.rstrip()}")
                        print(f"> {line2.rstrip()}")
                
                if len(lines1) > len(lines2):
                    for i in range(len(lines2), len(lines1)):
                        print(f"{i+1}d{i}")
                        print(f"< {lines1[i].rstrip()}")
                elif len(lines2) > len(lines1):
                    for i in range(len(lines1), len(lines2)):
                        print(f"{i}a{i+1}")
                        print(f"> {lines2[i].rstrip()}")
        except FileNotFoundError as e:
            print(f"diff: {e.filename}: Нет такого файла или директории")
        except IsADirectoryError:
            print(f"diff: один из аргументов является директорией")
        except PermissionError:
            print(f"diff: невозможно открыть файл для чтения: Отказано в доступе")
    
    def sort(self, args):
        if not args:
            print("sort: требуется файл")
            return
        
        reverse = False
        numeric = False
        unique = False
        files = []
        
        
        for arg in args:
            if arg == "-r":
                reverse = True
            elif arg == "-n":
                numeric = True
            elif arg == "-u":
                unique = True
            else:
                files.append(arg)
        
        for filename in files:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'r') as f:
                    lines = [line.rstrip() for line in f.readlines()]
                    
                    if numeric:
                        
                        try:
                            lines.sort(key=lambda x: float(x) if x else 0, reverse=reverse)
                        except ValueError:
                            lines.sort(key=lambda x: float(x.split()[0]) if x else 0, reverse=reverse)
                    else:
                        # Обычная сортировка
                        lines.sort(reverse=reverse)
                    
                    if unique:
                        seen = set()
                        lines = [line for line in lines if not (line in seen or seen.add(line))]
                    
                    for line in lines:
                        print(line)
            except FileNotFoundError:
                print(f"sort: невозможно открыть '{filename}' для чтения: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"sort: ошибка чтения '{filename}': Это директория")
            except PermissionError:
                print(f"sort: невозможно открыть '{filename}' для чтения: Отказано в доступе")
    
    def wc(self, args):
        if not args:
            print("wc: требуется файл(ы)")
            return
        
        lines = False
        words = False
        chars = False
        files = []
        
        
        for arg in args:
            if arg == "-l":
                lines = True
            elif arg == "-w":
                words = True
            elif arg == "-c":
                chars = True
            else:
                files.append(arg)
        
        
        if not any([lines, words, chars]):
            lines = words = chars = True
        
        total_lines = 0
        total_words = 0
        total_chars = 0
        
        for filename in files:
            full_path = os.path.join(self.current_dir, filename) if not os.path.isabs(filename) else filename
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                    file_lines = content.count('\n')
                    file_words = len(content.split())
                    file_chars = len(content)
                    
                    output = []
                    if lines:
                        output.append(f"{file_lines:>8}")
                    if words:
                        output.append(f"{file_words:>8}")
                    if chars:
                        output.append(f"{file_chars:>8}")
                    
                    print(' '.join(output) + f" {filename}")
                    
                    total_lines += file_lines
                    total_words += file_words
                    total_chars += file_chars
            except FileNotFoundError:
                print(f"wc: невозможно открыть '{filename}' для чтения: Нет такого файла или директории")
            except IsADirectoryError:
                print(f"wc: ошибка чтения '{filename}': Это директория")
            except PermissionError:
                print(f"wc: невозможно открыть '{filename}' для чтения: Отказано в доступе")
        
        
        if len(files) > 1:
            output = []
            if lines:
                output.append(f"{total_lines:>8}")
            if words:
                output.append(f"{total_words:>8}")
            if chars:
                output.append(f"{total_chars:>8}")
            print(' '.join(output) + " итого")

def main():
    print("Добро пожаловать в Python WSL эмулятор!")
    print("Введите 'help' для списка команд, 'exit' для выхода\n")
    
    emulator = LinuxEmulator()
    
    try:
        while True:
            try:
                cmd = input(emulator.get_prompt()).strip()
                emulator.parse_command(cmd)
            except KeyboardInterrupt:
                print("^C")
            except EOFError:
                print()
                emulator.save_history()
                print("Выход из Python WSL эмулятора")
                break
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()