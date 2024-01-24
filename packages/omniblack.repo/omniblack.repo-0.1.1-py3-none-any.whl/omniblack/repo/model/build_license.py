from operator import attrgetter
from os import path, PathLike
from json import load, dump, JSONDecodeError

from requests import Session
from pydantic import BaseModel

from omniblack.model import Model
from .unicode import ensure_id_start
from .display import display


class LicenseInfo(BaseModel):
    isDeprecatedLicenseId: bool
    name: str
    licenseId: str


class LicenseList(BaseModel):
    licenses: list[LicenseInfo]


class GitObject(BaseModel):
    sha: str


class GitRef(BaseModel):
    object: GitObject


def ensure_valid_id(raw_id: str) -> str:
    replaced_id = raw_id.translate(replacements)

    return ensure_id_start(replaced_id)


replacements = str.maketrans({
    '-': '_',
    '.': '_',
    '+': '_plus',
    '(': '',
    ')': '',
})

checkUrl = "https://api.github.com/repos/spdx/license-list-data/git/refs/heads/main"
url = "https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json"


UNIT_SEPARATOR = '\u001F'


def update_needed(s, built_file: PathLike):
    with s.get(checkUrl) as resp:
        raw_obj = resp.json()

    main_ref = GitRef.model_validate(raw_obj)

    try:
        with open(built_file, mode='r') as file_obj:
            raw_current = load(file_obj)
    except JSONDecodeError:
        return main_ref.object.sha

    if raw_current.get('__version') != main_ref.object.sha:
        return main_ref.object.sha


def update_file(
    session: Session,
    new_version: str,
    built_file: PathLike,
    template_file: PathLike,
):
    meta_model = Model('', no_expose=True).load_meta_model(
        'Meta Model',
        no_expose=True,
    )
    choice_member = meta_model.structs.choice_member
    ui_string = meta_model.structs.ui_string

    with session.get(url, stream=True) as resp:
        raw_obj = resp.json()

    parsed = LicenseList.model_validate(raw_obj)

    enum_members = [
        choice_member(
            internal=ensure_valid_id(license.licenseId),
            name=license.licenseId,
            display=ui_string(en=license.name),
        )
        for license in sorted(parsed.licenses, key=attrgetter('licenseId'))
    ]

    with open(template_file, mode='r') as file:
        template = load(file)

    id_field = template['fields'][1]

    id_field['choice_attrs']['choices'] = [
        meta_model.coerce_to(enum_member, 'json')
        for enum_member in enum_members
    ]

    template['__version'] = new_version

    with open(built_file, mode='w') as file:
        dump(template, file)


with Session() as s:
    model_dir = path.dirname(__file__)
    built_file = path.join(model_dir, 'license.json')
    template_file = path.join(model_dir, 'license.json.template')

    if new_version := update_needed(s, built_file):
        update_file(s, new_version, built_file, template_file)
        display.print('[green]license.json has been rebuilt.[/]')
    else:
        display.print('[blue]No update needed[/]')
