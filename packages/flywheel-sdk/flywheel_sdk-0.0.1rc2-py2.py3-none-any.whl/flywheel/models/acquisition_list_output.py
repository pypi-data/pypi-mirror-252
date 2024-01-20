# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401
import six

from flywheel.models.acquisition_parents import AcquisitionParents  # noqa: F401,E501
from flywheel.models.file_list_output import FileListOutput  # noqa: F401,E501
from flywheel.models.join_origins import JoinOrigins  # noqa: F401,E501
from flywheel.models.note import Note  # noqa: F401,E501
from flywheel.models.role_permission import RolePermission  # noqa: F401,E501

from .mixins import AcquisitionMixin
class AcquisitionListOutput(AcquisitionMixin):

    swagger_types = {
        'id': 'str',
        'parents': 'AcquisitionParents',
        'label': 'str',
        'session': 'str',
        'info': 'object',
        'info_exists': 'bool',
        'metadata': 'object',
        'uid': 'str',
        'timestamp': 'datetime',
        'timezone': 'str',
        'created': 'datetime',
        'tags': 'list[str]',
        'modified': 'datetime',
        'revision': 'int',
        'permissions': 'list[RolePermission]',
        'notes': 'list[Note]',
        'analyses': 'list[union[AnalysisListOutput,AnalysisListOutputInflatedJob]]',
        'collections': 'list[str]',
        'join_origin': 'JoinOrigins',
        'files': 'list[FileListOutput]',
        'copy_of': 'str',
        'original_copy_of': 'str'
    }

    attribute_map = {
        'id': '_id',
        'parents': 'parents',
        'label': 'label',
        'session': 'session',
        'info': 'info',
        'info_exists': 'info_exists',
        'metadata': 'metadata',
        'uid': 'uid',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'created': 'created',
        'tags': 'tags',
        'modified': 'modified',
        'revision': 'revision',
        'permissions': 'permissions',
        'notes': 'notes',
        'analyses': 'analyses',
        'collections': 'collections',
        'join_origin': 'join-origin',
        'files': 'files',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of'
    }

    rattribute_map = {
        '_id': 'id',
        'parents': 'parents',
        'label': 'label',
        'session': 'session',
        'info': 'info',
        'info_exists': 'info_exists',
        'metadata': 'metadata',
        'uid': 'uid',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'created': 'created',
        'tags': 'tags',
        'modified': 'modified',
        'revision': 'revision',
        'permissions': 'permissions',
        'notes': 'notes',
        'analyses': 'analyses',
        'collections': 'collections',
        'join-origin': 'join_origin',
        'files': 'files',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of'
    }

    def __init__(self, id=None, parents=None, label=None, session=None, info=None, info_exists=None, metadata=None, uid=None, timestamp=None, timezone=None, created=None, tags=None, modified=None, revision=1, permissions=None, notes=None, analyses=None, collections=None, join_origin=None, files=None, copy_of=None, original_copy_of=None):  # noqa: E501
        """AcquisitionListOutput - a model defined in Swagger"""
        super(AcquisitionListOutput, self).__init__()

        self._id = None
        self._parents = None
        self._label = None
        self._session = None
        self._info = None
        self._info_exists = None
        self._metadata = None
        self._uid = None
        self._timestamp = None
        self._timezone = None
        self._created = None
        self._tags = None
        self._modified = None
        self._revision = None
        self._permissions = None
        self._notes = None
        self._analyses = None
        self._collections = None
        self._join_origin = None
        self._files = None
        self._copy_of = None
        self._original_copy_of = None
        self.discriminator = None
        self.alt_discriminator = None

        self.id = id
        self.parents = parents
        if label is not None:
            self.label = label
        self.session = session
        self.info = info
        self.info_exists = info_exists
        if metadata is not None:
            self.metadata = metadata
        if uid is not None:
            self.uid = uid
        if timestamp is not None:
            self.timestamp = timestamp
        if timezone is not None:
            self.timezone = timezone
        self.created = created
        if tags is not None:
            self.tags = tags
        self.modified = modified
        if revision is not None:
            self.revision = revision
        self.permissions = permissions
        if notes is not None:
            self.notes = notes
        if analyses is not None:
            self.analyses = analyses
        if collections is not None:
            self.collections = collections
        if join_origin is not None:
            self.join_origin = join_origin
        if files is not None:
            self.files = files
        if copy_of is not None:
            self.copy_of = copy_of
        if original_copy_of is not None:
            self.original_copy_of = original_copy_of

    @property
    def id(self):
        """Gets the id of this AcquisitionListOutput.


        :return: The id of this AcquisitionListOutput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AcquisitionListOutput.


        :param id: The id of this AcquisitionListOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def parents(self):
        """Gets the parents of this AcquisitionListOutput.


        :return: The parents of this AcquisitionListOutput.
        :rtype: AcquisitionParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this AcquisitionListOutput.


        :param parents: The parents of this AcquisitionListOutput.  # noqa: E501
        :type: AcquisitionParents
        """

        self._parents = parents

    @property
    def label(self):
        """Gets the label of this AcquisitionListOutput.


        :return: The label of this AcquisitionListOutput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this AcquisitionListOutput.


        :param label: The label of this AcquisitionListOutput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def session(self):
        """Gets the session of this AcquisitionListOutput.


        :return: The session of this AcquisitionListOutput.
        :rtype: str
        """
        return self._session

    @session.setter
    def session(self, session):
        """Sets the session of this AcquisitionListOutput.


        :param session: The session of this AcquisitionListOutput.  # noqa: E501
        :type: str
        """

        self._session = session

    @property
    def info(self):
        """Gets the info of this AcquisitionListOutput.


        :return: The info of this AcquisitionListOutput.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this AcquisitionListOutput.


        :param info: The info of this AcquisitionListOutput.  # noqa: E501
        :type: object
        """

        self._info = info

    @property
    def info_exists(self):
        """Gets the info_exists of this AcquisitionListOutput.


        :return: The info_exists of this AcquisitionListOutput.
        :rtype: bool
        """
        return self._info_exists

    @info_exists.setter
    def info_exists(self, info_exists):
        """Sets the info_exists of this AcquisitionListOutput.


        :param info_exists: The info_exists of this AcquisitionListOutput.  # noqa: E501
        :type: bool
        """

        self._info_exists = info_exists

    @property
    def metadata(self):
        """Gets the metadata of this AcquisitionListOutput.


        :return: The metadata of this AcquisitionListOutput.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this AcquisitionListOutput.


        :param metadata: The metadata of this AcquisitionListOutput.  # noqa: E501
        :type: object
        """

        self._metadata = metadata

    @property
    def uid(self):
        """Gets the uid of this AcquisitionListOutput.


        :return: The uid of this AcquisitionListOutput.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this AcquisitionListOutput.


        :param uid: The uid of this AcquisitionListOutput.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def timestamp(self):
        """Gets the timestamp of this AcquisitionListOutput.


        :return: The timestamp of this AcquisitionListOutput.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this AcquisitionListOutput.


        :param timestamp: The timestamp of this AcquisitionListOutput.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def timezone(self):
        """Gets the timezone of this AcquisitionListOutput.


        :return: The timezone of this AcquisitionListOutput.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """Sets the timezone of this AcquisitionListOutput.


        :param timezone: The timezone of this AcquisitionListOutput.  # noqa: E501
        :type: str
        """

        self._timezone = timezone

    @property
    def created(self):
        """Gets the created of this AcquisitionListOutput.


        :return: The created of this AcquisitionListOutput.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this AcquisitionListOutput.


        :param created: The created of this AcquisitionListOutput.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def tags(self):
        """Gets the tags of this AcquisitionListOutput.


        :return: The tags of this AcquisitionListOutput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this AcquisitionListOutput.


        :param tags: The tags of this AcquisitionListOutput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def modified(self):
        """Gets the modified of this AcquisitionListOutput.


        :return: The modified of this AcquisitionListOutput.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this AcquisitionListOutput.


        :param modified: The modified of this AcquisitionListOutput.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def revision(self):
        """Gets the revision of this AcquisitionListOutput.


        :return: The revision of this AcquisitionListOutput.
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this AcquisitionListOutput.


        :param revision: The revision of this AcquisitionListOutput.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def permissions(self):
        """Gets the permissions of this AcquisitionListOutput.


        :return: The permissions of this AcquisitionListOutput.
        :rtype: list[RolePermission]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this AcquisitionListOutput.


        :param permissions: The permissions of this AcquisitionListOutput.  # noqa: E501
        :type: list[RolePermission]
        """

        self._permissions = permissions

    @property
    def notes(self):
        """Gets the notes of this AcquisitionListOutput.


        :return: The notes of this AcquisitionListOutput.
        :rtype: list[Note]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this AcquisitionListOutput.


        :param notes: The notes of this AcquisitionListOutput.  # noqa: E501
        :type: list[Note]
        """

        self._notes = notes

    @property
    def analyses(self):
        """Gets the analyses of this AcquisitionListOutput.


        :return: The analyses of this AcquisitionListOutput.
        :rtype: list[union[AnalysisListOutput,AnalysisListOutputInflatedJob]]
        """
        return self._analyses

    @analyses.setter
    def analyses(self, analyses):
        """Sets the analyses of this AcquisitionListOutput.


        :param analyses: The analyses of this AcquisitionListOutput.  # noqa: E501
        :type: list[union[AnalysisListOutput,AnalysisListOutputInflatedJob]]
        """

        self._analyses = analyses

    @property
    def collections(self):
        """Gets the collections of this AcquisitionListOutput.


        :return: The collections of this AcquisitionListOutput.
        :rtype: list[str]
        """
        return self._collections

    @collections.setter
    def collections(self, collections):
        """Sets the collections of this AcquisitionListOutput.


        :param collections: The collections of this AcquisitionListOutput.  # noqa: E501
        :type: list[str]
        """

        self._collections = collections

    @property
    def join_origin(self):
        """Gets the join_origin of this AcquisitionListOutput.


        :return: The join_origin of this AcquisitionListOutput.
        :rtype: JoinOrigins
        """
        return self._join_origin

    @join_origin.setter
    def join_origin(self, join_origin):
        """Sets the join_origin of this AcquisitionListOutput.


        :param join_origin: The join_origin of this AcquisitionListOutput.  # noqa: E501
        :type: JoinOrigins
        """

        self._join_origin = join_origin

    @property
    def files(self):
        """Gets the files of this AcquisitionListOutput.


        :return: The files of this AcquisitionListOutput.
        :rtype: list[FileListOutput]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this AcquisitionListOutput.


        :param files: The files of this AcquisitionListOutput.  # noqa: E501
        :type: list[FileListOutput]
        """

        self._files = files

    @property
    def copy_of(self):
        """Gets the copy_of of this AcquisitionListOutput.


        :return: The copy_of of this AcquisitionListOutput.
        :rtype: str
        """
        return self._copy_of

    @copy_of.setter
    def copy_of(self, copy_of):
        """Sets the copy_of of this AcquisitionListOutput.


        :param copy_of: The copy_of of this AcquisitionListOutput.  # noqa: E501
        :type: str
        """

        self._copy_of = copy_of

    @property
    def original_copy_of(self):
        """Gets the original_copy_of of this AcquisitionListOutput.


        :return: The original_copy_of of this AcquisitionListOutput.
        :rtype: str
        """
        return self._original_copy_of

    @original_copy_of.setter
    def original_copy_of(self, original_copy_of):
        """Sets the original_copy_of of this AcquisitionListOutput.


        :param original_copy_of: The original_copy_of of this AcquisitionListOutput.  # noqa: E501
        :type: str
        """

        self._original_copy_of = original_copy_of


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        # Import relatives
        from flywheel.models.acquisition_output import AcquisitionOutput
        from flywheel.models.acquisition_container_output import AcquisitionContainerOutput
        relatives = (
            AcquisitionOutput,
            AcquisitionContainerOutput,
        )
        if not isinstance(other, relatives + (AcquisitionListOutput,)):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
