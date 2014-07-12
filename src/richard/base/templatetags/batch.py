# richard -- video index system
# Copyright (C) 2012, 2013 richard contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django import template


register = template.Library()


@register.filter
def batch(elems, args):
    """Filter that batches an iterator into batchsize sized groups

    Takes a single string argument in one of two forms:

    1. batchsize as an int. e.g. ``batch:"4"``
    2. batchsize as an int followed by a comma followed by a string to
       pad the last row with. e.g. ``batch:"4,&nbsp"``

    """
    args = args.split(',')
    batchsize = int(args[0])
    if len(args) > 1:
        padwith = args[1]
    else:
        padwith = None

    if batchsize == 0:
        return []

    if batchsize == 1:
        return elems

    batch = []
    batches = []
    for i, elem in enumerate(elems):
        if i % batchsize == 0:
            if batch:
                batches.append(batch)
                batch = []

        batch.append(elem)

    if batch:
        if padwith is not None:
            while len(batch) % batchsize != 0:
                batch.append(padwith)

        batches.append(batch)

    return batches
