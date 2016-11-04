import modes

def mode_from_str(str_mode):
    retval = None

    if str_mode == "disabled":
        retval = modes.SELINUX_DISABLED
    elif str_mode == "enforcing":
        retval = modes.SELINUX_ENFORCING
    elif str_mode == "permissive":
        retval = modes.SELINUX_PERMISSIVE

    return retval
