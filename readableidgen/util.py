import os
from datetime import datetime

import colorama


def load_corpus(fnm, path='corpus') -> list[str]:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), path, fnm)) as f:
        return [wd.strip() for wd in f.readlines()]


def now(as_str=True, sep=':'):
    d = datetime.now()
    return d.strftime(f'%Y-%m-%d %H{sep}%M{sep}%S') if as_str else d  # Considering file output path


def log(s, c: str = 'log', as_str=False):
    """
    Prints `s` to console with color `c`
    """
    if not hasattr(log, 'reset'):
        log.reset = colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL
    if not hasattr(log, 'd'):
        log.d = dict(
            log='',
            warn=colorama.Fore.YELLOW,
            error=colorama.Fore.RED,
            err=colorama.Fore.RED,
            success=colorama.Fore.GREEN,
            suc=colorama.Fore.GREEN,
            info=colorama.Fore.BLUE,
            i=colorama.Fore.BLUE,

            y=colorama.Fore.YELLOW,
            yellow=colorama.Fore.YELLOW,
            red=colorama.Fore.RED,
            r=colorama.Fore.RED,
            green=colorama.Fore.GREEN,
            g=colorama.Fore.GREEN,
            blue=colorama.Fore.BLUE,
            b=colorama.Fore.BLUE,
        )
    if c in log.d:
        c = log.d[c]
    if as_str:
        return f'{c}{s}{log.reset}'
    else:
        print(f'{c}{now()}| {s}{log.reset}')


def logs(s, c='log'):
    return log(s, c=c, as_str=True)


def logi(s):
    """
    Syntactic sugar for logging `info`
    """
    return logs(s, c='i')

