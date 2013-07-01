"""

Ctimer - A timer context manager measuring the
clock wall time of the code block it contains.

Copyright (C) 2013 Balthazar Rouberol - <brouberol@imap.cc>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__version__ = '0.1.0'

from timeit import default_timer


class Timer(object):
    """ A timer as a context manager

    Wraps around a timer. A custom timer can be passed
    to the constructor. The default timer is timeit.default_timer.

    Note that the latter measures wall clock time, not CPU time!
    On Unix systems, it corresponds to time.time.
    On Windows systems, it corresponds to time.clock.

    """
    def __init__(self, timer=default_timer, factor=1):
        self.timer = timer
        self.factor = factor
        self.end = None

    def __call__(self):
        """ Return the current time """
        return self.timer()

    def __enter__(self):
        """ Set the start time """
        self.start = self()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Set the end time """
        self.end = self()

    def __str__(self):
        return '%.3f' % (self.elapsed)

    @property
    def elapsed(self):
        """ Return the current elapsed time since start

        If the `elapsed` property is called in the context manager scope,
        the elapsed time bewteen start and property access is returned.
        However, if it is accessed outside of the context manager scope,
        it returns the elapsed time bewteen entering and exiting the scope.

        The `elapsed` property can thus be accessed at different points within
        the context manager scope, to time different parts of the block.

        """
        if self.end is None:
            # if elapsed is called in the context manager scope
            return (self() - self.start) * self.factor
        else:
            # if elapsed is called out of the context manager scope
            return (self.end - self.start) * self.factor


def timer(**kwargs):
    """ Function decorator displaying the function execution time

    All kwargs are the arguments taken by the Timer class constructor.

    """
    def wrapped_f(f):
        def wrapped():
            with Timer(**kwargs) as t:
                out = f()
            print u"function %s execution time: %.3f " % (f.__name__, t.elapsed)
            return out
        return wrapped
    return wrapped_f