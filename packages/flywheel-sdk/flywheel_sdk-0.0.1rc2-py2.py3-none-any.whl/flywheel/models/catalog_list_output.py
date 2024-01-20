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

from flywheel.models.body_region import BodyRegion  # noqa: F401,E501
from flywheel.models.organ_system import OrganSystem  # noqa: F401,E501
from flywheel.models.project_contact import ProjectContact  # noqa: F401,E501
from flywheel.models.project_institution import ProjectInstitution  # noqa: F401,E501
from flywheel.models.project_stats import ProjectStats  # noqa: F401,E501
from flywheel.models.therapeutic_area import TherapeuticArea  # noqa: F401,E501

class CatalogListOutput(object):

    swagger_types = {
        'id': 'str',
        'label': 'str',
        'tags': 'list[str]',
        'therapeutic_areas': 'list[TherapeuticArea]',
        'body_regions': 'list[BodyRegion]',
        'organ_systems': 'list[OrganSystem]',
        'project_institutions': 'list[ProjectInstitution]',
        'project_contacts': 'list[ProjectContact]',
        'summary': 'str',
        'stats': 'ProjectStats'
    }

    attribute_map = {
        'id': 'id',
        'label': 'label',
        'tags': 'tags',
        'therapeutic_areas': 'therapeutic_areas',
        'body_regions': 'body_regions',
        'organ_systems': 'organ_systems',
        'project_institutions': 'project_institutions',
        'project_contacts': 'project_contacts',
        'summary': 'summary',
        'stats': 'stats'
    }

    rattribute_map = {
        'id': 'id',
        'label': 'label',
        'tags': 'tags',
        'therapeutic_areas': 'therapeutic_areas',
        'body_regions': 'body_regions',
        'organ_systems': 'organ_systems',
        'project_institutions': 'project_institutions',
        'project_contacts': 'project_contacts',
        'summary': 'summary',
        'stats': 'stats'
    }

    def __init__(self, id=None, label=None, tags=None, therapeutic_areas=None, body_regions=None, organ_systems=None, project_institutions=None, project_contacts=None, summary=None, stats=None):  # noqa: E501
        """CatalogListOutput - a model defined in Swagger"""
        super(CatalogListOutput, self).__init__()

        self._id = None
        self._label = None
        self._tags = None
        self._therapeutic_areas = None
        self._body_regions = None
        self._organ_systems = None
        self._project_institutions = None
        self._project_contacts = None
        self._summary = None
        self._stats = None
        self.discriminator = None
        self.alt_discriminator = None

        self.id = id
        if label is not None:
            self.label = label
        self.tags = tags
        self.therapeutic_areas = therapeutic_areas
        self.body_regions = body_regions
        self.organ_systems = organ_systems
        self.project_institutions = project_institutions
        self.project_contacts = project_contacts
        self.summary = summary
        if stats is not None:
            self.stats = stats

    @property
    def id(self):
        """Gets the id of this CatalogListOutput.


        :return: The id of this CatalogListOutput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CatalogListOutput.


        :param id: The id of this CatalogListOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this CatalogListOutput.


        :return: The label of this CatalogListOutput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this CatalogListOutput.


        :param label: The label of this CatalogListOutput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def tags(self):
        """Gets the tags of this CatalogListOutput.


        :return: The tags of this CatalogListOutput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CatalogListOutput.


        :param tags: The tags of this CatalogListOutput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def therapeutic_areas(self):
        """Gets the therapeutic_areas of this CatalogListOutput.


        :return: The therapeutic_areas of this CatalogListOutput.
        :rtype: list[TherapeuticArea]
        """
        return self._therapeutic_areas

    @therapeutic_areas.setter
    def therapeutic_areas(self, therapeutic_areas):
        """Sets the therapeutic_areas of this CatalogListOutput.


        :param therapeutic_areas: The therapeutic_areas of this CatalogListOutput.  # noqa: E501
        :type: list[TherapeuticArea]
        """

        self._therapeutic_areas = therapeutic_areas

    @property
    def body_regions(self):
        """Gets the body_regions of this CatalogListOutput.


        :return: The body_regions of this CatalogListOutput.
        :rtype: list[BodyRegion]
        """
        return self._body_regions

    @body_regions.setter
    def body_regions(self, body_regions):
        """Sets the body_regions of this CatalogListOutput.


        :param body_regions: The body_regions of this CatalogListOutput.  # noqa: E501
        :type: list[BodyRegion]
        """

        self._body_regions = body_regions

    @property
    def organ_systems(self):
        """Gets the organ_systems of this CatalogListOutput.


        :return: The organ_systems of this CatalogListOutput.
        :rtype: list[OrganSystem]
        """
        return self._organ_systems

    @organ_systems.setter
    def organ_systems(self, organ_systems):
        """Sets the organ_systems of this CatalogListOutput.


        :param organ_systems: The organ_systems of this CatalogListOutput.  # noqa: E501
        :type: list[OrganSystem]
        """

        self._organ_systems = organ_systems

    @property
    def project_institutions(self):
        """Gets the project_institutions of this CatalogListOutput.


        :return: The project_institutions of this CatalogListOutput.
        :rtype: list[ProjectInstitution]
        """
        return self._project_institutions

    @project_institutions.setter
    def project_institutions(self, project_institutions):
        """Sets the project_institutions of this CatalogListOutput.


        :param project_institutions: The project_institutions of this CatalogListOutput.  # noqa: E501
        :type: list[ProjectInstitution]
        """

        self._project_institutions = project_institutions

    @property
    def project_contacts(self):
        """Gets the project_contacts of this CatalogListOutput.


        :return: The project_contacts of this CatalogListOutput.
        :rtype: list[ProjectContact]
        """
        return self._project_contacts

    @project_contacts.setter
    def project_contacts(self, project_contacts):
        """Sets the project_contacts of this CatalogListOutput.


        :param project_contacts: The project_contacts of this CatalogListOutput.  # noqa: E501
        :type: list[ProjectContact]
        """

        self._project_contacts = project_contacts

    @property
    def summary(self):
        """Gets the summary of this CatalogListOutput.


        :return: The summary of this CatalogListOutput.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """Sets the summary of this CatalogListOutput.


        :param summary: The summary of this CatalogListOutput.  # noqa: E501
        :type: str
        """

        self._summary = summary

    @property
    def stats(self):
        """Gets the stats of this CatalogListOutput.


        :return: The stats of this CatalogListOutput.
        :rtype: ProjectStats
        """
        return self._stats

    @stats.setter
    def stats(self, stats):
        """Sets the stats of this CatalogListOutput.


        :param stats: The stats of this CatalogListOutput.  # noqa: E501
        :type: ProjectStats
        """

        self._stats = stats


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
        if not isinstance(other, CatalogListOutput):
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
