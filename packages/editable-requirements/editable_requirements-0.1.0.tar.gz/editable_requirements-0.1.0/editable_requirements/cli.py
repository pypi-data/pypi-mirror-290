from pathlib import Path
from click import group, option, argument

@group('editreq')
def editreq():
    return 


def main():
    editreq()



@editreq.command()
@argument('folder', default='./', type=Path)
def generate(folder):
    from editable_requirements import generate_requirements
    generate_requirements(folder)


@editreq.command()
@argument('folder', default='./', type=Path)
@option('--output', '-o', help= 'Alternative output path')
@option('--pretend', '-p', help= 'Do not do anything. Just pretend', is_flag=True)
def rebuild(folder, output=None, pretend=False):
    from editable_requirements import rebuild_editables
    print(folder, output)
    rebuild_editables(folder, output, pretend)