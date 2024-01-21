from os import EX_CONFIG, environ
from sys import exit
from os.path import join

from public import public
from rich.prompt import InvalidResponse, PromptBase
from rich.text import Text
from ruamel.yaml import YAML
from sh import ErrorReturnCode, git

from .display import error

yaml = YAML()
load = yaml.load
dump = yaml.dump

try:
    branches_path = join(environ['DOTFILES'],  'branches.yaml')
except KeyError:
    pass


def bad_brach(branch: str) -> Text:
    return Text.assemble(
        (branch, 'bold red'),
        'is not a valid git branch',
    )


def is_good_branch(_, current: str) -> bool:
    try:
        git('rev-parse', '--quiet', '--verify', current)
    except ErrorReturnCode:
        return False
    else:
        return True


class Prompt(PromptBase[str]):
    response_type = str

    check_choice = is_good_branch

    def on_validate_error(self, current, err):
        msg = Text.assemble((current, 'red'), 'is not a git branch')
        newErr = InvalidResponse(msg)
        return super().on_validate_error(current, newErr)


remote = 'origin'


def load_branches():
    with open(branches_path) as branches_file:
        return load(branches_file)


def get_env():
    try:
        return environ['WRK_ENV']
    except KeyError:
        error.print('[red][bold]`WRK_ENV`[/bold] is not set.[/]')
        error.print('Are you in a wrk environment?')
        exit(EX_CONFIG)


@public
def get_branch():
    wrk_env = get_env()
    branches = load_branches()
    main_branch = branches.get(wrk_env, 'master')

    if not is_good_branch(None, main_branch):
        error.print(bad_brach(main_branch))
        prompt = Prompt()
        main_branch = prompt.ask(
            f'What is the main branch of [green]{wrk_env}[/]?'
        )

        branches[wrk_env] = main_branch

        with open(branches_path, 'w') as branches_file:
            dump(branches, branches_file)

        return branches[wrk_env]
    else:
        return main_branch
