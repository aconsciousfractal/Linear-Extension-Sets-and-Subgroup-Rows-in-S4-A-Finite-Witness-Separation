from itertools import permutations, combinations

S4 = tuple(permutations((1, 2, 3, 4)))


def transitive_closure(rel):
    closure = set(rel)
    changed = True
    while changed:
        changed = False
        for a, b in list(closure):
            for c, d in list(closure):
                if b == c and (a, d) not in closure:
                    closure.add((a, d))
                    changed = True
    return closure


def is_strict_poset(rel):
    closure = transitive_closure(rel)
    return closure == set(rel) and all(a != b for a, b in rel)


def linear_extensions(rel):
    return {
        word
        for word in S4
        if all(word.index(a) < word.index(b) for a, b in rel)
    }


def compose(p, q):
    return tuple(p[q[i] - 1] for i in range(4))


def is_subgroup(words):
    identity = (1, 2, 3, 4)
    rows = set(words)
    return identity in rows and all(compose(a, b) in rows for a in rows for b in rows)


def common_precedence(words):
    rows = set(words)
    rel = set()
    for a, b in permutations((1, 2, 3, 4), 2):
        if all(word.index(a) < word.index(b) for word in rows):
            rel.add((a, b))
    return transitive_closure(rel)


def generated_subgroup(generators):
    rows = {(1, 2, 3, 4), *generators}
    changed = True
    while changed:
        changed = False
        for a in list(rows):
            for b in list(rows):
                c = compose(a, b)
                if c not in rows:
                    rows.add(c)
                    changed = True
    return rows


def test_strict_labeled_posets_on_four_labels_count_219():
    pairs = [(a, b) for a, b in permutations((1, 2, 3, 4), 2)]
    posets = []
    for mask in range(1 << len(pairs)):
        rel = {pairs[i] for i in range(len(pairs)) if mask & (1 << i)}
        if is_strict_poset(rel):
            posets.append(frozenset(rel))
    assert len(posets) == 219


def test_linear_extension_sets_of_strict_posets_are_219_distinct():
    pairs = [(a, b) for a, b in permutations((1, 2, 3, 4), 2)]
    extension_sets = set()
    for mask in range(1 << len(pairs)):
        rel = {pairs[i] for i in range(len(pairs)) if mask & (1 << i)}
        if is_strict_poset(rel):
            extension_sets.add(frozenset(linear_extensions(rel)))
    assert len(extension_sets) == 219


def test_s4_subgroup_count_is_30_under_locked_composition():
    subgroups = {frozenset({(1, 2, 3, 4)})}
    for a in S4:
        subgroups.add(frozenset(generated_subgroup({a})))
    for a, b in combinations(S4, 2):
        subgroups.add(frozenset(generated_subgroup({a, b})))
    for a, b, c in combinations(S4, 3):
        subgroups.add(frozenset(generated_subgroup({a, b, c})))
    assert all(is_subgroup(rows) for rows in subgroups)
    assert len(subgroups) == 30


def test_d4_v4_common_precedence_empty_and_closure_all_s4():
    d4 = {
        (1, 2, 3, 4),
        (1, 3, 2, 4),
        (2, 1, 4, 3),
        (2, 4, 1, 3),
        (3, 1, 4, 2),
        (3, 4, 1, 2),
        (4, 2, 3, 1),
        (4, 3, 2, 1),
    }
    v4 = {
        (1, 2, 3, 4),
        (2, 1, 4, 3),
        (3, 4, 1, 2),
        (4, 3, 2, 1),
    }
    for row in (d4, v4):
        rel = common_precedence(row)
        assert rel == set()
        assert linear_extensions(rel) == set(S4)
        assert len(row) != len(S4)


def test_n_poset_has_five_extensions_and_is_not_subgroup_size():
    n_rel = {(1, 3), (2, 3), (2, 4)}
    expected = {
        (1, 2, 3, 4),
        (1, 2, 4, 3),
        (2, 1, 3, 4),
        (2, 1, 4, 3),
        (2, 4, 1, 3),
    }
    extensions = linear_extensions(n_rel)
    assert extensions == expected
    assert len(extensions) == 5
    assert len(S4) % len(extensions) != 0