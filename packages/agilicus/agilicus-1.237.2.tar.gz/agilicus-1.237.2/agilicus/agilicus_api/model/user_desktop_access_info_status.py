"""
    Agilicus API

    Agilicus is API-first. Modern software is controlled by other software, is open, is available for you to use the way you want, securely, simply.  The OpenAPI Specification in YAML format is available on [www](https://www.agilicus.com/www/api/agilicus-openapi.yaml) for importing to other tools.  A rendered, online viewable and usable version of this specification is available at [api](https://www.agilicus.com/api). You may try the API inline directly in the web page. To do so, first obtain an Authentication Token (the simplest way is to install the Python SDK, and then run `agilicus-cli --issuer https://MYISSUER get-token`). You will need an org-id for most calls (and can obtain from `agilicus-cli --issuer https://MYISSUER list-orgs`). The `MYISSUER` will typically be `auth.MYDOMAIN`, and you will see it as you sign-in to the administrative UI.  This API releases on Bearer-Token authentication. To obtain a valid bearer token you will need to Authenticate to an Issuer with OpenID Connect (a superset of OAUTH2).  Your \"issuer\" will look like https://auth.MYDOMAIN. For example, when you signed-up, if you said \"use my own domain name\" and assigned a CNAME of cloud.example.com, then your issuer would be https://auth.cloud.example.com.  If you selected \"use an Agilicus supplied domain name\", your issuer would look like https://auth.myorg.agilicus.cloud.  For test purposes you can use our [Python SDK](https://pypi.org/project/agilicus/) and run `agilicus-cli --issuer https://auth.MYDOMAIN get-token`.  This API may be used in any language runtime that supports OpenAPI 3.0, or, you may use our [Python SDK](https://pypi.org/project/agilicus/), our [Typescript SDK](https://www.npmjs.com/package/@agilicus/angular), or our [Golang SDK](https://git.agilicus.com/pub/sdk-go).  100% of the activities in our system our API-driven, from our web-admin, through our progressive web applications, to all internals: there is nothing that is not accessible.  For more information, see [developer resources](https://www.agilicus.com/developer).   # noqa: E501

    The version of the OpenAPI document: 2024.01.19
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from agilicus_api.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from agilicus_api.exceptions import ApiAttributeError


def lazy_import():
    from agilicus_api.model.custom_desktop_client_config import CustomDesktopClientConfig
    from agilicus_api.model.display_info import DisplayInfo
    from agilicus_api.model.remote_app_access_info import RemoteAppAccessInfo
    globals()['CustomDesktopClientConfig'] = CustomDesktopClientConfig
    globals()['DisplayInfo'] = DisplayInfo
    globals()['RemoteAppAccessInfo'] = RemoteAppAccessInfo


class UserDesktopAccessInfoStatus(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('desktop_type',): {
            'RDP': "rdp",
            'VNC': "vnc",
        },
        ('access_level',): {
            'REQUESTED': "requested",
            'GRANTED': "granted",
            'NONE': "none",
        },
    }

    validations = {
        ('user_id',): {
            'max_length': 40,
            'min_length': 1,
        },
        ('org_id',): {
            'max_length': 40,
            'min_length': 1,
        },
        ('org_name',): {
            'max_length': 100,
        },
        ('resource_name',): {
            'max_length': 128,
        },
        ('resource_type',): {
            'max_length': 128,
        },
        ('desktop_type',): {
            'max_length': 128,
        },
        ('parent_org_id',): {
            'max_length': 40,
            'min_length': 1,
        },
        ('parent_org_name',): {
            'max_length': 100,
        },
        ('resource_uri',): {
            'max_length': 1024,
        },
        ('web_client_uri',): {
            'max_length': 1024,
            'min_length': 1,
        },
    }

    @property
    def user_id(self):
       return self.get("user_id")

    @user_id.setter
    def user_id(self, new_value):
       self.user_id = new_value

    @property
    def org_id(self):
       return self.get("org_id")

    @org_id.setter
    def org_id(self, new_value):
       self.org_id = new_value

    @property
    def org_name(self):
       return self.get("org_name")

    @org_name.setter
    def org_name(self, new_value):
       self.org_name = new_value

    @property
    def parent_org_id(self):
       return self.get("parent_org_id")

    @parent_org_id.setter
    def parent_org_id(self, new_value):
       self.parent_org_id = new_value

    @property
    def parent_org_name(self):
       return self.get("parent_org_name")

    @parent_org_name.setter
    def parent_org_name(self, new_value):
       self.parent_org_name = new_value

    @property
    def resource_id(self):
       return self.get("resource_id")

    @resource_id.setter
    def resource_id(self, new_value):
       self.resource_id = new_value

    @property
    def resource_name(self):
       return self.get("resource_name")

    @resource_name.setter
    def resource_name(self, new_value):
       self.resource_name = new_value

    @property
    def resource_type(self):
       return self.get("resource_type")

    @resource_type.setter
    def resource_type(self, new_value):
       self.resource_type = new_value

    @property
    def desktop_type(self):
       return self.get("desktop_type")

    @desktop_type.setter
    def desktop_type(self, new_value):
       self.desktop_type = new_value

    @property
    def resource_uri(self):
       return self.get("resource_uri")

    @resource_uri.setter
    def resource_uri(self, new_value):
       self.resource_uri = new_value

    @property
    def access_level(self):
       return self.get("access_level")

    @access_level.setter
    def access_level(self, new_value):
       self.access_level = new_value

    @property
    def roles(self):
       return self.get("roles")

    @roles.setter
    def roles(self, new_value):
       self.roles = new_value

    @property
    def remote_app(self):
       return self.get("remote_app")

    @remote_app.setter
    def remote_app(self, new_value):
       self.remote_app = new_value

    @property
    def display_info(self):
       return self.get("display_info")

    @display_info.setter
    def display_info(self, new_value):
       self.display_info = new_value

    @property
    def web_client_uri(self):
       return self.get("web_client_uri")

    @web_client_uri.setter
    def web_client_uri(self, new_value):
       self.web_client_uri = new_value

    @property
    def config_overrides(self):
       return self.get("config_overrides")

    @config_overrides.setter
    def config_overrides(self, new_value):
       self.config_overrides = new_value

    @property
    def config_overrides_error(self):
       return self.get("config_overrides_error")

    @config_overrides_error.setter
    def config_overrides_error(self, new_value):
       self.config_overrides_error = new_value

    @property
    def updated(self):
       return self.get("updated")

    @updated.setter
    def updated(self, new_value):
       self.updated = new_value

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'user_id': (str,),  # noqa: E501
            'org_id': (str,),  # noqa: E501
            'org_name': (str,),  # noqa: E501
            'resource_id': (str,),  # noqa: E501
            'resource_name': (str,),  # noqa: E501
            'resource_type': (str,),  # noqa: E501
            'desktop_type': (str,),  # noqa: E501
            'access_level': (str,),  # noqa: E501
            'parent_org_id': (str,),  # noqa: E501
            'parent_org_name': (str,),  # noqa: E501
            'resource_uri': (str,),  # noqa: E501
            'roles': ([str],),  # noqa: E501
            'remote_app': (RemoteAppAccessInfo,),  # noqa: E501
            'display_info': (DisplayInfo,),  # noqa: E501
            'web_client_uri': (str,),  # noqa: E501
            'config_overrides': ([CustomDesktopClientConfig],),  # noqa: E501
            'config_overrides_error': (str, none_type,),  # noqa: E501
            'updated': (datetime,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None



    attribute_map = {
        'user_id': 'user_id',  # noqa: E501
        'org_id': 'org_id',  # noqa: E501
        'org_name': 'org_name',  # noqa: E501
        'resource_id': 'resource_id',  # noqa: E501
        'resource_name': 'resource_name',  # noqa: E501
        'resource_type': 'resource_type',  # noqa: E501
        'desktop_type': 'desktop_type',  # noqa: E501
        'access_level': 'access_level',  # noqa: E501
        'parent_org_id': 'parent_org_id',  # noqa: E501
        'parent_org_name': 'parent_org_name',  # noqa: E501
        'resource_uri': 'resource_uri',  # noqa: E501
        'roles': 'roles',  # noqa: E501
        'remote_app': 'remote_app',  # noqa: E501
        'display_info': 'display_info',  # noqa: E501
        'web_client_uri': 'web_client_uri',  # noqa: E501
        'config_overrides': 'config_overrides',  # noqa: E501
        'config_overrides_error': 'config_overrides_error',  # noqa: E501
        'updated': 'updated',  # noqa: E501
    }

    read_only_vars = {
        'updated',  # noqa: E501
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, user_id, org_id, org_name, resource_id, resource_name, resource_type, desktop_type, access_level, *args, **kwargs):  # noqa: E501
        """UserDesktopAccessInfoStatus - a model defined in OpenAPI

        Args:
            user_id (str): The unique id of the User to which this record applies. 
            org_id (str): The unique id of the Organisation to which this record applies. 
            org_name (str): The name of Organisation to which this record applies. 
            resource_id (str): Unique identifier
            resource_name (str): The name of the resource. 
            resource_type (str): The type of the resource. 
            desktop_type (str): The type of the desktop
            access_level (str): Whether the user has access, has requested access, etc. The possible values have the following meanings:   - requested: the user has requested access to this resource.   - granted: the user has access to this resource   - none: the user has no relation to this resource. 

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            parent_org_id (str): The unique id of the parent of the Organisation to which this record applies. Omitted if the Organisation has no parent. . [optional]  # noqa: E501
            parent_org_name (str): The name of the parent of the Organisation to which this record applies. Omitted if the Organisation has no parent. . [optional]  # noqa: E501
            resource_uri (str): Many resources have corresponding URIs which may be used to access them. This field provides the URI for the resource represented by this object. . [optional]  # noqa: E501
            roles ([str]): The list of roles held by the user for the given resource.. [optional]  # noqa: E501
            remote_app (RemoteAppAccessInfo): [optional]  # noqa: E501
            display_info (DisplayInfo): [optional]  # noqa: E501
            web_client_uri (str): The uri for launching user's resource via web client . [optional]  # noqa: E501
            config_overrides ([CustomDesktopClientConfig]): Configuration overrides applicable to this desktop. If the configured overrides are invalid, this list will be empty, and config_overrides_error will be populated. . [optional]  # noqa: E501
            config_overrides_error (str, none_type): If the system encounters an invalid CustomDesktopClientConfig associated with this desktop, then the corresponding error will be provided here for ease of diagnostics. If this value is not empty, the client should not proceed with creating configuration for the desktop. . [optional]  # noqa: E501
            updated (datetime): Update time. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.user_id = user_id
        self.org_id = org_id
        self.org_name = org_name
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.desktop_type = desktop_type
        self.access_level = access_level
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    def __python_set(val):
        return set(val)
 
    required_properties = __python_set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, user_id, org_id, org_name, resource_id, resource_name, resource_type, desktop_type, access_level, *args, **kwargs):  # noqa: E501
        """UserDesktopAccessInfoStatus - a model defined in OpenAPI

        Args:
            user_id (str): The unique id of the User to which this record applies. 
            org_id (str): The unique id of the Organisation to which this record applies. 
            org_name (str): The name of Organisation to which this record applies. 
            resource_id (str): Unique identifier
            resource_name (str): The name of the resource. 
            resource_type (str): The type of the resource. 
            desktop_type (str): The type of the desktop
            access_level (str): Whether the user has access, has requested access, etc. The possible values have the following meanings:   - requested: the user has requested access to this resource.   - granted: the user has access to this resource   - none: the user has no relation to this resource. 

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            parent_org_id (str): The unique id of the parent of the Organisation to which this record applies. Omitted if the Organisation has no parent. . [optional]  # noqa: E501
            parent_org_name (str): The name of the parent of the Organisation to which this record applies. Omitted if the Organisation has no parent. . [optional]  # noqa: E501
            resource_uri (str): Many resources have corresponding URIs which may be used to access them. This field provides the URI for the resource represented by this object. . [optional]  # noqa: E501
            roles ([str]): The list of roles held by the user for the given resource.. [optional]  # noqa: E501
            remote_app (RemoteAppAccessInfo): [optional]  # noqa: E501
            display_info (DisplayInfo): [optional]  # noqa: E501
            web_client_uri (str): The uri for launching user's resource via web client . [optional]  # noqa: E501
            config_overrides ([CustomDesktopClientConfig]): Configuration overrides applicable to this desktop. If the configured overrides are invalid, this list will be empty, and config_overrides_error will be populated. . [optional]  # noqa: E501
            config_overrides_error (str, none_type): If the system encounters an invalid CustomDesktopClientConfig associated with this desktop, then the corresponding error will be provided here for ease of diagnostics. If this value is not empty, the client should not proceed with creating configuration for the desktop. . [optional]  # noqa: E501
            updated (datetime): Update time. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.user_id = user_id
        self.org_id = org_id
        self.org_name = org_name
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.desktop_type = desktop_type
        self.access_level = access_level
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")

