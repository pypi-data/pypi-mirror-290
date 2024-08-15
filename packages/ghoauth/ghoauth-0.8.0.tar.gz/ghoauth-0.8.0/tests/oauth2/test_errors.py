# -*- coding: utf-8 -*-
#
# Copyright 2017 Gehirn Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase

from webob import Response

from ghoauth.oauth2 import OAuth2Request
from ghoauth.oauth2.errors import (
    AccessDeniedError,
    ServerError,
)


class OAuth2ErrorTest(TestCase):

    def test_o2_use_redirect(self):
        request = OAuth2Request.blank(
            "https://example.com/authorization"
            "?state=csrftoken"
            "&redirect_uri=https%3A//rp.example.com/callback"
        )
        inst = AccessDeniedError(request)
        inst.o2_use_redirect()

        self.assertTrue(inst.o2_prepared)
        self.assertIsInstance(inst, Response)
        self.assertEqual(inst.status_code, 302)
        self.assertEqual(
            inst.location,
            "https://rp.example.com/callback"
            "?error=access_denied&state=csrftoken",
        )

    def test_o2_use_redirect_fragment(self):
        request = OAuth2Request.blank(
            "https://example.com/authorization"
            "?state=csrftoken"
            "&redirect_uri=https%3A//rp.example.com/callback"
            "&response_mode=fragment"
        )
        inst = AccessDeniedError(request)
        inst.o2_use_redirect()

        self.assertTrue(inst.o2_prepared)
        self.assertIsInstance(inst, Response)
        self.assertEqual(inst.status_code, 302)
        self.assertEqual(
            inst.location,
            "https://rp.example.com/callback"
            "#error=access_denied&state=csrftoken",
        )

    def test_o2_use_json(self):
        request = OAuth2Request.blank(
            "https://example.com/authorization"
            "?state=csrftoken"
            "&redirect_uri=https%3A//rp.example.com/callback"
        )
        inst = ServerError(request, "https://example.com/docs/")
        inst.o2_use_json()

        self.assertTrue(inst.o2_prepared)
        self.assertIsInstance(inst, Response)
        self.assertEqual(inst.status_code, 500)
        self.assertEqual(inst.content_type, "application/json")
        self.assertEqual(
            inst.json,
            {
                "error": "server_error",
                "error_uri": "https://example.com/docs/",
                "state": "csrftoken",
            },
        )
