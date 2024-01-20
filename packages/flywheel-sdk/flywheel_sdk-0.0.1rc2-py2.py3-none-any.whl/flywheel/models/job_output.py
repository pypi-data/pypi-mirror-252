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

from flywheel.models.container_reference import ContainerReference  # noqa: F401,E501
from flywheel.models.deleted_file import DeletedFile  # noqa: F401,E501
from flywheel.models.file_output import FileOutput  # noqa: F401,E501
from flywheel.models.file_reference import FileReference  # noqa: F401,E501
from flywheel.models.gear_info import GearInfo  # noqa: F401,E501
from flywheel.models.job_detail_parent_info import JobDetailParentInfo  # noqa: F401,E501
from flywheel.models.job_output_config import JobOutputConfig  # noqa: F401,E501
from flywheel.models.job_parents import JobParents  # noqa: F401,E501
from flywheel.models.job_profile import JobProfile  # noqa: F401,E501
from flywheel.models.job_request import JobRequest  # noqa: F401,E501
from flywheel.models.job_state import JobState  # noqa: F401,E501
from flywheel.models.origin import Origin  # noqa: F401,E501

from .mixins import JobMixin
class JobOutput(JobMixin):

    swagger_types = {
        'gear_id': 'str',
        'gear_info': 'GearInfo',
        'rule_id': 'str',
        'role_id': 'str',
        'inputs': 'dict(str, FileReference)',
        'destination': 'ContainerReference',
        'tags': 'list[str]',
        'priority': 'JobPriority',
        'attempt': 'int',
        'previous_job_id': 'str',
        'created': 'datetime',
        'modified': 'datetime',
        'retried': 'datetime',
        'state': 'JobState',
        'request': 'JobRequest',
        'id': 'str',
        'config': 'JobOutputConfig',
        'origin': 'Origin',
        'saved_files': 'list[str]',
        'outputs': 'list[FileOutput]',
        'deleted_outputs': 'list[DeletedFile]',
        'produced_metadata': 'object',
        'batch': 'str',
        'failed_output_accepted': 'bool',
        'profile': 'JobProfile',
        'failure_reason': 'str',
        'related_container_ids': 'list[str]',
        'label': 'str',
        'compute_provider_id': 'str',
        'parents': 'JobParents',
        'transitions': 'Transitions',
        'parent_info': 'JobDetailParentInfo'
    }

    attribute_map = {
        'gear_id': 'gear_id',
        'gear_info': 'gear_info',
        'rule_id': 'rule_id',
        'role_id': 'role_id',
        'inputs': 'inputs',
        'destination': 'destination',
        'tags': 'tags',
        'priority': 'priority',
        'attempt': 'attempt',
        'previous_job_id': 'previous_job_id',
        'created': 'created',
        'modified': 'modified',
        'retried': 'retried',
        'state': 'state',
        'request': 'request',
        'id': 'id',
        'config': 'config',
        'origin': 'origin',
        'saved_files': 'saved_files',
        'outputs': 'outputs',
        'deleted_outputs': 'deleted_outputs',
        'produced_metadata': 'produced_metadata',
        'batch': 'batch',
        'failed_output_accepted': 'failed_output_accepted',
        'profile': 'profile',
        'failure_reason': 'failure_reason',
        'related_container_ids': 'related_container_ids',
        'label': 'label',
        'compute_provider_id': 'compute_provider_id',
        'parents': 'parents',
        'transitions': 'transitions',
        'parent_info': 'parent_info'
    }

    rattribute_map = {
        'gear_id': 'gear_id',
        'gear_info': 'gear_info',
        'rule_id': 'rule_id',
        'role_id': 'role_id',
        'inputs': 'inputs',
        'destination': 'destination',
        'tags': 'tags',
        'priority': 'priority',
        'attempt': 'attempt',
        'previous_job_id': 'previous_job_id',
        'created': 'created',
        'modified': 'modified',
        'retried': 'retried',
        'state': 'state',
        'request': 'request',
        'id': 'id',
        'config': 'config',
        'origin': 'origin',
        'saved_files': 'saved_files',
        'outputs': 'outputs',
        'deleted_outputs': 'deleted_outputs',
        'produced_metadata': 'produced_metadata',
        'batch': 'batch',
        'failed_output_accepted': 'failed_output_accepted',
        'profile': 'profile',
        'failure_reason': 'failure_reason',
        'related_container_ids': 'related_container_ids',
        'label': 'label',
        'compute_provider_id': 'compute_provider_id',
        'parents': 'parents',
        'transitions': 'transitions',
        'parent_info': 'parent_info'
    }

    def __init__(self, gear_id=None, gear_info=None, rule_id=None, role_id=None, inputs=None, destination=None, tags=None, priority=None, attempt=None, previous_job_id=None, created=None, modified=None, retried=None, state=None, request=None, id=None, config=None, origin=None, saved_files=None, outputs=None, deleted_outputs=None, produced_metadata=None, batch=None, failed_output_accepted=None, profile=None, failure_reason=None, related_container_ids=None, label=None, compute_provider_id=None, parents=None, transitions=None, parent_info=None):  # noqa: E501
        """JobOutput - a model defined in Swagger"""
        super(JobOutput, self).__init__()

        self._gear_id = None
        self._gear_info = None
        self._rule_id = None
        self._role_id = None
        self._inputs = None
        self._destination = None
        self._tags = None
        self._priority = None
        self._attempt = None
        self._previous_job_id = None
        self._created = None
        self._modified = None
        self._retried = None
        self._state = None
        self._request = None
        self._id = None
        self._config = None
        self._origin = None
        self._saved_files = None
        self._outputs = None
        self._deleted_outputs = None
        self._produced_metadata = None
        self._batch = None
        self._failed_output_accepted = None
        self._profile = None
        self._failure_reason = None
        self._related_container_ids = None
        self._label = None
        self._compute_provider_id = None
        self._parents = None
        self._transitions = None
        self._parent_info = None
        self.discriminator = None
        self.alt_discriminator = None

        self.gear_id = gear_id
        if gear_info is not None:
            self.gear_info = gear_info
        if rule_id is not None:
            self.rule_id = rule_id
        if role_id is not None:
            self.role_id = role_id
        self.inputs = inputs
        self.destination = destination
        self.tags = tags
        if priority is not None:
            self.priority = priority
        self.attempt = attempt
        if previous_job_id is not None:
            self.previous_job_id = previous_job_id
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if retried is not None:
            self.retried = retried
        self.state = state
        if request is not None:
            self.request = request
        self.id = id
        self.config = config
        self.origin = origin
        if saved_files is not None:
            self.saved_files = saved_files
        self.outputs = outputs
        self.deleted_outputs = deleted_outputs
        if produced_metadata is not None:
            self.produced_metadata = produced_metadata
        if batch is not None:
            self.batch = batch
        if failed_output_accepted is not None:
            self.failed_output_accepted = failed_output_accepted
        if profile is not None:
            self.profile = profile
        if failure_reason is not None:
            self.failure_reason = failure_reason
        self.related_container_ids = related_container_ids
        if label is not None:
            self.label = label
        if compute_provider_id is not None:
            self.compute_provider_id = compute_provider_id
        self.parents = parents
        if transitions is not None:
            self.transitions = transitions
        if parent_info is not None:
            self.parent_info = parent_info

    @property
    def gear_id(self):
        """Gets the gear_id of this JobOutput.


        :return: The gear_id of this JobOutput.
        :rtype: str
        """
        return self._gear_id

    @gear_id.setter
    def gear_id(self, gear_id):
        """Sets the gear_id of this JobOutput.


        :param gear_id: The gear_id of this JobOutput.  # noqa: E501
        :type: str
        """

        self._gear_id = gear_id

    @property
    def gear_info(self):
        """Gets the gear_info of this JobOutput.


        :return: The gear_info of this JobOutput.
        :rtype: GearInfo
        """
        return self._gear_info

    @gear_info.setter
    def gear_info(self, gear_info):
        """Sets the gear_info of this JobOutput.


        :param gear_info: The gear_info of this JobOutput.  # noqa: E501
        :type: GearInfo
        """

        self._gear_info = gear_info

    @property
    def rule_id(self):
        """Gets the rule_id of this JobOutput.


        :return: The rule_id of this JobOutput.
        :rtype: str
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id):
        """Sets the rule_id of this JobOutput.


        :param rule_id: The rule_id of this JobOutput.  # noqa: E501
        :type: str
        """

        self._rule_id = rule_id

    @property
    def role_id(self):
        """Gets the role_id of this JobOutput.


        :return: The role_id of this JobOutput.
        :rtype: str
        """
        return self._role_id

    @role_id.setter
    def role_id(self, role_id):
        """Sets the role_id of this JobOutput.


        :param role_id: The role_id of this JobOutput.  # noqa: E501
        :type: str
        """

        self._role_id = role_id

    @property
    def inputs(self):
        """Gets the inputs of this JobOutput.


        :return: The inputs of this JobOutput.
        :rtype: dict(str, FileReference)
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this JobOutput.


        :param inputs: The inputs of this JobOutput.  # noqa: E501
        :type: dict(str, FileReference)
        """

        self._inputs = inputs

    @property
    def destination(self):
        """Gets the destination of this JobOutput.


        :return: The destination of this JobOutput.
        :rtype: ContainerReference
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this JobOutput.


        :param destination: The destination of this JobOutput.  # noqa: E501
        :type: ContainerReference
        """

        self._destination = destination

    @property
    def tags(self):
        """Gets the tags of this JobOutput.


        :return: The tags of this JobOutput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this JobOutput.


        :param tags: The tags of this JobOutput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def priority(self):
        """Gets the priority of this JobOutput.


        :return: The priority of this JobOutput.
        :rtype: JobPriority
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this JobOutput.


        :param priority: The priority of this JobOutput.  # noqa: E501
        :type: JobPriority
        """

        self._priority = priority

    @property
    def attempt(self):
        """Gets the attempt of this JobOutput.


        :return: The attempt of this JobOutput.
        :rtype: int
        """
        return self._attempt

    @attempt.setter
    def attempt(self, attempt):
        """Sets the attempt of this JobOutput.


        :param attempt: The attempt of this JobOutput.  # noqa: E501
        :type: int
        """

        self._attempt = attempt

    @property
    def previous_job_id(self):
        """Gets the previous_job_id of this JobOutput.


        :return: The previous_job_id of this JobOutput.
        :rtype: str
        """
        return self._previous_job_id

    @previous_job_id.setter
    def previous_job_id(self, previous_job_id):
        """Sets the previous_job_id of this JobOutput.


        :param previous_job_id: The previous_job_id of this JobOutput.  # noqa: E501
        :type: str
        """

        self._previous_job_id = previous_job_id

    @property
    def created(self):
        """Gets the created of this JobOutput.


        :return: The created of this JobOutput.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this JobOutput.


        :param created: The created of this JobOutput.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this JobOutput.


        :return: The modified of this JobOutput.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this JobOutput.


        :param modified: The modified of this JobOutput.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def retried(self):
        """Gets the retried of this JobOutput.


        :return: The retried of this JobOutput.
        :rtype: datetime
        """
        return self._retried

    @retried.setter
    def retried(self, retried):
        """Sets the retried of this JobOutput.


        :param retried: The retried of this JobOutput.  # noqa: E501
        :type: datetime
        """

        self._retried = retried

    @property
    def state(self):
        """Gets the state of this JobOutput.


        :return: The state of this JobOutput.
        :rtype: JobState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this JobOutput.


        :param state: The state of this JobOutput.  # noqa: E501
        :type: JobState
        """

        self._state = state

    @property
    def request(self):
        """Gets the request of this JobOutput.


        :return: The request of this JobOutput.
        :rtype: JobRequest
        """
        return self._request

    @request.setter
    def request(self, request):
        """Sets the request of this JobOutput.


        :param request: The request of this JobOutput.  # noqa: E501
        :type: JobRequest
        """

        self._request = request

    @property
    def id(self):
        """Gets the id of this JobOutput.


        :return: The id of this JobOutput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this JobOutput.


        :param id: The id of this JobOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def config(self):
        """Gets the config of this JobOutput.


        :return: The config of this JobOutput.
        :rtype: JobOutputConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this JobOutput.


        :param config: The config of this JobOutput.  # noqa: E501
        :type: JobOutputConfig
        """

        self._config = config

    @property
    def origin(self):
        """Gets the origin of this JobOutput.


        :return: The origin of this JobOutput.
        :rtype: Origin
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this JobOutput.


        :param origin: The origin of this JobOutput.  # noqa: E501
        :type: Origin
        """

        self._origin = origin

    @property
    def saved_files(self):
        """Gets the saved_files of this JobOutput.


        :return: The saved_files of this JobOutput.
        :rtype: list[str]
        """
        return self._saved_files

    @saved_files.setter
    def saved_files(self, saved_files):
        """Sets the saved_files of this JobOutput.


        :param saved_files: The saved_files of this JobOutput.  # noqa: E501
        :type: list[str]
        """

        self._saved_files = saved_files

    @property
    def outputs(self):
        """Gets the outputs of this JobOutput.


        :return: The outputs of this JobOutput.
        :rtype: list[FileOutput]
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this JobOutput.


        :param outputs: The outputs of this JobOutput.  # noqa: E501
        :type: list[FileOutput]
        """

        self._outputs = outputs

    @property
    def deleted_outputs(self):
        """Gets the deleted_outputs of this JobOutput.


        :return: The deleted_outputs of this JobOutput.
        :rtype: list[DeletedFile]
        """
        return self._deleted_outputs

    @deleted_outputs.setter
    def deleted_outputs(self, deleted_outputs):
        """Sets the deleted_outputs of this JobOutput.


        :param deleted_outputs: The deleted_outputs of this JobOutput.  # noqa: E501
        :type: list[DeletedFile]
        """

        self._deleted_outputs = deleted_outputs

    @property
    def produced_metadata(self):
        """Gets the produced_metadata of this JobOutput.


        :return: The produced_metadata of this JobOutput.
        :rtype: object
        """
        return self._produced_metadata

    @produced_metadata.setter
    def produced_metadata(self, produced_metadata):
        """Sets the produced_metadata of this JobOutput.


        :param produced_metadata: The produced_metadata of this JobOutput.  # noqa: E501
        :type: object
        """

        self._produced_metadata = produced_metadata

    @property
    def batch(self):
        """Gets the batch of this JobOutput.


        :return: The batch of this JobOutput.
        :rtype: str
        """
        return self._batch

    @batch.setter
    def batch(self, batch):
        """Sets the batch of this JobOutput.


        :param batch: The batch of this JobOutput.  # noqa: E501
        :type: str
        """

        self._batch = batch

    @property
    def failed_output_accepted(self):
        """Gets the failed_output_accepted of this JobOutput.


        :return: The failed_output_accepted of this JobOutput.
        :rtype: bool
        """
        return self._failed_output_accepted

    @failed_output_accepted.setter
    def failed_output_accepted(self, failed_output_accepted):
        """Sets the failed_output_accepted of this JobOutput.


        :param failed_output_accepted: The failed_output_accepted of this JobOutput.  # noqa: E501
        :type: bool
        """

        self._failed_output_accepted = failed_output_accepted

    @property
    def profile(self):
        """Gets the profile of this JobOutput.


        :return: The profile of this JobOutput.
        :rtype: JobProfile
        """
        return self._profile

    @profile.setter
    def profile(self, profile):
        """Sets the profile of this JobOutput.


        :param profile: The profile of this JobOutput.  # noqa: E501
        :type: JobProfile
        """

        self._profile = profile

    @property
    def failure_reason(self):
        """Gets the failure_reason of this JobOutput.


        :return: The failure_reason of this JobOutput.
        :rtype: str
        """
        return self._failure_reason

    @failure_reason.setter
    def failure_reason(self, failure_reason):
        """Sets the failure_reason of this JobOutput.


        :param failure_reason: The failure_reason of this JobOutput.  # noqa: E501
        :type: str
        """

        self._failure_reason = failure_reason

    @property
    def related_container_ids(self):
        """Gets the related_container_ids of this JobOutput.


        :return: The related_container_ids of this JobOutput.
        :rtype: list[str]
        """
        return self._related_container_ids

    @related_container_ids.setter
    def related_container_ids(self, related_container_ids):
        """Sets the related_container_ids of this JobOutput.


        :param related_container_ids: The related_container_ids of this JobOutput.  # noqa: E501
        :type: list[str]
        """

        self._related_container_ids = related_container_ids

    @property
    def label(self):
        """Gets the label of this JobOutput.


        :return: The label of this JobOutput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this JobOutput.


        :param label: The label of this JobOutput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def compute_provider_id(self):
        """Gets the compute_provider_id of this JobOutput.


        :return: The compute_provider_id of this JobOutput.
        :rtype: str
        """
        return self._compute_provider_id

    @compute_provider_id.setter
    def compute_provider_id(self, compute_provider_id):
        """Sets the compute_provider_id of this JobOutput.


        :param compute_provider_id: The compute_provider_id of this JobOutput.  # noqa: E501
        :type: str
        """

        self._compute_provider_id = compute_provider_id

    @property
    def parents(self):
        """Gets the parents of this JobOutput.


        :return: The parents of this JobOutput.
        :rtype: JobParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this JobOutput.


        :param parents: The parents of this JobOutput.  # noqa: E501
        :type: JobParents
        """

        self._parents = parents

    @property
    def transitions(self):
        """Gets the transitions of this JobOutput.


        :return: The transitions of this JobOutput.
        :rtype: Transitions
        """
        return self._transitions

    @transitions.setter
    def transitions(self, transitions):
        """Sets the transitions of this JobOutput.


        :param transitions: The transitions of this JobOutput.  # noqa: E501
        :type: Transitions
        """

        self._transitions = transitions

    @property
    def parent_info(self):
        """Gets the parent_info of this JobOutput.


        :return: The parent_info of this JobOutput.
        :rtype: JobDetailParentInfo
        """
        return self._parent_info

    @parent_info.setter
    def parent_info(self, parent_info):
        """Sets the parent_info of this JobOutput.


        :param parent_info: The parent_info of this JobOutput.  # noqa: E501
        :type: JobDetailParentInfo
        """

        self._parent_info = parent_info


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
        if not isinstance(other, JobOutput):
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
