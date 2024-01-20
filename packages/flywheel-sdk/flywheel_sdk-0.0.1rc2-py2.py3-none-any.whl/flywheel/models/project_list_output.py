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

from flywheel.models.edition import Edition  # noqa: F401,E501
from flywheel.models.file_list_output import FileListOutput  # noqa: F401,E501
from flywheel.models.join_origins import JoinOrigins  # noqa: F401,E501
from flywheel.models.ldap_sync_status import LdapSyncStatus  # noqa: F401,E501
from flywheel.models.locked import Locked  # noqa: F401,E501
from flywheel.models.note import Note  # noqa: F401,E501
from flywheel.models.project_parents import ProjectParents  # noqa: F401,E501
from flywheel.models.project_settings_output import ProjectSettingsOutput  # noqa: F401,E501
from flywheel.models.project_stats import ProjectStats  # noqa: F401,E501
from flywheel.models.project_template import ProjectTemplate  # noqa: F401,E501
from flywheel.models.providers import Providers  # noqa: F401,E501
from flywheel.models.role_permission import RolePermission  # noqa: F401,E501

from .mixins import ProjectMixin
class ProjectListOutput(ProjectMixin):

    swagger_types = {
        'id': 'str',
        'label': 'str',
        'description': 'str',
        'group': 'str',
        'parents': 'ProjectParents',
        'editions': 'Edition',
        'providers': 'Providers',
        'ldap_sync': 'LdapSyncStatus',
        'permissions': 'list[RolePermission]',
        'files': 'list[FileListOutput]',
        'info': 'object',
        'info_exists': 'bool',
        'notes': 'list[Note]',
        'tags': 'list[str]',
        'templates': 'list[ProjectTemplate]',
        'join_origin': 'JoinOrigins',
        'analyses': 'list[union[AnalysisListOutput,AnalysisListOutputInflatedJob]]',
        'locked': 'Locked',
        'copyable': 'bool',
        'copy_status': 'str',
        'copy_failure_reason': 'str',
        'copy_of': 'str',
        'original_copy_of': 'str',
        'stats': 'ProjectStats',
        'revision': 'int',
        'modified': 'datetime',
        'created': 'datetime',
        'settings': 'ProjectSettingsOutput'
    }

    attribute_map = {
        'id': '_id',
        'label': 'label',
        'description': 'description',
        'group': 'group',
        'parents': 'parents',
        'editions': 'editions',
        'providers': 'providers',
        'ldap_sync': 'ldap_sync',
        'permissions': 'permissions',
        'files': 'files',
        'info': 'info',
        'info_exists': 'info_exists',
        'notes': 'notes',
        'tags': 'tags',
        'templates': 'templates',
        'join_origin': 'join-origin',
        'analyses': 'analyses',
        'locked': 'locked',
        'copyable': 'copyable',
        'copy_status': 'copy_status',
        'copy_failure_reason': 'copy_failure_reason',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of',
        'stats': 'stats',
        'revision': 'revision',
        'modified': 'modified',
        'created': 'created',
        'settings': 'settings'
    }

    rattribute_map = {
        '_id': 'id',
        'label': 'label',
        'description': 'description',
        'group': 'group',
        'parents': 'parents',
        'editions': 'editions',
        'providers': 'providers',
        'ldap_sync': 'ldap_sync',
        'permissions': 'permissions',
        'files': 'files',
        'info': 'info',
        'info_exists': 'info_exists',
        'notes': 'notes',
        'tags': 'tags',
        'templates': 'templates',
        'join-origin': 'join_origin',
        'analyses': 'analyses',
        'locked': 'locked',
        'copyable': 'copyable',
        'copy_status': 'copy_status',
        'copy_failure_reason': 'copy_failure_reason',
        'copy_of': 'copy_of',
        'original_copy_of': 'original_copy_of',
        'stats': 'stats',
        'revision': 'revision',
        'modified': 'modified',
        'created': 'created',
        'settings': 'settings'
    }

    def __init__(self, id=None, label=None, description=None, group=None, parents=None, editions=None, providers=None, ldap_sync=None, permissions=None, files=None, info=None, info_exists=None, notes=None, tags=None, templates=None, join_origin=None, analyses=None, locked=None, copyable=None, copy_status=None, copy_failure_reason=None, copy_of=None, original_copy_of=None, stats=None, revision=None, modified=None, created=None, settings=None):  # noqa: E501
        """ProjectListOutput - a model defined in Swagger"""
        super(ProjectListOutput, self).__init__()

        self._id = None
        self._label = None
        self._description = None
        self._group = None
        self._parents = None
        self._editions = None
        self._providers = None
        self._ldap_sync = None
        self._permissions = None
        self._files = None
        self._info = None
        self._info_exists = None
        self._notes = None
        self._tags = None
        self._templates = None
        self._join_origin = None
        self._analyses = None
        self._locked = None
        self._copyable = None
        self._copy_status = None
        self._copy_failure_reason = None
        self._copy_of = None
        self._original_copy_of = None
        self._stats = None
        self._revision = None
        self._modified = None
        self._created = None
        self._settings = None
        self.discriminator = None
        self.alt_discriminator = None

        self.id = id
        if label is not None:
            self.label = label
        self.description = description
        self.group = group
        self.parents = parents
        self.editions = editions
        self.providers = providers
        if ldap_sync is not None:
            self.ldap_sync = ldap_sync
        self.permissions = permissions
        self.files = files
        self.info = info
        if info_exists is not None:
            self.info_exists = info_exists
        if notes is not None:
            self.notes = notes
        self.tags = tags
        self.templates = templates
        if join_origin is not None:
            self.join_origin = join_origin
        if analyses is not None:
            self.analyses = analyses
        if locked is not None:
            self.locked = locked
        if copyable is not None:
            self.copyable = copyable
        if copy_status is not None:
            self.copy_status = copy_status
        if copy_failure_reason is not None:
            self.copy_failure_reason = copy_failure_reason
        if copy_of is not None:
            self.copy_of = copy_of
        if original_copy_of is not None:
            self.original_copy_of = original_copy_of
        if stats is not None:
            self.stats = stats
        self.revision = revision
        self.modified = modified
        self.created = created
        if settings is not None:
            self.settings = settings

    @property
    def id(self):
        """Gets the id of this ProjectListOutput.


        :return: The id of this ProjectListOutput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ProjectListOutput.


        :param id: The id of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this ProjectListOutput.


        :return: The label of this ProjectListOutput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this ProjectListOutput.


        :param label: The label of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def description(self):
        """Gets the description of this ProjectListOutput.


        :return: The description of this ProjectListOutput.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ProjectListOutput.


        :param description: The description of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def group(self):
        """Gets the group of this ProjectListOutput.


        :return: The group of this ProjectListOutput.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this ProjectListOutput.


        :param group: The group of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._group = group

    @property
    def parents(self):
        """Gets the parents of this ProjectListOutput.


        :return: The parents of this ProjectListOutput.
        :rtype: ProjectParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this ProjectListOutput.


        :param parents: The parents of this ProjectListOutput.  # noqa: E501
        :type: ProjectParents
        """

        self._parents = parents

    @property
    def editions(self):
        """Gets the editions of this ProjectListOutput.


        :return: The editions of this ProjectListOutput.
        :rtype: Edition
        """
        return self._editions

    @editions.setter
    def editions(self, editions):
        """Sets the editions of this ProjectListOutput.


        :param editions: The editions of this ProjectListOutput.  # noqa: E501
        :type: Edition
        """

        self._editions = editions

    @property
    def providers(self):
        """Gets the providers of this ProjectListOutput.


        :return: The providers of this ProjectListOutput.
        :rtype: Providers
        """
        return self._providers

    @providers.setter
    def providers(self, providers):
        """Sets the providers of this ProjectListOutput.


        :param providers: The providers of this ProjectListOutput.  # noqa: E501
        :type: Providers
        """

        self._providers = providers

    @property
    def ldap_sync(self):
        """Gets the ldap_sync of this ProjectListOutput.


        :return: The ldap_sync of this ProjectListOutput.
        :rtype: LdapSyncStatus
        """
        return self._ldap_sync

    @ldap_sync.setter
    def ldap_sync(self, ldap_sync):
        """Sets the ldap_sync of this ProjectListOutput.


        :param ldap_sync: The ldap_sync of this ProjectListOutput.  # noqa: E501
        :type: LdapSyncStatus
        """

        self._ldap_sync = ldap_sync

    @property
    def permissions(self):
        """Gets the permissions of this ProjectListOutput.


        :return: The permissions of this ProjectListOutput.
        :rtype: list[RolePermission]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this ProjectListOutput.


        :param permissions: The permissions of this ProjectListOutput.  # noqa: E501
        :type: list[RolePermission]
        """

        self._permissions = permissions

    @property
    def files(self):
        """Gets the files of this ProjectListOutput.


        :return: The files of this ProjectListOutput.
        :rtype: list[FileListOutput]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this ProjectListOutput.


        :param files: The files of this ProjectListOutput.  # noqa: E501
        :type: list[FileListOutput]
        """

        self._files = files

    @property
    def info(self):
        """Gets the info of this ProjectListOutput.


        :return: The info of this ProjectListOutput.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this ProjectListOutput.


        :param info: The info of this ProjectListOutput.  # noqa: E501
        :type: object
        """

        self._info = info

    @property
    def info_exists(self):
        """Gets the info_exists of this ProjectListOutput.


        :return: The info_exists of this ProjectListOutput.
        :rtype: bool
        """
        return self._info_exists

    @info_exists.setter
    def info_exists(self, info_exists):
        """Sets the info_exists of this ProjectListOutput.


        :param info_exists: The info_exists of this ProjectListOutput.  # noqa: E501
        :type: bool
        """

        self._info_exists = info_exists

    @property
    def notes(self):
        """Gets the notes of this ProjectListOutput.


        :return: The notes of this ProjectListOutput.
        :rtype: list[Note]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this ProjectListOutput.


        :param notes: The notes of this ProjectListOutput.  # noqa: E501
        :type: list[Note]
        """

        self._notes = notes

    @property
    def tags(self):
        """Gets the tags of this ProjectListOutput.


        :return: The tags of this ProjectListOutput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ProjectListOutput.


        :param tags: The tags of this ProjectListOutput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def templates(self):
        """Gets the templates of this ProjectListOutput.


        :return: The templates of this ProjectListOutput.
        :rtype: list[ProjectTemplate]
        """
        return self._templates

    @templates.setter
    def templates(self, templates):
        """Sets the templates of this ProjectListOutput.


        :param templates: The templates of this ProjectListOutput.  # noqa: E501
        :type: list[ProjectTemplate]
        """

        self._templates = templates

    @property
    def join_origin(self):
        """Gets the join_origin of this ProjectListOutput.


        :return: The join_origin of this ProjectListOutput.
        :rtype: JoinOrigins
        """
        return self._join_origin

    @join_origin.setter
    def join_origin(self, join_origin):
        """Sets the join_origin of this ProjectListOutput.


        :param join_origin: The join_origin of this ProjectListOutput.  # noqa: E501
        :type: JoinOrigins
        """

        self._join_origin = join_origin

    @property
    def analyses(self):
        """Gets the analyses of this ProjectListOutput.


        :return: The analyses of this ProjectListOutput.
        :rtype: list[union[AnalysisListOutput,AnalysisListOutputInflatedJob]]
        """
        return self._analyses

    @analyses.setter
    def analyses(self, analyses):
        """Sets the analyses of this ProjectListOutput.


        :param analyses: The analyses of this ProjectListOutput.  # noqa: E501
        :type: list[union[AnalysisListOutput,AnalysisListOutputInflatedJob]]
        """

        self._analyses = analyses

    @property
    def locked(self):
        """Gets the locked of this ProjectListOutput.


        :return: The locked of this ProjectListOutput.
        :rtype: Locked
        """
        return self._locked

    @locked.setter
    def locked(self, locked):
        """Sets the locked of this ProjectListOutput.


        :param locked: The locked of this ProjectListOutput.  # noqa: E501
        :type: Locked
        """

        self._locked = locked

    @property
    def copyable(self):
        """Gets the copyable of this ProjectListOutput.


        :return: The copyable of this ProjectListOutput.
        :rtype: bool
        """
        return self._copyable

    @copyable.setter
    def copyable(self, copyable):
        """Sets the copyable of this ProjectListOutput.


        :param copyable: The copyable of this ProjectListOutput.  # noqa: E501
        :type: bool
        """

        self._copyable = copyable

    @property
    def copy_status(self):
        """Gets the copy_status of this ProjectListOutput.


        :return: The copy_status of this ProjectListOutput.
        :rtype: str
        """
        return self._copy_status

    @copy_status.setter
    def copy_status(self, copy_status):
        """Sets the copy_status of this ProjectListOutput.


        :param copy_status: The copy_status of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._copy_status = copy_status

    @property
    def copy_failure_reason(self):
        """Gets the copy_failure_reason of this ProjectListOutput.


        :return: The copy_failure_reason of this ProjectListOutput.
        :rtype: str
        """
        return self._copy_failure_reason

    @copy_failure_reason.setter
    def copy_failure_reason(self, copy_failure_reason):
        """Sets the copy_failure_reason of this ProjectListOutput.


        :param copy_failure_reason: The copy_failure_reason of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._copy_failure_reason = copy_failure_reason

    @property
    def copy_of(self):
        """Gets the copy_of of this ProjectListOutput.


        :return: The copy_of of this ProjectListOutput.
        :rtype: str
        """
        return self._copy_of

    @copy_of.setter
    def copy_of(self, copy_of):
        """Sets the copy_of of this ProjectListOutput.


        :param copy_of: The copy_of of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._copy_of = copy_of

    @property
    def original_copy_of(self):
        """Gets the original_copy_of of this ProjectListOutput.


        :return: The original_copy_of of this ProjectListOutput.
        :rtype: str
        """
        return self._original_copy_of

    @original_copy_of.setter
    def original_copy_of(self, original_copy_of):
        """Sets the original_copy_of of this ProjectListOutput.


        :param original_copy_of: The original_copy_of of this ProjectListOutput.  # noqa: E501
        :type: str
        """

        self._original_copy_of = original_copy_of

    @property
    def stats(self):
        """Gets the stats of this ProjectListOutput.


        :return: The stats of this ProjectListOutput.
        :rtype: ProjectStats
        """
        return self._stats

    @stats.setter
    def stats(self, stats):
        """Sets the stats of this ProjectListOutput.


        :param stats: The stats of this ProjectListOutput.  # noqa: E501
        :type: ProjectStats
        """

        self._stats = stats

    @property
    def revision(self):
        """Gets the revision of this ProjectListOutput.


        :return: The revision of this ProjectListOutput.
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this ProjectListOutput.


        :param revision: The revision of this ProjectListOutput.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def modified(self):
        """Gets the modified of this ProjectListOutput.


        :return: The modified of this ProjectListOutput.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this ProjectListOutput.


        :param modified: The modified of this ProjectListOutput.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def created(self):
        """Gets the created of this ProjectListOutput.


        :return: The created of this ProjectListOutput.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this ProjectListOutput.


        :param created: The created of this ProjectListOutput.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def settings(self):
        """Gets the settings of this ProjectListOutput.


        :return: The settings of this ProjectListOutput.
        :rtype: ProjectSettingsOutput
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """Sets the settings of this ProjectListOutput.


        :param settings: The settings of this ProjectListOutput.  # noqa: E501
        :type: ProjectSettingsOutput
        """

        self._settings = settings


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
        from flywheel.models.project import Project
        relatives = (
            Project,
        )
        if not isinstance(other, relatives + (ProjectListOutput,)):
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
