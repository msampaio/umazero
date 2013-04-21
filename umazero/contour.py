#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from music21.contour import Contour
import _utils


def counting(seq):
    if type(seq[0]) == Contour:
        seq = [tuple(x) for x in seq]
    return Counter(seq)


# FIXME: Update music21 with contour package to use Sampaio Prime Form Algorithm
def sampaio(cseg):
    i = cseg.inversion()
    r = cseg.retrogression()
    ri = i.retrogression()
    return Contour(sorted([list(cseg), list(i), list(r), list(ri)])[0])


def contour_prime_count(MusicUnitsList):
    return counting([sampaio(un.contour.reduction_morris()[0]) for un in MusicUnitsList])


def contour_highest_cp_count(MusicUnitsList):
    return counting([max(un.contour.translation()) for un in MusicUnitsList])


def contour_oscillation_count(MusicUnitsList):
    return counting([MusicUnitObj.contour.oscillation_index() for MusicUnitObj in MusicUnitsList])


def first_movement(MusicUnitsList):
    return counting([MusicUnitObj.contour.internal_diagonals()[0] for MusicUnitObj in MusicUnitsList])


def last_movement(MusicUnitsList):
    return counting([MusicUnitObj.contour.internal_diagonals()[-1] for MusicUnitObj in MusicUnitsList])


def passing_contour(MusicUnitObj):
    reduced = MusicUnitObj.contour.reduction_bor(3)
    size = MusicUnitObj.contour_size
    reduced_size = len(reduced)
    return 1 - (reduced_size / float(size))


def multicount(MusicUnitsList, fn):
    return counting([fn(MusicUnitObj) for MusicUnitObj in MusicUnitsList])
