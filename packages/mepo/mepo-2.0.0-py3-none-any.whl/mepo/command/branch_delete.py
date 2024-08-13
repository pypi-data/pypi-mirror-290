from ..state import MepoState
from ..utilities import verify
from ..git import GitRepository


def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2delbr = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2delbr:
        git = GitRepository(comp.remote, comp.local)
        git.delete_branch(args.branch_name, args.force)
        print("- {}: {}".format(comp.name, args.branch_name))
