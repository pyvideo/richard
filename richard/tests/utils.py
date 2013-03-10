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

from functools import wraps


def with_save(func):
    """
    Decorates the given modelmaker adding the `save` keyword argument.

    If save is provided and its `True`, the created model will be
    saved after its creation.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        save = kwargs.pop('save', False)

        model = func(*args, **kwargs)

        if save and callable(getattr(model, 'save', None)):
            model.save()

        return model

    return wrapper
