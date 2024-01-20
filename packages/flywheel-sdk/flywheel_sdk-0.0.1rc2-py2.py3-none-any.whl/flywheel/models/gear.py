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

from flywheel.models.gear_config import GearConfig  # noqa: F401,E501
from flywheel.models.gear_custom import GearCustom  # noqa: F401,E501
from flywheel.models.gear_environment import GearEnvironment  # noqa: F401,E501
from flywheel.models.gear_inputs import GearInputs  # noqa: F401,E501

class Gear(object):

    swagger_types = {
        'author': 'str',
        'capabilities': 'list[str]',
        'maintainer': 'str',
        'cite': 'str',
        'config': 'GearConfig',
        'custom': 'GearCustom',
        'description': 'str',
        'environment': 'GearEnvironment',
        'flywheel': 'object',
        'command': 'str',
        'inputs': 'GearInputs',
        'label': 'str',
        'license': 'str',
        'name': 'str',
        'source': 'str',
        'url': 'str',
        'version': 'str'
    }

    attribute_map = {
        'author': 'author',
        'capabilities': 'capabilities',
        'maintainer': 'maintainer',
        'cite': 'cite',
        'config': 'config',
        'custom': 'custom',
        'description': 'description',
        'environment': 'environment',
        'flywheel': 'flywheel',
        'command': 'command',
        'inputs': 'inputs',
        'label': 'label',
        'license': 'license',
        'name': 'name',
        'source': 'source',
        'url': 'url',
        'version': 'version'
    }

    rattribute_map = {
        'author': 'author',
        'capabilities': 'capabilities',
        'maintainer': 'maintainer',
        'cite': 'cite',
        'config': 'config',
        'custom': 'custom',
        'description': 'description',
        'environment': 'environment',
        'flywheel': 'flywheel',
        'command': 'command',
        'inputs': 'inputs',
        'label': 'label',
        'license': 'license',
        'name': 'name',
        'source': 'source',
        'url': 'url',
        'version': 'version'
    }

    def __init__(self, author=None, capabilities=None, maintainer=None, cite=None, config=None, custom=None, description=None, environment=None, flywheel=None, command=None, inputs=None, label=None, license=None, name=None, source=None, url=None, version=None):  # noqa: E501
        """Gear - a model defined in Swagger"""
        super(Gear, self).__init__()

        self._author = None
        self._capabilities = None
        self._maintainer = None
        self._cite = None
        self._config = None
        self._custom = None
        self._description = None
        self._environment = None
        self._flywheel = None
        self._command = None
        self._inputs = None
        self._label = None
        self._license = None
        self._name = None
        self._source = None
        self._url = None
        self._version = None
        self.discriminator = None
        self.alt_discriminator = None

        self.author = author
        if capabilities is not None:
            self.capabilities = capabilities
        if maintainer is not None:
            self.maintainer = maintainer
        if cite is not None:
            self.cite = cite
        self.config = config
        if custom is not None:
            self.custom = custom
        self.description = description
        if environment is not None:
            self.environment = environment
        if flywheel is not None:
            self.flywheel = flywheel
        if command is not None:
            self.command = command
        self.inputs = inputs
        self.label = label
        self.license = license
        self.name = name
        self.source = source
        self.url = url
        self.version = version

    @property
    def author(self):
        """Gets the author of this Gear.

        The author of this gear.

        :return: The author of this Gear.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this Gear.

        The author of this gear.

        :param author: The author of this Gear.  # noqa: E501
        :type: str
        """

        self._author = author

    @property
    def capabilities(self):
        """Gets the capabilities of this Gear.


        :return: The capabilities of this Gear.
        :rtype: list[str]
        """
        return self._capabilities

    @capabilities.setter
    def capabilities(self, capabilities):
        """Sets the capabilities of this Gear.


        :param capabilities: The capabilities of this Gear.  # noqa: E501
        :type: list[str]
        """

        self._capabilities = capabilities

    @property
    def maintainer(self):
        """Gets the maintainer of this Gear.

        (optional) The maintainer of this gear. Can be used to distinguish the algorithm author from the gear maintainer.

        :return: The maintainer of this Gear.
        :rtype: str
        """
        return self._maintainer

    @maintainer.setter
    def maintainer(self, maintainer):
        """Sets the maintainer of this Gear.

        (optional) The maintainer of this gear. Can be used to distinguish the algorithm author from the gear maintainer.

        :param maintainer: The maintainer of this Gear.  # noqa: E501
        :type: str
        """

        self._maintainer = maintainer

    @property
    def cite(self):
        """Gets the cite of this Gear.

        (optional) Any citations relevant to the algorithm(s) or work present in the gear.

        :return: The cite of this Gear.
        :rtype: str
        """
        return self._cite

    @cite.setter
    def cite(self, cite):
        """Sets the cite of this Gear.

        (optional) Any citations relevant to the algorithm(s) or work present in the gear.

        :param cite: The cite of this Gear.  # noqa: E501
        :type: str
        """

        self._cite = cite

    @property
    def config(self):
        """Gets the config of this Gear.


        :return: The config of this Gear.
        :rtype: GearConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this Gear.


        :param config: The config of this Gear.  # noqa: E501
        :type: GearConfig
        """

        self._config = config

    @property
    def custom(self):
        """Gets the custom of this Gear.


        :return: The custom of this Gear.
        :rtype: GearCustom
        """
        return self._custom

    @custom.setter
    def custom(self, custom):
        """Sets the custom of this Gear.


        :param custom: The custom of this Gear.  # noqa: E501
        :type: GearCustom
        """

        self._custom = custom

    @property
    def description(self):
        """Gets the description of this Gear.

        A brief description of the gear's purpose. Ideally 1-4 sentences.

        :return: The description of this Gear.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Gear.

        A brief description of the gear's purpose. Ideally 1-4 sentences.

        :param description: The description of this Gear.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def environment(self):
        """Gets the environment of this Gear.


        :return: The environment of this Gear.
        :rtype: GearEnvironment
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """Sets the environment of this Gear.


        :param environment: The environment of this Gear.  # noqa: E501
        :type: GearEnvironment
        """

        self._environment = environment

    @property
    def flywheel(self):
        """Gets the flywheel of this Gear.


        :return: The flywheel of this Gear.
        :rtype: object
        """
        return self._flywheel

    @flywheel.setter
    def flywheel(self, flywheel):
        """Sets the flywheel of this Gear.


        :param flywheel: The flywheel of this Gear.  # noqa: E501
        :type: object
        """

        self._flywheel = flywheel

    @property
    def command(self):
        """Gets the command of this Gear.

        If provided, the starting command for the gear, rather than /flywheel/v0/run. Will be templated according to the spec.

        :return: The command of this Gear.
        :rtype: str
        """
        return self._command

    @command.setter
    def command(self, command):
        """Sets the command of this Gear.

        If provided, the starting command for the gear, rather than /flywheel/v0/run. Will be templated according to the spec.

        :param command: The command of this Gear.  # noqa: E501
        :type: str
        """

        self._command = command

    @property
    def inputs(self):
        """Gets the inputs of this Gear.


        :return: The inputs of this Gear.
        :rtype: GearInputs
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this Gear.


        :param inputs: The inputs of this Gear.  # noqa: E501
        :type: GearInputs
        """

        self._inputs = inputs

    @property
    def label(self):
        """Gets the label of this Gear.

        The human-friendly name of this gear.

        :return: The label of this Gear.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Gear.

        The human-friendly name of this gear.

        :param label: The label of this Gear.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def license(self):
        """Gets the license of this Gear.

        Software license of the gear

        :return: The license of this Gear.
        :rtype: str
        """
        return self._license

    @license.setter
    def license(self, license):
        """Sets the license of this Gear.

        Software license of the gear

        :param license: The license of this Gear.  # noqa: E501
        :type: str
        """

        self._license = license

    @property
    def name(self):
        """Gets the name of this Gear.

        The identification of this gear.

        :return: The name of this Gear.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Gear.

        The identification of this gear.

        :param name: The name of this Gear.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def source(self):
        """Gets the source of this Gear.

        A valid URI, or empty string.

        :return: The source of this Gear.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this Gear.

        A valid URI, or empty string.

        :param source: The source of this Gear.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def url(self):
        """Gets the url of this Gear.

        A valid URI, or empty string.

        :return: The url of this Gear.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Gear.

        A valid URI, or empty string.

        :param url: The url of this Gear.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def version(self):
        """Gets the version of this Gear.

        A human-friendly string explaining the release version of this gear. Example: 3.2.1

        :return: The version of this Gear.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Gear.

        A human-friendly string explaining the release version of this gear. Example: 3.2.1

        :param version: The version of this Gear.  # noqa: E501
        :type: str
        """

        self._version = version


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
        from flywheel.models.gear_manifest import GearManifest
        relatives = (
            GearManifest,
        )
        if not isinstance(other, relatives + (Gear,)):
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
