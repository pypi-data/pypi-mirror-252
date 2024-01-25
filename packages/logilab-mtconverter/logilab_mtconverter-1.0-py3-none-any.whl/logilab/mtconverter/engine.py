# copyright 2006-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-mtconverter.
#
# logilab-mtconverter is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-mtconverter is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-mtconverter. If not, see <http://www.gnu.org/licenses/>.
"""the transformation engine"""

from logilab.mtconverter import TransformData, TransformError
from logilab.mtconverter.transform import Transform, TransformsChain

from typing import Tuple, Dict, List, Optional


def split_mimetype(mimetype: str) -> Tuple[str, str]:
    try:
        main, sub = mimetype.split("/")
    except ValueError:
        raise TransformError(f"bad mime type {mimetype}")
    if not (main and sub):
        raise TransformError(f"bad mime type {mimetype}")
    return main, sub


class TransformEngine:
    """mimetype oriented conversions engine"""

    def __init__(self) -> None:
        self._mtmap: Dict[str, dict] = {}
        self._mtmainmap: Dict[str, dict] = {}
        self.transforms: Dict[str, Transform] = {}

    def add_transform(self, transform: Transform) -> None:
        """register a new transform"""
        self._map_transform(transform)

    def remove_transform(self, name: str, *inputs: str) -> None:
        """unregister a transform
        name is the name of a registered transform
        """
        self._unmap_transform(self.transforms[name], *inputs)

    def has_input(self, mimetype: str) -> bool:
        """return True if the engine has a transformation taking the given
        mimetype as input
        """
        return mimetype in self._mtmap or split_mimetype(mimetype)[0] in self._mtmainmap

    def convert(self, trdata: TransformData, targetmimetype: str) -> TransformData:
        """convert the given data structure into the given mime type"""
        trdata.check_encoding()
        # get a path to output mime type
        #
        # even if target mime type is the same as input mime type, try
        # to find a path in case an identity transform is available
        path = self.find_path(trdata.mimetype, targetmimetype)
        if not path:
            if trdata.mimetype == targetmimetype:
                return trdata
            raise TransformError(
                f"no transformation path from {trdata.mimetype} to {targetmimetype}"
            )
        if len(path) > 1:
            transform = TransformsChain("aname", path)
        else:
            transform = path[0]
        return transform.convert(trdata)

    def _map_transform(self, transform: Transform) -> None:
        """map transform to internal structures"""
        if not (transform.inputs and transform.output):
            raise TransformError("transform is missing input or output")
        if split_mimetype(transform.output)[1] == "*":
            raise TransformError(
                "bad output mime type, wildcard only allowed in inputs"
            )
        if transform.name in self.transforms:
            raise TransformError(f"a transform named {transform.name} already exists")
        for mt in transform.inputs:
            main, sub = split_mimetype(mt)
            if sub == "*":
                inmap = self._mtmainmap.setdefault(main, {})
            else:
                inmap = self._mtmap.setdefault(mt, {})
            try:
                inmap[transform.output].append(transform)
            except KeyError:
                inmap[transform.output] = [transform]
        assert transform.name is not None
        self.transforms[transform.name] = transform

    def _unmap_transform(self, transform: Transform, *inputs: str) -> None:
        """unmap transform from internal structures"""
        if not inputs:
            inputs = transform.inputs  # type: ignore[assignment]
        for mt in inputs:
            main, sub = split_mimetype(mt)
            if sub == "*":
                inmap = self._mtmainmap[main]
            else:
                inmap = self._mtmap[mt]
            inmap[transform.output].remove(transform)
        assert transform.name is not None
        del self.transforms[transform.name]

    def find_path(
        self, orig: str, target: str, required_transforms: List[str] = []
    ) -> Optional[TransformsChain]:
        """return the shortest path for transformation from orig mimetype to
        target mimetype
        """
        # naive algorithm :
        #  find all possible paths with required transforms
        #  take the shortest
        #
        # it should be enough since we should not have so much possible paths
        # and I wouldn't like to get a 1000 transformations path
        shortest, winner = 100, None
        for path in self._get_paths(orig, target, required_transforms):
            if len(path) < shortest:
                winner = path
                shortest = len(path)
        return winner

    def _get_paths(  # type: ignore[no-untyped-def]
        self, orig: str, target: str, requirements: List[str], path=None, result=None
    ) -> List[TransformsChain]:
        """return a all path for transformation from orig mimetype to
        target mimetype
        """
        if (
            path is None
        ):  # FIXME: why not empty list as default value for path & result?
            result = []
            path = []
            requirements = list(requirements)
        # get main type, and check mime type at the same time
        main = split_mimetype(orig)[0]
        # search most specific first
        outputs = self._mtmap.get(orig)
        if outputs is not None:
            self._search_outputs(outputs, target, requirements, path, result)
        # then search generic wildcard transforms
        outputs = self._mtmainmap.get(main)
        if outputs is not None:
            self._search_outputs(outputs, target, requirements, path, result)
        # we are done
        return result

    def _search_outputs(
        self,
        outputs: Dict[str, List[Transform]],
        target: str,
        requirements: List[str],
        path: List[Optional[Transform]],
        result: List[List[Optional[Transform]]],
    ) -> None:
        path.append(None)
        for outputmimetype, transforms in outputs.items():
            for transform in transforms:
                required = False
                name = transform.name
                if name in requirements:
                    requirements.remove(name)
                    required = True
                if transform in path:
                    # avoid infinite loop...
                    continue
                path[-1] = transform
                if outputmimetype == target:
                    if not requirements:
                        assert result is not None
                        result.append(path[:])
                else:
                    self._get_paths(outputmimetype, target, requirements, path, result)
                if required:
                    assert name is not None
                    requirements.append(name)
        path.pop()
