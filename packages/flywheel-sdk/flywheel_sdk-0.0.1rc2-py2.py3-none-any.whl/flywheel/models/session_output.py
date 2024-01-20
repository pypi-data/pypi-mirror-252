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

from flywheel.models.file_output import FileOutput  # noqa: F401,E501
from flywheel.models.join_origins import JoinOrigins  # noqa: F401,E501
from flywheel.models.note import Note  # noqa: F401,E501
from flywheel.models.role_permission import RolePermission  # noqa: F401,E501
from flywheel.models.session_parents import SessionParents  # noqa: F401,E501
from flywheel.models.subject_output import SubjectOutput  # noqa: F401,E501

from .mixins import SessionMixin
class SessionOutput(SessionMixin):

    swagger_types = {
        'id': 'str',
        'group': 'str',
        'project': 'str',
        'parents': 'SessionParents',
        'label': 'str',
        'info': 'object',
        'uid': 'str',
        'timestamp': 'datetime',
        'timezone': 'str',
        'tags': 'list[str]',
        'notes': 'list[Note]',
        'permissions': 'list[RolePermission]',
        'subject': 'SubjectOutput',
        'age': 'int',
        'weight': 'float',
        'operator': 'str',
        'files': 'list[FileOutput]',
        'created': 'datetime',
        'modified': 'datetime',
        'revision': 'int',
        'satisfies_template': 'bool',
        'analyses': 'list[union[AnalysisOutput,AnalysisOutputInflatedJob]]',
        'project_has_template': 'bool',
        'join_origin': 'JoinOrigins',
        'copy_of': 'str',
        'original_copy_of': 'str',
        'info_exists': 'bool'
    }

    attribute_map = {
        'id': '_id',
        'group': 'group',
        'project': 'project',
        'parents': 'parents',
        'label': 'label',
        'info': 'info',
        'uid': 'uid',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'tags': 'tags',
        'notes': 'notes',
        'permissions': 'permissions',
        'subject': 'subject',
        'age': 'age',
        'weight': 'weight',
        'operator': 'operator',
        'files': 'files',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'satisfies_template': 'satisfies_template',
        'analyses': 'analyses',
        'project_has_template': 'project_has_template',
        'join_origin': 'join-origin',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of',
        'info_exists': 'info_exists'
    }

    rattribute_map = {
        '_id': 'id',
        'group': 'group',
        'project': 'project',
        'parents': 'parents',
        'label': 'label',
        'info': 'info',
        'uid': 'uid',
        'timestamp': 'timestamp',
        'timezone': 'timezone',
        'tags': 'tags',
        'notes': 'notes',
        'permissions': 'permissions',
        'subject': 'subject',
        'age': 'age',
        'weight': 'weight',
        'operator': 'operator',
        'files': 'files',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'satisfies_template': 'satisfies_template',
        'analyses': 'analyses',
        'project_has_template': 'project_has_template',
        'join-origin': 'join_origin',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of',
        'info_exists': 'info_exists'
    }

    def __init__(self, id=None, group=None, project=None, parents=None, label=None, info=None, uid=None, timestamp=None, timezone=None, tags=None, notes=None, permissions=None, subject=None, age=None, weight=None, operator=None, files=None, created=None, modified=None, revision=None, satisfies_template=None, analyses=None, project_has_template=False, join_origin=None, copy_of=None, original_copy_of=None, info_exists=None):  # noqa: E501
        """SessionOutput - a model defined in Swagger"""
        super(SessionOutput, self).__init__()

        self._id = None
        self._group = None
        self._project = None
        self._parents = None
        self._label = None
        self._info = None
        self._uid = None
        self._timestamp = None
        self._timezone = None
        self._tags = None
        self._notes = None
        self._permissions = None
        self._subject = None
        self._age = None
        self._weight = None
        self._operator = None
        self._files = None
        self._created = None
        self._modified = None
        self._revision = None
        self._satisfies_template = None
        self._analyses = None
        self._project_has_template = None
        self._join_origin = None
        self._copy_of = None
        self._original_copy_of = None
        self._info_exists = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        self.group = group
        self.project = project
        self.parents = parents
        if label is not None:
            self.label = label
        if info is not None:
            self.info = info
        if uid is not None:
            self.uid = uid
        if timestamp is not None:
            self.timestamp = timestamp
        if timezone is not None:
            self.timezone = timezone
        self.tags = tags
        self.notes = notes
        self.permissions = permissions
        self.subject = subject
        if age is not None:
            self.age = age
        if weight is not None:
            self.weight = weight
        if operator is not None:
            self.operator = operator
        self.files = files
        self.created = created
        self.modified = modified
        self.revision = revision
        if satisfies_template is not None:
            self.satisfies_template = satisfies_template
        if analyses is not None:
            self.analyses = analyses
        if project_has_template is not None:
            self.project_has_template = project_has_template
        if join_origin is not None:
            self.join_origin = join_origin
        if copy_of is not None:
            self.copy_of = copy_of
        if original_copy_of is not None:
            self.original_copy_of = original_copy_of
        if info_exists is not None:
            self.info_exists = info_exists

    @property
    def id(self):
        """Gets the id of this SessionOutput.


        :return: The id of this SessionOutput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SessionOutput.


        :param id: The id of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def group(self):
        """Gets the group of this SessionOutput.


        :return: The group of this SessionOutput.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this SessionOutput.


        :param group: The group of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._group = group

    @property
    def project(self):
        """Gets the project of this SessionOutput.


        :return: The project of this SessionOutput.
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this SessionOutput.


        :param project: The project of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._project = project

    @property
    def parents(self):
        """Gets the parents of this SessionOutput.


        :return: The parents of this SessionOutput.
        :rtype: SessionParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this SessionOutput.


        :param parents: The parents of this SessionOutput.  # noqa: E501
        :type: SessionParents
        """

        self._parents = parents

    @property
    def label(self):
        """Gets the label of this SessionOutput.


        :return: The label of this SessionOutput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this SessionOutput.


        :param label: The label of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def info(self):
        """Gets the info of this SessionOutput.


        :return: The info of this SessionOutput.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this SessionOutput.


        :param info: The info of this SessionOutput.  # noqa: E501
        :type: object
        """

        self._info = info

    @property
    def uid(self):
        """Gets the uid of this SessionOutput.


        :return: The uid of this SessionOutput.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this SessionOutput.


        :param uid: The uid of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def timestamp(self):
        """Gets the timestamp of this SessionOutput.


        :return: The timestamp of this SessionOutput.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this SessionOutput.


        :param timestamp: The timestamp of this SessionOutput.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def timezone(self):
        """Gets the timezone of this SessionOutput.


        :return: The timezone of this SessionOutput.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """Sets the timezone of this SessionOutput.


        :param timezone: The timezone of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._timezone = timezone

    @property
    def tags(self):
        """Gets the tags of this SessionOutput.


        :return: The tags of this SessionOutput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this SessionOutput.


        :param tags: The tags of this SessionOutput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def notes(self):
        """Gets the notes of this SessionOutput.


        :return: The notes of this SessionOutput.
        :rtype: list[Note]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this SessionOutput.


        :param notes: The notes of this SessionOutput.  # noqa: E501
        :type: list[Note]
        """

        self._notes = notes

    @property
    def permissions(self):
        """Gets the permissions of this SessionOutput.


        :return: The permissions of this SessionOutput.
        :rtype: list[RolePermission]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this SessionOutput.


        :param permissions: The permissions of this SessionOutput.  # noqa: E501
        :type: list[RolePermission]
        """

        self._permissions = permissions

    @property
    def subject(self):
        """Gets the subject of this SessionOutput.


        :return: The subject of this SessionOutput.
        :rtype: SubjectOutput
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this SessionOutput.


        :param subject: The subject of this SessionOutput.  # noqa: E501
        :type: SubjectOutput
        """

        self._subject = subject

    @property
    def age(self):
        """Gets the age of this SessionOutput.


        :return: The age of this SessionOutput.
        :rtype: int
        """
        return self._age

    @age.setter
    def age(self, age):
        """Sets the age of this SessionOutput.


        :param age: The age of this SessionOutput.  # noqa: E501
        :type: int
        """

        self._age = age

    @property
    def weight(self):
        """Gets the weight of this SessionOutput.


        :return: The weight of this SessionOutput.
        :rtype: float
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this SessionOutput.


        :param weight: The weight of this SessionOutput.  # noqa: E501
        :type: float
        """

        self._weight = weight

    @property
    def operator(self):
        """Gets the operator of this SessionOutput.


        :return: The operator of this SessionOutput.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """Sets the operator of this SessionOutput.


        :param operator: The operator of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._operator = operator

    @property
    def files(self):
        """Gets the files of this SessionOutput.


        :return: The files of this SessionOutput.
        :rtype: list[FileOutput]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this SessionOutput.


        :param files: The files of this SessionOutput.  # noqa: E501
        :type: list[FileOutput]
        """

        self._files = files

    @property
    def created(self):
        """Gets the created of this SessionOutput.


        :return: The created of this SessionOutput.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this SessionOutput.


        :param created: The created of this SessionOutput.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this SessionOutput.


        :return: The modified of this SessionOutput.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this SessionOutput.


        :param modified: The modified of this SessionOutput.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def revision(self):
        """Gets the revision of this SessionOutput.


        :return: The revision of this SessionOutput.
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this SessionOutput.


        :param revision: The revision of this SessionOutput.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def satisfies_template(self):
        """Gets the satisfies_template of this SessionOutput.


        :return: The satisfies_template of this SessionOutput.
        :rtype: bool
        """
        return self._satisfies_template

    @satisfies_template.setter
    def satisfies_template(self, satisfies_template):
        """Sets the satisfies_template of this SessionOutput.


        :param satisfies_template: The satisfies_template of this SessionOutput.  # noqa: E501
        :type: bool
        """

        self._satisfies_template = satisfies_template

    @property
    def analyses(self):
        """Gets the analyses of this SessionOutput.


        :return: The analyses of this SessionOutput.
        :rtype: list[union[AnalysisOutput,AnalysisOutputInflatedJob]]
        """
        return self._analyses

    @analyses.setter
    def analyses(self, analyses):
        """Sets the analyses of this SessionOutput.


        :param analyses: The analyses of this SessionOutput.  # noqa: E501
        :type: list[union[AnalysisOutput,AnalysisOutputInflatedJob]]
        """

        self._analyses = analyses

    @property
    def project_has_template(self):
        """Gets the project_has_template of this SessionOutput.


        :return: The project_has_template of this SessionOutput.
        :rtype: bool
        """
        return self._project_has_template

    @project_has_template.setter
    def project_has_template(self, project_has_template):
        """Sets the project_has_template of this SessionOutput.


        :param project_has_template: The project_has_template of this SessionOutput.  # noqa: E501
        :type: bool
        """

        self._project_has_template = project_has_template

    @property
    def join_origin(self):
        """Gets the join_origin of this SessionOutput.


        :return: The join_origin of this SessionOutput.
        :rtype: JoinOrigins
        """
        return self._join_origin

    @join_origin.setter
    def join_origin(self, join_origin):
        """Sets the join_origin of this SessionOutput.


        :param join_origin: The join_origin of this SessionOutput.  # noqa: E501
        :type: JoinOrigins
        """

        self._join_origin = join_origin

    @property
    def copy_of(self):
        """Gets the copy_of of this SessionOutput.


        :return: The copy_of of this SessionOutput.
        :rtype: str
        """
        return self._copy_of

    @copy_of.setter
    def copy_of(self, copy_of):
        """Sets the copy_of of this SessionOutput.


        :param copy_of: The copy_of of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._copy_of = copy_of

    @property
    def original_copy_of(self):
        """Gets the original_copy_of of this SessionOutput.


        :return: The original_copy_of of this SessionOutput.
        :rtype: str
        """
        return self._original_copy_of

    @original_copy_of.setter
    def original_copy_of(self, original_copy_of):
        """Sets the original_copy_of of this SessionOutput.


        :param original_copy_of: The original_copy_of of this SessionOutput.  # noqa: E501
        :type: str
        """

        self._original_copy_of = original_copy_of

    @property
    def info_exists(self):
        """Gets the info_exists of this SessionOutput.


        :return: The info_exists of this SessionOutput.
        :rtype: bool
        """
        return self._info_exists

    @info_exists.setter
    def info_exists(self, info_exists):
        """Sets the info_exists of this SessionOutput.


        :param info_exists: The info_exists of this SessionOutput.  # noqa: E501
        :type: bool
        """

        self._info_exists = info_exists


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
        from flywheel.models.session import Session
        from flywheel.models.session_list_output import SessionListOutput
        relatives = (
            Session,
            SessionListOutput,
        )
        if not isinstance(other, relatives + (SessionOutput,)):
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
