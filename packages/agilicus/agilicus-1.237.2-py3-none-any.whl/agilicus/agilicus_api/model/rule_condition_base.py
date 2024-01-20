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
    from agilicus_api.model.compound_rule_condition import CompoundRuleCondition
    from agilicus_api.model.host_prefix_rule_condition import HostPrefixRuleCondition
    from agilicus_api.model.http_rule_condition import HttpRuleCondition
    from agilicus_api.model.rule_condition import RuleCondition
    from agilicus_api.model.rule_matcher_list import RuleMatcherList
    from agilicus_api.model.rule_query_body import RuleQueryBody
    from agilicus_api.model.rule_query_parameter import RuleQueryParameter
    from agilicus_api.model.source_iso_country_code_condition import SourceISOCountryCodeCondition
    from agilicus_api.model.template_path import TemplatePath
    globals()['CompoundRuleCondition'] = CompoundRuleCondition
    globals()['HostPrefixRuleCondition'] = HostPrefixRuleCondition
    globals()['HttpRuleCondition'] = HttpRuleCondition
    globals()['RuleCondition'] = RuleCondition
    globals()['RuleMatcherList'] = RuleMatcherList
    globals()['RuleQueryBody'] = RuleQueryBody
    globals()['RuleQueryParameter'] = RuleQueryParameter
    globals()['SourceISOCountryCodeCondition'] = SourceISOCountryCodeCondition
    globals()['TemplatePath'] = TemplatePath


class RuleConditionBase(ModelComposed):
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
        ('methods',): {
            'GET': "get",
            'PUT': "put",
            'POST': "post",
            'DELETE': "delete",
            'HEAD': "head",
            'OPTIONS': "options",
            'CONNECT': "connect",
            'TRACE': "trace",
            'PATCH': "patch",
            'COPY': "copy",
            'LOCK': "lock",
            'MKCOL': "mkcol",
            'MOVE': "move",
            'PROPFIND': "propfind",
            'PROPPATCH': "proppatch",
            'UNLOCK': "unlock",
            'ALL': "all",
        },
        ('list_type',): {
            'CNF': "cnf",
            'DNF': "dnf",
        },
        ('operator',): {
            'IN': "in",
            'NOT_IN': "not_in",
        },
    }

    validations = {
        ('methods',): {
        },
        ('path_regex',): {
            'max_length': 512,
        },
        ('prefix',): {
            'max_length': 4096,
            'regex': {
                'pattern': r'^\/[^?]*$',  # noqa: E501
            },
        },
        ('host',): {
            'max_length': 256,
            'regex': {
                'pattern': r'[a-zA-Z0-9_.:\[\]-]*',  # noqa: E501
            },
        },
    }

    @property
    def rule_type(self):
       return self.get("rule_type")

    @rule_type.setter
    def rule_type(self, new_value):
       self.rule_type = new_value

    @property
    def methods(self):
       return self.get("methods")

    @methods.setter
    def methods(self, new_value):
       self.methods = new_value

    @property
    def path_regex(self):
       return self.get("path_regex")

    @path_regex.setter
    def path_regex(self, new_value):
       self.path_regex = new_value

    @property
    def path_template(self):
       return self.get("path_template")

    @path_template.setter
    def path_template(self, new_value):
       self.path_template = new_value

    @property
    def query_parameters(self):
       return self.get("query_parameters")

    @query_parameters.setter
    def query_parameters(self, new_value):
       self.query_parameters = new_value

    @property
    def body(self):
       return self.get("body")

    @body.setter
    def body(self, new_value):
       self.body = new_value

    @property
    def matchers(self):
       return self.get("matchers")

    @matchers.setter
    def matchers(self, new_value):
       self.matchers = new_value

    @property
    def separate_query(self):
       return self.get("separate_query")

    @separate_query.setter
    def separate_query(self, new_value):
       self.separate_query = new_value

    @property
    def condition_type(self):
       return self.get("condition_type")

    @condition_type.setter
    def condition_type(self, new_value):
       self.condition_type = new_value

    @property
    def condition_list(self):
       return self.get("condition_list")

    @condition_list.setter
    def condition_list(self, new_value):
       self.condition_list = new_value

    @property
    def list_type(self):
       return self.get("list_type")

    @list_type.setter
    def list_type(self, new_value):
       self.list_type = new_value

    @property
    def operator(self):
       return self.get("operator")

    @operator.setter
    def operator(self, new_value):
       self.operator = new_value

    @property
    def value(self):
       return self.get("value")

    @value.setter
    def value(self, new_value):
       self.value = new_value

    @property
    def host(self):
       return self.get("host")

    @host.setter
    def host(self, new_value):
       self.host = new_value

    @property
    def prefix(self):
       return self.get("prefix")

    @prefix.setter
    def prefix(self, new_value):
       self.prefix = new_value

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
            'condition_type': (str,),  # noqa: E501
            'methods': ([str],),  # noqa: E501
            'path_regex': (str,),  # noqa: E501
            'path_template': (TemplatePath,),  # noqa: E501
            'query_parameters': ([RuleQueryParameter],),  # noqa: E501
            'body': (RuleQueryBody,),  # noqa: E501
            'matchers': (RuleMatcherList,),  # noqa: E501
            'separate_query': (bool,),  # noqa: E501
            'prefix': (str,),  # noqa: E501
            'rule_type': (str,),  # noqa: E501
            'condition_list': ([RuleCondition],),  # noqa: E501
            'list_type': (str,),  # noqa: E501
            'operator': (str,),  # noqa: E501
            'value': ([str],),  # noqa: E501
            'host': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        lazy_import()
        val = {
            'CompoundRuleCondition': CompoundRuleCondition,
            'HostPrefixRuleCondition': HostPrefixRuleCondition,
            'HttpRuleCondition': HttpRuleCondition,
            'SourceISOCountryCodeCondition': SourceISOCountryCodeCondition,
            'compound_rule_condition': CompoundRuleCondition,
            'host_prefix_rule_condition': HostPrefixRuleCondition,
            'http_rule_condition': HttpRuleCondition,
            'source_iso_country_code_condition': SourceISOCountryCodeCondition,
        }
        if not val:
            return None
        return {'condition_type': val}


    attribute_map = {
        'condition_type': 'condition_type',  # noqa: E501
        'methods': 'methods',  # noqa: E501
        'path_regex': 'path_regex',  # noqa: E501
        'path_template': 'path_template',  # noqa: E501
        'query_parameters': 'query_parameters',  # noqa: E501
        'body': 'body',  # noqa: E501
        'matchers': 'matchers',  # noqa: E501
        'separate_query': 'separate_query',  # noqa: E501
        'prefix': 'prefix',  # noqa: E501
        'rule_type': 'rule_type',  # noqa: E501
        'condition_list': 'condition_list',  # noqa: E501
        'list_type': 'list_type',  # noqa: E501
        'operator': 'operator',  # noqa: E501
        'value': 'value',  # noqa: E501
        'host': 'host',  # noqa: E501
    }

    read_only_vars = {
    }

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """RuleConditionBase - a model defined in OpenAPI

        Keyword Args:
            condition_type (str): The discriminator for the condition
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
            methods ([str]): The HTTP methods to allow. If any of the listed methods are matched, then this portion of the rule matches. . [optional]  # noqa: E501
            path_regex (str): regex for HTTP path. Can be templatized with jinja2 using definitions collection.. [optional]  # noqa: E501
            path_template (TemplatePath): [optional]  # noqa: E501
            query_parameters ([RuleQueryParameter]): A set of constraints on the parameters specified in the query string.. [optional]  # noqa: E501
            body (RuleQueryBody): [optional]  # noqa: E501
            matchers (RuleMatcherList): [optional]  # noqa: E501
            separate_query (bool): Whether or not to include the query parameter in path operations such as regex matches. If `true`, then the query parameter will be treated as separate from the path. Otherwise, if the path constraints will evaluate all of the query parameters as part of the http path. For example, if a regex path constraint is `^/part1/part2$` and separate_query is true, then an input path of `/part1/part2?key=value` will pass. However, if separate_query is false, it will fail. If not present, defaults to false. . [optional]  # noqa: E501
            prefix (str): A case-sensitive, absolute prefix to match against. The prefix cannot contain a query string. . [optional]  # noqa: E501
            rule_type (str): Used to distinguish between different types of rule. [optional]  # noqa: E501
            condition_list ([RuleCondition]): The list of conditions whose truth determines the truth of the CompoundRuleCondition. How that the conditions' truth is combined depends on `list_type`. . [optional]  # noqa: E501
            list_type (str): How to combine the truth of the conditions in `condition_list` to determine the overall truth of the CompoundRuleCondition. - `cnf`: Conjunctive Normal Form. The conditions are combined using an AND operator. - `dnf`: Disjunctive Normal Form. The conditions are combined using an OR operator. . [optional]  # noqa: E501
            operator (str): How to evaluate the variable against the value. - `in`: set membership. Checks that variable is in value, assuming value is a list. - `not_in`: set anti-membership. Checks that variable is in value, assuming value is a list. . [optional]  # noqa: E501
            value ([str]): The set of country codes to check against. [optional]  # noqa: E501
            host (str): A case insensitive host or IP address, possibly including a port. Note that if the host is an empty string, then it s considered a trivial match. . [optional]  # noqa: E501
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

        constant_args = {
            '_check_type': _check_type,
            '_path_to_item': _path_to_item,
            '_spec_property_naming': _spec_property_naming,
            '_configuration': _configuration,
            '_visited_composed_classes': self._visited_composed_classes,
        }
        composed_info = validate_get_composed_info(
            constant_args, kwargs, self, from_openapi_data=True)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]
        discarded_args = composed_info[3]

        for var_name, var_value in kwargs.items():
            if var_name in discarded_args and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self._additional_properties_model_instances:
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
        '_composed_instances',
        '_var_name_to_model_instances',
        '_additional_properties_model_instances',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """RuleConditionBase - a model defined in OpenAPI

        Keyword Args:
            condition_type (str): The discriminator for the condition
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
            methods ([str]): The HTTP methods to allow. If any of the listed methods are matched, then this portion of the rule matches. . [optional]  # noqa: E501
            path_regex (str): regex for HTTP path. Can be templatized with jinja2 using definitions collection.. [optional]  # noqa: E501
            path_template (TemplatePath): [optional]  # noqa: E501
            query_parameters ([RuleQueryParameter]): A set of constraints on the parameters specified in the query string.. [optional]  # noqa: E501
            body (RuleQueryBody): [optional]  # noqa: E501
            matchers (RuleMatcherList): [optional]  # noqa: E501
            separate_query (bool): Whether or not to include the query parameter in path operations such as regex matches. If `true`, then the query parameter will be treated as separate from the path. Otherwise, if the path constraints will evaluate all of the query parameters as part of the http path. For example, if a regex path constraint is `^/part1/part2$` and separate_query is true, then an input path of `/part1/part2?key=value` will pass. However, if separate_query is false, it will fail. If not present, defaults to false. . [optional]  # noqa: E501
            prefix (str): A case-sensitive, absolute prefix to match against. The prefix cannot contain a query string. . [optional]  # noqa: E501
            rule_type (str): Used to distinguish between different types of rule. [optional]  # noqa: E501
            condition_list ([RuleCondition]): The list of conditions whose truth determines the truth of the CompoundRuleCondition. How that the conditions' truth is combined depends on `list_type`. . [optional]  # noqa: E501
            list_type (str): How to combine the truth of the conditions in `condition_list` to determine the overall truth of the CompoundRuleCondition. - `cnf`: Conjunctive Normal Form. The conditions are combined using an AND operator. - `dnf`: Disjunctive Normal Form. The conditions are combined using an OR operator. . [optional]  # noqa: E501
            operator (str): How to evaluate the variable against the value. - `in`: set membership. Checks that variable is in value, assuming value is a list. - `not_in`: set anti-membership. Checks that variable is in value, assuming value is a list. . [optional]  # noqa: E501
            value ([str]): The set of country codes to check against. [optional]  # noqa: E501
            host (str): A case insensitive host or IP address, possibly including a port. Note that if the host is an empty string, then it s considered a trivial match. . [optional]  # noqa: E501
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

        constant_args = {
            '_check_type': _check_type,
            '_path_to_item': _path_to_item,
            '_spec_property_naming': _spec_property_naming,
            '_configuration': _configuration,
            '_visited_composed_classes': self._visited_composed_classes,
        }
        composed_info = validate_get_composed_info(
            constant_args, kwargs, self)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]
        discarded_args = composed_info[3]

        for var_name, var_value in kwargs.items():
            if var_name in discarded_args and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self._additional_properties_model_instances:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")


    @cached_property
    def _composed_schemas():
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error beause the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        lazy_import()
        return {
          'anyOf': [
          ],
          'allOf': [
          ],
          'oneOf': [
              CompoundRuleCondition,
              HostPrefixRuleCondition,
              HttpRuleCondition,
              SourceISOCountryCodeCondition,
          ],
        }
