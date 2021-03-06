# appends a file with user's data

import open_file
import read_from_stack
import write_to_stack
import lseek

O_RDONLY = 00000000
O_WRONLY = 00000001
O_RDWR   = 00000002
O_CREAT  = 00000100
O_APPEND = 00002000

SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

MAXSIZE  = 128

def generate(filepath, sock):
    """write with append option a file with user's data

    Args:
        filepath(str)    : file name to open

        sock(int/str/reg): read a sock to write data
    """

    sc = open_file.generate(filepath, O_WRONLY | O_CREAT | O_APPEND, 0644)
    #sc += lseek.generate('x6', 0, SEEK_END)
    sc += """
loop_1:
    """
    sc += write_to_stack.generate(sock, MAXSIZE)
    sc += """
    mov x5, x0
    """
    sc += read_from_stack.generate('x6', 'x0')

    sc += """
    cmp x5, %s
    beq loop_1
    """ % (MAXSIZE)

    return sc
