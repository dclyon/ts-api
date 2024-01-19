# function to list each group
import grp


def list_groups():
    return [g.gr_name for g in grp.getgrall()]


if __name__ == '__main__':
    print(list_groups())
