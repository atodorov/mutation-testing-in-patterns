import modes

def mode_from_int(int_mode):
    retval = ""

    if int_mode == modes.SELINUX_DISABLED:
        retval += "disabled"
    elif int_mode == modes.SELINUX_ENFORCING:
        retval += "enforcing"
    elif int_mode == modes.SELINUX_PERMISSIVE:
        retval += "permissive"

    return retval
