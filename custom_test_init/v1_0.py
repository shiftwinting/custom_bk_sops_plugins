# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import logging
from django.utils.translation import ugettext_lazy as _

from pipeline.core.flow.activity import Service
from pipeline.component_framework.component import Component
from gcloud.conf import settings
from gcloud.utils.handlers import handle_api_error

logger = logging.getLogger('celery')
get_client_by_user = settings.ESB_GET_CLIENT_BY_USER

__group_name__ = _("配置平台(CMDB)")
VERSION = "v1.0"


class CustomTestInitService(Service):

    def inputs_format(self):
        return [
            self.InputItem(
                name=_("测试一下"),
                key="test_data",
                type="string",
                schema=StringItemSchema(description=_("测试一下")),
            )
        ]

    def outputs_format(self):
        return [
            self.OutputItem(
                name=_("获取数据"), key="ipstr", type="string", schema=StringItemSchema(description=_("获取数据"))
            )
        ]

    def execute(self, data, parent_data):
        executor = parent_data.get_one_of_inputs('executor')
        biz_cc_id = parent_data.inputs.biz_cc_id
        client = get_client_by_user(executor)

        data.set_outputs('ipstr', data.get_one_of_inputs("test_data", '无法获取'))
        return True


class CustomTestInitComponent(Component):
    name = _("[自定义]我是从远程来的")
	embedded_form = True
    code = "cc_custom_test_init"
    bound_service = CustomTestInitService
    # 表单定义
    form = """ 
    (function(){
        $.atoms.cc_custom_test_init = [
            {
                tag_code: "test_data",
                type: "input",
                attrs: {
                    name: gettext("测试一下"),
                    placeholder: gettext("请输入字符串"),
                    hookable: true,
                    validation: [
                        {
                            type: "required"
                        }
                    ]
                }
            }
        ]
    })();
    """
    version = VERSION
