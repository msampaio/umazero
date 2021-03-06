#!/usr/bin/env python
# -*- coding: utf-8 -*-

import music21
import _utils
import retrieval
import song


def _aux_getBy(segments, save):
    allseg = getSegmentsData(segments)
    allseg.segments = segments
    allseg.segments_number = len(allseg.segments)
    allseg.save = save
    return allseg


class AllSegments(object):
    """Class for a set of Segment objects. This class has attributes
    and methods to return information about Segment objects
    parameters."""

    def __init__(self):
        self.save = None
        self.segments = None
        self.segments_number = None

        self.allComposers = None
        self.allTitles = None
        self.allCollections = None
        self.allContours = None
        self.allContourSizes = None
        self.allContourPrimes = None
        self.allAmbitus = None
        self.allTimeSignatures = None
        self.allMeters = None
        self.allIntervals = None
        self.allSemitoneIntervals = None
        self.allFirstIntervals = None
        self.allLastIntervals = None
        self.allFilenames = None

    def __repr__(self):
        return "<AllSegments: {0} segments>".format(self.segments_number)

    def getByIndex(self, index):
        """Return a Segment object by a given index number."""

        return self.segments[index]

    def getByTypeOf(self, typeof):
        """Return a new AllSegment object with all Segment objects
        with a given type as attribute, such as Phrase or Link."""

        return _aux_getBy([seg for seg in self.segments if seg.typeof == typeof], self.save)

    def getByComposer(self, composer):
        """Return a new AllSegment object with all Segment objects
        with a given composer as attribute. It's possible to exclude
        the given composer, to find the complement of his segments
        """

        if composer == 'All composers':
            return self
        else:
            if composer[0] == '!':
                return _aux_getBy([seg for seg in self.segments if composer[1:] not in seg.composers], self.save)
            else:
                return _aux_getBy([seg for seg in self.segments if composer in seg.composers], self.save)

    def getByTitle(self, title):
        """Return a new AllSegment object with all Segment objects
        with a given song title as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.title == title], self.save)

    def getByAmbitus(self, ambitus):
        """Return a new AllSegment object with all Segment objects
        with a given ambitus value as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.ambitus == ambitus], self.save)

    def getByContourPrime(self, contour_prime):
        """Return a new AllSegment object with all Segment objects
        with a given Contour Prime value as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.contour_prime == contour_prime], self.save)

    def getByPickup(self, pickup=True):
        """Return a new AllSegment object with all Segment objects
        with pickup measure."""

        return _aux_getBy([seg for seg in self.segments if seg.pickup == pickup], self.save)

    def getByInterval(self, interval, without=False):
        """Return a new AllSegment object with all Segment objects
        with a given _interval value as attribute."""

        if without:
            return _aux_getBy([seg for seg in self.segments if interval not in seg.intervals], self.save)
        else:
            return _aux_getBy([seg for seg in self.segments if interval in seg.intervals], self.save)

    def getBySemitoneInterval(self, interval):
        """Return a new AllSegment object with all Segment objects
        with a given _interval value as attribute."""

        return _aux_getBy([seg for seg in self.segments if interval in seg.intervals_with_direction_semitones], self.save)

    def getByFirstInterval(self, first_interval):
        """Return a new AllSegment object with all Segment objects
        with a given first_interval value as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.first_interval == first_interval], self.save)

    def getByLastInterval(self, last_interval):
        """Return a new AllSegment object with all Segment objects
        with a given last_interval value as attribute."""

        return _aux_getBy([seg for seg in self.segments if seg.last_interval == last_interval], self.save)


def getData(SegmentsList, attrib):
    """Return all attribute values from a given Segments objects list
    and attribute."""

    s = set()
    r = []
    for SegmentObj in SegmentsList:
        value = getattr(SegmentObj, attrib)
        if type(value) == music21.contour.contour.Contour:
            value = tuple(value)
            s.add(value)
            r = [music21.contour.contour.Contour(cseg) for cseg in sorted(s)]
        elif type(value) == list:
            for el in value:
                s.add(el)
                r = sorted(s)
        else:
            s.add(value)
            r = sorted(s)
    return r


def getSegmentsData(SegmentsList):
    """Return a dictionary with the data raised in Segment objects."""


    allseg = AllSegments()
    allseg.allComposers = getData(SegmentsList, 'composers')
    allseg.allTitles = getData(SegmentsList, 'title')
    allseg.allCollections = getData(SegmentsList, 'collection')
    allseg.allContours = getData(SegmentsList, 'contour')
    allseg.allContourSizes = getData(SegmentsList, 'contour_size')
    allseg.allContourPrimes = getData(SegmentsList, 'contour_prime')
    allseg.allAmbitus = getData(SegmentsList, 'ambitus')
    allseg.allTimeSignatures = getData(SegmentsList, 'time_signature')
    allseg.allMeters = getData(SegmentsList, 'meter')
    allseg.allIntervals = getData(SegmentsList, 'intervals')
    allseg.allSemitoneIntervals = getData(SegmentsList, 'intervals_with_direction_semitones')
    allseg.allFirstIntervals = getData(SegmentsList, 'first_interval')
    allseg.allLastIntervals = getData(SegmentsList, 'last_interval')
    allseg.allFilenames = getData(SegmentsList, 'filename')

    return allseg


def makeAllSegmentsBySongSequence(songs, save=False):
    """Return an AllSegment object with all Segment objects from a
    given sequence of songs."""

    SegmentsList = []

    for s in songs:
        SegmentsList.extend(s.segments)

    allseg = getSegmentsData(SegmentsList)
    allseg.segments = SegmentsList
    allseg.segments_number = len(allseg.segments)
    allseg.save = save
    return allseg


def makeAllSegmentsByCollection(collection, save=False):
    """Return an AllSegment object with all Segment objects from a
    given collection name."""

    songs = retrieval.load_pickle('songs', collection)

    return makeAllSegmentsBySongSequence(songs, save)


def makeAllSegments(path='choros-corpus', save=False):
    """Return an AllSegment object with all Segment objects saved in a
    pickle or in available collections."""

    if save:
        songs = retrieval.load_pickle()
    else:
        songs = song.makeSongAllCollections(True)

    return makeAllSegmentsBySongSequence(songs, True)


def composersFilter(allSegmentsObj, percentual=0.03):
    def segmentsPercentual(composer, segments_total):
        return allSegmentsObj.getByComposer(composer).segments_number / float(segments_total)

    composers = allSegmentsObj.allComposers
    segments_total = allSegmentsObj.segments_number

    return [composer for composer in composers if segmentsPercentual(composer, segments_total) >= percentual]
