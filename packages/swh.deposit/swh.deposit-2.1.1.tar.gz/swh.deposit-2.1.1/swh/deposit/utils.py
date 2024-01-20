# Copyright (C) 2018-2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import logging
from typing import Any, Dict, Optional, Tuple, Union
from xml.etree import ElementTree

import iso8601

from swh.model.exceptions import ValidationError
from swh.model.model import TimestampWithTimezone
from swh.model.swhids import ExtendedSWHID, ObjectType, QualifiedSWHID

logger = logging.getLogger(__name__)


NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "app": "http://www.w3.org/2007/app",
    "dc": "http://purl.org/dc/terms/",
    "codemeta": "https://doi.org/10.5063/SCHEMA/CODEMETA-2.0",
    "sword": "http://purl.org/net/sword/terms/",
    "swh": "https://www.softwareheritage.org/schema/2018/deposit",
    "schema": "http://schema.org/",
}


def normalize_date(date):
    """Normalize date fields as expected by swh workers.

    If date is a list, elect arbitrarily the first element of that
    list

    If date is (then) a string, parse it through
    dateutil.parser.parse to extract a datetime.

    Then normalize it through
    :class:`swh.model.model.TimestampWithTimezone`

    Returns
        The swh date object

    """
    if isinstance(date, list):
        date = date[0]
    if isinstance(date, str):
        date = iso8601.parse_date(date)

    tstz = TimestampWithTimezone.from_dict(date)

    return {
        "timestamp": tstz.timestamp.to_dict(),
        "offset": tstz.offset_minutes(),
    }


def compute_metadata_context(swhid_reference: QualifiedSWHID) -> Dict[str, Any]:
    """Given a SWHID object, determine the context as a dict."""
    metadata_context: Dict[str, Any] = {"origin": None}
    if swhid_reference.qualifiers():
        metadata_context = {
            "origin": swhid_reference.origin,
            "path": swhid_reference.path,
        }
        snapshot = swhid_reference.visit
        if snapshot:
            metadata_context["snapshot"] = snapshot

        anchor = swhid_reference.anchor
        if anchor:
            metadata_context[anchor.object_type.name.lower()] = anchor

    return metadata_context


ALLOWED_QUALIFIERS_NODE_TYPE = (
    ObjectType.SNAPSHOT,
    ObjectType.REVISION,
    ObjectType.RELEASE,
    ObjectType.DIRECTORY,
)


def parse_swh_metadata_provenance(
    metadata: ElementTree.Element,
) -> Optional[str]:
    """Parse swh metadata-provenance within the metadata dict reference if found, None
    otherwise.

    .. code-block:: xml

         <swh:deposit>
           <swh:metadata-provenance>
             <schema:url>https://example.org/metadata/url</schema:url>
           </swh:metadata-provenance>
         </swh:deposit>

    Args:
        metadata: result of parsing an Atom document with :func:`parse_xml`

    Raises:
        ValidationError in case of invalid xml

    Returns:
        Either the metadata provenance url if any or None otherwise

    """
    url_element = metadata.find(
        "swh:deposit/swh:metadata-provenance/schema:url", namespaces=NAMESPACES
    )
    if url_element is not None:
        return url_element.text
    return None


def parse_swh_deposit_origin(
    metadata: ElementTree.Element,
) -> Tuple[Optional[str], Optional[str]]:
    """Parses <swh:add_to_origin> and <swh:create_origin> from metadata document,
    if any.

    .. code-block:: xml

       <swh:deposit>
         <swh:create_origin>
           <swh:origin url='https://example.org/repo/software123/'/>
         </swh:reference>
       </swh:deposit>

    .. code-block:: xml

       <swh:deposit>
         <swh:add_to_origin>
           <swh:origin url='https://example.org/repo/software123/'/>
         </swh:add_to_origin>
       </swh:deposit>

    Returns:
        tuple of (origin_to_create, origin_to_add). If both are non-None, this
        should typically be an error raised to the user.
    """
    create_origin = metadata.find(
        "swh:deposit/swh:create_origin/swh:origin", namespaces=NAMESPACES
    )
    add_to_origin = metadata.find(
        "swh:deposit/swh:add_to_origin/swh:origin", namespaces=NAMESPACES
    )

    return (
        None if create_origin is None else create_origin.attrib["url"],
        None if add_to_origin is None else add_to_origin.attrib["url"],
    )


def parse_swh_reference(
    metadata: ElementTree.Element,
) -> Optional[Union[QualifiedSWHID, str]]:
    """Parse <swh:reference> within the metadata document, if any.

    .. code-block:: xml

       <swh:deposit>
         <swh:reference>
           <swh:origin url='https://github.com/user/repo'/>
         </swh:reference>
       </swh:deposit>

    or:

    .. code-block:: xml

       <swh:deposit>
         <swh:reference>
           <swh:object swhid="swh:1:dir:31b5c8cc985d190b5a7ef4878128ebfdc2358f49;origin=https://hal.archives-ouvertes.fr/hal-01243573;visit=swh:1:snp:4fc1e36fca86b2070204bedd51106014a614f321;anchor=swh:1:rev:9c5de20cfb54682370a398fcc733e829903c8cba;path=/moranegg-AffectationRO-df7f68b/" />
       </swh:deposit>

    Args:
        metadata: result of parsing an Atom document

    Raises:
        ValidationError in case the swhid referenced (if any) is invalid

    Returns:
        Either swhid or origin reference if any. None otherwise.

    """  # noqa
    ref_origin = metadata.find(
        "swh:deposit/swh:reference/swh:origin[@url]", namespaces=NAMESPACES
    )
    if ref_origin is not None:
        return ref_origin.attrib["url"]

    ref_object = metadata.find(
        "swh:deposit/swh:reference/swh:object[@swhid]", namespaces=NAMESPACES
    )
    if ref_object is None:
        return None
    swhid = ref_object.attrib["swhid"]
    if not swhid:
        return None

    swhid_reference = QualifiedSWHID.from_string(swhid)

    if swhid_reference.qualifiers():
        anchor = swhid_reference.anchor
        if anchor:
            if anchor.object_type not in ALLOWED_QUALIFIERS_NODE_TYPE:
                error_msg = (
                    "anchor qualifier should be a core SWHID with type one of "
                    f"{', '.join(t.name.lower() for t in ALLOWED_QUALIFIERS_NODE_TYPE)}"
                )
                raise ValidationError(error_msg)

        visit = swhid_reference.visit
        if visit:
            if visit.object_type != ObjectType.SNAPSHOT:
                raise ValidationError(
                    f"visit qualifier should be a core SWHID with type snp, "
                    f"not {visit.object_type.value}"
                )

        if (
            visit
            and anchor
            and visit.object_type == ObjectType.SNAPSHOT
            and anchor.object_type == ObjectType.SNAPSHOT
        ):
            logger.warn(
                "SWHID use of both anchor and visit targeting "
                f"a snapshot: {swhid_reference}"
            )
            raise ValidationError(
                "'anchor=swh:1:snp:' is not supported when 'visit' is also provided."
            )

    return swhid_reference


def extended_swhid_from_qualified(swhid: QualifiedSWHID) -> ExtendedSWHID:
    """Used to get the target of a metadata object from a <swh:reference>,
    as the latter uses a QualifiedSWHID."""
    return ExtendedSWHID.from_string(str(swhid).split(";")[0])


def to_header_link(link: str, link_name: str) -> str:
    """Build a single header link.

    >>> link_next = to_header_link("next-url", "next")
    >>> link_next
    '<next-url>; rel="next"'
    >>> ','.join([link_next, to_header_link("prev-url", "prev")])
    '<next-url>; rel="next",<prev-url>; rel="prev"'

    """
    return f'<{link}>; rel="{link_name}"'
