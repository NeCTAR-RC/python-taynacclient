#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import copy
from datetime import datetime
from requests import Response
import six

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


def getid(obj):
    """Get obj's id or object itself if no id
    Abstracts the common pattern of allowing both an object or
    an object's ID as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        return obj


class Manager(object):
    """Interacts with type of API
    Managers interact with a particular type of API (instances, types, etc.)
    and provide CRUD operations for them.
    """
    resource_class = None

    def __init__(self, api):
        self.api = api

    def _post(self, url, data, response_key=None, return_raw=False,
              headers=None):
        if headers is None:
            headers = {}
        headers["Content-Type"] = "application/json"
        resp, body = self.api.post(url, json=data, headers=headers)
        if return_raw:
            if response_key:
                body = body[response_key]
            return self.convert_into_with_meta(body, resp)
        # POST requests may not return a body
        if body:
            if response_key:
                return self.resource_class(self, body[response_key], resp=resp,
                                           loaded=True)
            return self.resource_class(self, body, resp=resp, loaded=True)
        else:
            return StrWithMeta(body, resp)


class RequestIdMixin(object):
    """Wrapper class to expose x-openstack-request-id to the caller."""
    def request_ids_setup(self):
        self.x_openstack_request_ids = []

    @property
    def request_ids(self):
        return self.x_openstack_request_ids

    def append_request_ids(self, resp):
        """Add request_ids as an attribute to the object
        :param resp: Response object or list of Response objects
        """
        if isinstance(resp, list):
            # Add list of request_ids if response is of type list.
            for resp_obj in resp:
                self._append_request_id(resp_obj)
        elif resp is not None:
            # Add request_ids if response contains single object.
            self._append_request_id(resp)

    def _append_request_id(self, resp):
        if isinstance(resp, Response):
            # Extract 'X-Openstack-Request-Id' from headers if
            # response is a Response object.
            request_id = (resp.headers.get('Openstack-Request-Id')
                          or resp.headers.get('x-openstack-request-id')
                          or resp.headers.get('x-compute-request-id'))
        else:
            # If resp is of type string or None.
            request_id = resp
        if request_id not in self.x_openstack_request_ids:
            self.x_openstack_request_ids.append(request_id)


class Resource(RequestIdMixin):
    """Represents an instance of an object
    A resource represents a particular instance of an object (instance, type,
    etc). This is pretty much just a bag for attributes.
    :param manager: BaseManager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    :param resp: Response or list of Response objects
    """

    date_fields = []

    def __init__(self, manager, info, loaded=False, resp=None):
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._loaded = loaded
        self.request_ids_setup()
        self.append_request_ids(resp)

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            if k in self.date_fields:
                try:
                    setattr(self, k, datetime.strptime(v, DATE_FORMAT))
                    continue
                except Exception:
                    # Couldn't pasrse date, fallback to string
                    pass
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute
                # on the class
                pass

    def __setstate__(self, d):
        for k, v in d.items():
            setattr(self, k, v)

    def __getattr__(self, k):
        if k not in self.__dict__:
            # NOTE(RuiChen): disallow lazy-loading if already loaded once
            if not self.is_loaded():
                self.get()
                return self.__getattr__(k)
            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys() if k[0] != '_'
                          and k not in ('manager', 'x_openstack_request_ids'))
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    def get(self):
        # set_loaded() first ... so if we have to bail, we know we tried.
        self.set_loaded(True)
        if not hasattr(self.manager, 'get'):
            return

        new = self.manager.get(self.id)
        if new:
            self._add_details(new._info)
            # The 'request_ids' attribute has been added,
            # so store the request id to it instead of _info
            self.append_request_ids(new.request_ids)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._info == other._info

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_loaded(self):
        return self._loaded

    def set_loaded(self, val):
        self._loaded = val

    def to_dict(self):
        return copy.deepcopy(self._info)


class StrWithMeta(str, RequestIdMixin):
    def __new__(cls, value, resp):
        return super(StrWithMeta, cls).__new__(cls, value)

    def __init__(self, values, resp):
        self.request_ids_setup()
        self.append_request_ids(resp)
