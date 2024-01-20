# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from flywheel.api_client import ApiClient
import flywheel.models

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

class RolesApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_role(self, body, **kwargs):  # noqa: E501
        """Add a new role

        This method makes a synchronous HTTP request by default.

        :param RoleInput body: (required)
        :param bool async_: Perform the request asynchronously
        :return: RoleOutput
        """
        ignore_simplified_return_value = kwargs.pop('_ignore_simplified_return_value', False)
        kwargs['_return_http_data_only'] = True

        if kwargs.get('async_'):
            return self.add_role_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.add_role_with_http_info(body, **kwargs)  # noqa: E501
            if (
                data
                and hasattr(data, 'return_value')
                and not ignore_simplified_return_value
            ):
                return data.return_value()
            return data


    def add_role_with_http_info(self, body, **kwargs):  # noqa: E501
        """Add a new role

        This method makes a synchronous HTTP request by default.

        :param RoleInput body: (required)
        :param bool async: Perform the request asynchronously
        :return: RoleOutput
        """

        all_params = ['body',]  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_role" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `add_role`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            if 'RoleInput'.startswith('union'):
                body_type = type(params['body'])
                if getattr(body_type, 'positional_to_model', None):
                    body_params = body_type.positional_to_model(params['body'])
                else:
                    body_params = params['body']
            else:
                body_params = flywheel.models.RoleInput.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/roles', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RoleOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def delete_role(self, role_id, **kwargs):  # noqa: E501
        """Delete the role

        This method makes a synchronous HTTP request by default.

        :param str role_id: The ID of the role (required)
        :param bool async_: Perform the request asynchronously
        :return: None
        """
        ignore_simplified_return_value = kwargs.pop('_ignore_simplified_return_value', False)
        kwargs['_return_http_data_only'] = True

        if kwargs.get('async_'):
            return self.delete_role_with_http_info(role_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_role_with_http_info(role_id, **kwargs)  # noqa: E501
            if (
                data
                and hasattr(data, 'return_value')
                and not ignore_simplified_return_value
            ):
                return data.return_value()
            return data


    def delete_role_with_http_info(self, role_id, **kwargs):  # noqa: E501
        """Delete the role

        This method makes a synchronous HTTP request by default.

        :param str role_id: The ID of the role (required)
        :param bool async: Perform the request asynchronously
        :return: None
        """

        all_params = ['role_id',]  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_role" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'role_id' is set
        if ('role_id' not in params or
                params['role_id'] is None):
            raise ValueError("Missing the required parameter `role_id` when calling `delete_role`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'role_id' in params:
            path_params['role_id'] = params['role_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/roles/{role_id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_all_roles(self, **kwargs):  # noqa: E501
        """Get list of all roles

        This method makes a synchronous HTTP request by default.

        :param str filter: The filter to apply. (e.g. label=my-label,created>2018-09-22)
        :param str sort: The sort fields and order.(e.g. label:asc,created:desc)
        :param int limit: The maximum number of entries to return
        :param int skip: The number of entries to skip
        :param int page: The page number (i.e. skip limit*page entries)
        :param str after_id: Paginate after the given id. (Cannot be used with sort, page or skip)
        :param list[str] x_accept_feature:
        :param bool async_: Perform the request asynchronously
        :return: union[list[RoleOutput],Page]
        """
        ignore_simplified_return_value = kwargs.pop('_ignore_simplified_return_value', False)
        kwargs['_return_http_data_only'] = True

        if kwargs.get('async_'):
            return self.get_all_roles_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_roles_with_http_info(**kwargs)  # noqa: E501
            if (
                data
                and hasattr(data, 'return_value')
                and not ignore_simplified_return_value
            ):
                return data.return_value()
            return data


    def get_all_roles_with_http_info(self, **kwargs):  # noqa: E501
        """Get list of all roles

        This method makes a synchronous HTTP request by default.

        :param str filter: The filter to apply. (e.g. label=my-label,created>2018-09-22)
        :param str sort: The sort fields and order.(e.g. label:asc,created:desc)
        :param int limit: The maximum number of entries to return
        :param int skip: The number of entries to skip
        :param int page: The page number (i.e. skip limit*page entries)
        :param str after_id: Paginate after the given id. (Cannot be used with sort, page or skip)
        :param list[str] x_accept_feature:
        :param bool async: Perform the request asynchronously
        :return: union[list[RoleOutput],Page]
        """

        all_params = ['filter','sort','limit','skip','page','after_id','x_accept_feature',]  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_roles" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'skip' in params:
            query_params.append(('skip', params['skip']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'after_id' in params:
            query_params.append(('after_id', params['after_id']))  # noqa: E501

        header_params = {}
        if 'x_accept_feature' in params:
            header_params['x-accept-feature'] = params['x_accept_feature']  # noqa: E501
            collection_formats['x-accept-feature'] = ''  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/roles', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='union[list[RoleOutput],Page]',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def get_role(self, role_id, **kwargs):  # noqa: E501
        """Return the role identified by the RoleId

        This method makes a synchronous HTTP request by default.

        :param str role_id: The ID of the role (required)
        :param bool async_: Perform the request asynchronously
        :return: RoleOutput
        """
        ignore_simplified_return_value = kwargs.pop('_ignore_simplified_return_value', False)
        kwargs['_return_http_data_only'] = True

        if kwargs.get('async_'):
            return self.get_role_with_http_info(role_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_role_with_http_info(role_id, **kwargs)  # noqa: E501
            if (
                data
                and hasattr(data, 'return_value')
                and not ignore_simplified_return_value
            ):
                return data.return_value()
            return data


    def get_role_with_http_info(self, role_id, **kwargs):  # noqa: E501
        """Return the role identified by the RoleId

        This method makes a synchronous HTTP request by default.

        :param str role_id: The ID of the role (required)
        :param bool async: Perform the request asynchronously
        :return: RoleOutput
        """

        all_params = ['role_id',]  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_role" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'role_id' is set
        if ('role_id' not in params or
                params['role_id'] is None):
            raise ValueError("Missing the required parameter `role_id` when calling `get_role`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'role_id' in params:
            path_params['role_id'] = params['role_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/roles/{role_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RoleOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)

    def modify_role(self, role_id, body, **kwargs):  # noqa: E501
        """Update the role identified by RoleId

        This method makes a synchronous HTTP request by default.

        :param str role_id: (required)
        :param RoleUpdate body: (required)
        :param list[union[HeaderFeature,string]] x_accept_feature:
        :param bool async_: Perform the request asynchronously
        :return: RoleOutput
        """
        ignore_simplified_return_value = kwargs.pop('_ignore_simplified_return_value', False)
        kwargs['_return_http_data_only'] = True

        if kwargs.get('async_'):
            return self.modify_role_with_http_info(role_id, body, **kwargs)  # noqa: E501
        else:
            (data) = self.modify_role_with_http_info(role_id, body, **kwargs)  # noqa: E501
            if (
                data
                and hasattr(data, 'return_value')
                and not ignore_simplified_return_value
            ):
                return data.return_value()
            return data


    def modify_role_with_http_info(self, role_id, body, **kwargs):  # noqa: E501
        """Update the role identified by RoleId

        This method makes a synchronous HTTP request by default.

        :param str role_id: (required)
        :param RoleUpdate body: (required)
        :param list[union[HeaderFeature,string]] x_accept_feature:
        :param bool async: Perform the request asynchronously
        :return: RoleOutput
        """

        all_params = ['role_id','body','x_accept_feature',]  # noqa: E501
        all_params.append('async_')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_request_out')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method modify_role" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'role_id' is set
        if ('role_id' not in params or
                params['role_id'] is None):
            raise ValueError("Missing the required parameter `role_id` when calling `modify_role`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `modify_role`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'role_id' in params:
            path_params['role_id'] = params['role_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_accept_feature' in params:
            header_params['x-accept-feature'] = params['x_accept_feature']  # noqa: E501
            collection_formats['x-accept-feature'] = ''  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            if 'RoleUpdate'.startswith('union'):
                body_type = type(params['body'])
                if getattr(body_type, 'positional_to_model', None):
                    body_params = body_type.positional_to_model(params['body'])
                else:
                    body_params = params['body']
            else:
                body_params = flywheel.models.RoleUpdate.positional_to_model(params['body'])
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKey']  # noqa: E501

        return self.api_client.call_api(
            '/roles/{role_id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RoleOutput',  # noqa: E501
            auth_settings=auth_settings,
            async_=params.get('async_'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            _request_out=params.get('_request_out'),
            collection_formats=collection_formats)
