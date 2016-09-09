import modes

def mode_from_int(int_mode):
    retval = ""

    if int_mode == modes.SELINUX_DISABLED:
        retval += "disabled"
    elif int_mode == modes.SELINUX_ENFORCING:
        retval += "enforcing"
    elif int_mode == modes.SELINUX_PERMISSIVE:
        retval += "permissive"
# it doesn't matter if we have a trailing else clause or not
# uncomment this to experiment
#    else:
#        retval += "unknown"

    return retval
