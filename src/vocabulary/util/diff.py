import difflib
from ..Config import Color

def show_diff(text, n_text):
    """
    http://stackoverflow.com/a/788780
    Unify operations between two compared strings seqm is a difflib.
    SequenceMatcher instance whose a & b are strings
    """
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        #print(opcode)
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append(Color.RED + seqm.b[b0:b1] + Color.END)
        elif opcode == 'delete':
            output.append(Color.GREEN + seqm.a[a0:a1] + Color.END)
        elif opcode == 'replace':
            # seqm.a[a0:a1] -> seqm.b[b0:b1]
            output.append(Color.BLUE + seqm.b[b0:b1] + Color.END)
        else:
            print("Error")
    return ''.join(output)