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
    from agilicus_api.model.certificate_transparency_settings import CertificateTransparencySettings
    from agilicus_api.model.content_type_options_settings import ContentTypeOptionsSettings
    from agilicus_api.model.cors_settings import CORSSettings
    from agilicus_api.model.cross_origin_embedder_policy_settings import CrossOriginEmbedderPolicySettings
    from agilicus_api.model.cross_origin_opener_policy_settings import CrossOriginOpenerPolicySettings
    from agilicus_api.model.cross_origin_resource_policy_settings import CrossOriginResourcePolicySettings
    from agilicus_api.model.csp_settings import CSPSettings
    from agilicus_api.model.frame_options_settings import FrameOptionsSettings
    from agilicus_api.model.hsts_settings import HSTSSettings
    from agilicus_api.model.permitted_cross_domain_policies_settings import PermittedCrossDomainPoliciesSettings
    from agilicus_api.model.referrer_policy_settings import ReferrerPolicySettings
    from agilicus_api.model.xss_settings import XSSSettings
    globals()['CORSSettings'] = CORSSettings
    globals()['CSPSettings'] = CSPSettings
    globals()['CertificateTransparencySettings'] = CertificateTransparencySettings
    globals()['ContentTypeOptionsSettings'] = ContentTypeOptionsSettings
    globals()['CrossOriginEmbedderPolicySettings'] = CrossOriginEmbedderPolicySettings
    globals()['CrossOriginOpenerPolicySettings'] = CrossOriginOpenerPolicySettings
    globals()['CrossOriginResourcePolicySettings'] = CrossOriginResourcePolicySettings
    globals()['FrameOptionsSettings'] = FrameOptionsSettings
    globals()['HSTSSettings'] = HSTSSettings
    globals()['PermittedCrossDomainPoliciesSettings'] = PermittedCrossDomainPoliciesSettings
    globals()['ReferrerPolicySettings'] = ReferrerPolicySettings
    globals()['XSSSettings'] = XSSSettings


class HTTPSecuritySettings(ModelNormal):
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
    }

    validations = {
    }

    @property
    def csp(self):
       return self.get("csp")

    @csp.setter
    def csp(self, new_value):
       self.csp = new_value

    @property
    def cors(self):
       return self.get("cors")

    @cors.setter
    def cors(self, new_value):
       self.cors = new_value

    @property
    def hsts(self):
       return self.get("hsts")

    @hsts.setter
    def hsts(self, new_value):
       self.hsts = new_value

    @property
    def xss_protection(self):
       return self.get("xss_protection")

    @xss_protection.setter
    def xss_protection(self, new_value):
       self.xss_protection = new_value

    @property
    def certificate_transparency(self):
       return self.get("certificate_transparency")

    @certificate_transparency.setter
    def certificate_transparency(self, new_value):
       self.certificate_transparency = new_value

    @property
    def frame_options(self):
       return self.get("frame_options")

    @frame_options.setter
    def frame_options(self, new_value):
       self.frame_options = new_value

    @property
    def content_type_options(self):
       return self.get("content_type_options")

    @content_type_options.setter
    def content_type_options(self, new_value):
       self.content_type_options = new_value

    @property
    def permitted_cross_domain_policies(self):
       return self.get("permitted_cross_domain_policies")

    @permitted_cross_domain_policies.setter
    def permitted_cross_domain_policies(self, new_value):
       self.permitted_cross_domain_policies = new_value

    @property
    def coep(self):
       return self.get("coep")

    @coep.setter
    def coep(self, new_value):
       self.coep = new_value

    @property
    def coop(self):
       return self.get("coop")

    @coop.setter
    def coop(self, new_value):
       self.coop = new_value

    @property
    def corp(self):
       return self.get("corp")

    @corp.setter
    def corp(self, new_value):
       self.corp = new_value

    @property
    def referrer_policy(self):
       return self.get("referrer_policy")

    @referrer_policy.setter
    def referrer_policy(self, new_value):
       self.referrer_policy = new_value

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
            'csp': (CSPSettings,),  # noqa: E501
            'cors': (CORSSettings,),  # noqa: E501
            'hsts': (HSTSSettings,),  # noqa: E501
            'xss_protection': (XSSSettings,),  # noqa: E501
            'certificate_transparency': (CertificateTransparencySettings,),  # noqa: E501
            'frame_options': (FrameOptionsSettings,),  # noqa: E501
            'content_type_options': (ContentTypeOptionsSettings,),  # noqa: E501
            'permitted_cross_domain_policies': (PermittedCrossDomainPoliciesSettings,),  # noqa: E501
            'coep': (CrossOriginEmbedderPolicySettings,),  # noqa: E501
            'coop': (CrossOriginOpenerPolicySettings,),  # noqa: E501
            'corp': (CrossOriginResourcePolicySettings,),  # noqa: E501
            'referrer_policy': (ReferrerPolicySettings,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None



    attribute_map = {
        'csp': 'csp',  # noqa: E501
        'cors': 'cors',  # noqa: E501
        'hsts': 'hsts',  # noqa: E501
        'xss_protection': 'xss_protection',  # noqa: E501
        'certificate_transparency': 'certificate_transparency',  # noqa: E501
        'frame_options': 'frame_options',  # noqa: E501
        'content_type_options': 'content_type_options',  # noqa: E501
        'permitted_cross_domain_policies': 'permitted_cross_domain_policies',  # noqa: E501
        'coep': 'coep',  # noqa: E501
        'coop': 'coop',  # noqa: E501
        'corp': 'corp',  # noqa: E501
        'referrer_policy': 'referrer_policy',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """HTTPSecuritySettings - a model defined in OpenAPI

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
            csp (CSPSettings): [optional]  # noqa: E501
            cors (CORSSettings): [optional]  # noqa: E501
            hsts (HSTSSettings): [optional]  # noqa: E501
            xss_protection (XSSSettings): [optional]  # noqa: E501
            certificate_transparency (CertificateTransparencySettings): [optional]  # noqa: E501
            frame_options (FrameOptionsSettings): [optional]  # noqa: E501
            content_type_options (ContentTypeOptionsSettings): [optional]  # noqa: E501
            permitted_cross_domain_policies (PermittedCrossDomainPoliciesSettings): [optional]  # noqa: E501
            coep (CrossOriginEmbedderPolicySettings): [optional]  # noqa: E501
            coop (CrossOriginOpenerPolicySettings): [optional]  # noqa: E501
            corp (CrossOriginResourcePolicySettings): [optional]  # noqa: E501
            referrer_policy (ReferrerPolicySettings): [optional]  # noqa: E501
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
    def __init__(self, *args, **kwargs):  # noqa: E501
        """HTTPSecuritySettings - a model defined in OpenAPI

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
            csp (CSPSettings): [optional]  # noqa: E501
            cors (CORSSettings): [optional]  # noqa: E501
            hsts (HSTSSettings): [optional]  # noqa: E501
            xss_protection (XSSSettings): [optional]  # noqa: E501
            certificate_transparency (CertificateTransparencySettings): [optional]  # noqa: E501
            frame_options (FrameOptionsSettings): [optional]  # noqa: E501
            content_type_options (ContentTypeOptionsSettings): [optional]  # noqa: E501
            permitted_cross_domain_policies (PermittedCrossDomainPoliciesSettings): [optional]  # noqa: E501
            coep (CrossOriginEmbedderPolicySettings): [optional]  # noqa: E501
            coop (CrossOriginOpenerPolicySettings): [optional]  # noqa: E501
            corp (CrossOriginResourcePolicySettings): [optional]  # noqa: E501
            referrer_policy (ReferrerPolicySettings): [optional]  # noqa: E501
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

