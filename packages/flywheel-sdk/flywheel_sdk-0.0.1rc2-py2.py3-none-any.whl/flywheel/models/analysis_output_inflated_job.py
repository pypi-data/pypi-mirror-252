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

from flywheel.models.analysis_parents import AnalysisParents  # noqa: F401,E501
from flywheel.models.container_reference import ContainerReference  # noqa: F401,E501
from flywheel.models.file_output import FileOutput  # noqa: F401,E501
from flywheel.models.gear_info import GearInfo  # noqa: F401,E501
from flywheel.models.job_output import JobOutput  # noqa: F401,E501
from flywheel.models.join_origins import JoinOrigins  # noqa: F401,E501
from flywheel.models.note import Note  # noqa: F401,E501

class AnalysisOutputInflatedJob(object):

    swagger_types = {
        'id': 'str',
        'label': 'str',
        'parent': 'ContainerReference',
        'parents': 'AnalysisParents',
        'created': 'datetime',
        'modified': 'datetime',
        'revision': 'int',
        'inputs': 'list[FileOutput]',
        'description': 'str',
        'info': 'object',
        'files': 'list[FileOutput]',
        'notes': 'list[Note]',
        'tags': 'list[str]',
        'job_id': 'str',
        'job': 'JobOutput',
        'gear_info': 'GearInfo',
        'compute_provider_id': 'str',
        'join_origin': 'JoinOrigins',
        'copy_of': 'str',
        'original_copy_of': 'str'
    }

    attribute_map = {
        'id': '_id',
        'label': 'label',
        'parent': 'parent',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'inputs': 'inputs',
        'description': 'description',
        'info': 'info',
        'files': 'files',
        'notes': 'notes',
        'tags': 'tags',
        'job_id': 'job_id',
        'job': 'job',
        'gear_info': 'gear_info',
        'compute_provider_id': 'compute_provider_id',
        'join_origin': 'join-origin',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of'
    }

    rattribute_map = {
        '_id': 'id',
        'label': 'label',
        'parent': 'parent',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'inputs': 'inputs',
        'description': 'description',
        'info': 'info',
        'files': 'files',
        'notes': 'notes',
        'tags': 'tags',
        'job_id': 'job_id',
        'job': 'job',
        'gear_info': 'gear_info',
        'compute_provider_id': 'compute_provider_id',
        'join-origin': 'join_origin',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of'
    }

    def __init__(self, id=None, label=None, parent=None, parents=None, created=None, modified=None, revision=None, inputs=None, description=None, info=None, files=None, notes=None, tags=None, job_id=None, job=None, gear_info=None, compute_provider_id=None, join_origin=None, copy_of=None, original_copy_of=None):  # noqa: E501
        """AnalysisOutputInflatedJob - a model defined in Swagger"""
        super(AnalysisOutputInflatedJob, self).__init__()

        self._id = None
        self._label = None
        self._parent = None
        self._parents = None
        self._created = None
        self._modified = None
        self._revision = None
        self._inputs = None
        self._description = None
        self._info = None
        self._files = None
        self._notes = None
        self._tags = None
        self._job_id = None
        self._job = None
        self._gear_info = None
        self._compute_provider_id = None
        self._join_origin = None
        self._copy_of = None
        self._original_copy_of = None
        self.discriminator = None
        self.alt_discriminator = None

        self.id = id
        self.label = label
        self.parent = parent
        self.parents = parents
        self.created = created
        self.modified = modified
        self.revision = revision
        self.inputs = inputs
        self.description = description
        if info is not None:
            self.info = info
        self.files = files
        self.notes = notes
        self.tags = tags
        if job_id is not None:
            self.job_id = job_id
        if job is not None:
            self.job = job
        if gear_info is not None:
            self.gear_info = gear_info
        if compute_provider_id is not None:
            self.compute_provider_id = compute_provider_id
        if join_origin is not None:
            self.join_origin = join_origin
        if copy_of is not None:
            self.copy_of = copy_of
        if original_copy_of is not None:
            self.original_copy_of = original_copy_of

    @property
    def id(self):
        """Gets the id of this AnalysisOutputInflatedJob.


        :return: The id of this AnalysisOutputInflatedJob.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AnalysisOutputInflatedJob.


        :param id: The id of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this AnalysisOutputInflatedJob.


        :return: The label of this AnalysisOutputInflatedJob.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this AnalysisOutputInflatedJob.


        :param label: The label of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def parent(self):
        """Gets the parent of this AnalysisOutputInflatedJob.


        :return: The parent of this AnalysisOutputInflatedJob.
        :rtype: ContainerReference
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Sets the parent of this AnalysisOutputInflatedJob.


        :param parent: The parent of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: ContainerReference
        """

        self._parent = parent

    @property
    def parents(self):
        """Gets the parents of this AnalysisOutputInflatedJob.


        :return: The parents of this AnalysisOutputInflatedJob.
        :rtype: AnalysisParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this AnalysisOutputInflatedJob.


        :param parents: The parents of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: AnalysisParents
        """

        self._parents = parents

    @property
    def created(self):
        """Gets the created of this AnalysisOutputInflatedJob.


        :return: The created of this AnalysisOutputInflatedJob.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this AnalysisOutputInflatedJob.


        :param created: The created of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this AnalysisOutputInflatedJob.


        :return: The modified of this AnalysisOutputInflatedJob.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this AnalysisOutputInflatedJob.


        :param modified: The modified of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def revision(self):
        """Gets the revision of this AnalysisOutputInflatedJob.


        :return: The revision of this AnalysisOutputInflatedJob.
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this AnalysisOutputInflatedJob.


        :param revision: The revision of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def inputs(self):
        """Gets the inputs of this AnalysisOutputInflatedJob.


        :return: The inputs of this AnalysisOutputInflatedJob.
        :rtype: list[FileOutput]
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this AnalysisOutputInflatedJob.


        :param inputs: The inputs of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: list[FileOutput]
        """

        self._inputs = inputs

    @property
    def description(self):
        """Gets the description of this AnalysisOutputInflatedJob.


        :return: The description of this AnalysisOutputInflatedJob.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AnalysisOutputInflatedJob.


        :param description: The description of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def info(self):
        """Gets the info of this AnalysisOutputInflatedJob.


        :return: The info of this AnalysisOutputInflatedJob.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this AnalysisOutputInflatedJob.


        :param info: The info of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: object
        """

        self._info = info

    @property
    def files(self):
        """Gets the files of this AnalysisOutputInflatedJob.


        :return: The files of this AnalysisOutputInflatedJob.
        :rtype: list[FileOutput]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this AnalysisOutputInflatedJob.


        :param files: The files of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: list[FileOutput]
        """

        self._files = files

    @property
    def notes(self):
        """Gets the notes of this AnalysisOutputInflatedJob.


        :return: The notes of this AnalysisOutputInflatedJob.
        :rtype: list[Note]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this AnalysisOutputInflatedJob.


        :param notes: The notes of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: list[Note]
        """

        self._notes = notes

    @property
    def tags(self):
        """Gets the tags of this AnalysisOutputInflatedJob.


        :return: The tags of this AnalysisOutputInflatedJob.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this AnalysisOutputInflatedJob.


        :param tags: The tags of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def job_id(self):
        """Gets the job_id of this AnalysisOutputInflatedJob.


        :return: The job_id of this AnalysisOutputInflatedJob.
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this AnalysisOutputInflatedJob.


        :param job_id: The job_id of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def job(self):
        """Gets the job of this AnalysisOutputInflatedJob.


        :return: The job of this AnalysisOutputInflatedJob.
        :rtype: JobOutput
        """
        return self._job

    @job.setter
    def job(self, job):
        """Sets the job of this AnalysisOutputInflatedJob.


        :param job: The job of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: JobOutput
        """

        self._job = job

    @property
    def gear_info(self):
        """Gets the gear_info of this AnalysisOutputInflatedJob.


        :return: The gear_info of this AnalysisOutputInflatedJob.
        :rtype: GearInfo
        """
        return self._gear_info

    @gear_info.setter
    def gear_info(self, gear_info):
        """Sets the gear_info of this AnalysisOutputInflatedJob.


        :param gear_info: The gear_info of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: GearInfo
        """

        self._gear_info = gear_info

    @property
    def compute_provider_id(self):
        """Gets the compute_provider_id of this AnalysisOutputInflatedJob.


        :return: The compute_provider_id of this AnalysisOutputInflatedJob.
        :rtype: str
        """
        return self._compute_provider_id

    @compute_provider_id.setter
    def compute_provider_id(self, compute_provider_id):
        """Sets the compute_provider_id of this AnalysisOutputInflatedJob.


        :param compute_provider_id: The compute_provider_id of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: str
        """

        self._compute_provider_id = compute_provider_id

    @property
    def join_origin(self):
        """Gets the join_origin of this AnalysisOutputInflatedJob.


        :return: The join_origin of this AnalysisOutputInflatedJob.
        :rtype: JoinOrigins
        """
        return self._join_origin

    @join_origin.setter
    def join_origin(self, join_origin):
        """Sets the join_origin of this AnalysisOutputInflatedJob.


        :param join_origin: The join_origin of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: JoinOrigins
        """

        self._join_origin = join_origin

    @property
    def copy_of(self):
        """Gets the copy_of of this AnalysisOutputInflatedJob.


        :return: The copy_of of this AnalysisOutputInflatedJob.
        :rtype: str
        """
        return self._copy_of

    @copy_of.setter
    def copy_of(self, copy_of):
        """Sets the copy_of of this AnalysisOutputInflatedJob.


        :param copy_of: The copy_of of this AnalysisOutputInflatedJob.  # noqa: E501
        :type: str
        """

        self._copy_of = copy_of

    @property
    def original_copy_of(self):
        """Gets the original_copy_of of this AnalysisOutputInflatedJob.


        :return: The original_copy_of of this AnalysisOutputInflatedJob.
        :rtype: str
        """
        return self._original_copy_of

    @original_copy_of.setter
    def original_copy_of(self, original_copy_of):
        """Sets the original_copy_of of this AnalysisOutputInflatedJob.


        :param original_copy_of: The original_copy_of of this AnalysisOutputInflatedJob.  # noqa: E501
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
        if not isinstance(other, AnalysisOutputInflatedJob):
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
