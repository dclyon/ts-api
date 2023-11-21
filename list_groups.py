import grp


def list_groups():
    return [g.gr_name for g in grp.getgrall()]


# If you want to test the function independently
if __name__ == '__main__':
    print(list_groups())
