from flops_utils.timer import Timer

_context = None


def init_context():
    global _context
    _context = Timer()


def get_context():
    return _context
