
def get_user_branch(user):
    grp_names = ['Baliwag', 'San Rafael', 'San Miguel']

    user_grp = user.groups.filter(name__in=grp_names).first()
    branch = user_grp.branch_set

    return branch
