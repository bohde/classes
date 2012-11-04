from itertools import imap, ifilter

def head(seq):
    return seq[0]


def tail(seq):
    return seq[1:]


def not_in_tails(seq):
    tails = map(tail, seq)
    return lambda c: all(c not in s for s in tails)


def tail_if_not_eq(val):
    return lambda s: tail(s) if head(s) == val else s


def non_empty(seq):
    return filter(bool, seq)


def merge_mro(seqs):
    seqs = map(list, seqs)

    non_empty_seqs = non_empty(seqs)

    while True:
        try:
            heads = imap(head, non_empty_seqs)
            cand = next(ifilter(not_in_tails(non_empty_seqs),
                                heads))
        except StopIteration:
            raise Exception("Inconsistent hierarchy")

        yield cand

        non_empty_seqs = non_empty(
            map(tail_if_not_eq(cand), non_empty_seqs))

        if not non_empty_seqs:
            return
