# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict, Any


class ProblemLevelGroupValue(TeaModel):
    def __init__(
        self,
        child_rule_relation: int = None,
        match_count: int = None,
        time_window: int = None,
        time_window_unit: str = None,
        enable_upgrade: bool = None,
        upgrade_time_window: int = None,
        upgrade_time_window_unit: str = None,
    ):
        self.child_rule_relation = child_rule_relation
        self.match_count = match_count
        self.time_window = time_window
        self.time_window_unit = time_window_unit
        self.enable_upgrade = enable_upgrade
        self.upgrade_time_window = upgrade_time_window
        self.upgrade_time_window_unit = upgrade_time_window_unit

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.child_rule_relation is not None:
            result['childRuleRelation'] = self.child_rule_relation
        if self.match_count is not None:
            result['matchCount'] = self.match_count
        if self.time_window is not None:
            result['timeWindow'] = self.time_window
        if self.time_window_unit is not None:
            result['timeWindowUnit'] = self.time_window_unit
        if self.enable_upgrade is not None:
            result['enableUpgrade'] = self.enable_upgrade
        if self.upgrade_time_window is not None:
            result['upgradeTimeWindow'] = self.upgrade_time_window
        if self.upgrade_time_window_unit is not None:
            result['upgradeTimeWindowUnit'] = self.upgrade_time_window_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('childRuleRelation') is not None:
            self.child_rule_relation = m.get('childRuleRelation')
        if m.get('matchCount') is not None:
            self.match_count = m.get('matchCount')
        if m.get('timeWindow') is not None:
            self.time_window = m.get('timeWindow')
        if m.get('timeWindowUnit') is not None:
            self.time_window_unit = m.get('timeWindowUnit')
        if m.get('enableUpgrade') is not None:
            self.enable_upgrade = m.get('enableUpgrade')
        if m.get('upgradeTimeWindow') is not None:
            self.upgrade_time_window = m.get('upgradeTimeWindow')
        if m.get('upgradeTimeWindowUnit') is not None:
            self.upgrade_time_window_unit = m.get('upgradeTimeWindowUnit')
        return self


class DataProblemLevelGroupValue(TeaModel):
    def __init__(
        self,
        child_rule_relation: int = None,
        match_count: int = None,
        time_window: int = None,
        time_window_unit: str = None,
        enable_upgrade: bool = None,
        upgrade_time_window: int = None,
        upgrade_time_window_unit: str = None,
    ):
        self.child_rule_relation = child_rule_relation
        self.match_count = match_count
        self.time_window = time_window
        self.time_window_unit = time_window_unit
        self.enable_upgrade = enable_upgrade
        self.upgrade_time_window = upgrade_time_window
        self.upgrade_time_window_unit = upgrade_time_window_unit

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.child_rule_relation is not None:
            result['childRuleRelation'] = self.child_rule_relation
        if self.match_count is not None:
            result['matchCount'] = self.match_count
        if self.time_window is not None:
            result['timeWindow'] = self.time_window
        if self.time_window_unit is not None:
            result['timeWindowUnit'] = self.time_window_unit
        if self.enable_upgrade is not None:
            result['enableUpgrade'] = self.enable_upgrade
        if self.upgrade_time_window is not None:
            result['upgradeTimeWindow'] = self.upgrade_time_window
        if self.upgrade_time_window_unit is not None:
            result['upgradeTimeWindowUnit'] = self.upgrade_time_window_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('childRuleRelation') is not None:
            self.child_rule_relation = m.get('childRuleRelation')
        if m.get('matchCount') is not None:
            self.match_count = m.get('matchCount')
        if m.get('timeWindow') is not None:
            self.time_window = m.get('timeWindow')
        if m.get('timeWindowUnit') is not None:
            self.time_window_unit = m.get('timeWindowUnit')
        if m.get('enableUpgrade') is not None:
            self.enable_upgrade = m.get('enableUpgrade')
        if m.get('upgradeTimeWindow') is not None:
            self.upgrade_time_window = m.get('upgradeTimeWindow')
        if m.get('upgradeTimeWindowUnit') is not None:
            self.upgrade_time_window_unit = m.get('upgradeTimeWindowUnit')
        return self


class DataValue(TeaModel):
    def __init__(
        self,
        code: str = None,
        description: str = None,
        config_description: str = None,
        config_code: str = None,
        parent_code: str = None,
        config_key: str = None,
        config_value: str = None,
        requirement: bool = None,
    ):
        self.code = code
        self.description = description
        self.config_description = config_description
        self.config_code = config_code
        self.parent_code = parent_code
        self.config_key = config_key
        self.config_value = config_value
        self.requirement = requirement

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['code'] = self.code
        if self.description is not None:
            result['description'] = self.description
        if self.config_description is not None:
            result['configDescription'] = self.config_description
        if self.config_code is not None:
            result['configCode'] = self.config_code
        if self.parent_code is not None:
            result['parentCode'] = self.parent_code
        if self.config_key is not None:
            result['configKey'] = self.config_key
        if self.config_value is not None:
            result['configValue'] = self.config_value
        if self.requirement is not None:
            result['requirement'] = self.requirement
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('code') is not None:
            self.code = m.get('code')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('configDescription') is not None:
            self.config_description = m.get('configDescription')
        if m.get('configCode') is not None:
            self.config_code = m.get('configCode')
        if m.get('parentCode') is not None:
            self.parent_code = m.get('parentCode')
        if m.get('configKey') is not None:
            self.config_key = m.get('configKey')
        if m.get('configValue') is not None:
            self.config_value = m.get('configValue')
        if m.get('requirement') is not None:
            self.requirement = m.get('requirement')
        return self


class AddProblemServiceGroupRequest(TeaModel):
    def __init__(
        self,
        problem_id: int = None,
        service_group_ids: List[int] = None,
    ):
        self.problem_id = problem_id
        self.service_group_ids = service_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.service_group_ids is not None:
            result['serviceGroupIds'] = self.service_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('serviceGroupIds') is not None:
            self.service_group_ids = m.get('serviceGroupIds')
        return self


class AddProblemServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class AddProblemServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: AddProblemServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AddProblemServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BillingStatisticsResponseBodyData(TeaModel):
    def __init__(
        self,
        app_user_count: int = None,
        app_user_count_free: int = None,
        email_send: int = None,
        email_send_free: int = None,
        escalation_plan_count: int = None,
        escalation_plan_count_free: int = None,
        event_report_api: int = None,
        event_report_api_free: int = None,
        has_schedule_service_group_count: int = None,
        has_schedule_service_group_count_free: int = None,
        im_msg_send: int = None,
        im_msg_send_free: int = None,
        rule_count: int = None,
        rule_count_free: int = None,
        sms_send: int = None,
        sms_send_free: int = None,
        subscription_notify_count: int = None,
        subscription_notify_count_free: int = None,
        type: bool = None,
        voice_send: int = None,
        voice_send_free: int = None,
    ):
        self.app_user_count = app_user_count
        self.app_user_count_free = app_user_count_free
        self.email_send = email_send
        self.email_send_free = email_send_free
        self.escalation_plan_count = escalation_plan_count
        self.escalation_plan_count_free = escalation_plan_count_free
        self.event_report_api = event_report_api
        self.event_report_api_free = event_report_api_free
        self.has_schedule_service_group_count = has_schedule_service_group_count
        self.has_schedule_service_group_count_free = has_schedule_service_group_count_free
        self.im_msg_send = im_msg_send
        self.im_msg_send_free = im_msg_send_free
        self.rule_count = rule_count
        self.rule_count_free = rule_count_free
        self.sms_send = sms_send
        self.sms_send_free = sms_send_free
        self.subscription_notify_count = subscription_notify_count
        self.subscription_notify_count_free = subscription_notify_count_free
        self.type = type
        self.voice_send = voice_send
        self.voice_send_free = voice_send_free

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.app_user_count is not None:
            result['appUserCount'] = self.app_user_count
        if self.app_user_count_free is not None:
            result['appUserCountFree'] = self.app_user_count_free
        if self.email_send is not None:
            result['emailSend'] = self.email_send
        if self.email_send_free is not None:
            result['emailSendFree'] = self.email_send_free
        if self.escalation_plan_count is not None:
            result['escalationPlanCount'] = self.escalation_plan_count
        if self.escalation_plan_count_free is not None:
            result['escalationPlanCountFree'] = self.escalation_plan_count_free
        if self.event_report_api is not None:
            result['eventReportApi'] = self.event_report_api
        if self.event_report_api_free is not None:
            result['eventReportApiFree'] = self.event_report_api_free
        if self.has_schedule_service_group_count is not None:
            result['hasScheduleServiceGroupCount'] = self.has_schedule_service_group_count
        if self.has_schedule_service_group_count_free is not None:
            result['hasScheduleServiceGroupCountFree'] = self.has_schedule_service_group_count_free
        if self.im_msg_send is not None:
            result['imMsgSend'] = self.im_msg_send
        if self.im_msg_send_free is not None:
            result['imMsgSendFree'] = self.im_msg_send_free
        if self.rule_count is not None:
            result['ruleCount'] = self.rule_count
        if self.rule_count_free is not None:
            result['ruleCountFree'] = self.rule_count_free
        if self.sms_send is not None:
            result['smsSend'] = self.sms_send
        if self.sms_send_free is not None:
            result['smsSendFree'] = self.sms_send_free
        if self.subscription_notify_count is not None:
            result['subscriptionNotifyCount'] = self.subscription_notify_count
        if self.subscription_notify_count_free is not None:
            result['subscriptionNotifyCountFree'] = self.subscription_notify_count_free
        if self.type is not None:
            result['type'] = self.type
        if self.voice_send is not None:
            result['voiceSend'] = self.voice_send
        if self.voice_send_free is not None:
            result['voiceSendFree'] = self.voice_send_free
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('appUserCount') is not None:
            self.app_user_count = m.get('appUserCount')
        if m.get('appUserCountFree') is not None:
            self.app_user_count_free = m.get('appUserCountFree')
        if m.get('emailSend') is not None:
            self.email_send = m.get('emailSend')
        if m.get('emailSendFree') is not None:
            self.email_send_free = m.get('emailSendFree')
        if m.get('escalationPlanCount') is not None:
            self.escalation_plan_count = m.get('escalationPlanCount')
        if m.get('escalationPlanCountFree') is not None:
            self.escalation_plan_count_free = m.get('escalationPlanCountFree')
        if m.get('eventReportApi') is not None:
            self.event_report_api = m.get('eventReportApi')
        if m.get('eventReportApiFree') is not None:
            self.event_report_api_free = m.get('eventReportApiFree')
        if m.get('hasScheduleServiceGroupCount') is not None:
            self.has_schedule_service_group_count = m.get('hasScheduleServiceGroupCount')
        if m.get('hasScheduleServiceGroupCountFree') is not None:
            self.has_schedule_service_group_count_free = m.get('hasScheduleServiceGroupCountFree')
        if m.get('imMsgSend') is not None:
            self.im_msg_send = m.get('imMsgSend')
        if m.get('imMsgSendFree') is not None:
            self.im_msg_send_free = m.get('imMsgSendFree')
        if m.get('ruleCount') is not None:
            self.rule_count = m.get('ruleCount')
        if m.get('ruleCountFree') is not None:
            self.rule_count_free = m.get('ruleCountFree')
        if m.get('smsSend') is not None:
            self.sms_send = m.get('smsSend')
        if m.get('smsSendFree') is not None:
            self.sms_send_free = m.get('smsSendFree')
        if m.get('subscriptionNotifyCount') is not None:
            self.subscription_notify_count = m.get('subscriptionNotifyCount')
        if m.get('subscriptionNotifyCountFree') is not None:
            self.subscription_notify_count_free = m.get('subscriptionNotifyCountFree')
        if m.get('type') is not None:
            self.type = m.get('type')
        if m.get('voiceSend') is not None:
            self.voice_send = m.get('voiceSend')
        if m.get('voiceSendFree') is not None:
            self.voice_send_free = m.get('voiceSendFree')
        return self


class BillingStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: BillingStatisticsResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('data') is not None:
            temp_model = BillingStatisticsResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        return self


class BillingStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: BillingStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = BillingStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CancelProblemRequest(TeaModel):
    def __init__(
        self,
        cancel_reason: int = None,
        cancel_reason_description: str = None,
        client_token: str = None,
        problem_id: int = None,
        problem_notify_type: int = None,
    ):
        self.cancel_reason = cancel_reason
        self.cancel_reason_description = cancel_reason_description
        self.client_token = client_token
        self.problem_id = problem_id
        self.problem_notify_type = problem_notify_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cancel_reason is not None:
            result['cancelReason'] = self.cancel_reason
        if self.cancel_reason_description is not None:
            result['cancelReasonDescription'] = self.cancel_reason_description
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('cancelReason') is not None:
            self.cancel_reason = m.get('cancelReason')
        if m.get('cancelReasonDescription') is not None:
            self.cancel_reason_description = m.get('cancelReasonDescription')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        return self


class CancelProblemResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CancelProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CancelProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CancelProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CheckWebhookRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        webhook: str = None,
        webhook_type: str = None,
    ):
        self.client_token = client_token
        self.webhook = webhook
        self.webhook_type = webhook_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.webhook is not None:
            result['webhook'] = self.webhook
        if self.webhook_type is not None:
            result['webhookType'] = self.webhook_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('webhook') is not None:
            self.webhook = m.get('webhook')
        if m.get('webhookType') is not None:
            self.webhook_type = m.get('webhookType')
        return self


class CheckWebhookResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CheckWebhookResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CheckWebhookResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CheckWebhookResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ConfirmIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class ConfirmIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ConfirmIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ConfirmIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ConfirmIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateEscalationPlanRequestEscalationPlanRulesEscalationPlanConditions(TeaModel):
    def __init__(
        self,
        effection: str = None,
        level: str = None,
    ):
        # This parameter is required.
        self.effection = effection
        # This parameter is required.
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.effection is not None:
            result['effection'] = self.effection
        if self.level is not None:
            result['level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('level') is not None:
            self.level = m.get('level')
        return self


class CreateEscalationPlanRequestEscalationPlanRulesEscalationPlanStrategies(TeaModel):
    def __init__(
        self,
        enable_webhook: bool = None,
        escalation_plan_type: str = None,
        notice_channels: List[str] = None,
        notice_objects: List[int] = None,
        notice_role_list: List[int] = None,
        notice_time: str = None,
        service_group_ids: List[int] = None,
    ):
        # This parameter is required.
        self.enable_webhook = enable_webhook
        self.escalation_plan_type = escalation_plan_type
        # This parameter is required.
        self.notice_channels = notice_channels
        # This parameter is required.
        self.notice_objects = notice_objects
        self.notice_role_list = notice_role_list
        # This parameter is required.
        self.notice_time = notice_time
        self.service_group_ids = service_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_webhook is not None:
            result['enableWebhook'] = self.enable_webhook
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        if self.notice_channels is not None:
            result['noticeChannels'] = self.notice_channels
        if self.notice_objects is not None:
            result['noticeObjects'] = self.notice_objects
        if self.notice_role_list is not None:
            result['noticeRoleList'] = self.notice_role_list
        if self.notice_time is not None:
            result['noticeTime'] = self.notice_time
        if self.service_group_ids is not None:
            result['serviceGroupIds'] = self.service_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('enableWebhook') is not None:
            self.enable_webhook = m.get('enableWebhook')
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        if m.get('noticeChannels') is not None:
            self.notice_channels = m.get('noticeChannels')
        if m.get('noticeObjects') is not None:
            self.notice_objects = m.get('noticeObjects')
        if m.get('noticeRoleList') is not None:
            self.notice_role_list = m.get('noticeRoleList')
        if m.get('noticeTime') is not None:
            self.notice_time = m.get('noticeTime')
        if m.get('serviceGroupIds') is not None:
            self.service_group_ids = m.get('serviceGroupIds')
        return self


class CreateEscalationPlanRequestEscalationPlanRules(TeaModel):
    def __init__(
        self,
        escalation_plan_conditions: List[CreateEscalationPlanRequestEscalationPlanRulesEscalationPlanConditions] = None,
        escalation_plan_strategies: List[CreateEscalationPlanRequestEscalationPlanRulesEscalationPlanStrategies] = None,
        escalation_plan_type: str = None,
    ):
        # This parameter is required.
        self.escalation_plan_conditions = escalation_plan_conditions
        # This parameter is required.
        self.escalation_plan_strategies = escalation_plan_strategies
        self.escalation_plan_type = escalation_plan_type

    def validate(self):
        if self.escalation_plan_conditions:
            for k in self.escalation_plan_conditions:
                if k:
                    k.validate()
        if self.escalation_plan_strategies:
            for k in self.escalation_plan_strategies:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['escalationPlanConditions'] = []
        if self.escalation_plan_conditions is not None:
            for k in self.escalation_plan_conditions:
                result['escalationPlanConditions'].append(k.to_map() if k else None)
        result['escalationPlanStrategies'] = []
        if self.escalation_plan_strategies is not None:
            for k in self.escalation_plan_strategies:
                result['escalationPlanStrategies'].append(k.to_map() if k else None)
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.escalation_plan_conditions = []
        if m.get('escalationPlanConditions') is not None:
            for k in m.get('escalationPlanConditions'):
                temp_model = CreateEscalationPlanRequestEscalationPlanRulesEscalationPlanConditions()
                self.escalation_plan_conditions.append(temp_model.from_map(k))
        self.escalation_plan_strategies = []
        if m.get('escalationPlanStrategies') is not None:
            for k in m.get('escalationPlanStrategies'):
                temp_model = CreateEscalationPlanRequestEscalationPlanRulesEscalationPlanStrategies()
                self.escalation_plan_strategies.append(temp_model.from_map(k))
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        return self


class CreateEscalationPlanRequestEscalationPlanScopeObjects(TeaModel):
    def __init__(
        self,
        scope: str = None,
        scope_object_id: int = None,
    ):
        self.scope = scope
        # This parameter is required.
        self.scope_object_id = scope_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        return self


class CreateEscalationPlanRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_description: str = None,
        escalation_plan_name: str = None,
        escalation_plan_rules: List[CreateEscalationPlanRequestEscalationPlanRules] = None,
        escalation_plan_scope_objects: List[CreateEscalationPlanRequestEscalationPlanScopeObjects] = None,
        is_global: bool = None,
    ):
        # clientToken
        self.client_token = client_token
        # This parameter is required.
        self.escalation_plan_description = escalation_plan_description
        # This parameter is required.
        self.escalation_plan_name = escalation_plan_name
        # This parameter is required.
        self.escalation_plan_rules = escalation_plan_rules
        # This parameter is required.
        self.escalation_plan_scope_objects = escalation_plan_scope_objects
        self.is_global = is_global

    def validate(self):
        if self.escalation_plan_rules:
            for k in self.escalation_plan_rules:
                if k:
                    k.validate()
        if self.escalation_plan_scope_objects:
            for k in self.escalation_plan_scope_objects:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_description is not None:
            result['escalationPlanDescription'] = self.escalation_plan_description
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        result['escalationPlanRules'] = []
        if self.escalation_plan_rules is not None:
            for k in self.escalation_plan_rules:
                result['escalationPlanRules'].append(k.to_map() if k else None)
        result['escalationPlanScopeObjects'] = []
        if self.escalation_plan_scope_objects is not None:
            for k in self.escalation_plan_scope_objects:
                result['escalationPlanScopeObjects'].append(k.to_map() if k else None)
        if self.is_global is not None:
            result['isGlobal'] = self.is_global
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanDescription') is not None:
            self.escalation_plan_description = m.get('escalationPlanDescription')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        self.escalation_plan_rules = []
        if m.get('escalationPlanRules') is not None:
            for k in m.get('escalationPlanRules'):
                temp_model = CreateEscalationPlanRequestEscalationPlanRules()
                self.escalation_plan_rules.append(temp_model.from_map(k))
        self.escalation_plan_scope_objects = []
        if m.get('escalationPlanScopeObjects') is not None:
            for k in m.get('escalationPlanScopeObjects'):
                temp_model = CreateEscalationPlanRequestEscalationPlanScopeObjects()
                self.escalation_plan_scope_objects.append(temp_model.from_map(k))
        if m.get('isGlobal') is not None:
            self.is_global = m.get('isGlobal')
        return self


class CreateEscalationPlanResponseBodyData(TeaModel):
    def __init__(
        self,
        escalation_plan_id: int = None,
    ):
        self.escalation_plan_id = escalation_plan_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        return self


class CreateEscalationPlanResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateEscalationPlanResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateEscalationPlanResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateEscalationPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateEscalationPlanResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateEscalationPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateIncidentRequest(TeaModel):
    def __init__(
        self,
        assign_user_id: int = None,
        channels: List[str] = None,
        client_token: str = None,
        effect: str = None,
        incident_description: str = None,
        incident_level: str = None,
        incident_title: str = None,
        related_service_id: int = None,
        service_group_id: int = None,
    ):
        self.assign_user_id = assign_user_id
        self.channels = channels
        self.client_token = client_token
        self.effect = effect
        self.incident_description = incident_description
        self.incident_level = incident_level
        self.incident_title = incident_title
        self.related_service_id = related_service_id
        # 12000
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_user_id is not None:
            result['assignUserId'] = self.assign_user_id
        if self.channels is not None:
            result['channels'] = self.channels
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.effect is not None:
            result['effect'] = self.effect
        if self.incident_description is not None:
            result['incidentDescription'] = self.incident_description
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignUserId') is not None:
            self.assign_user_id = m.get('assignUserId')
        if m.get('channels') is not None:
            self.channels = m.get('channels')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('effect') is not None:
            self.effect = m.get('effect')
        if m.get('incidentDescription') is not None:
            self.incident_description = m.get('incidentDescription')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class CreateIncidentResponseBodyData(TeaModel):
    def __init__(
        self,
        incident_id: int = None,
    ):
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class CreateIncidentResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateIncidentResponseBodyData = None,
        request_id: str = None,
    ):
        # Id of the request
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateIncidentResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateIncidentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateIncidentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateIncidentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateIncidentSubtotalRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        description: str = None,
        incident_id: int = None,
    ):
        self.client_token = client_token
        self.description = description
        # This parameter is required.
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.description is not None:
            result['description'] = self.description
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class CreateIncidentSubtotalResponseBodyData(TeaModel):
    def __init__(
        self,
        subtotal_id: int = None,
    ):
        self.subtotal_id = subtotal_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.subtotal_id is not None:
            result['subtotalId'] = self.subtotal_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('subtotalId') is not None:
            self.subtotal_id = m.get('subtotalId')
        return self


class CreateIncidentSubtotalResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateIncidentSubtotalResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateIncidentSubtotalResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateIncidentSubtotalResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateIncidentSubtotalResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateIncidentSubtotalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        monitor_source_id: int = None,
    ):
        self.client_token = client_token
        self.monitor_source_id = monitor_source_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        return self


class CreateIntegrationConfigResponseBodyData(TeaModel):
    def __init__(
        self,
        integration_config_id: int = None,
    ):
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class CreateIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateIntegrationConfigResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateIntegrationConfigResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateProblemRequest(TeaModel):
    def __init__(
        self,
        affect_service_ids: List[int] = None,
        client_token: str = None,
        discover_time: str = None,
        incident_id: int = None,
        main_handler_id: int = None,
        preliminary_reason: str = None,
        problem_level: str = None,
        problem_name: str = None,
        problem_notify_type: str = None,
        problem_status: str = None,
        progress_summary: str = None,
        progress_summary_rich_text_id: int = None,
        recovery_time: str = None,
        related_service_id: int = None,
        service_group_ids: List[int] = None,
    ):
        self.affect_service_ids = affect_service_ids
        self.client_token = client_token
        self.discover_time = discover_time
        self.incident_id = incident_id
        self.main_handler_id = main_handler_id
        self.preliminary_reason = preliminary_reason
        self.problem_level = problem_level
        self.problem_name = problem_name
        self.problem_notify_type = problem_notify_type
        self.problem_status = problem_status
        self.progress_summary = progress_summary
        self.progress_summary_rich_text_id = progress_summary_rich_text_id
        self.recovery_time = recovery_time
        self.related_service_id = related_service_id
        self.service_group_ids = service_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.affect_service_ids is not None:
            result['affectServiceIds'] = self.affect_service_ids
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.discover_time is not None:
            result['discoverTime'] = self.discover_time
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.main_handler_id is not None:
            result['mainHandlerId'] = self.main_handler_id
        if self.preliminary_reason is not None:
            result['preliminaryReason'] = self.preliminary_reason
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        if self.problem_name is not None:
            result['problemName'] = self.problem_name
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        if self.problem_status is not None:
            result['problemStatus'] = self.problem_status
        if self.progress_summary is not None:
            result['progressSummary'] = self.progress_summary
        if self.progress_summary_rich_text_id is not None:
            result['progressSummaryRichTextId'] = self.progress_summary_rich_text_id
        if self.recovery_time is not None:
            result['recoveryTime'] = self.recovery_time
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.service_group_ids is not None:
            result['serviceGroupIds'] = self.service_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('affectServiceIds') is not None:
            self.affect_service_ids = m.get('affectServiceIds')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('discoverTime') is not None:
            self.discover_time = m.get('discoverTime')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('mainHandlerId') is not None:
            self.main_handler_id = m.get('mainHandlerId')
        if m.get('preliminaryReason') is not None:
            self.preliminary_reason = m.get('preliminaryReason')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        if m.get('problemName') is not None:
            self.problem_name = m.get('problemName')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        if m.get('problemStatus') is not None:
            self.problem_status = m.get('problemStatus')
        if m.get('progressSummary') is not None:
            self.progress_summary = m.get('progressSummary')
        if m.get('progressSummaryRichTextId') is not None:
            self.progress_summary_rich_text_id = m.get('progressSummaryRichTextId')
        if m.get('recoveryTime') is not None:
            self.recovery_time = m.get('recoveryTime')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('serviceGroupIds') is not None:
            self.service_group_ids = m.get('serviceGroupIds')
        return self


class CreateProblemResponseBodyData(TeaModel):
    def __init__(
        self,
        problem_id: int = None,
    ):
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class CreateProblemResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateProblemResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateProblemResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateProblemEffectionServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        description: str = None,
        level: str = None,
        picture_url: List[str] = None,
        problem_id: int = None,
        service_id: int = None,
        status: str = None,
    ):
        # clientToken
        self.client_token = client_token
        self.description = description
        self.level = level
        self.picture_url = picture_url
        # This parameter is required.
        self.problem_id = problem_id
        self.service_id = service_id
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.description is not None:
            result['description'] = self.description
        if self.level is not None:
            result['level'] = self.level
        if self.picture_url is not None:
            result['pictureUrl'] = self.picture_url
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('level') is not None:
            self.level = m.get('level')
        if m.get('pictureUrl') is not None:
            self.picture_url = m.get('pictureUrl')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class CreateProblemEffectionServiceResponseBodyData(TeaModel):
    def __init__(
        self,
        effection_service_id: int = None,
    ):
        self.effection_service_id = effection_service_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.effection_service_id is not None:
            result['effectionServiceId'] = self.effection_service_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('effectionServiceId') is not None:
            self.effection_service_id = m.get('effectionServiceId')
        return self


class CreateProblemEffectionServiceResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateProblemEffectionServiceResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateProblemEffectionServiceResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateProblemEffectionServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateProblemEffectionServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateProblemEffectionServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateProblemMeasureRequest(TeaModel):
    def __init__(
        self,
        check_standard: str = None,
        check_user_id: int = None,
        client_token: str = None,
        content: str = None,
        director_id: int = None,
        plan_finish_time: str = None,
        problem_id: int = None,
        stalker_id: int = None,
        status: str = None,
        type: int = None,
    ):
        self.check_standard = check_standard
        self.check_user_id = check_user_id
        self.client_token = client_token
        self.content = content
        self.director_id = director_id
        self.plan_finish_time = plan_finish_time
        # This parameter is required.
        self.problem_id = problem_id
        self.stalker_id = stalker_id
        self.status = status
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.check_standard is not None:
            result['checkStandard'] = self.check_standard
        if self.check_user_id is not None:
            result['checkUserId'] = self.check_user_id
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.content is not None:
            result['content'] = self.content
        if self.director_id is not None:
            result['directorId'] = self.director_id
        if self.plan_finish_time is not None:
            result['planFinishTime'] = self.plan_finish_time
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.stalker_id is not None:
            result['stalkerId'] = self.stalker_id
        if self.status is not None:
            result['status'] = self.status
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('checkStandard') is not None:
            self.check_standard = m.get('checkStandard')
        if m.get('checkUserId') is not None:
            self.check_user_id = m.get('checkUserId')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('directorId') is not None:
            self.director_id = m.get('directorId')
        if m.get('planFinishTime') is not None:
            self.plan_finish_time = m.get('planFinishTime')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('stalkerId') is not None:
            self.stalker_id = m.get('stalkerId')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class CreateProblemMeasureResponseBodyData(TeaModel):
    def __init__(
        self,
        measure_id: int = None,
    ):
        self.measure_id = measure_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.measure_id is not None:
            result['measureId'] = self.measure_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('measureId') is not None:
            self.measure_id = m.get('measureId')
        return self


class CreateProblemMeasureResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateProblemMeasureResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateProblemMeasureResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateProblemMeasureResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateProblemMeasureResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateProblemMeasureResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateProblemSubtotalRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        description: str = None,
        problem_id: int = None,
    ):
        self.client_token = client_token
        self.description = description
        # This parameter is required.
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.description is not None:
            result['description'] = self.description
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class CreateProblemSubtotalResponseBodyData(TeaModel):
    def __init__(
        self,
        subtotal_id: int = None,
    ):
        self.subtotal_id = subtotal_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.subtotal_id is not None:
            result['subtotalId'] = self.subtotal_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('subtotalId') is not None:
            self.subtotal_id = m.get('subtotalId')
        return self


class CreateProblemSubtotalResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateProblemSubtotalResponseBodyData = None,
        request_id: str = None,
    ):
        # object
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateProblemSubtotalResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateProblemSubtotalResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateProblemSubtotalResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateProblemSubtotalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateProblemTimelineRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        content: str = None,
        key_node: str = None,
        problem_id: int = None,
        time: str = None,
    ):
        self.client_token = client_token
        self.content = content
        self.key_node = key_node
        # This parameter is required.
        self.problem_id = problem_id
        self.time = time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.content is not None:
            result['content'] = self.content
        if self.key_node is not None:
            result['keyNode'] = self.key_node
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.time is not None:
            result['time'] = self.time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('keyNode') is not None:
            self.key_node = m.get('keyNode')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('time') is not None:
            self.time = m.get('time')
        return self


class CreateProblemTimelineResponseBodyData(TeaModel):
    def __init__(
        self,
        problem_timeline_id: int = None,
    ):
        self.problem_timeline_id = problem_timeline_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.problem_timeline_id is not None:
            result['problemTimelineId'] = self.problem_timeline_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('problemTimelineId') is not None:
            self.problem_timeline_id = m.get('problemTimelineId')
        return self


class CreateProblemTimelineResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateProblemTimelineResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateProblemTimelineResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateProblemTimelineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateProblemTimelineResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateProblemTimelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateProblemTimelinesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
        timeline_nodes: str = None,
    ):
        # clientToken
        self.client_token = client_token
        # This parameter is required.
        self.problem_id = problem_id
        self.timeline_nodes = timeline_nodes

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.timeline_nodes is not None:
            result['timelineNodes'] = self.timeline_nodes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('timelineNodes') is not None:
            self.timeline_nodes = m.get('timelineNodes')
        return self


class CreateProblemTimelinesResponseBodyData(TeaModel):
    def __init__(
        self,
        problem_timeline_ids: List[int] = None,
    ):
        self.problem_timeline_ids = problem_timeline_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.problem_timeline_ids is not None:
            result['problemTimelineIds'] = self.problem_timeline_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('problemTimelineIds') is not None:
            self.problem_timeline_ids = m.get('problemTimelineIds')
        return self


class CreateProblemTimelinesResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateProblemTimelinesResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateProblemTimelinesResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateProblemTimelinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateProblemTimelinesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateProblemTimelinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateRichTextRequest(TeaModel):
    def __init__(
        self,
        instance_id: int = None,
        instance_type: str = None,
        rich_text: str = None,
    ):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.rich_text = rich_text

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.rich_text is not None:
            result['richText'] = self.rich_text
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('richText') is not None:
            self.rich_text = m.get('richText')
        return self


class CreateRichTextResponseBodyData(TeaModel):
    def __init__(
        self,
        instance_id: int = None,
        instance_type: int = None,
        rich_text: str = None,
    ):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.rich_text = rich_text

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.rich_text is not None:
            result['richText'] = self.rich_text
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('richText') is not None:
            self.rich_text = m.get('richText')
        return self


class CreateRichTextResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateRichTextResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateRichTextResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateRichTextResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateRichTextResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateRichTextResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateRouteRuleRequestRouteChildRulesConditions(TeaModel):
    def __init__(
        self,
        key: str = None,
        operation_symbol: str = None,
        value: str = None,
    ):
        # This parameter is required.
        self.key = key
        # This parameter is required.
        self.operation_symbol = operation_symbol
        # This parameter is required.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.operation_symbol is not None:
            result['operationSymbol'] = self.operation_symbol
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('operationSymbol') is not None:
            self.operation_symbol = m.get('operationSymbol')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class CreateRouteRuleRequestRouteChildRules(TeaModel):
    def __init__(
        self,
        child_condition_relation: int = None,
        conditions: List[CreateRouteRuleRequestRouteChildRulesConditions] = None,
        monitor_source_id: int = None,
        problem_level: str = None,
    ):
        self.child_condition_relation = child_condition_relation
        # This parameter is required.
        self.conditions = conditions
        # This parameter is required.
        self.monitor_source_id = monitor_source_id
        self.problem_level = problem_level

    def validate(self):
        if self.conditions:
            for k in self.conditions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.child_condition_relation is not None:
            result['childConditionRelation'] = self.child_condition_relation
        result['conditions'] = []
        if self.conditions is not None:
            for k in self.conditions:
                result['conditions'].append(k.to_map() if k else None)
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('childConditionRelation') is not None:
            self.child_condition_relation = m.get('childConditionRelation')
        self.conditions = []
        if m.get('conditions') is not None:
            for k in m.get('conditions'):
                temp_model = CreateRouteRuleRequestRouteChildRulesConditions()
                self.conditions.append(temp_model.from_map(k))
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        return self


class CreateRouteRuleRequest(TeaModel):
    def __init__(
        self,
        assign_object_id: int = None,
        assign_object_type: str = None,
        child_rule_relation: str = None,
        client_token: str = None,
        convergence_fields: List[str] = None,
        convergence_type: int = None,
        coverage_problem_levels: List[str] = None,
        effection: str = None,
        enable_status: str = None,
        incident_level: str = None,
        match_count: int = None,
        notify_channels: List[str] = None,
        problem_effection_services: List[int] = None,
        problem_level_group: Dict[str, ProblemLevelGroupValue] = None,
        related_service_id: int = None,
        route_child_rules: List[CreateRouteRuleRequestRouteChildRules] = None,
        route_type: str = None,
        rule_name: str = None,
        time_window: int = None,
        time_window_unit: str = None,
    ):
        # This parameter is required.
        self.assign_object_id = assign_object_id
        # This parameter is required.
        self.assign_object_type = assign_object_type
        # This parameter is required.
        self.child_rule_relation = child_rule_relation
        self.client_token = client_token
        self.convergence_fields = convergence_fields
        self.convergence_type = convergence_type
        self.coverage_problem_levels = coverage_problem_levels
        # This parameter is required.
        self.effection = effection
        self.enable_status = enable_status
        # This parameter is required.
        self.incident_level = incident_level
        # This parameter is required.
        self.match_count = match_count
        # This parameter is required.
        self.notify_channels = notify_channels
        self.problem_effection_services = problem_effection_services
        self.problem_level_group = problem_level_group
        # This parameter is required.
        self.related_service_id = related_service_id
        # This parameter is required.
        self.route_child_rules = route_child_rules
        # This parameter is required.
        self.route_type = route_type
        # This parameter is required.
        self.rule_name = rule_name
        # This parameter is required.
        self.time_window = time_window
        # This parameter is required.
        self.time_window_unit = time_window_unit

    def validate(self):
        if self.problem_level_group:
            for v in self.problem_level_group.values():
                if v:
                    v.validate()
        if self.route_child_rules:
            for k in self.route_child_rules:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_object_id is not None:
            result['assignObjectId'] = self.assign_object_id
        if self.assign_object_type is not None:
            result['assignObjectType'] = self.assign_object_type
        if self.child_rule_relation is not None:
            result['childRuleRelation'] = self.child_rule_relation
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.convergence_fields is not None:
            result['convergenceFields'] = self.convergence_fields
        if self.convergence_type is not None:
            result['convergenceType'] = self.convergence_type
        if self.coverage_problem_levels is not None:
            result['coverageProblemLevels'] = self.coverage_problem_levels
        if self.effection is not None:
            result['effection'] = self.effection
        if self.enable_status is not None:
            result['enableStatus'] = self.enable_status
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.match_count is not None:
            result['matchCount'] = self.match_count
        if self.notify_channels is not None:
            result['notifyChannels'] = self.notify_channels
        if self.problem_effection_services is not None:
            result['problemEffectionServices'] = self.problem_effection_services
        result['problemLevelGroup'] = {}
        if self.problem_level_group is not None:
            for k, v in self.problem_level_group.items():
                result['problemLevelGroup'][k] = v.to_map()
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        result['routeChildRules'] = []
        if self.route_child_rules is not None:
            for k in self.route_child_rules:
                result['routeChildRules'].append(k.to_map() if k else None)
        if self.route_type is not None:
            result['routeType'] = self.route_type
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        if self.time_window is not None:
            result['timeWindow'] = self.time_window
        if self.time_window_unit is not None:
            result['timeWindowUnit'] = self.time_window_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignObjectId') is not None:
            self.assign_object_id = m.get('assignObjectId')
        if m.get('assignObjectType') is not None:
            self.assign_object_type = m.get('assignObjectType')
        if m.get('childRuleRelation') is not None:
            self.child_rule_relation = m.get('childRuleRelation')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('convergenceFields') is not None:
            self.convergence_fields = m.get('convergenceFields')
        if m.get('convergenceType') is not None:
            self.convergence_type = m.get('convergenceType')
        if m.get('coverageProblemLevels') is not None:
            self.coverage_problem_levels = m.get('coverageProblemLevels')
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('enableStatus') is not None:
            self.enable_status = m.get('enableStatus')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('matchCount') is not None:
            self.match_count = m.get('matchCount')
        if m.get('notifyChannels') is not None:
            self.notify_channels = m.get('notifyChannels')
        if m.get('problemEffectionServices') is not None:
            self.problem_effection_services = m.get('problemEffectionServices')
        self.problem_level_group = {}
        if m.get('problemLevelGroup') is not None:
            for k, v in m.get('problemLevelGroup').items():
                temp_model = ProblemLevelGroupValue()
                self.problem_level_group[k] = temp_model.from_map(v)
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        self.route_child_rules = []
        if m.get('routeChildRules') is not None:
            for k in m.get('routeChildRules'):
                temp_model = CreateRouteRuleRequestRouteChildRules()
                self.route_child_rules.append(temp_model.from_map(k))
        if m.get('routeType') is not None:
            self.route_type = m.get('routeType')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        if m.get('timeWindow') is not None:
            self.time_window = m.get('timeWindow')
        if m.get('timeWindowUnit') is not None:
            self.time_window_unit = m.get('timeWindowUnit')
        return self


class CreateRouteRuleResponseBodyData(TeaModel):
    def __init__(
        self,
        route_rule_id: int = None,
    ):
        self.route_rule_id = route_rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        return self


class CreateRouteRuleResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateRouteRuleResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateRouteRuleResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateRouteRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateRouteRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateRouteRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_id: int = None,
        service_description: str = None,
        service_group_id_list: List[int] = None,
        service_name: str = None,
    ):
        self.client_token = client_token
        self.escalation_plan_id = escalation_plan_id
        self.service_description = service_description
        self.service_group_id_list = service_group_id_list
        # This parameter is required.
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.service_description is not None:
            result['serviceDescription'] = self.service_description
        if self.service_group_id_list is not None:
            result['serviceGroupIdList'] = self.service_group_id_list
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('serviceDescription') is not None:
            self.service_description = m.get('serviceDescription')
        if m.get('serviceGroupIdList') is not None:
            self.service_group_id_list = m.get('serviceGroupIdList')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class CreateServiceResponseBodyData(TeaModel):
    def __init__(
        self,
        service_id: int = None,
    ):
        self.service_id = service_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        return self


class CreateServiceResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateServiceResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateServiceResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateServiceGroupRequestMonitorSourceTemplates(TeaModel):
    def __init__(
        self,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
        template_content: str = None,
        template_id: int = None,
    ):
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name
        self.template_content = template_content
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.template_content is not None:
            result['templateContent'] = self.template_content
        if self.template_id is not None:
            result['templateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('templateContent') is not None:
            self.template_content = m.get('templateContent')
        if m.get('templateId') is not None:
            self.template_id = m.get('templateId')
        return self


class CreateServiceGroupRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        enable_webhook: str = None,
        monitor_source_templates: List[CreateServiceGroupRequestMonitorSourceTemplates] = None,
        service_group_description: str = None,
        service_group_name: str = None,
        user_ids: List[int] = None,
        webhook_link: str = None,
        webhook_type: str = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.enable_webhook = enable_webhook
        self.monitor_source_templates = monitor_source_templates
        self.service_group_description = service_group_description
        # This parameter is required.
        self.service_group_name = service_group_name
        # This parameter is required.
        self.user_ids = user_ids
        # webhooklink
        # 
        # This parameter is required.
        self.webhook_link = webhook_link
        # This parameter is required.
        self.webhook_type = webhook_type

    def validate(self):
        if self.monitor_source_templates:
            for k in self.monitor_source_templates:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.enable_webhook is not None:
            result['enableWebhook'] = self.enable_webhook
        result['monitorSourceTemplates'] = []
        if self.monitor_source_templates is not None:
            for k in self.monitor_source_templates:
                result['monitorSourceTemplates'].append(k.to_map() if k else None)
        if self.service_group_description is not None:
            result['serviceGroupDescription'] = self.service_group_description
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        if self.user_ids is not None:
            result['userIds'] = self.user_ids
        if self.webhook_link is not None:
            result['webhookLink'] = self.webhook_link
        if self.webhook_type is not None:
            result['webhookType'] = self.webhook_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('enableWebhook') is not None:
            self.enable_webhook = m.get('enableWebhook')
        self.monitor_source_templates = []
        if m.get('monitorSourceTemplates') is not None:
            for k in m.get('monitorSourceTemplates'):
                temp_model = CreateServiceGroupRequestMonitorSourceTemplates()
                self.monitor_source_templates.append(temp_model.from_map(k))
        if m.get('serviceGroupDescription') is not None:
            self.service_group_description = m.get('serviceGroupDescription')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        if m.get('userIds') is not None:
            self.user_ids = m.get('userIds')
        if m.get('webhookLink') is not None:
            self.webhook_link = m.get('webhookLink')
        if m.get('webhookType') is not None:
            self.webhook_type = m.get('webhookType')
        return self


class CreateServiceGroupResponseBodyData(TeaModel):
    def __init__(
        self,
        service_group_id: int = None,
    ):
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class CreateServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateServiceGroupResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateServiceGroupResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateServiceGroupSchedulingRequestFastSchedulingSchedulingUsers(TeaModel):
    def __init__(
        self,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
    ):
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        return self


class CreateServiceGroupSchedulingRequestFastScheduling(TeaModel):
    def __init__(
        self,
        duty_plan: str = None,
        scheduling_users: List[CreateServiceGroupSchedulingRequestFastSchedulingSchedulingUsers] = None,
        single_duration: int = None,
        single_duration_unit: str = None,
    ):
        self.duty_plan = duty_plan
        self.scheduling_users = scheduling_users
        self.single_duration = single_duration
        self.single_duration_unit = single_duration_unit

    def validate(self):
        if self.scheduling_users:
            for k in self.scheduling_users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.duty_plan is not None:
            result['dutyPlan'] = self.duty_plan
        result['schedulingUsers'] = []
        if self.scheduling_users is not None:
            for k in self.scheduling_users:
                result['schedulingUsers'].append(k.to_map() if k else None)
        if self.single_duration is not None:
            result['singleDuration'] = self.single_duration
        if self.single_duration_unit is not None:
            result['singleDurationUnit'] = self.single_duration_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dutyPlan') is not None:
            self.duty_plan = m.get('dutyPlan')
        self.scheduling_users = []
        if m.get('schedulingUsers') is not None:
            for k in m.get('schedulingUsers'):
                temp_model = CreateServiceGroupSchedulingRequestFastSchedulingSchedulingUsers()
                self.scheduling_users.append(temp_model.from_map(k))
        if m.get('singleDuration') is not None:
            self.single_duration = m.get('singleDuration')
        if m.get('singleDurationUnit') is not None:
            self.single_duration_unit = m.get('singleDurationUnit')
        return self


class CreateServiceGroupSchedulingRequestFineSchedulingSchedulingFineShifts(TeaModel):
    def __init__(
        self,
        cycle_order: int = None,
        scheduling_end_time: str = None,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
        shift_name: str = None,
        skip_one_day: bool = None,
    ):
        self.cycle_order = cycle_order
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_start_time = scheduling_start_time
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list
        self.shift_name = shift_name
        self.skip_one_day = skip_one_day

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cycle_order is not None:
            result['cycleOrder'] = self.cycle_order
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        if self.shift_name is not None:
            result['shiftName'] = self.shift_name
        if self.skip_one_day is not None:
            result['skipOneDay'] = self.skip_one_day
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('cycleOrder') is not None:
            self.cycle_order = m.get('cycleOrder')
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        if m.get('shiftName') is not None:
            self.shift_name = m.get('shiftName')
        if m.get('skipOneDay') is not None:
            self.skip_one_day = m.get('skipOneDay')
        return self


class CreateServiceGroupSchedulingRequestFineSchedulingSchedulingTemplateFineShifts(TeaModel):
    def __init__(
        self,
        scheduling_end_time: str = None,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
        scheduling_user_name: str = None,
        skip_one_day: bool = None,
    ):
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_start_time = scheduling_start_time
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list
        self.scheduling_user_name = scheduling_user_name
        self.skip_one_day = skip_one_day

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        if self.scheduling_user_name is not None:
            result['schedulingUserName'] = self.scheduling_user_name
        if self.skip_one_day is not None:
            result['skipOneDay'] = self.skip_one_day
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        if m.get('schedulingUserName') is not None:
            self.scheduling_user_name = m.get('schedulingUserName')
        if m.get('skipOneDay') is not None:
            self.skip_one_day = m.get('skipOneDay')
        return self


class CreateServiceGroupSchedulingRequestFineScheduling(TeaModel):
    def __init__(
        self,
        period: int = None,
        period_unit: str = None,
        scheduling_fine_shifts: List[CreateServiceGroupSchedulingRequestFineSchedulingSchedulingFineShifts] = None,
        scheduling_template_fine_shifts: List[CreateServiceGroupSchedulingRequestFineSchedulingSchedulingTemplateFineShifts] = None,
        shift_type: str = None,
    ):
        self.period = period
        self.period_unit = period_unit
        self.scheduling_fine_shifts = scheduling_fine_shifts
        self.scheduling_template_fine_shifts = scheduling_template_fine_shifts
        self.shift_type = shift_type

    def validate(self):
        if self.scheduling_fine_shifts:
            for k in self.scheduling_fine_shifts:
                if k:
                    k.validate()
        if self.scheduling_template_fine_shifts:
            for k in self.scheduling_template_fine_shifts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.period is not None:
            result['period'] = self.period
        if self.period_unit is not None:
            result['periodUnit'] = self.period_unit
        result['schedulingFineShifts'] = []
        if self.scheduling_fine_shifts is not None:
            for k in self.scheduling_fine_shifts:
                result['schedulingFineShifts'].append(k.to_map() if k else None)
        result['schedulingTemplateFineShifts'] = []
        if self.scheduling_template_fine_shifts is not None:
            for k in self.scheduling_template_fine_shifts:
                result['schedulingTemplateFineShifts'].append(k.to_map() if k else None)
        if self.shift_type is not None:
            result['shiftType'] = self.shift_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('period') is not None:
            self.period = m.get('period')
        if m.get('periodUnit') is not None:
            self.period_unit = m.get('periodUnit')
        self.scheduling_fine_shifts = []
        if m.get('schedulingFineShifts') is not None:
            for k in m.get('schedulingFineShifts'):
                temp_model = CreateServiceGroupSchedulingRequestFineSchedulingSchedulingFineShifts()
                self.scheduling_fine_shifts.append(temp_model.from_map(k))
        self.scheduling_template_fine_shifts = []
        if m.get('schedulingTemplateFineShifts') is not None:
            for k in m.get('schedulingTemplateFineShifts'):
                temp_model = CreateServiceGroupSchedulingRequestFineSchedulingSchedulingTemplateFineShifts()
                self.scheduling_template_fine_shifts.append(temp_model.from_map(k))
        if m.get('shiftType') is not None:
            self.shift_type = m.get('shiftType')
        return self


class CreateServiceGroupSchedulingRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        fast_scheduling: CreateServiceGroupSchedulingRequestFastScheduling = None,
        fine_scheduling: CreateServiceGroupSchedulingRequestFineScheduling = None,
        scheduling_way: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.fast_scheduling = fast_scheduling
        self.fine_scheduling = fine_scheduling
        # This parameter is required.
        self.scheduling_way = scheduling_way
        # This parameter is required.
        self.service_group_id = service_group_id

    def validate(self):
        if self.fast_scheduling:
            self.fast_scheduling.validate()
        if self.fine_scheduling:
            self.fine_scheduling.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.fast_scheduling is not None:
            result['fastScheduling'] = self.fast_scheduling.to_map()
        if self.fine_scheduling is not None:
            result['fineScheduling'] = self.fine_scheduling.to_map()
        if self.scheduling_way is not None:
            result['schedulingWay'] = self.scheduling_way
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('fastScheduling') is not None:
            temp_model = CreateServiceGroupSchedulingRequestFastScheduling()
            self.fast_scheduling = temp_model.from_map(m['fastScheduling'])
        if m.get('fineScheduling') is not None:
            temp_model = CreateServiceGroupSchedulingRequestFineScheduling()
            self.fine_scheduling = temp_model.from_map(m['fineScheduling'])
        if m.get('schedulingWay') is not None:
            self.scheduling_way = m.get('schedulingWay')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class CreateServiceGroupSchedulingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateServiceGroupSchedulingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateServiceGroupSchedulingResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateServiceGroupSchedulingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateSubscriptionRequestNotifyObjectList(TeaModel):
    def __init__(
        self,
        notify_object_id: int = None,
    ):
        # This parameter is required.
        self.notify_object_id = notify_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.notify_object_id is not None:
            result['notifyObjectId'] = self.notify_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('notifyObjectId') is not None:
            self.notify_object_id = m.get('notifyObjectId')
        return self


class CreateSubscriptionRequestNotifyStrategyListPeriodChannel(TeaModel):
    def __init__(
        self,
        non_workday: str = None,
        workday: str = None,
    ):
        self.non_workday = non_workday
        self.workday = workday

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.non_workday is not None:
            result['nonWorkday'] = self.non_workday
        if self.workday is not None:
            result['workday'] = self.workday
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('nonWorkday') is not None:
            self.non_workday = m.get('nonWorkday')
        if m.get('workday') is not None:
            self.workday = m.get('workday')
        return self


class CreateSubscriptionRequestNotifyStrategyListStrategiesConditions(TeaModel):
    def __init__(
        self,
        action: str = None,
        effection: str = None,
        level: str = None,
        problem_notify_type: str = None,
    ):
        self.action = action
        self.effection = effection
        self.level = level
        self.problem_notify_type = problem_notify_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['action'] = self.action
        if self.effection is not None:
            result['effection'] = self.effection
        if self.level is not None:
            result['level'] = self.level
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('action') is not None:
            self.action = m.get('action')
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('level') is not None:
            self.level = m.get('level')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        return self


class CreateSubscriptionRequestNotifyStrategyListStrategies(TeaModel):
    def __init__(
        self,
        conditions: List[CreateSubscriptionRequestNotifyStrategyListStrategiesConditions] = None,
    ):
        self.conditions = conditions

    def validate(self):
        if self.conditions:
            for k in self.conditions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['conditions'] = []
        if self.conditions is not None:
            for k in self.conditions:
                result['conditions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.conditions = []
        if m.get('conditions') is not None:
            for k in m.get('conditions'):
                temp_model = CreateSubscriptionRequestNotifyStrategyListStrategiesConditions()
                self.conditions.append(temp_model.from_map(k))
        return self


class CreateSubscriptionRequestNotifyStrategyList(TeaModel):
    def __init__(
        self,
        channels: str = None,
        instance_type: int = None,
        period_channel: CreateSubscriptionRequestNotifyStrategyListPeriodChannel = None,
        strategies: List[CreateSubscriptionRequestNotifyStrategyListStrategies] = None,
    ):
        # This parameter is required.
        self.channels = channels
        # This parameter is required.
        self.instance_type = instance_type
        self.period_channel = period_channel
        # This parameter is required.
        self.strategies = strategies

    def validate(self):
        if self.period_channel:
            self.period_channel.validate()
        if self.strategies:
            for k in self.strategies:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channels is not None:
            result['channels'] = self.channels
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.period_channel is not None:
            result['periodChannel'] = self.period_channel.to_map()
        result['strategies'] = []
        if self.strategies is not None:
            for k in self.strategies:
                result['strategies'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('channels') is not None:
            self.channels = m.get('channels')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('periodChannel') is not None:
            temp_model = CreateSubscriptionRequestNotifyStrategyListPeriodChannel()
            self.period_channel = temp_model.from_map(m['periodChannel'])
        self.strategies = []
        if m.get('strategies') is not None:
            for k in m.get('strategies'):
                temp_model = CreateSubscriptionRequestNotifyStrategyListStrategies()
                self.strategies.append(temp_model.from_map(k))
        return self


class CreateSubscriptionRequestScopeObjectList(TeaModel):
    def __init__(
        self,
        scope_object_id: int = None,
    ):
        # This parameter is required.
        self.scope_object_id = scope_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        return self


class CreateSubscriptionRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        end_time: str = None,
        expired_type: int = None,
        notify_object_list: List[CreateSubscriptionRequestNotifyObjectList] = None,
        notify_object_type: int = None,
        notify_strategy_list: List[CreateSubscriptionRequestNotifyStrategyList] = None,
        period: str = None,
        scope: int = None,
        scope_object_list: List[CreateSubscriptionRequestScopeObjectList] = None,
        start_time: str = None,
        subscription_title: str = None,
    ):
        self.client_token = client_token
        self.end_time = end_time
        # This parameter is required.
        self.expired_type = expired_type
        # This parameter is required.
        self.notify_object_list = notify_object_list
        # This parameter is required.
        self.notify_object_type = notify_object_type
        # This parameter is required.
        self.notify_strategy_list = notify_strategy_list
        self.period = period
        # This parameter is required.
        self.scope = scope
        # This parameter is required.
        self.scope_object_list = scope_object_list
        self.start_time = start_time
        # This parameter is required.
        self.subscription_title = subscription_title

    def validate(self):
        if self.notify_object_list:
            for k in self.notify_object_list:
                if k:
                    k.validate()
        if self.notify_strategy_list:
            for k in self.notify_strategy_list:
                if k:
                    k.validate()
        if self.scope_object_list:
            for k in self.scope_object_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.expired_type is not None:
            result['expiredType'] = self.expired_type
        result['notifyObjectList'] = []
        if self.notify_object_list is not None:
            for k in self.notify_object_list:
                result['notifyObjectList'].append(k.to_map() if k else None)
        if self.notify_object_type is not None:
            result['notifyObjectType'] = self.notify_object_type
        result['notifyStrategyList'] = []
        if self.notify_strategy_list is not None:
            for k in self.notify_strategy_list:
                result['notifyStrategyList'].append(k.to_map() if k else None)
        if self.period is not None:
            result['period'] = self.period
        if self.scope is not None:
            result['scope'] = self.scope
        result['scopeObjectList'] = []
        if self.scope_object_list is not None:
            for k in self.scope_object_list:
                result['scopeObjectList'].append(k.to_map() if k else None)
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.subscription_title is not None:
            result['subscriptionTitle'] = self.subscription_title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('expiredType') is not None:
            self.expired_type = m.get('expiredType')
        self.notify_object_list = []
        if m.get('notifyObjectList') is not None:
            for k in m.get('notifyObjectList'):
                temp_model = CreateSubscriptionRequestNotifyObjectList()
                self.notify_object_list.append(temp_model.from_map(k))
        if m.get('notifyObjectType') is not None:
            self.notify_object_type = m.get('notifyObjectType')
        self.notify_strategy_list = []
        if m.get('notifyStrategyList') is not None:
            for k in m.get('notifyStrategyList'):
                temp_model = CreateSubscriptionRequestNotifyStrategyList()
                self.notify_strategy_list.append(temp_model.from_map(k))
        if m.get('period') is not None:
            self.period = m.get('period')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        self.scope_object_list = []
        if m.get('scopeObjectList') is not None:
            for k in m.get('scopeObjectList'):
                temp_model = CreateSubscriptionRequestScopeObjectList()
                self.scope_object_list.append(temp_model.from_map(k))
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('subscriptionTitle') is not None:
            self.subscription_title = m.get('subscriptionTitle')
        return self


class CreateSubscriptionResponseBodyData(TeaModel):
    def __init__(
        self,
        subscription_id: int = None,
    ):
        self.subscription_id = subscription_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        return self


class CreateSubscriptionResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateSubscriptionResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # request id
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateSubscriptionResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateSubscriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateSubscriptionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateSubscriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateTenantApplicationRequest(TeaModel):
    def __init__(
        self,
        channel: str = None,
        client_token: str = None,
    ):
        # This parameter is required.
        self.channel = channel
        # This parameter is required.
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channel is not None:
            result['channel'] = self.channel
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('channel') is not None:
            self.channel = m.get('channel')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class CreateTenantApplicationResponseBodyData(TeaModel):
    def __init__(
        self,
        open_url: str = None,
        progress: str = None,
    ):
        self.open_url = open_url
        self.progress = progress

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.open_url is not None:
            result['openUrl'] = self.open_url
        if self.progress is not None:
            result['progress'] = self.progress
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('openUrl') is not None:
            self.open_url = m.get('openUrl')
        if m.get('progress') is not None:
            self.progress = m.get('progress')
        return self


class CreateTenantApplicationResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateTenantApplicationResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the req
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateTenantApplicationResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateTenantApplicationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateTenantApplicationResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateTenantApplicationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateUserRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        email: str = None,
        phone: str = None,
        ram_id: int = None,
        role_id_list: List[int] = None,
        username: str = None,
    ):
        self.client_token = client_token
        self.email = email
        self.phone = phone
        self.ram_id = ram_id
        self.role_id_list = role_id_list
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.email is not None:
            result['email'] = self.email
        if self.phone is not None:
            result['phone'] = self.phone
        if self.ram_id is not None:
            result['ramId'] = self.ram_id
        if self.role_id_list is not None:
            result['roleIdList'] = self.role_id_list
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('email') is not None:
            self.email = m.get('email')
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('ramId') is not None:
            self.ram_id = m.get('ramId')
        if m.get('roleIdList') is not None:
            self.role_id_list = m.get('roleIdList')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class CreateUserResponseBodyData(TeaModel):
    def __init__(
        self,
        user_id: int = None,
    ):
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class CreateUserResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateUserResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = CreateUserResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class CreateUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteEscalationPlanRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.escalation_plan_id = escalation_plan_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        return self


class DeleteEscalationPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteEscalationPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteEscalationPlanResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteEscalationPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteIncidentRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_id: int = None,
    ):
        self.client_token = client_token
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class DeleteIncidentResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteIncidentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteIncidentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteIncidentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class DeleteIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteProblemRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class DeleteProblemResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteProblemEffectionServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        effection_service_id: int = None,
        problem_id: int = None,
    ):
        # clientToken
        self.client_token = client_token
        self.effection_service_id = effection_service_id
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.effection_service_id is not None:
            result['effectionServiceId'] = self.effection_service_id
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('effectionServiceId') is not None:
            self.effection_service_id = m.get('effectionServiceId')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class DeleteProblemEffectionServiceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteProblemEffectionServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteProblemEffectionServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteProblemEffectionServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteProblemMeasureRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        measure_id: int = None,
        problem_id: str = None,
    ):
        self.client_token = client_token
        self.measure_id = measure_id
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.measure_id is not None:
            result['measureId'] = self.measure_id
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('measureId') is not None:
            self.measure_id = m.get('measureId')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class DeleteProblemMeasureResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteProblemMeasureResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteProblemMeasureResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteProblemMeasureResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteProblemTimelineRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
        problem_timeline_id: int = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id
        self.problem_timeline_id = problem_timeline_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_timeline_id is not None:
            result['problemTimelineId'] = self.problem_timeline_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemTimelineId') is not None:
            self.problem_timeline_id = m.get('problemTimelineId')
        return self


class DeleteProblemTimelineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteProblemTimelineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteProblemTimelineResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteProblemTimelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteRouteRuleRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        route_rule_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.route_rule_id = route_rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        return self


class DeleteRouteRuleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: int = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteRouteRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteRouteRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteRouteRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_id: int = None,
    ):
        self.client_token = client_token
        self.service_id = service_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        return self


class DeleteServiceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteServiceGroupRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class DeleteServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteServiceGroupSchedulingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteServiceGroupSchedulingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteServiceGroupSchedulingResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteServiceGroupSchedulingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteServiceGroupUserRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        new_user_id: int = None,
        old_user_id: int = None,
        remove_user: bool = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.new_user_id = new_user_id
        self.old_user_id = old_user_id
        self.remove_user = remove_user
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.new_user_id is not None:
            result['newUserId'] = self.new_user_id
        if self.old_user_id is not None:
            result['oldUserId'] = self.old_user_id
        if self.remove_user is not None:
            result['removeUser'] = self.remove_user
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('newUserId') is not None:
            self.new_user_id = m.get('newUserId')
        if m.get('oldUserId') is not None:
            self.old_user_id = m.get('oldUserId')
        if m.get('removeUser') is not None:
            self.remove_user = m.get('removeUser')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class DeleteServiceGroupUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteServiceGroupUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteServiceGroupUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteServiceGroupUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteSubscriptionRequest(TeaModel):
    def __init__(
        self,
        subscription_id: int = None,
    ):
        self.subscription_id = subscription_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        return self


class DeleteSubscriptionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteSubscriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteSubscriptionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteSubscriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteUserRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        user_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class DeleteUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeleteUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeliverIncidentRequest(TeaModel):
    def __init__(
        self,
        assign_user_id: int = None,
        client_token: str = None,
        incident_id: int = None,
    ):
        self.assign_user_id = assign_user_id
        self.client_token = client_token
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_user_id is not None:
            result['assignUserId'] = self.assign_user_id
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignUserId') is not None:
            self.assign_user_id = m.get('assignUserId')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class DeliverIncidentResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DeliverIncidentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeliverIncidentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeliverIncidentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableEscalationPlanRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.escalation_plan_id = escalation_plan_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        return self


class DisableEscalationPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DisableEscalationPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DisableEscalationPlanResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DisableEscalationPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class DisableIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DisableIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DisableIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DisableIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableRouteRuleRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        route_rule_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.route_rule_id = route_rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        return self


class DisableRouteRuleResponseBody(TeaModel):
    def __init__(
        self,
        data: int = None,
        request_id: str = None,
    ):
        # C4BE3837-1A13-413B-A225-2C88188E8A43
        self.data = data
        # This parameter is required.
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DisableRouteRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DisableRouteRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DisableRouteRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableServiceGroupWebhookRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class DisableServiceGroupWebhookResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DisableServiceGroupWebhookResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DisableServiceGroupWebhookResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DisableServiceGroupWebhookResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableSubscriptionRequest(TeaModel):
    def __init__(
        self,
        subscription_id: int = None,
    ):
        self.subscription_id = subscription_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        return self


class DisableSubscriptionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class DisableSubscriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DisableSubscriptionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DisableSubscriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableEscalationPlanRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.escalation_plan_id = escalation_plan_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        return self


class EnableEscalationPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class EnableEscalationPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: EnableEscalationPlanResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = EnableEscalationPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class EnableIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class EnableIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: EnableIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = EnableIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableRouteRuleRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        route_rule_id: int = None,
    ):
        # This parameter is required.
        self.client_token = client_token
        # This parameter is required.
        self.route_rule_id = route_rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        return self


class EnableRouteRuleResponseBody(TeaModel):
    def __init__(
        self,
        data: int = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class EnableRouteRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: EnableRouteRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = EnableRouteRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableServiceGroupWebhookRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class EnableServiceGroupWebhookResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class EnableServiceGroupWebhookResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: EnableServiceGroupWebhookResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = EnableServiceGroupWebhookResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableSubscriptionRequest(TeaModel):
    def __init__(
        self,
        subscription_id: int = None,
    ):
        self.subscription_id = subscription_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        return self


class EnableSubscriptionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class EnableSubscriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: EnableSubscriptionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = EnableSubscriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class FinishIncidentRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_finish_reason: int = None,
        incident_finish_reason_description: str = None,
        incident_finish_solution: int = None,
        incident_finish_solution_description: str = None,
        incident_ids: List[int] = None,
    ):
        self.client_token = client_token
        self.incident_finish_reason = incident_finish_reason
        self.incident_finish_reason_description = incident_finish_reason_description
        self.incident_finish_solution = incident_finish_solution
        self.incident_finish_solution_description = incident_finish_solution_description
        # This parameter is required.
        self.incident_ids = incident_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_finish_reason is not None:
            result['incidentFinishReason'] = self.incident_finish_reason
        if self.incident_finish_reason_description is not None:
            result['incidentFinishReasonDescription'] = self.incident_finish_reason_description
        if self.incident_finish_solution is not None:
            result['incidentFinishSolution'] = self.incident_finish_solution
        if self.incident_finish_solution_description is not None:
            result['incidentFinishSolutionDescription'] = self.incident_finish_solution_description
        if self.incident_ids is not None:
            result['incidentIds'] = self.incident_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentFinishReason') is not None:
            self.incident_finish_reason = m.get('incidentFinishReason')
        if m.get('incidentFinishReasonDescription') is not None:
            self.incident_finish_reason_description = m.get('incidentFinishReasonDescription')
        if m.get('incidentFinishSolution') is not None:
            self.incident_finish_solution = m.get('incidentFinishSolution')
        if m.get('incidentFinishSolutionDescription') is not None:
            self.incident_finish_solution_description = m.get('incidentFinishSolutionDescription')
        if m.get('incidentIds') is not None:
            self.incident_ids = m.get('incidentIds')
        return self


class FinishIncidentResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class FinishIncidentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: FinishIncidentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = FinishIncidentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class FinishProblemRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class FinishProblemResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class FinishProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: FinishProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = FinishProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GeneratePictureLinkRequest(TeaModel):
    def __init__(
        self,
        keys: List[str] = None,
        problem_id: int = None,
    ):
        # keys
        self.keys = keys
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.keys is not None:
            result['keys'] = self.keys
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('keys') is not None:
            self.keys = m.get('keys')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class GeneratePictureLinkResponseBodyDataLinks(TeaModel):
    def __init__(
        self,
        key: str = None,
        link: str = None,
    ):
        # oss key
        self.key = key
        # url
        self.link = link

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.link is not None:
            result['link'] = self.link
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('link') is not None:
            self.link = m.get('link')
        return self


class GeneratePictureLinkResponseBodyData(TeaModel):
    def __init__(
        self,
        links: List[GeneratePictureLinkResponseBodyDataLinks] = None,
    ):
        # array
        self.links = links

    def validate(self):
        if self.links:
            for k in self.links:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['links'] = []
        if self.links is not None:
            for k in self.links:
                result['links'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.links = []
        if m.get('links') is not None:
            for k in m.get('links'):
                temp_model = GeneratePictureLinkResponseBodyDataLinks()
                self.links.append(temp_model.from_map(k))
        return self


class GeneratePictureLinkResponseBody(TeaModel):
    def __init__(
        self,
        data: GeneratePictureLinkResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GeneratePictureLinkResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GeneratePictureLinkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GeneratePictureLinkResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GeneratePictureLinkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GeneratePictureUploadSignRequestFiles(TeaModel):
    def __init__(
        self,
        file_name: str = None,
        file_size: int = None,
        file_type: str = None,
    ):
        self.file_name = file_name
        self.file_size = file_size
        self.file_type = file_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.file_name is not None:
            result['fileName'] = self.file_name
        if self.file_size is not None:
            result['fileSize'] = self.file_size
        if self.file_type is not None:
            result['fileType'] = self.file_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fileName') is not None:
            self.file_name = m.get('fileName')
        if m.get('fileSize') is not None:
            self.file_size = m.get('fileSize')
        if m.get('fileType') is not None:
            self.file_type = m.get('fileType')
        return self


class GeneratePictureUploadSignRequest(TeaModel):
    def __init__(
        self,
        files: List[GeneratePictureUploadSignRequestFiles] = None,
        instance_id: int = None,
        instance_type: str = None,
    ):
        self.files = files
        self.instance_id = instance_id
        self.instance_type = instance_type

    def validate(self):
        if self.files:
            for k in self.files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['files'] = []
        if self.files is not None:
            for k in self.files:
                result['files'].append(k.to_map() if k else None)
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.files = []
        if m.get('files') is not None:
            for k in m.get('files'):
                temp_model = GeneratePictureUploadSignRequestFiles()
                self.files.append(temp_model.from_map(k))
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        return self


class GeneratePictureUploadSignResponseBodyDataFiles(TeaModel):
    def __init__(
        self,
        file_name: str = None,
        file_size: int = None,
        file_type: str = None,
        key: str = None,
    ):
        self.file_name = file_name
        self.file_size = file_size
        self.file_type = file_type
        # oss key
        self.key = key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.file_name is not None:
            result['fileName'] = self.file_name
        if self.file_size is not None:
            result['fileSize'] = self.file_size
        if self.file_type is not None:
            result['fileType'] = self.file_type
        if self.key is not None:
            result['key'] = self.key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fileName') is not None:
            self.file_name = m.get('fileName')
        if m.get('fileSize') is not None:
            self.file_size = m.get('fileSize')
        if m.get('fileType') is not None:
            self.file_type = m.get('fileType')
        if m.get('key') is not None:
            self.key = m.get('key')
        return self


class GeneratePictureUploadSignResponseBodyData(TeaModel):
    def __init__(
        self,
        access_key_id: str = None,
        bucket_name: str = None,
        files: List[GeneratePictureUploadSignResponseBodyDataFiles] = None,
        policy: str = None,
        signature: str = None,
        url: str = None,
    ):
        # accessKeyId
        self.access_key_id = access_key_id
        # oss bucket name
        self.bucket_name = bucket_name
        # files
        self.files = files
        # policy
        self.policy = policy
        # signature
        self.signature = signature
        # url
        self.url = url

    def validate(self):
        if self.files:
            for k in self.files:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key_id is not None:
            result['accessKeyId'] = self.access_key_id
        if self.bucket_name is not None:
            result['bucketName'] = self.bucket_name
        result['files'] = []
        if self.files is not None:
            for k in self.files:
                result['files'].append(k.to_map() if k else None)
        if self.policy is not None:
            result['policy'] = self.policy
        if self.signature is not None:
            result['signature'] = self.signature
        if self.url is not None:
            result['url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKeyId') is not None:
            self.access_key_id = m.get('accessKeyId')
        if m.get('bucketName') is not None:
            self.bucket_name = m.get('bucketName')
        self.files = []
        if m.get('files') is not None:
            for k in m.get('files'):
                temp_model = GeneratePictureUploadSignResponseBodyDataFiles()
                self.files.append(temp_model.from_map(k))
        if m.get('policy') is not None:
            self.policy = m.get('policy')
        if m.get('signature') is not None:
            self.signature = m.get('signature')
        if m.get('url') is not None:
            self.url = m.get('url')
        return self


class GeneratePictureUploadSignResponseBody(TeaModel):
    def __init__(
        self,
        data: GeneratePictureUploadSignResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GeneratePictureUploadSignResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GeneratePictureUploadSignResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GeneratePictureUploadSignResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GeneratePictureUploadSignResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GenerateProblemPictureLinkRequest(TeaModel):
    def __init__(
        self,
        keys: List[str] = None,
        problem_id: str = None,
    ):
        # oss key
        self.keys = keys
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.keys is not None:
            result['keys'] = self.keys
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('keys') is not None:
            self.keys = m.get('keys')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class GenerateProblemPictureLinkResponseBodyDataLinks(TeaModel):
    def __init__(
        self,
        key: str = None,
        link: str = None,
    ):
        # oss key
        self.key = key
        self.link = link

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.link is not None:
            result['link'] = self.link
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('link') is not None:
            self.link = m.get('link')
        return self


class GenerateProblemPictureLinkResponseBodyData(TeaModel):
    def __init__(
        self,
        links: List[GenerateProblemPictureLinkResponseBodyDataLinks] = None,
    ):
        self.links = links

    def validate(self):
        if self.links:
            for k in self.links:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['links'] = []
        if self.links is not None:
            for k in self.links:
                result['links'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.links = []
        if m.get('links') is not None:
            for k in m.get('links'):
                temp_model = GenerateProblemPictureLinkResponseBodyDataLinks()
                self.links.append(temp_model.from_map(k))
        return self


class GenerateProblemPictureLinkResponseBody(TeaModel):
    def __init__(
        self,
        data: GenerateProblemPictureLinkResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GenerateProblemPictureLinkResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GenerateProblemPictureLinkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GenerateProblemPictureLinkResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GenerateProblemPictureLinkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GenerateProblemPictureUploadSignRequest(TeaModel):
    def __init__(
        self,
        file_name: str = None,
        file_size: int = None,
        file_type: str = None,
        problem_id: int = None,
    ):
        self.file_name = file_name
        self.file_size = file_size
        self.file_type = file_type
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.file_name is not None:
            result['fileName'] = self.file_name
        if self.file_size is not None:
            result['fileSize'] = self.file_size
        if self.file_type is not None:
            result['fileType'] = self.file_type
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fileName') is not None:
            self.file_name = m.get('fileName')
        if m.get('fileSize') is not None:
            self.file_size = m.get('fileSize')
        if m.get('fileType') is not None:
            self.file_type = m.get('fileType')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class GenerateProblemPictureUploadSignResponseBodyData(TeaModel):
    def __init__(
        self,
        access_key_id: str = None,
        bucket_name: str = None,
        key: str = None,
        policy: str = None,
        signature: str = None,
        url: str = None,
    ):
        # ossaccessKeyId
        self.access_key_id = access_key_id
        # oss bucket name
        self.bucket_name = bucket_name
        # oss key
        self.key = key
        # policy
        self.policy = policy
        # signature
        self.signature = signature
        # url
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key_id is not None:
            result['accessKeyId'] = self.access_key_id
        if self.bucket_name is not None:
            result['bucketName'] = self.bucket_name
        if self.key is not None:
            result['key'] = self.key
        if self.policy is not None:
            result['policy'] = self.policy
        if self.signature is not None:
            result['signature'] = self.signature
        if self.url is not None:
            result['url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKeyId') is not None:
            self.access_key_id = m.get('accessKeyId')
        if m.get('bucketName') is not None:
            self.bucket_name = m.get('bucketName')
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('policy') is not None:
            self.policy = m.get('policy')
        if m.get('signature') is not None:
            self.signature = m.get('signature')
        if m.get('url') is not None:
            self.url = m.get('url')
        return self


class GenerateProblemPictureUploadSignResponseBody(TeaModel):
    def __init__(
        self,
        data: GenerateProblemPictureUploadSignResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GenerateProblemPictureUploadSignResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GenerateProblemPictureUploadSignResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GenerateProblemPictureUploadSignResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GenerateProblemPictureUploadSignResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetEscalationPlanRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.escalation_plan_id = escalation_plan_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        return self


class GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanConditions(TeaModel):
    def __init__(
        self,
        effection: str = None,
        level: str = None,
    ):
        self.effection = effection
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.effection is not None:
            result['effection'] = self.effection
        if self.level is not None:
            result['level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('level') is not None:
            self.level = m.get('level')
        return self


class GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesNoticeObjectList(TeaModel):
    def __init__(
        self,
        notice_object_id: int = None,
        notice_object_name: str = None,
    ):
        self.notice_object_id = notice_object_id
        self.notice_object_name = notice_object_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.notice_object_id is not None:
            result['noticeObjectId'] = self.notice_object_id
        if self.notice_object_name is not None:
            result['noticeObjectName'] = self.notice_object_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('noticeObjectId') is not None:
            self.notice_object_id = m.get('noticeObjectId')
        if m.get('noticeObjectName') is not None:
            self.notice_object_name = m.get('noticeObjectName')
        return self


class GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesNoticeRoleObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        name: str = None,
    ):
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesServiceGroups(TeaModel):
    def __init__(
        self,
        id: int = None,
        service_group_name: str = None,
    ):
        self.id = id
        self.service_group_name = service_group_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        return self


class GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategies(TeaModel):
    def __init__(
        self,
        enable_webhook: bool = None,
        escalation_plan_type: str = None,
        notice_channels: str = None,
        notice_object_list: List[GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesNoticeObjectList] = None,
        notice_objects: List[int] = None,
        notice_role_list: List[int] = None,
        notice_role_object_list: List[GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesNoticeRoleObjectList] = None,
        notice_time: int = None,
        service_groups: List[GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesServiceGroups] = None,
    ):
        self.enable_webhook = enable_webhook
        self.escalation_plan_type = escalation_plan_type
        self.notice_channels = notice_channels
        self.notice_object_list = notice_object_list
        self.notice_objects = notice_objects
        self.notice_role_list = notice_role_list
        self.notice_role_object_list = notice_role_object_list
        self.notice_time = notice_time
        self.service_groups = service_groups

    def validate(self):
        if self.notice_object_list:
            for k in self.notice_object_list:
                if k:
                    k.validate()
        if self.notice_role_object_list:
            for k in self.notice_role_object_list:
                if k:
                    k.validate()
        if self.service_groups:
            for k in self.service_groups:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_webhook is not None:
            result['enableWebhook'] = self.enable_webhook
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        if self.notice_channels is not None:
            result['noticeChannels'] = self.notice_channels
        result['noticeObjectList'] = []
        if self.notice_object_list is not None:
            for k in self.notice_object_list:
                result['noticeObjectList'].append(k.to_map() if k else None)
        if self.notice_objects is not None:
            result['noticeObjects'] = self.notice_objects
        if self.notice_role_list is not None:
            result['noticeRoleList'] = self.notice_role_list
        result['noticeRoleObjectList'] = []
        if self.notice_role_object_list is not None:
            for k in self.notice_role_object_list:
                result['noticeRoleObjectList'].append(k.to_map() if k else None)
        if self.notice_time is not None:
            result['noticeTime'] = self.notice_time
        result['serviceGroups'] = []
        if self.service_groups is not None:
            for k in self.service_groups:
                result['serviceGroups'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('enableWebhook') is not None:
            self.enable_webhook = m.get('enableWebhook')
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        if m.get('noticeChannels') is not None:
            self.notice_channels = m.get('noticeChannels')
        self.notice_object_list = []
        if m.get('noticeObjectList') is not None:
            for k in m.get('noticeObjectList'):
                temp_model = GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesNoticeObjectList()
                self.notice_object_list.append(temp_model.from_map(k))
        if m.get('noticeObjects') is not None:
            self.notice_objects = m.get('noticeObjects')
        if m.get('noticeRoleList') is not None:
            self.notice_role_list = m.get('noticeRoleList')
        self.notice_role_object_list = []
        if m.get('noticeRoleObjectList') is not None:
            for k in m.get('noticeRoleObjectList'):
                temp_model = GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesNoticeRoleObjectList()
                self.notice_role_object_list.append(temp_model.from_map(k))
        if m.get('noticeTime') is not None:
            self.notice_time = m.get('noticeTime')
        self.service_groups = []
        if m.get('serviceGroups') is not None:
            for k in m.get('serviceGroups'):
                temp_model = GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategiesServiceGroups()
                self.service_groups.append(temp_model.from_map(k))
        return self


class GetEscalationPlanResponseBodyDataEscalationPlanRules(TeaModel):
    def __init__(
        self,
        escalation_plan_conditions: List[GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanConditions] = None,
        escalation_plan_rule_id: int = None,
        escalation_plan_strategies: List[GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategies] = None,
    ):
        self.escalation_plan_conditions = escalation_plan_conditions
        self.escalation_plan_rule_id = escalation_plan_rule_id
        self.escalation_plan_strategies = escalation_plan_strategies

    def validate(self):
        if self.escalation_plan_conditions:
            for k in self.escalation_plan_conditions:
                if k:
                    k.validate()
        if self.escalation_plan_strategies:
            for k in self.escalation_plan_strategies:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['escalationPlanConditions'] = []
        if self.escalation_plan_conditions is not None:
            for k in self.escalation_plan_conditions:
                result['escalationPlanConditions'].append(k.to_map() if k else None)
        if self.escalation_plan_rule_id is not None:
            result['escalationPlanRuleId'] = self.escalation_plan_rule_id
        result['escalationPlanStrategies'] = []
        if self.escalation_plan_strategies is not None:
            for k in self.escalation_plan_strategies:
                result['escalationPlanStrategies'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.escalation_plan_conditions = []
        if m.get('escalationPlanConditions') is not None:
            for k in m.get('escalationPlanConditions'):
                temp_model = GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanConditions()
                self.escalation_plan_conditions.append(temp_model.from_map(k))
        if m.get('escalationPlanRuleId') is not None:
            self.escalation_plan_rule_id = m.get('escalationPlanRuleId')
        self.escalation_plan_strategies = []
        if m.get('escalationPlanStrategies') is not None:
            for k in m.get('escalationPlanStrategies'):
                temp_model = GetEscalationPlanResponseBodyDataEscalationPlanRulesEscalationPlanStrategies()
                self.escalation_plan_strategies.append(temp_model.from_map(k))
        return self


class GetEscalationPlanResponseBodyDataEscalationPlanScopeObjects(TeaModel):
    def __init__(
        self,
        escalation_plan_scope_objects: int = None,
        scope: str = None,
        scope_object_deleted_type: int = None,
        scope_object_id: int = None,
        scope_object_name: str = None,
    ):
        self.escalation_plan_scope_objects = escalation_plan_scope_objects
        self.scope = scope
        self.scope_object_deleted_type = scope_object_deleted_type
        self.scope_object_id = scope_object_id
        self.scope_object_name = scope_object_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_scope_objects is not None:
            result['escalationPlanScopeObjects'] = self.escalation_plan_scope_objects
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object_deleted_type is not None:
            result['scopeObjectDeletedType'] = self.scope_object_deleted_type
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        if self.scope_object_name is not None:
            result['scopeObjectName'] = self.scope_object_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanScopeObjects') is not None:
            self.escalation_plan_scope_objects = m.get('escalationPlanScopeObjects')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObjectDeletedType') is not None:
            self.scope_object_deleted_type = m.get('scopeObjectDeletedType')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        if m.get('scopeObjectName') is not None:
            self.scope_object_name = m.get('scopeObjectName')
        return self


class GetEscalationPlanResponseBodyData(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        escalation_plan_description: str = None,
        escalation_plan_id: int = None,
        escalation_plan_name: str = None,
        escalation_plan_rules: List[GetEscalationPlanResponseBodyDataEscalationPlanRules] = None,
        escalation_plan_scope_objects: List[GetEscalationPlanResponseBodyDataEscalationPlanScopeObjects] = None,
        is_global: bool = None,
    ):
        self.create_time = create_time
        self.escalation_plan_description = escalation_plan_description
        self.escalation_plan_id = escalation_plan_id
        self.escalation_plan_name = escalation_plan_name
        self.escalation_plan_rules = escalation_plan_rules
        self.escalation_plan_scope_objects = escalation_plan_scope_objects
        self.is_global = is_global

    def validate(self):
        if self.escalation_plan_rules:
            for k in self.escalation_plan_rules:
                if k:
                    k.validate()
        if self.escalation_plan_scope_objects:
            for k in self.escalation_plan_scope_objects:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.escalation_plan_description is not None:
            result['escalationPlanDescription'] = self.escalation_plan_description
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        result['escalationPlanRules'] = []
        if self.escalation_plan_rules is not None:
            for k in self.escalation_plan_rules:
                result['escalationPlanRules'].append(k.to_map() if k else None)
        result['escalationPlanScopeObjects'] = []
        if self.escalation_plan_scope_objects is not None:
            for k in self.escalation_plan_scope_objects:
                result['escalationPlanScopeObjects'].append(k.to_map() if k else None)
        if self.is_global is not None:
            result['isGlobal'] = self.is_global
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('escalationPlanDescription') is not None:
            self.escalation_plan_description = m.get('escalationPlanDescription')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        self.escalation_plan_rules = []
        if m.get('escalationPlanRules') is not None:
            for k in m.get('escalationPlanRules'):
                temp_model = GetEscalationPlanResponseBodyDataEscalationPlanRules()
                self.escalation_plan_rules.append(temp_model.from_map(k))
        self.escalation_plan_scope_objects = []
        if m.get('escalationPlanScopeObjects') is not None:
            for k in m.get('escalationPlanScopeObjects'):
                temp_model = GetEscalationPlanResponseBodyDataEscalationPlanScopeObjects()
                self.escalation_plan_scope_objects.append(temp_model.from_map(k))
        if m.get('isGlobal') is not None:
            self.is_global = m.get('isGlobal')
        return self


class GetEscalationPlanResponseBody(TeaModel):
    def __init__(
        self,
        data: GetEscalationPlanResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetEscalationPlanResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetEscalationPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetEscalationPlanResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetEscalationPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetEventRequest(TeaModel):
    def __init__(
        self,
        monitor_source_id: int = None,
    ):
        # This parameter is required.
        self.monitor_source_id = monitor_source_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        return self


class GetEventResponseBodyData(TeaModel):
    def __init__(
        self,
        event_json: str = None,
        event_time: str = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
    ):
        self.event_json = event_json
        self.event_time = event_time
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.event_json is not None:
            result['eventJson'] = self.event_json
        if self.event_time is not None:
            result['eventTime'] = self.event_time
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('eventJson') is not None:
            self.event_json = m.get('eventJson')
        if m.get('eventTime') is not None:
            self.event_time = m.get('eventTime')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        return self


class GetEventResponseBody(TeaModel):
    def __init__(
        self,
        data: GetEventResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetEventResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetEventResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetEventResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetEventResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetHomePageGuidanceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class GetHomePageGuidanceResponseBodyData(TeaModel):
    def __init__(
        self,
        notify_subscription_status: bool = None,
        service_group_status: bool = None,
        service_status: bool = None,
        users_status: bool = None,
    ):
        self.notify_subscription_status = notify_subscription_status
        self.service_group_status = service_group_status
        self.service_status = service_status
        self.users_status = users_status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.notify_subscription_status is not None:
            result['notifySubscriptionStatus'] = self.notify_subscription_status
        if self.service_group_status is not None:
            result['serviceGroupStatus'] = self.service_group_status
        if self.service_status is not None:
            result['serviceStatus'] = self.service_status
        if self.users_status is not None:
            result['usersStatus'] = self.users_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('notifySubscriptionStatus') is not None:
            self.notify_subscription_status = m.get('notifySubscriptionStatus')
        if m.get('serviceGroupStatus') is not None:
            self.service_group_status = m.get('serviceGroupStatus')
        if m.get('serviceStatus') is not None:
            self.service_status = m.get('serviceStatus')
        if m.get('usersStatus') is not None:
            self.users_status = m.get('usersStatus')
        return self


class GetHomePageGuidanceResponseBody(TeaModel):
    def __init__(
        self,
        data: GetHomePageGuidanceResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetHomePageGuidanceResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetHomePageGuidanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetHomePageGuidanceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetHomePageGuidanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIncidentRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_id: int = None,
    ):
        self.client_token = client_token
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class GetIncidentResponseBodyData(TeaModel):
    def __init__(
        self,
        assign_to_who_is_valid: int = None,
        assign_user_id: int = None,
        assign_user_name: str = None,
        assign_user_phone: str = None,
        create_time: str = None,
        default_assign_to_who: int = None,
        default_assign_to_who_is_valid: int = None,
        default_assign_to_who_name: str = None,
        duration_time: int = None,
        effect: str = None,
        incident_description: str = None,
        incident_id: int = None,
        incident_level: str = None,
        incident_number: str = None,
        incident_status: str = None,
        incident_title: str = None,
        is_manual: bool = None,
        is_upgrade: bool = None,
        notify_channels: List[str] = None,
        problem_id: int = None,
        problem_number: str = None,
        rel_route_rule_delete_type: int = None,
        rel_service_delete_type: int = None,
        rel_service_group_is_valid: int = None,
        related_service_description: str = None,
        related_service_group_id: int = None,
        related_service_group_name: str = None,
        related_service_id: int = None,
        related_service_name: str = None,
        route_rule_id: int = None,
        route_rule_name: str = None,
    ):
        self.assign_to_who_is_valid = assign_to_who_is_valid
        self.assign_user_id = assign_user_id
        self.assign_user_name = assign_user_name
        self.assign_user_phone = assign_user_phone
        self.create_time = create_time
        self.default_assign_to_who = default_assign_to_who
        self.default_assign_to_who_is_valid = default_assign_to_who_is_valid
        self.default_assign_to_who_name = default_assign_to_who_name
        self.duration_time = duration_time
        self.effect = effect
        self.incident_description = incident_description
        self.incident_id = incident_id
        self.incident_level = incident_level
        self.incident_number = incident_number
        self.incident_status = incident_status
        self.incident_title = incident_title
        self.is_manual = is_manual
        self.is_upgrade = is_upgrade
        self.notify_channels = notify_channels
        self.problem_id = problem_id
        self.problem_number = problem_number
        self.rel_route_rule_delete_type = rel_route_rule_delete_type
        self.rel_service_delete_type = rel_service_delete_type
        self.rel_service_group_is_valid = rel_service_group_is_valid
        self.related_service_description = related_service_description
        self.related_service_group_id = related_service_group_id
        self.related_service_group_name = related_service_group_name
        self.related_service_id = related_service_id
        self.related_service_name = related_service_name
        self.route_rule_id = route_rule_id
        self.route_rule_name = route_rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_to_who_is_valid is not None:
            result['assignToWhoIsValid'] = self.assign_to_who_is_valid
        if self.assign_user_id is not None:
            result['assignUserId'] = self.assign_user_id
        if self.assign_user_name is not None:
            result['assignUserName'] = self.assign_user_name
        if self.assign_user_phone is not None:
            result['assignUserPhone'] = self.assign_user_phone
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.default_assign_to_who is not None:
            result['defaultAssignToWho'] = self.default_assign_to_who
        if self.default_assign_to_who_is_valid is not None:
            result['defaultAssignToWhoIsValid'] = self.default_assign_to_who_is_valid
        if self.default_assign_to_who_name is not None:
            result['defaultAssignToWhoName'] = self.default_assign_to_who_name
        if self.duration_time is not None:
            result['durationTime'] = self.duration_time
        if self.effect is not None:
            result['effect'] = self.effect
        if self.incident_description is not None:
            result['incidentDescription'] = self.incident_description
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.incident_number is not None:
            result['incidentNumber'] = self.incident_number
        if self.incident_status is not None:
            result['incidentStatus'] = self.incident_status
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.is_manual is not None:
            result['isManual'] = self.is_manual
        if self.is_upgrade is not None:
            result['isUpgrade'] = self.is_upgrade
        if self.notify_channels is not None:
            result['notifyChannels'] = self.notify_channels
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_number is not None:
            result['problemNumber'] = self.problem_number
        if self.rel_route_rule_delete_type is not None:
            result['relRouteRuleDeleteType'] = self.rel_route_rule_delete_type
        if self.rel_service_delete_type is not None:
            result['relServiceDeleteType'] = self.rel_service_delete_type
        if self.rel_service_group_is_valid is not None:
            result['relServiceGroupIsValid'] = self.rel_service_group_is_valid
        if self.related_service_description is not None:
            result['relatedServiceDescription'] = self.related_service_description
        if self.related_service_group_id is not None:
            result['relatedServiceGroupId'] = self.related_service_group_id
        if self.related_service_group_name is not None:
            result['relatedServiceGroupName'] = self.related_service_group_name
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.route_rule_name is not None:
            result['routeRuleName'] = self.route_rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignToWhoIsValid') is not None:
            self.assign_to_who_is_valid = m.get('assignToWhoIsValid')
        if m.get('assignUserId') is not None:
            self.assign_user_id = m.get('assignUserId')
        if m.get('assignUserName') is not None:
            self.assign_user_name = m.get('assignUserName')
        if m.get('assignUserPhone') is not None:
            self.assign_user_phone = m.get('assignUserPhone')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('defaultAssignToWho') is not None:
            self.default_assign_to_who = m.get('defaultAssignToWho')
        if m.get('defaultAssignToWhoIsValid') is not None:
            self.default_assign_to_who_is_valid = m.get('defaultAssignToWhoIsValid')
        if m.get('defaultAssignToWhoName') is not None:
            self.default_assign_to_who_name = m.get('defaultAssignToWhoName')
        if m.get('durationTime') is not None:
            self.duration_time = m.get('durationTime')
        if m.get('effect') is not None:
            self.effect = m.get('effect')
        if m.get('incidentDescription') is not None:
            self.incident_description = m.get('incidentDescription')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('incidentNumber') is not None:
            self.incident_number = m.get('incidentNumber')
        if m.get('incidentStatus') is not None:
            self.incident_status = m.get('incidentStatus')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('isManual') is not None:
            self.is_manual = m.get('isManual')
        if m.get('isUpgrade') is not None:
            self.is_upgrade = m.get('isUpgrade')
        if m.get('notifyChannels') is not None:
            self.notify_channels = m.get('notifyChannels')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemNumber') is not None:
            self.problem_number = m.get('problemNumber')
        if m.get('relRouteRuleDeleteType') is not None:
            self.rel_route_rule_delete_type = m.get('relRouteRuleDeleteType')
        if m.get('relServiceDeleteType') is not None:
            self.rel_service_delete_type = m.get('relServiceDeleteType')
        if m.get('relServiceGroupIsValid') is not None:
            self.rel_service_group_is_valid = m.get('relServiceGroupIsValid')
        if m.get('relatedServiceDescription') is not None:
            self.related_service_description = m.get('relatedServiceDescription')
        if m.get('relatedServiceGroupId') is not None:
            self.related_service_group_id = m.get('relatedServiceGroupId')
        if m.get('relatedServiceGroupName') is not None:
            self.related_service_group_name = m.get('relatedServiceGroupName')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('routeRuleName') is not None:
            self.route_rule_name = m.get('routeRuleName')
        return self


class GetIncidentResponseBody(TeaModel):
    def __init__(
        self,
        data: GetIncidentResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetIncidentResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetIncidentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIncidentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIncidentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIncidentListByIdListRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_id_list: List[int] = None,
    ):
        self.client_token = client_token
        self.incident_id_list = incident_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_id_list is not None:
            result['incidentIdList'] = self.incident_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentIdList') is not None:
            self.incident_id_list = m.get('incidentIdList')
        return self


class GetIncidentListByIdListResponseBodyData(TeaModel):
    def __init__(
        self,
        assign_to_who_is_valid: int = None,
        assign_user_id: int = None,
        assign_user_name: str = None,
        assign_user_phone: str = None,
        create_time: str = None,
        default_assign_to_who: int = None,
        default_assign_to_who_is_valid: int = None,
        default_assign_to_who_name: str = None,
        duration_time: str = None,
        effect: str = None,
        incident_description: str = None,
        incident_id: int = None,
        incident_level: str = None,
        incident_number: str = None,
        incident_status: str = None,
        incident_title: str = None,
        is_manual: bool = None,
        is_upgrade: bool = None,
        notify_channels: List[str] = None,
        problem_id: int = None,
        problem_number: str = None,
        rel_route_rule_delete_type: int = None,
        rel_service_delete_type: int = None,
        rel_service_group_is_valid: int = None,
        related_service_description: str = None,
        related_service_group_id: int = None,
        related_service_group_name: str = None,
        related_service_id: int = None,
        related_service_name: str = None,
        route_rule_id: int = None,
        route_rule_name: str = None,
    ):
        self.assign_to_who_is_valid = assign_to_who_is_valid
        self.assign_user_id = assign_user_id
        self.assign_user_name = assign_user_name
        self.assign_user_phone = assign_user_phone
        self.create_time = create_time
        self.default_assign_to_who = default_assign_to_who
        self.default_assign_to_who_is_valid = default_assign_to_who_is_valid
        self.default_assign_to_who_name = default_assign_to_who_name
        self.duration_time = duration_time
        self.effect = effect
        self.incident_description = incident_description
        self.incident_id = incident_id
        self.incident_level = incident_level
        self.incident_number = incident_number
        self.incident_status = incident_status
        self.incident_title = incident_title
        self.is_manual = is_manual
        self.is_upgrade = is_upgrade
        self.notify_channels = notify_channels
        self.problem_id = problem_id
        self.problem_number = problem_number
        self.rel_route_rule_delete_type = rel_route_rule_delete_type
        self.rel_service_delete_type = rel_service_delete_type
        self.rel_service_group_is_valid = rel_service_group_is_valid
        self.related_service_description = related_service_description
        self.related_service_group_id = related_service_group_id
        self.related_service_group_name = related_service_group_name
        self.related_service_id = related_service_id
        self.related_service_name = related_service_name
        self.route_rule_id = route_rule_id
        self.route_rule_name = route_rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_to_who_is_valid is not None:
            result['assignToWhoIsValid'] = self.assign_to_who_is_valid
        if self.assign_user_id is not None:
            result['assignUserId'] = self.assign_user_id
        if self.assign_user_name is not None:
            result['assignUserName'] = self.assign_user_name
        if self.assign_user_phone is not None:
            result['assignUserPhone'] = self.assign_user_phone
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.default_assign_to_who is not None:
            result['defaultAssignToWho'] = self.default_assign_to_who
        if self.default_assign_to_who_is_valid is not None:
            result['defaultAssignToWhoIsValid'] = self.default_assign_to_who_is_valid
        if self.default_assign_to_who_name is not None:
            result['defaultAssignToWhoName'] = self.default_assign_to_who_name
        if self.duration_time is not None:
            result['durationTime'] = self.duration_time
        if self.effect is not None:
            result['effect'] = self.effect
        if self.incident_description is not None:
            result['incidentDescription'] = self.incident_description
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.incident_number is not None:
            result['incidentNumber'] = self.incident_number
        if self.incident_status is not None:
            result['incidentStatus'] = self.incident_status
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.is_manual is not None:
            result['isManual'] = self.is_manual
        if self.is_upgrade is not None:
            result['isUpgrade'] = self.is_upgrade
        if self.notify_channels is not None:
            result['notifyChannels'] = self.notify_channels
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_number is not None:
            result['problemNumber'] = self.problem_number
        if self.rel_route_rule_delete_type is not None:
            result['relRouteRuleDeleteType'] = self.rel_route_rule_delete_type
        if self.rel_service_delete_type is not None:
            result['relServiceDeleteType'] = self.rel_service_delete_type
        if self.rel_service_group_is_valid is not None:
            result['relServiceGroupIsValid'] = self.rel_service_group_is_valid
        if self.related_service_description is not None:
            result['relatedServiceDescription'] = self.related_service_description
        if self.related_service_group_id is not None:
            result['relatedServiceGroupId'] = self.related_service_group_id
        if self.related_service_group_name is not None:
            result['relatedServiceGroupName'] = self.related_service_group_name
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.route_rule_name is not None:
            result['routeRuleName'] = self.route_rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignToWhoIsValid') is not None:
            self.assign_to_who_is_valid = m.get('assignToWhoIsValid')
        if m.get('assignUserId') is not None:
            self.assign_user_id = m.get('assignUserId')
        if m.get('assignUserName') is not None:
            self.assign_user_name = m.get('assignUserName')
        if m.get('assignUserPhone') is not None:
            self.assign_user_phone = m.get('assignUserPhone')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('defaultAssignToWho') is not None:
            self.default_assign_to_who = m.get('defaultAssignToWho')
        if m.get('defaultAssignToWhoIsValid') is not None:
            self.default_assign_to_who_is_valid = m.get('defaultAssignToWhoIsValid')
        if m.get('defaultAssignToWhoName') is not None:
            self.default_assign_to_who_name = m.get('defaultAssignToWhoName')
        if m.get('durationTime') is not None:
            self.duration_time = m.get('durationTime')
        if m.get('effect') is not None:
            self.effect = m.get('effect')
        if m.get('incidentDescription') is not None:
            self.incident_description = m.get('incidentDescription')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('incidentNumber') is not None:
            self.incident_number = m.get('incidentNumber')
        if m.get('incidentStatus') is not None:
            self.incident_status = m.get('incidentStatus')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('isManual') is not None:
            self.is_manual = m.get('isManual')
        if m.get('isUpgrade') is not None:
            self.is_upgrade = m.get('isUpgrade')
        if m.get('notifyChannels') is not None:
            self.notify_channels = m.get('notifyChannels')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemNumber') is not None:
            self.problem_number = m.get('problemNumber')
        if m.get('relRouteRuleDeleteType') is not None:
            self.rel_route_rule_delete_type = m.get('relRouteRuleDeleteType')
        if m.get('relServiceDeleteType') is not None:
            self.rel_service_delete_type = m.get('relServiceDeleteType')
        if m.get('relServiceGroupIsValid') is not None:
            self.rel_service_group_is_valid = m.get('relServiceGroupIsValid')
        if m.get('relatedServiceDescription') is not None:
            self.related_service_description = m.get('relatedServiceDescription')
        if m.get('relatedServiceGroupId') is not None:
            self.related_service_group_id = m.get('relatedServiceGroupId')
        if m.get('relatedServiceGroupName') is not None:
            self.related_service_group_name = m.get('relatedServiceGroupName')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('routeRuleName') is not None:
            self.route_rule_name = m.get('routeRuleName')
        return self


class GetIncidentListByIdListResponseBody(TeaModel):
    def __init__(
        self,
        data: List[GetIncidentListByIdListResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = GetIncidentListByIdListResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetIncidentListByIdListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIncidentListByIdListResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIncidentListByIdListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIncidentStatisticsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class GetIncidentStatisticsResponseBodyData(TeaModel):
    def __init__(
        self,
        all_finish: int = None,
        all_response: int = None,
        my_finish: int = None,
        my_response: int = None,
    ):
        self.all_finish = all_finish
        self.all_response = all_response
        self.my_finish = my_finish
        self.my_response = my_response

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.all_finish is not None:
            result['allFinish'] = self.all_finish
        if self.all_response is not None:
            result['allResponse'] = self.all_response
        if self.my_finish is not None:
            result['myFinish'] = self.my_finish
        if self.my_response is not None:
            result['myResponse'] = self.my_response
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('allFinish') is not None:
            self.all_finish = m.get('allFinish')
        if m.get('allResponse') is not None:
            self.all_response = m.get('allResponse')
        if m.get('myFinish') is not None:
            self.my_finish = m.get('myFinish')
        if m.get('myResponse') is not None:
            self.my_response = m.get('myResponse')
        return self


class GetIncidentStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        data: GetIncidentStatisticsResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetIncidentStatisticsResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetIncidentStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIncidentStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIncidentStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIncidentSubtotalCountRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_ids: List[int] = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.incident_ids = incident_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_ids is not None:
            result['incidentIds'] = self.incident_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentIds') is not None:
            self.incident_ids = m.get('incidentIds')
        return self


class GetIncidentSubtotalCountResponseBodyData(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        subtotal_count: Dict[str, Any] = None,
    ):
        # id of the request
        self.request_id = request_id
        # map
        self.subtotal_count = subtotal_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.subtotal_count is not None:
            result['subtotalCount'] = self.subtotal_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('subtotalCount') is not None:
            self.subtotal_count = m.get('subtotalCount')
        return self


class GetIncidentSubtotalCountResponseBody(TeaModel):
    def __init__(
        self,
        data: GetIncidentSubtotalCountResponseBodyData = None,
    ):
        # data
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetIncidentSubtotalCountResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        return self


class GetIncidentSubtotalCountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIncidentSubtotalCountResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIncidentSubtotalCountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class GetIntegrationConfigResponseBodyData(TeaModel):
    def __init__(
        self,
        access_key: str = None,
        integration_config_id: int = None,
        is_received_event: bool = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
        monitor_source_short_name: str = None,
        status: str = None,
    ):
        self.access_key = access_key
        self.integration_config_id = integration_config_id
        self.is_received_event = is_received_event
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name
        self.monitor_source_short_name = monitor_source_short_name
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key is not None:
            result['accessKey'] = self.access_key
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        if self.is_received_event is not None:
            result['isReceivedEvent'] = self.is_received_event
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.monitor_source_short_name is not None:
            result['monitorSourceShortName'] = self.monitor_source_short_name
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKey') is not None:
            self.access_key = m.get('accessKey')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        if m.get('isReceivedEvent') is not None:
            self.is_received_event = m.get('isReceivedEvent')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('monitorSourceShortName') is not None:
            self.monitor_source_short_name = m.get('monitorSourceShortName')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class GetIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        data: GetIntegrationConfigResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetIntegrationConfigResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetProblemRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class GetProblemResponseBodyDataCancelProblemOperateLogs(TeaModel):
    def __init__(
        self,
        action_name: str = None,
        action_time: str = None,
        operator: str = None,
        user_id: int = None,
    ):
        self.action_name = action_name
        self.action_time = action_time
        self.operator = operator
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action_name is not None:
            result['actionName'] = self.action_name
        if self.action_time is not None:
            result['actionTime'] = self.action_time
        if self.operator is not None:
            result['operator'] = self.operator
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('actionName') is not None:
            self.action_name = m.get('actionName')
        if m.get('actionTime') is not None:
            self.action_time = m.get('actionTime')
        if m.get('operator') is not None:
            self.operator = m.get('operator')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class GetProblemResponseBodyDataCoordinationGroups(TeaModel):
    def __init__(
        self,
        is_valid: int = None,
        service_group_id: int = None,
        service_group_name: str = None,
    ):
        self.is_valid = is_valid
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_valid is not None:
            result['isValid'] = self.is_valid
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('isValid') is not None:
            self.is_valid = m.get('isValid')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        return self


class GetProblemResponseBodyDataEffectionServices(TeaModel):
    def __init__(
        self,
        description: str = None,
        effection_level: int = None,
        effection_service_id: int = None,
        effection_status: int = None,
        service_delete_type: int = None,
        service_name: str = None,
    ):
        self.description = description
        self.effection_level = effection_level
        self.effection_service_id = effection_service_id
        self.effection_status = effection_status
        self.service_delete_type = service_delete_type
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['description'] = self.description
        if self.effection_level is not None:
            result['effectionLevel'] = self.effection_level
        if self.effection_service_id is not None:
            result['effectionServiceId'] = self.effection_service_id
        if self.effection_status is not None:
            result['effectionStatus'] = self.effection_status
        if self.service_delete_type is not None:
            result['serviceDeleteType'] = self.service_delete_type
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('effectionLevel') is not None:
            self.effection_level = m.get('effectionLevel')
        if m.get('effectionServiceId') is not None:
            self.effection_service_id = m.get('effectionServiceId')
        if m.get('effectionStatus') is not None:
            self.effection_status = m.get('effectionStatus')
        if m.get('serviceDeleteType') is not None:
            self.service_delete_type = m.get('serviceDeleteType')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class GetProblemResponseBodyDataHandingProblemOperateLogs(TeaModel):
    def __init__(
        self,
        action_name: str = None,
        action_time: str = None,
        operator: str = None,
        user_id: int = None,
        user_is_valid: int = None,
    ):
        self.action_name = action_name
        self.action_time = action_time
        self.operator = operator
        self.user_id = user_id
        self.user_is_valid = user_is_valid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action_name is not None:
            result['actionName'] = self.action_name
        if self.action_time is not None:
            result['actionTime'] = self.action_time
        if self.operator is not None:
            result['operator'] = self.operator
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_is_valid is not None:
            result['userIsValid'] = self.user_is_valid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('actionName') is not None:
            self.action_name = m.get('actionName')
        if m.get('actionTime') is not None:
            self.action_time = m.get('actionTime')
        if m.get('operator') is not None:
            self.operator = m.get('operator')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userIsValid') is not None:
            self.user_is_valid = m.get('userIsValid')
        return self


class GetProblemResponseBodyDataReplayProblemOperateLogs(TeaModel):
    def __init__(
        self,
        action_name: str = None,
        action_time: str = None,
        operator: str = None,
        user_id: int = None,
        user_is_valid: int = None,
    ):
        self.action_name = action_name
        self.action_time = action_time
        self.operator = operator
        self.user_id = user_id
        self.user_is_valid = user_is_valid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action_name is not None:
            result['actionName'] = self.action_name
        if self.action_time is not None:
            result['actionTime'] = self.action_time
        if self.operator is not None:
            result['operator'] = self.operator
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_is_valid is not None:
            result['userIsValid'] = self.user_is_valid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('actionName') is not None:
            self.action_name = m.get('actionName')
        if m.get('actionTime') is not None:
            self.action_time = m.get('actionTime')
        if m.get('operator') is not None:
            self.operator = m.get('operator')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userIsValid') is not None:
            self.user_is_valid = m.get('userIsValid')
        return self


class GetProblemResponseBodyDataReplayingProblemOperateLogs(TeaModel):
    def __init__(
        self,
        action_name: str = None,
        action_time: str = None,
        operator: str = None,
        user_id: int = None,
        user_is_valid: int = None,
    ):
        self.action_name = action_name
        self.action_time = action_time
        self.operator = operator
        self.user_id = user_id
        self.user_is_valid = user_is_valid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action_name is not None:
            result['actionName'] = self.action_name
        if self.action_time is not None:
            result['actionTime'] = self.action_time
        if self.operator is not None:
            result['operator'] = self.operator
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_is_valid is not None:
            result['userIsValid'] = self.user_is_valid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('actionName') is not None:
            self.action_name = m.get('actionName')
        if m.get('actionTime') is not None:
            self.action_time = m.get('actionTime')
        if m.get('operator') is not None:
            self.operator = m.get('operator')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userIsValid') is not None:
            self.user_is_valid = m.get('userIsValid')
        return self


class GetProblemResponseBodyDataRestoredProblemOperateLogs(TeaModel):
    def __init__(
        self,
        action_name: str = None,
        action_time: str = None,
        operator: str = None,
        user_id: int = None,
        user_is_valid: int = None,
    ):
        self.action_name = action_name
        self.action_time = action_time
        self.operator = operator
        self.user_id = user_id
        self.user_is_valid = user_is_valid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action_name is not None:
            result['actionName'] = self.action_name
        if self.action_time is not None:
            result['actionTime'] = self.action_time
        if self.operator is not None:
            result['operator'] = self.operator
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_is_valid is not None:
            result['userIsValid'] = self.user_is_valid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('actionName') is not None:
            self.action_name = m.get('actionName')
        if m.get('actionTime') is not None:
            self.action_time = m.get('actionTime')
        if m.get('operator') is not None:
            self.operator = m.get('operator')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userIsValid') is not None:
            self.user_is_valid = m.get('userIsValid')
        return self


class GetProblemResponseBodyDataTimelines(TeaModel):
    def __init__(
        self,
        key_node: str = None,
    ):
        self.key_node = key_node

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key_node is not None:
            result['keyNode'] = self.key_node
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('keyNode') is not None:
            self.key_node = m.get('keyNode')
        return self


class GetProblemResponseBodyData(TeaModel):
    def __init__(
        self,
        cancel_problem_operate_logs: List[GetProblemResponseBodyDataCancelProblemOperateLogs] = None,
        cancel_reason: int = None,
        cancel_reason_description: str = None,
        coordination_groups: List[GetProblemResponseBodyDataCoordinationGroups] = None,
        create_time: str = None,
        discover_time: str = None,
        duration_time: int = None,
        effection_services: List[GetProblemResponseBodyDataEffectionServices] = None,
        feedback: str = None,
        handing_problem_operate_logs: List[GetProblemResponseBodyDataHandingProblemOperateLogs] = None,
        incident_id: int = None,
        incident_number: str = None,
        is_rule_trigger: bool = None,
        main_handler: int = None,
        main_handler_id: int = None,
        main_handler_is_valid: int = None,
        main_handler_phone: str = None,
        preliminary_reason: str = None,
        problem_id: int = None,
        problem_level: int = None,
        problem_name: str = None,
        problem_number: str = None,
        problem_status: int = None,
        progress_summary: str = None,
        progress_summary_rich_text_id: int = None,
        recovery_time: str = None,
        related_service_id: int = None,
        replay_problem_operate_logs: List[GetProblemResponseBodyDataReplayProblemOperateLogs] = None,
        replaying_problem_operate_logs: List[GetProblemResponseBodyDataReplayingProblemOperateLogs] = None,
        restored_problem_operate_logs: List[GetProblemResponseBodyDataRestoredProblemOperateLogs] = None,
        service_delete_type: int = None,
        service_name: str = None,
        timelines: List[GetProblemResponseBodyDataTimelines] = None,
    ):
        self.cancel_problem_operate_logs = cancel_problem_operate_logs
        self.cancel_reason = cancel_reason
        self.cancel_reason_description = cancel_reason_description
        self.coordination_groups = coordination_groups
        self.create_time = create_time
        self.discover_time = discover_time
        self.duration_time = duration_time
        self.effection_services = effection_services
        self.feedback = feedback
        self.handing_problem_operate_logs = handing_problem_operate_logs
        self.incident_id = incident_id
        self.incident_number = incident_number
        self.is_rule_trigger = is_rule_trigger
        self.main_handler = main_handler
        self.main_handler_id = main_handler_id
        self.main_handler_is_valid = main_handler_is_valid
        self.main_handler_phone = main_handler_phone
        self.preliminary_reason = preliminary_reason
        # ID
        # 
        # This parameter is required.
        self.problem_id = problem_id
        self.problem_level = problem_level
        self.problem_name = problem_name
        self.problem_number = problem_number
        self.problem_status = problem_status
        self.progress_summary = progress_summary
        self.progress_summary_rich_text_id = progress_summary_rich_text_id
        self.recovery_time = recovery_time
        self.related_service_id = related_service_id
        self.replay_problem_operate_logs = replay_problem_operate_logs
        self.replaying_problem_operate_logs = replaying_problem_operate_logs
        self.restored_problem_operate_logs = restored_problem_operate_logs
        # serviceDeleteType
        self.service_delete_type = service_delete_type
        self.service_name = service_name
        self.timelines = timelines

    def validate(self):
        if self.cancel_problem_operate_logs:
            for k in self.cancel_problem_operate_logs:
                if k:
                    k.validate()
        if self.coordination_groups:
            for k in self.coordination_groups:
                if k:
                    k.validate()
        if self.effection_services:
            for k in self.effection_services:
                if k:
                    k.validate()
        if self.handing_problem_operate_logs:
            for k in self.handing_problem_operate_logs:
                if k:
                    k.validate()
        if self.replay_problem_operate_logs:
            for k in self.replay_problem_operate_logs:
                if k:
                    k.validate()
        if self.replaying_problem_operate_logs:
            for k in self.replaying_problem_operate_logs:
                if k:
                    k.validate()
        if self.restored_problem_operate_logs:
            for k in self.restored_problem_operate_logs:
                if k:
                    k.validate()
        if self.timelines:
            for k in self.timelines:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['cancelProblemOperateLogs'] = []
        if self.cancel_problem_operate_logs is not None:
            for k in self.cancel_problem_operate_logs:
                result['cancelProblemOperateLogs'].append(k.to_map() if k else None)
        if self.cancel_reason is not None:
            result['cancelReason'] = self.cancel_reason
        if self.cancel_reason_description is not None:
            result['cancelReasonDescription'] = self.cancel_reason_description
        result['coordinationGroups'] = []
        if self.coordination_groups is not None:
            for k in self.coordination_groups:
                result['coordinationGroups'].append(k.to_map() if k else None)
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.discover_time is not None:
            result['discoverTime'] = self.discover_time
        if self.duration_time is not None:
            result['durationTime'] = self.duration_time
        result['effectionServices'] = []
        if self.effection_services is not None:
            for k in self.effection_services:
                result['effectionServices'].append(k.to_map() if k else None)
        if self.feedback is not None:
            result['feedback'] = self.feedback
        result['handingProblemOperateLogs'] = []
        if self.handing_problem_operate_logs is not None:
            for k in self.handing_problem_operate_logs:
                result['handingProblemOperateLogs'].append(k.to_map() if k else None)
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_number is not None:
            result['incidentNumber'] = self.incident_number
        if self.is_rule_trigger is not None:
            result['isRuleTrigger'] = self.is_rule_trigger
        if self.main_handler is not None:
            result['mainHandler'] = self.main_handler
        if self.main_handler_id is not None:
            result['mainHandlerId'] = self.main_handler_id
        if self.main_handler_is_valid is not None:
            result['mainHandlerIsValid'] = self.main_handler_is_valid
        if self.main_handler_phone is not None:
            result['mainHandlerPhone'] = self.main_handler_phone
        if self.preliminary_reason is not None:
            result['preliminaryReason'] = self.preliminary_reason
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        if self.problem_name is not None:
            result['problemName'] = self.problem_name
        if self.problem_number is not None:
            result['problemNumber'] = self.problem_number
        if self.problem_status is not None:
            result['problemStatus'] = self.problem_status
        if self.progress_summary is not None:
            result['progressSummary'] = self.progress_summary
        if self.progress_summary_rich_text_id is not None:
            result['progressSummaryRichTextId'] = self.progress_summary_rich_text_id
        if self.recovery_time is not None:
            result['recoveryTime'] = self.recovery_time
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        result['replayProblemOperateLogs'] = []
        if self.replay_problem_operate_logs is not None:
            for k in self.replay_problem_operate_logs:
                result['replayProblemOperateLogs'].append(k.to_map() if k else None)
        result['replayingProblemOperateLogs'] = []
        if self.replaying_problem_operate_logs is not None:
            for k in self.replaying_problem_operate_logs:
                result['replayingProblemOperateLogs'].append(k.to_map() if k else None)
        result['restoredProblemOperateLogs'] = []
        if self.restored_problem_operate_logs is not None:
            for k in self.restored_problem_operate_logs:
                result['restoredProblemOperateLogs'].append(k.to_map() if k else None)
        if self.service_delete_type is not None:
            result['serviceDeleteType'] = self.service_delete_type
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        result['timelines'] = []
        if self.timelines is not None:
            for k in self.timelines:
                result['timelines'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.cancel_problem_operate_logs = []
        if m.get('cancelProblemOperateLogs') is not None:
            for k in m.get('cancelProblemOperateLogs'):
                temp_model = GetProblemResponseBodyDataCancelProblemOperateLogs()
                self.cancel_problem_operate_logs.append(temp_model.from_map(k))
        if m.get('cancelReason') is not None:
            self.cancel_reason = m.get('cancelReason')
        if m.get('cancelReasonDescription') is not None:
            self.cancel_reason_description = m.get('cancelReasonDescription')
        self.coordination_groups = []
        if m.get('coordinationGroups') is not None:
            for k in m.get('coordinationGroups'):
                temp_model = GetProblemResponseBodyDataCoordinationGroups()
                self.coordination_groups.append(temp_model.from_map(k))
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('discoverTime') is not None:
            self.discover_time = m.get('discoverTime')
        if m.get('durationTime') is not None:
            self.duration_time = m.get('durationTime')
        self.effection_services = []
        if m.get('effectionServices') is not None:
            for k in m.get('effectionServices'):
                temp_model = GetProblemResponseBodyDataEffectionServices()
                self.effection_services.append(temp_model.from_map(k))
        if m.get('feedback') is not None:
            self.feedback = m.get('feedback')
        self.handing_problem_operate_logs = []
        if m.get('handingProblemOperateLogs') is not None:
            for k in m.get('handingProblemOperateLogs'):
                temp_model = GetProblemResponseBodyDataHandingProblemOperateLogs()
                self.handing_problem_operate_logs.append(temp_model.from_map(k))
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentNumber') is not None:
            self.incident_number = m.get('incidentNumber')
        if m.get('isRuleTrigger') is not None:
            self.is_rule_trigger = m.get('isRuleTrigger')
        if m.get('mainHandler') is not None:
            self.main_handler = m.get('mainHandler')
        if m.get('mainHandlerId') is not None:
            self.main_handler_id = m.get('mainHandlerId')
        if m.get('mainHandlerIsValid') is not None:
            self.main_handler_is_valid = m.get('mainHandlerIsValid')
        if m.get('mainHandlerPhone') is not None:
            self.main_handler_phone = m.get('mainHandlerPhone')
        if m.get('preliminaryReason') is not None:
            self.preliminary_reason = m.get('preliminaryReason')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        if m.get('problemName') is not None:
            self.problem_name = m.get('problemName')
        if m.get('problemNumber') is not None:
            self.problem_number = m.get('problemNumber')
        if m.get('problemStatus') is not None:
            self.problem_status = m.get('problemStatus')
        if m.get('progressSummary') is not None:
            self.progress_summary = m.get('progressSummary')
        if m.get('progressSummaryRichTextId') is not None:
            self.progress_summary_rich_text_id = m.get('progressSummaryRichTextId')
        if m.get('recoveryTime') is not None:
            self.recovery_time = m.get('recoveryTime')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        self.replay_problem_operate_logs = []
        if m.get('replayProblemOperateLogs') is not None:
            for k in m.get('replayProblemOperateLogs'):
                temp_model = GetProblemResponseBodyDataReplayProblemOperateLogs()
                self.replay_problem_operate_logs.append(temp_model.from_map(k))
        self.replaying_problem_operate_logs = []
        if m.get('replayingProblemOperateLogs') is not None:
            for k in m.get('replayingProblemOperateLogs'):
                temp_model = GetProblemResponseBodyDataReplayingProblemOperateLogs()
                self.replaying_problem_operate_logs.append(temp_model.from_map(k))
        self.restored_problem_operate_logs = []
        if m.get('restoredProblemOperateLogs') is not None:
            for k in m.get('restoredProblemOperateLogs'):
                temp_model = GetProblemResponseBodyDataRestoredProblemOperateLogs()
                self.restored_problem_operate_logs.append(temp_model.from_map(k))
        if m.get('serviceDeleteType') is not None:
            self.service_delete_type = m.get('serviceDeleteType')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        self.timelines = []
        if m.get('timelines') is not None:
            for k in m.get('timelines'):
                temp_model = GetProblemResponseBodyDataTimelines()
                self.timelines.append(temp_model.from_map(k))
        return self


class GetProblemResponseBody(TeaModel):
    def __init__(
        self,
        data: GetProblemResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetProblemResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetProblemEffectionServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        effection_service_id: int = None,
        problem_id: int = None,
    ):
        # clientToken
        self.client_token = client_token
        self.effection_service_id = effection_service_id
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.effection_service_id is not None:
            result['effectionServiceId'] = self.effection_service_id
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('effectionServiceId') is not None:
            self.effection_service_id = m.get('effectionServiceId')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class GetProblemEffectionServiceResponseBodyData(TeaModel):
    def __init__(
        self,
        description: str = None,
        effection_service_id: int = None,
        level: int = None,
        pic_url: List[str] = None,
        service_id: int = None,
        service_name: str = None,
        status: int = None,
    ):
        self.description = description
        self.effection_service_id = effection_service_id
        self.level = level
        self.pic_url = pic_url
        self.service_id = service_id
        self.service_name = service_name
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['description'] = self.description
        if self.effection_service_id is not None:
            result['effectionServiceId'] = self.effection_service_id
        if self.level is not None:
            result['level'] = self.level
        if self.pic_url is not None:
            result['picUrl'] = self.pic_url
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('effectionServiceId') is not None:
            self.effection_service_id = m.get('effectionServiceId')
        if m.get('level') is not None:
            self.level = m.get('level')
        if m.get('picUrl') is not None:
            self.pic_url = m.get('picUrl')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class GetProblemEffectionServiceResponseBody(TeaModel):
    def __init__(
        self,
        data: GetProblemEffectionServiceResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetProblemEffectionServiceResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetProblemEffectionServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetProblemEffectionServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetProblemEffectionServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetProblemImprovementRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: str = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class GetProblemImprovementResponseBodyDataMeasureList(TeaModel):
    def __init__(
        self,
        check_standard: str = None,
        check_user_id: int = None,
        check_user_is_valid: int = None,
        check_user_name: str = None,
        content: str = None,
        director_id: int = None,
        director_is_valid: int = None,
        director_name: str = None,
        measure_id: int = None,
        plan_finish_time: str = None,
        stalker_id: int = None,
        stalker_is_valid: int = None,
        stalker_name: str = None,
        status: str = None,
        type: int = None,
    ):
        self.check_standard = check_standard
        self.check_user_id = check_user_id
        self.check_user_is_valid = check_user_is_valid
        self.check_user_name = check_user_name
        self.content = content
        self.director_id = director_id
        self.director_is_valid = director_is_valid
        self.director_name = director_name
        self.measure_id = measure_id
        self.plan_finish_time = plan_finish_time
        self.stalker_id = stalker_id
        self.stalker_is_valid = stalker_is_valid
        self.stalker_name = stalker_name
        self.status = status
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.check_standard is not None:
            result['checkStandard'] = self.check_standard
        if self.check_user_id is not None:
            result['checkUserId'] = self.check_user_id
        if self.check_user_is_valid is not None:
            result['checkUserIsValid'] = self.check_user_is_valid
        if self.check_user_name is not None:
            result['checkUserName'] = self.check_user_name
        if self.content is not None:
            result['content'] = self.content
        if self.director_id is not None:
            result['directorId'] = self.director_id
        if self.director_is_valid is not None:
            result['directorIsValid'] = self.director_is_valid
        if self.director_name is not None:
            result['directorName'] = self.director_name
        if self.measure_id is not None:
            result['measureId'] = self.measure_id
        if self.plan_finish_time is not None:
            result['planFinishTime'] = self.plan_finish_time
        if self.stalker_id is not None:
            result['stalkerId'] = self.stalker_id
        if self.stalker_is_valid is not None:
            result['stalkerIsValid'] = self.stalker_is_valid
        if self.stalker_name is not None:
            result['stalkerName'] = self.stalker_name
        if self.status is not None:
            result['status'] = self.status
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('checkStandard') is not None:
            self.check_standard = m.get('checkStandard')
        if m.get('checkUserId') is not None:
            self.check_user_id = m.get('checkUserId')
        if m.get('checkUserIsValid') is not None:
            self.check_user_is_valid = m.get('checkUserIsValid')
        if m.get('checkUserName') is not None:
            self.check_user_name = m.get('checkUserName')
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('directorId') is not None:
            self.director_id = m.get('directorId')
        if m.get('directorIsValid') is not None:
            self.director_is_valid = m.get('directorIsValid')
        if m.get('directorName') is not None:
            self.director_name = m.get('directorName')
        if m.get('measureId') is not None:
            self.measure_id = m.get('measureId')
        if m.get('planFinishTime') is not None:
            self.plan_finish_time = m.get('planFinishTime')
        if m.get('stalkerId') is not None:
            self.stalker_id = m.get('stalkerId')
        if m.get('stalkerIsValid') is not None:
            self.stalker_is_valid = m.get('stalkerIsValid')
        if m.get('stalkerName') is not None:
            self.stalker_name = m.get('stalkerName')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class GetProblemImprovementResponseBodyData(TeaModel):
    def __init__(
        self,
        custom_problem_reason: str = None,
        discover_source: str = None,
        duty_department_id: str = None,
        duty_department_name: str = None,
        duty_user_id: int = None,
        duty_user_is_valid: int = None,
        duty_user_name: str = None,
        duty_user_phone: str = None,
        injection_mode: str = None,
        is_manual: bool = None,
        measure_list: List[GetProblemImprovementResponseBodyDataMeasureList] = None,
        monitor_source_name: str = None,
        problem_id: str = None,
        problem_reason: str = None,
        recent_activity: str = None,
        recovery_mode: str = None,
        relation_changes: str = None,
        remark: str = None,
        replay_duty_user_id: int = None,
        replay_duty_user_is_valid: int = None,
        replay_duty_user_name: str = None,
        replay_duty_user_phone: str = None,
        user_report: int = None,
    ):
        self.custom_problem_reason = custom_problem_reason
        self.discover_source = discover_source
        self.duty_department_id = duty_department_id
        self.duty_department_name = duty_department_name
        self.duty_user_id = duty_user_id
        self.duty_user_is_valid = duty_user_is_valid
        self.duty_user_name = duty_user_name
        self.duty_user_phone = duty_user_phone
        self.injection_mode = injection_mode
        self.is_manual = is_manual
        self.measure_list = measure_list
        self.monitor_source_name = monitor_source_name
        self.problem_id = problem_id
        self.problem_reason = problem_reason
        self.recent_activity = recent_activity
        self.recovery_mode = recovery_mode
        self.relation_changes = relation_changes
        self.remark = remark
        self.replay_duty_user_id = replay_duty_user_id
        self.replay_duty_user_is_valid = replay_duty_user_is_valid
        self.replay_duty_user_name = replay_duty_user_name
        self.replay_duty_user_phone = replay_duty_user_phone
        self.user_report = user_report

    def validate(self):
        if self.measure_list:
            for k in self.measure_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.custom_problem_reason is not None:
            result['customProblemReason'] = self.custom_problem_reason
        if self.discover_source is not None:
            result['discoverSource'] = self.discover_source
        if self.duty_department_id is not None:
            result['dutyDepartmentId'] = self.duty_department_id
        if self.duty_department_name is not None:
            result['dutyDepartmentName'] = self.duty_department_name
        if self.duty_user_id is not None:
            result['dutyUserId'] = self.duty_user_id
        if self.duty_user_is_valid is not None:
            result['dutyUserIsValid'] = self.duty_user_is_valid
        if self.duty_user_name is not None:
            result['dutyUserName'] = self.duty_user_name
        if self.duty_user_phone is not None:
            result['dutyUserPhone'] = self.duty_user_phone
        if self.injection_mode is not None:
            result['injectionMode'] = self.injection_mode
        if self.is_manual is not None:
            result['isManual'] = self.is_manual
        result['measureList'] = []
        if self.measure_list is not None:
            for k in self.measure_list:
                result['measureList'].append(k.to_map() if k else None)
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_reason is not None:
            result['problemReason'] = self.problem_reason
        if self.recent_activity is not None:
            result['recentActivity'] = self.recent_activity
        if self.recovery_mode is not None:
            result['recoveryMode'] = self.recovery_mode
        if self.relation_changes is not None:
            result['relationChanges'] = self.relation_changes
        if self.remark is not None:
            result['remark'] = self.remark
        if self.replay_duty_user_id is not None:
            result['replayDutyUserId'] = self.replay_duty_user_id
        if self.replay_duty_user_is_valid is not None:
            result['replayDutyUserIsValid'] = self.replay_duty_user_is_valid
        if self.replay_duty_user_name is not None:
            result['replayDutyUserName'] = self.replay_duty_user_name
        if self.replay_duty_user_phone is not None:
            result['replayDutyUserPhone'] = self.replay_duty_user_phone
        if self.user_report is not None:
            result['userReport'] = self.user_report
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('customProblemReason') is not None:
            self.custom_problem_reason = m.get('customProblemReason')
        if m.get('discoverSource') is not None:
            self.discover_source = m.get('discoverSource')
        if m.get('dutyDepartmentId') is not None:
            self.duty_department_id = m.get('dutyDepartmentId')
        if m.get('dutyDepartmentName') is not None:
            self.duty_department_name = m.get('dutyDepartmentName')
        if m.get('dutyUserId') is not None:
            self.duty_user_id = m.get('dutyUserId')
        if m.get('dutyUserIsValid') is not None:
            self.duty_user_is_valid = m.get('dutyUserIsValid')
        if m.get('dutyUserName') is not None:
            self.duty_user_name = m.get('dutyUserName')
        if m.get('dutyUserPhone') is not None:
            self.duty_user_phone = m.get('dutyUserPhone')
        if m.get('injectionMode') is not None:
            self.injection_mode = m.get('injectionMode')
        if m.get('isManual') is not None:
            self.is_manual = m.get('isManual')
        self.measure_list = []
        if m.get('measureList') is not None:
            for k in m.get('measureList'):
                temp_model = GetProblemImprovementResponseBodyDataMeasureList()
                self.measure_list.append(temp_model.from_map(k))
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemReason') is not None:
            self.problem_reason = m.get('problemReason')
        if m.get('recentActivity') is not None:
            self.recent_activity = m.get('recentActivity')
        if m.get('recoveryMode') is not None:
            self.recovery_mode = m.get('recoveryMode')
        if m.get('relationChanges') is not None:
            self.relation_changes = m.get('relationChanges')
        if m.get('remark') is not None:
            self.remark = m.get('remark')
        if m.get('replayDutyUserId') is not None:
            self.replay_duty_user_id = m.get('replayDutyUserId')
        if m.get('replayDutyUserIsValid') is not None:
            self.replay_duty_user_is_valid = m.get('replayDutyUserIsValid')
        if m.get('replayDutyUserName') is not None:
            self.replay_duty_user_name = m.get('replayDutyUserName')
        if m.get('replayDutyUserPhone') is not None:
            self.replay_duty_user_phone = m.get('replayDutyUserPhone')
        if m.get('userReport') is not None:
            self.user_report = m.get('userReport')
        return self


class GetProblemImprovementResponseBody(TeaModel):
    def __init__(
        self,
        data: GetProblemImprovementResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetProblemImprovementResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetProblemImprovementResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetProblemImprovementResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetProblemImprovementResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetProblemPreviewRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        effect_service_ids: List[int] = None,
        incident_id: int = None,
        problem_id: int = None,
        problem_level: str = None,
        problem_notify_type: str = None,
        related_service_id: int = None,
        service_group_ids: List[int] = None,
    ):
        self.client_token = client_token
        self.effect_service_ids = effect_service_ids
        self.incident_id = incident_id
        self.problem_id = problem_id
        self.problem_level = problem_level
        self.problem_notify_type = problem_notify_type
        self.related_service_id = related_service_id
        self.service_group_ids = service_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.effect_service_ids is not None:
            result['effectServiceIds'] = self.effect_service_ids
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.service_group_ids is not None:
            result['serviceGroupIds'] = self.service_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('effectServiceIds') is not None:
            self.effect_service_ids = m.get('effectServiceIds')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('serviceGroupIds') is not None:
            self.service_group_ids = m.get('serviceGroupIds')
        return self


class GetProblemPreviewResponseBodyDataMailUsers(TeaModel):
    def __init__(
        self,
        username: str = None,
    ):
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class GetProblemPreviewResponseBodyDataMail(TeaModel):
    def __init__(
        self,
        count: int = None,
        users: List[GetProblemPreviewResponseBodyDataMailUsers] = None,
    ):
        self.count = count
        self.users = users

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count is not None:
            result['count'] = self.count
        result['users'] = []
        if self.users is not None:
            for k in self.users:
                result['users'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        self.users = []
        if m.get('users') is not None:
            for k in m.get('users'):
                temp_model = GetProblemPreviewResponseBodyDataMailUsers()
                self.users.append(temp_model.from_map(k))
        return self


class GetProblemPreviewResponseBodyDataProblemCoordinationGroups(TeaModel):
    def __init__(
        self,
        service_group_description: str = None,
        service_group_id: int = None,
        service_group_name: str = None,
    ):
        self.service_group_description = service_group_description
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_group_description is not None:
            result['serviceGroupDescription'] = self.service_group_description
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceGroupDescription') is not None:
            self.service_group_description = m.get('serviceGroupDescription')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        return self


class GetProblemPreviewResponseBodyDataProblemEffectionServices(TeaModel):
    def __init__(
        self,
        service_id: int = None,
        service_name: str = None,
    ):
        self.service_id = service_id
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class GetProblemPreviewResponseBodyDataProblem(TeaModel):
    def __init__(
        self,
        coordination_groups: List[GetProblemPreviewResponseBodyDataProblemCoordinationGroups] = None,
        create_time: str = None,
        discover_time: str = None,
        effection_services: List[GetProblemPreviewResponseBodyDataProblemEffectionServices] = None,
        is_manual: bool = None,
        is_upgrade: bool = None,
        main_handler_id: str = None,
        main_handler_name: str = None,
        preliminary_reason: str = None,
        problem_id: int = None,
        problem_level: str = None,
        problem_name: str = None,
        problem_status: str = None,
        progress_summary: str = None,
        progress_summary_rich_text_id: int = None,
        recovery_time: str = None,
        related_service_id: int = None,
        service_name: str = None,
    ):
        self.coordination_groups = coordination_groups
        self.create_time = create_time
        self.discover_time = discover_time
        self.effection_services = effection_services
        self.is_manual = is_manual
        self.is_upgrade = is_upgrade
        self.main_handler_id = main_handler_id
        self.main_handler_name = main_handler_name
        self.preliminary_reason = preliminary_reason
        self.problem_id = problem_id
        self.problem_level = problem_level
        self.problem_name = problem_name
        self.problem_status = problem_status
        self.progress_summary = progress_summary
        self.progress_summary_rich_text_id = progress_summary_rich_text_id
        self.recovery_time = recovery_time
        self.related_service_id = related_service_id
        self.service_name = service_name

    def validate(self):
        if self.coordination_groups:
            for k in self.coordination_groups:
                if k:
                    k.validate()
        if self.effection_services:
            for k in self.effection_services:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['coordinationGroups'] = []
        if self.coordination_groups is not None:
            for k in self.coordination_groups:
                result['coordinationGroups'].append(k.to_map() if k else None)
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.discover_time is not None:
            result['discoverTime'] = self.discover_time
        result['effectionServices'] = []
        if self.effection_services is not None:
            for k in self.effection_services:
                result['effectionServices'].append(k.to_map() if k else None)
        if self.is_manual is not None:
            result['isManual'] = self.is_manual
        if self.is_upgrade is not None:
            result['isUpgrade'] = self.is_upgrade
        if self.main_handler_id is not None:
            result['mainHandlerId'] = self.main_handler_id
        if self.main_handler_name is not None:
            result['mainHandlerName'] = self.main_handler_name
        if self.preliminary_reason is not None:
            result['preliminaryReason'] = self.preliminary_reason
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        if self.problem_name is not None:
            result['problemName'] = self.problem_name
        if self.problem_status is not None:
            result['problemStatus'] = self.problem_status
        if self.progress_summary is not None:
            result['progressSummary'] = self.progress_summary
        if self.progress_summary_rich_text_id is not None:
            result['progressSummaryRichTextId'] = self.progress_summary_rich_text_id
        if self.recovery_time is not None:
            result['recoveryTime'] = self.recovery_time
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.coordination_groups = []
        if m.get('coordinationGroups') is not None:
            for k in m.get('coordinationGroups'):
                temp_model = GetProblemPreviewResponseBodyDataProblemCoordinationGroups()
                self.coordination_groups.append(temp_model.from_map(k))
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('discoverTime') is not None:
            self.discover_time = m.get('discoverTime')
        self.effection_services = []
        if m.get('effectionServices') is not None:
            for k in m.get('effectionServices'):
                temp_model = GetProblemPreviewResponseBodyDataProblemEffectionServices()
                self.effection_services.append(temp_model.from_map(k))
        if m.get('isManual') is not None:
            self.is_manual = m.get('isManual')
        if m.get('isUpgrade') is not None:
            self.is_upgrade = m.get('isUpgrade')
        if m.get('mainHandlerId') is not None:
            self.main_handler_id = m.get('mainHandlerId')
        if m.get('mainHandlerName') is not None:
            self.main_handler_name = m.get('mainHandlerName')
        if m.get('preliminaryReason') is not None:
            self.preliminary_reason = m.get('preliminaryReason')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        if m.get('problemName') is not None:
            self.problem_name = m.get('problemName')
        if m.get('problemStatus') is not None:
            self.problem_status = m.get('problemStatus')
        if m.get('progressSummary') is not None:
            self.progress_summary = m.get('progressSummary')
        if m.get('progressSummaryRichTextId') is not None:
            self.progress_summary_rich_text_id = m.get('progressSummaryRichTextId')
        if m.get('recoveryTime') is not None:
            self.recovery_time = m.get('recoveryTime')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class GetProblemPreviewResponseBodyDataSmsUsers(TeaModel):
    def __init__(
        self,
        username: str = None,
    ):
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class GetProblemPreviewResponseBodyDataSms(TeaModel):
    def __init__(
        self,
        count: int = None,
        users: List[GetProblemPreviewResponseBodyDataSmsUsers] = None,
    ):
        self.count = count
        self.users = users

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count is not None:
            result['count'] = self.count
        result['users'] = []
        if self.users is not None:
            for k in self.users:
                result['users'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        self.users = []
        if m.get('users') is not None:
            for k in m.get('users'):
                temp_model = GetProblemPreviewResponseBodyDataSmsUsers()
                self.users.append(temp_model.from_map(k))
        return self


class GetProblemPreviewResponseBodyDataVoiceUsers(TeaModel):
    def __init__(
        self,
        username: str = None,
    ):
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class GetProblemPreviewResponseBodyDataVoice(TeaModel):
    def __init__(
        self,
        count: int = None,
        users: List[GetProblemPreviewResponseBodyDataVoiceUsers] = None,
    ):
        self.count = count
        self.users = users

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count is not None:
            result['count'] = self.count
        result['users'] = []
        if self.users is not None:
            for k in self.users:
                result['users'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        self.users = []
        if m.get('users') is not None:
            for k in m.get('users'):
                temp_model = GetProblemPreviewResponseBodyDataVoiceUsers()
                self.users.append(temp_model.from_map(k))
        return self


class GetProblemPreviewResponseBodyDataWebhookServiceGroups(TeaModel):
    def __init__(
        self,
        service_name: str = None,
    ):
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class GetProblemPreviewResponseBodyDataWebhook(TeaModel):
    def __init__(
        self,
        count: int = None,
        service_groups: List[GetProblemPreviewResponseBodyDataWebhookServiceGroups] = None,
    ):
        self.count = count
        self.service_groups = service_groups

    def validate(self):
        if self.service_groups:
            for k in self.service_groups:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count is not None:
            result['count'] = self.count
        result['serviceGroups'] = []
        if self.service_groups is not None:
            for k in self.service_groups:
                result['serviceGroups'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('count') is not None:
            self.count = m.get('count')
        self.service_groups = []
        if m.get('serviceGroups') is not None:
            for k in m.get('serviceGroups'):
                temp_model = GetProblemPreviewResponseBodyDataWebhookServiceGroups()
                self.service_groups.append(temp_model.from_map(k))
        return self


class GetProblemPreviewResponseBodyData(TeaModel):
    def __init__(
        self,
        de_after_data: str = None,
        de_before_data: str = None,
        mail: GetProblemPreviewResponseBodyDataMail = None,
        problem: GetProblemPreviewResponseBodyDataProblem = None,
        sms: GetProblemPreviewResponseBodyDataSms = None,
        up_after_data: str = None,
        up_before_data: str = None,
        voice: GetProblemPreviewResponseBodyDataVoice = None,
        webhook: GetProblemPreviewResponseBodyDataWebhook = None,
    ):
        self.de_after_data = de_after_data
        self.de_before_data = de_before_data
        self.mail = mail
        # object
        self.problem = problem
        self.sms = sms
        self.up_after_data = up_after_data
        self.up_before_data = up_before_data
        self.voice = voice
        # webhook
        self.webhook = webhook

    def validate(self):
        if self.mail:
            self.mail.validate()
        if self.problem:
            self.problem.validate()
        if self.sms:
            self.sms.validate()
        if self.voice:
            self.voice.validate()
        if self.webhook:
            self.webhook.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.de_after_data is not None:
            result['deAfterData'] = self.de_after_data
        if self.de_before_data is not None:
            result['deBeforeData'] = self.de_before_data
        if self.mail is not None:
            result['mail'] = self.mail.to_map()
        if self.problem is not None:
            result['problem'] = self.problem.to_map()
        if self.sms is not None:
            result['sms'] = self.sms.to_map()
        if self.up_after_data is not None:
            result['upAfterData'] = self.up_after_data
        if self.up_before_data is not None:
            result['upBeforeData'] = self.up_before_data
        if self.voice is not None:
            result['voice'] = self.voice.to_map()
        if self.webhook is not None:
            result['webhook'] = self.webhook.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('deAfterData') is not None:
            self.de_after_data = m.get('deAfterData')
        if m.get('deBeforeData') is not None:
            self.de_before_data = m.get('deBeforeData')
        if m.get('mail') is not None:
            temp_model = GetProblemPreviewResponseBodyDataMail()
            self.mail = temp_model.from_map(m['mail'])
        if m.get('problem') is not None:
            temp_model = GetProblemPreviewResponseBodyDataProblem()
            self.problem = temp_model.from_map(m['problem'])
        if m.get('sms') is not None:
            temp_model = GetProblemPreviewResponseBodyDataSms()
            self.sms = temp_model.from_map(m['sms'])
        if m.get('upAfterData') is not None:
            self.up_after_data = m.get('upAfterData')
        if m.get('upBeforeData') is not None:
            self.up_before_data = m.get('upBeforeData')
        if m.get('voice') is not None:
            temp_model = GetProblemPreviewResponseBodyDataVoice()
            self.voice = temp_model.from_map(m['voice'])
        if m.get('webhook') is not None:
            temp_model = GetProblemPreviewResponseBodyDataWebhook()
            self.webhook = temp_model.from_map(m['webhook'])
        return self


class GetProblemPreviewResponseBody(TeaModel):
    def __init__(
        self,
        data: GetProblemPreviewResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetProblemPreviewResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetProblemPreviewResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetProblemPreviewResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetProblemPreviewResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetResourceStatisticsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class GetResourceStatisticsResponseBodyData(TeaModel):
    def __init__(
        self,
        alert_count: int = None,
        incident_count: int = None,
        integration_count: int = None,
        problem_count: int = None,
    ):
        self.alert_count = alert_count
        self.incident_count = incident_count
        self.integration_count = integration_count
        self.problem_count = problem_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alert_count is not None:
            result['alertCount'] = self.alert_count
        if self.incident_count is not None:
            result['incidentCount'] = self.incident_count
        if self.integration_count is not None:
            result['integrationCount'] = self.integration_count
        if self.problem_count is not None:
            result['problemCount'] = self.problem_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('alertCount') is not None:
            self.alert_count = m.get('alertCount')
        if m.get('incidentCount') is not None:
            self.incident_count = m.get('incidentCount')
        if m.get('integrationCount') is not None:
            self.integration_count = m.get('integrationCount')
        if m.get('problemCount') is not None:
            self.problem_count = m.get('problemCount')
        return self


class GetResourceStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        data: GetResourceStatisticsResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetResourceStatisticsResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetResourceStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetResourceStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetResourceStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetRichTextRequest(TeaModel):
    def __init__(
        self,
        instance_id: int = None,
        instance_type: str = None,
        rich_text_id: int = None,
    ):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.rich_text_id = rich_text_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.rich_text_id is not None:
            result['richTextId'] = self.rich_text_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('richTextId') is not None:
            self.rich_text_id = m.get('richTextId')
        return self


class GetRichTextResponseBodyData(TeaModel):
    def __init__(
        self,
        instance_id: int = None,
        instance_type: int = None,
        rich_text: str = None,
    ):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.rich_text = rich_text

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.rich_text is not None:
            result['richText'] = self.rich_text
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('richText') is not None:
            self.rich_text = m.get('richText')
        return self


class GetRichTextResponseBody(TeaModel):
    def __init__(
        self,
        data: GetRichTextResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetRichTextResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetRichTextResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetRichTextResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetRichTextResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetRouteRuleRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        route_rule_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.route_rule_id = route_rule_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        return self


class GetRouteRuleResponseBodyDataEventRouteChildRulesConditions(TeaModel):
    def __init__(
        self,
        key: str = None,
        operation_symbol: str = None,
        value: str = None,
    ):
        self.key = key
        self.operation_symbol = operation_symbol
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.operation_symbol is not None:
            result['operationSymbol'] = self.operation_symbol
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('operationSymbol') is not None:
            self.operation_symbol = m.get('operationSymbol')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class GetRouteRuleResponseBodyDataEventRouteChildRules(TeaModel):
    def __init__(
        self,
        child_condition_relation: int = None,
        child_route_rule_id: int = None,
        conditions: List[GetRouteRuleResponseBodyDataEventRouteChildRulesConditions] = None,
        is_valid_child_rule: bool = None,
        monitor_integration_config_id: int = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
        parent_rule_id: int = None,
        problem_level: str = None,
    ):
        self.child_condition_relation = child_condition_relation
        self.child_route_rule_id = child_route_rule_id
        self.conditions = conditions
        self.is_valid_child_rule = is_valid_child_rule
        self.monitor_integration_config_id = monitor_integration_config_id
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name
        self.parent_rule_id = parent_rule_id
        self.problem_level = problem_level

    def validate(self):
        if self.conditions:
            for k in self.conditions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.child_condition_relation is not None:
            result['childConditionRelation'] = self.child_condition_relation
        if self.child_route_rule_id is not None:
            result['childRouteRuleId'] = self.child_route_rule_id
        result['conditions'] = []
        if self.conditions is not None:
            for k in self.conditions:
                result['conditions'].append(k.to_map() if k else None)
        if self.is_valid_child_rule is not None:
            result['isValidChildRule'] = self.is_valid_child_rule
        if self.monitor_integration_config_id is not None:
            result['monitorIntegrationConfigId'] = self.monitor_integration_config_id
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.parent_rule_id is not None:
            result['parentRuleId'] = self.parent_rule_id
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('childConditionRelation') is not None:
            self.child_condition_relation = m.get('childConditionRelation')
        if m.get('childRouteRuleId') is not None:
            self.child_route_rule_id = m.get('childRouteRuleId')
        self.conditions = []
        if m.get('conditions') is not None:
            for k in m.get('conditions'):
                temp_model = GetRouteRuleResponseBodyDataEventRouteChildRulesConditions()
                self.conditions.append(temp_model.from_map(k))
        if m.get('isValidChildRule') is not None:
            self.is_valid_child_rule = m.get('isValidChildRule')
        if m.get('monitorIntegrationConfigId') is not None:
            self.monitor_integration_config_id = m.get('monitorIntegrationConfigId')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('parentRuleId') is not None:
            self.parent_rule_id = m.get('parentRuleId')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        return self


class GetRouteRuleResponseBodyData(TeaModel):
    def __init__(
        self,
        assign_object_id: int = None,
        assign_object_name: str = None,
        assign_object_type: str = None,
        child_rule_relation: str = None,
        convergence_fields: List[str] = None,
        convergence_type: int = None,
        coverage_problem_levels: List[str] = None,
        create_time: str = None,
        effection: str = None,
        enable_status: str = None,
        event_route_child_rules: List[GetRouteRuleResponseBodyDataEventRouteChildRules] = None,
        incident_level: str = None,
        match_count: int = None,
        notify_channel_names: List[str] = None,
        notify_channels: List[str] = None,
        problem_effection_services: List[int] = None,
        problem_level_group: Dict[str, DataProblemLevelGroupValue] = None,
        rel_service_delete_type: int = None,
        related_service_id: int = None,
        related_service_name: str = None,
        route_rule_id: int = None,
        route_type: str = None,
        rule_name: str = None,
        time_window: int = None,
        update_time: str = None,
    ):
        self.assign_object_id = assign_object_id
        self.assign_object_name = assign_object_name
        self.assign_object_type = assign_object_type
        self.child_rule_relation = child_rule_relation
        self.convergence_fields = convergence_fields
        self.convergence_type = convergence_type
        self.coverage_problem_levels = coverage_problem_levels
        self.create_time = create_time
        self.effection = effection
        self.enable_status = enable_status
        self.event_route_child_rules = event_route_child_rules
        self.incident_level = incident_level
        self.match_count = match_count
        self.notify_channel_names = notify_channel_names
        self.notify_channels = notify_channels
        self.problem_effection_services = problem_effection_services
        self.problem_level_group = problem_level_group
        self.rel_service_delete_type = rel_service_delete_type
        self.related_service_id = related_service_id
        self.related_service_name = related_service_name
        self.route_rule_id = route_rule_id
        self.route_type = route_type
        self.rule_name = rule_name
        self.time_window = time_window
        self.update_time = update_time

    def validate(self):
        if self.event_route_child_rules:
            for k in self.event_route_child_rules:
                if k:
                    k.validate()
        if self.problem_level_group:
            for v in self.problem_level_group.values():
                if v:
                    v.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_object_id is not None:
            result['assignObjectId'] = self.assign_object_id
        if self.assign_object_name is not None:
            result['assignObjectName'] = self.assign_object_name
        if self.assign_object_type is not None:
            result['assignObjectType'] = self.assign_object_type
        if self.child_rule_relation is not None:
            result['childRuleRelation'] = self.child_rule_relation
        if self.convergence_fields is not None:
            result['convergenceFields'] = self.convergence_fields
        if self.convergence_type is not None:
            result['convergenceType'] = self.convergence_type
        if self.coverage_problem_levels is not None:
            result['coverageProblemLevels'] = self.coverage_problem_levels
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.effection is not None:
            result['effection'] = self.effection
        if self.enable_status is not None:
            result['enableStatus'] = self.enable_status
        result['eventRouteChildRules'] = []
        if self.event_route_child_rules is not None:
            for k in self.event_route_child_rules:
                result['eventRouteChildRules'].append(k.to_map() if k else None)
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.match_count is not None:
            result['matchCount'] = self.match_count
        if self.notify_channel_names is not None:
            result['notifyChannelNames'] = self.notify_channel_names
        if self.notify_channels is not None:
            result['notifyChannels'] = self.notify_channels
        if self.problem_effection_services is not None:
            result['problemEffectionServices'] = self.problem_effection_services
        result['problemLevelGroup'] = {}
        if self.problem_level_group is not None:
            for k, v in self.problem_level_group.items():
                result['problemLevelGroup'][k] = v.to_map()
        if self.rel_service_delete_type is not None:
            result['relServiceDeleteType'] = self.rel_service_delete_type
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.route_type is not None:
            result['routeType'] = self.route_type
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        if self.time_window is not None:
            result['timeWindow'] = self.time_window
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignObjectId') is not None:
            self.assign_object_id = m.get('assignObjectId')
        if m.get('assignObjectName') is not None:
            self.assign_object_name = m.get('assignObjectName')
        if m.get('assignObjectType') is not None:
            self.assign_object_type = m.get('assignObjectType')
        if m.get('childRuleRelation') is not None:
            self.child_rule_relation = m.get('childRuleRelation')
        if m.get('convergenceFields') is not None:
            self.convergence_fields = m.get('convergenceFields')
        if m.get('convergenceType') is not None:
            self.convergence_type = m.get('convergenceType')
        if m.get('coverageProblemLevels') is not None:
            self.coverage_problem_levels = m.get('coverageProblemLevels')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('enableStatus') is not None:
            self.enable_status = m.get('enableStatus')
        self.event_route_child_rules = []
        if m.get('eventRouteChildRules') is not None:
            for k in m.get('eventRouteChildRules'):
                temp_model = GetRouteRuleResponseBodyDataEventRouteChildRules()
                self.event_route_child_rules.append(temp_model.from_map(k))
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('matchCount') is not None:
            self.match_count = m.get('matchCount')
        if m.get('notifyChannelNames') is not None:
            self.notify_channel_names = m.get('notifyChannelNames')
        if m.get('notifyChannels') is not None:
            self.notify_channels = m.get('notifyChannels')
        if m.get('problemEffectionServices') is not None:
            self.problem_effection_services = m.get('problemEffectionServices')
        self.problem_level_group = {}
        if m.get('problemLevelGroup') is not None:
            for k, v in m.get('problemLevelGroup').items():
                temp_model = DataProblemLevelGroupValue()
                self.problem_level_group[k] = temp_model.from_map(v)
        if m.get('relServiceDeleteType') is not None:
            self.rel_service_delete_type = m.get('relServiceDeleteType')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('routeType') is not None:
            self.route_type = m.get('routeType')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        if m.get('timeWindow') is not None:
            self.time_window = m.get('timeWindow')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class GetRouteRuleResponseBody(TeaModel):
    def __init__(
        self,
        data: GetRouteRuleResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetRouteRuleResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetRouteRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetRouteRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetRouteRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.service_id = service_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        return self


class GetServiceResponseBodyData(TeaModel):
    def __init__(
        self,
        escalation_plan_id: int = None,
        service_description: str = None,
        service_group_id_list: List[int] = None,
        service_id: int = None,
        service_name: str = None,
        update_time: str = None,
    ):
        # This parameter is required.
        self.escalation_plan_id = escalation_plan_id
        self.service_description = service_description
        self.service_group_id_list = service_group_id_list
        self.service_id = service_id
        self.service_name = service_name
        self.update_time = update_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.service_description is not None:
            result['serviceDescription'] = self.service_description
        if self.service_group_id_list is not None:
            result['serviceGroupIdList'] = self.service_group_id_list
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('serviceDescription') is not None:
            self.service_description = m.get('serviceDescription')
        if m.get('serviceGroupIdList') is not None:
            self.service_group_id_list = m.get('serviceGroupIdList')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class GetServiceResponseBody(TeaModel):
    def __init__(
        self,
        data: GetServiceResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetServiceResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceGroupRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class GetServiceGroupResponseBodyDataUsers(TeaModel):
    def __init__(
        self,
        phone: str = None,
        role_name_list: List[str] = None,
        service_group_id: int = None,
        user_id: int = None,
        user_name: str = None,
    ):
        self.phone = phone
        self.role_name_list = role_name_list
        self.service_group_id = service_group_id
        self.user_id = user_id
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.phone is not None:
            result['phone'] = self.phone
        if self.role_name_list is not None:
            result['roleNameList'] = self.role_name_list
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_name is not None:
            result['userName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('roleNameList') is not None:
            self.role_name_list = m.get('roleNameList')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userName') is not None:
            self.user_name = m.get('userName')
        return self


class GetServiceGroupResponseBodyData(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        enable_webhook: str = None,
        service_group_description: str = None,
        service_group_id: int = None,
        service_group_name: str = None,
        update_time: str = None,
        users: List[GetServiceGroupResponseBodyDataUsers] = None,
        webhook_link: str = None,
        webhook_type: str = None,
    ):
        self.create_time = create_time
        self.enable_webhook = enable_webhook
        self.service_group_description = service_group_description
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name
        self.update_time = update_time
        self.users = users
        self.webhook_link = webhook_link
        self.webhook_type = webhook_type

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.enable_webhook is not None:
            result['enableWebhook'] = self.enable_webhook
        if self.service_group_description is not None:
            result['serviceGroupDescription'] = self.service_group_description
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        result['users'] = []
        if self.users is not None:
            for k in self.users:
                result['users'].append(k.to_map() if k else None)
        if self.webhook_link is not None:
            result['webhookLink'] = self.webhook_link
        if self.webhook_type is not None:
            result['webhookType'] = self.webhook_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('enableWebhook') is not None:
            self.enable_webhook = m.get('enableWebhook')
        if m.get('serviceGroupDescription') is not None:
            self.service_group_description = m.get('serviceGroupDescription')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        self.users = []
        if m.get('users') is not None:
            for k in m.get('users'):
                temp_model = GetServiceGroupResponseBodyDataUsers()
                self.users.append(temp_model.from_map(k))
        if m.get('webhookLink') is not None:
            self.webhook_link = m.get('webhookLink')
        if m.get('webhookType') is not None:
            self.webhook_type = m.get('webhookType')
        return self


class GetServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        data: GetServiceGroupResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetServiceGroupResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceGroupPersonSchedulingRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        end_time: str = None,
        service_group_id: int = None,
        start_time: str = None,
        user_id: int = None,
    ):
        self.client_token = client_token
        self.end_time = end_time
        self.service_group_id = service_group_id
        self.start_time = start_time
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class GetServiceGroupPersonSchedulingResponseBody(TeaModel):
    def __init__(
        self,
        data: Dict[str, Any] = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetServiceGroupPersonSchedulingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetServiceGroupPersonSchedulingResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetServiceGroupPersonSchedulingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceGroupSchedulingRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class GetServiceGroupSchedulingResponseBodyDataFastSchedulingSchedulingUsers(TeaModel):
    def __init__(
        self,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
        scheduling_user_name: str = None,
    ):
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list
        self.scheduling_user_name = scheduling_user_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        if self.scheduling_user_name is not None:
            result['schedulingUserName'] = self.scheduling_user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        if m.get('schedulingUserName') is not None:
            self.scheduling_user_name = m.get('schedulingUserName')
        return self


class GetServiceGroupSchedulingResponseBodyDataFastScheduling(TeaModel):
    def __init__(
        self,
        duty_plan: str = None,
        id: int = None,
        scheduling_users: List[GetServiceGroupSchedulingResponseBodyDataFastSchedulingSchedulingUsers] = None,
        single_duration: int = None,
        single_duration_unit: str = None,
    ):
        self.duty_plan = duty_plan
        self.id = id
        self.scheduling_users = scheduling_users
        self.single_duration = single_duration
        self.single_duration_unit = single_duration_unit

    def validate(self):
        if self.scheduling_users:
            for k in self.scheduling_users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.duty_plan is not None:
            result['dutyPlan'] = self.duty_plan
        if self.id is not None:
            result['id'] = self.id
        result['schedulingUsers'] = []
        if self.scheduling_users is not None:
            for k in self.scheduling_users:
                result['schedulingUsers'].append(k.to_map() if k else None)
        if self.single_duration is not None:
            result['singleDuration'] = self.single_duration
        if self.single_duration_unit is not None:
            result['singleDurationUnit'] = self.single_duration_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dutyPlan') is not None:
            self.duty_plan = m.get('dutyPlan')
        if m.get('id') is not None:
            self.id = m.get('id')
        self.scheduling_users = []
        if m.get('schedulingUsers') is not None:
            for k in m.get('schedulingUsers'):
                temp_model = GetServiceGroupSchedulingResponseBodyDataFastSchedulingSchedulingUsers()
                self.scheduling_users.append(temp_model.from_map(k))
        if m.get('singleDuration') is not None:
            self.single_duration = m.get('singleDuration')
        if m.get('singleDurationUnit') is not None:
            self.single_duration_unit = m.get('singleDurationUnit')
        return self


class GetServiceGroupSchedulingResponseBodyDataFineSchedulingSchedulingFineShifts(TeaModel):
    def __init__(
        self,
        cycle_order: int = None,
        scheduling_end_time: str = None,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
        scheduling_user_name: str = None,
        shift_name: str = None,
        skip_one_day: bool = None,
    ):
        self.cycle_order = cycle_order
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_start_time = scheduling_start_time
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list
        self.scheduling_user_name = scheduling_user_name
        self.shift_name = shift_name
        self.skip_one_day = skip_one_day

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cycle_order is not None:
            result['cycleOrder'] = self.cycle_order
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        if self.scheduling_user_name is not None:
            result['schedulingUserName'] = self.scheduling_user_name
        if self.shift_name is not None:
            result['shiftName'] = self.shift_name
        if self.skip_one_day is not None:
            result['skipOneDay'] = self.skip_one_day
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('cycleOrder') is not None:
            self.cycle_order = m.get('cycleOrder')
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        if m.get('schedulingUserName') is not None:
            self.scheduling_user_name = m.get('schedulingUserName')
        if m.get('shiftName') is not None:
            self.shift_name = m.get('shiftName')
        if m.get('skipOneDay') is not None:
            self.skip_one_day = m.get('skipOneDay')
        return self


class GetServiceGroupSchedulingResponseBodyDataFineSchedulingSchedulingTemplateFineShifts(TeaModel):
    def __init__(
        self,
        scheduling_end_time: str = None,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        scheduling_user_id: str = None,
        scheduling_user_id_list: List[int] = None,
        scheduling_user_name: str = None,
        shift_name: str = None,
        skip_one_day: bool = None,
    ):
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_start_time = scheduling_start_time
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list
        self.scheduling_user_name = scheduling_user_name
        self.shift_name = shift_name
        self.skip_one_day = skip_one_day

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        if self.scheduling_user_name is not None:
            result['schedulingUserName'] = self.scheduling_user_name
        if self.shift_name is not None:
            result['shiftName'] = self.shift_name
        if self.skip_one_day is not None:
            result['skipOneDay'] = self.skip_one_day
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        if m.get('schedulingUserName') is not None:
            self.scheduling_user_name = m.get('schedulingUserName')
        if m.get('shiftName') is not None:
            self.shift_name = m.get('shiftName')
        if m.get('skipOneDay') is not None:
            self.skip_one_day = m.get('skipOneDay')
        return self


class GetServiceGroupSchedulingResponseBodyDataFineScheduling(TeaModel):
    def __init__(
        self,
        id: int = None,
        period: int = None,
        period_unit: str = None,
        scheduling_fine_shifts: List[GetServiceGroupSchedulingResponseBodyDataFineSchedulingSchedulingFineShifts] = None,
        scheduling_template_fine_shifts: List[GetServiceGroupSchedulingResponseBodyDataFineSchedulingSchedulingTemplateFineShifts] = None,
        shift_type: str = None,
    ):
        # 1
        self.id = id
        # 1
        self.period = period
        self.period_unit = period_unit
        self.scheduling_fine_shifts = scheduling_fine_shifts
        self.scheduling_template_fine_shifts = scheduling_template_fine_shifts
        self.shift_type = shift_type

    def validate(self):
        if self.scheduling_fine_shifts:
            for k in self.scheduling_fine_shifts:
                if k:
                    k.validate()
        if self.scheduling_template_fine_shifts:
            for k in self.scheduling_template_fine_shifts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.period is not None:
            result['period'] = self.period
        if self.period_unit is not None:
            result['periodUnit'] = self.period_unit
        result['schedulingFineShifts'] = []
        if self.scheduling_fine_shifts is not None:
            for k in self.scheduling_fine_shifts:
                result['schedulingFineShifts'].append(k.to_map() if k else None)
        result['schedulingTemplateFineShifts'] = []
        if self.scheduling_template_fine_shifts is not None:
            for k in self.scheduling_template_fine_shifts:
                result['schedulingTemplateFineShifts'].append(k.to_map() if k else None)
        if self.shift_type is not None:
            result['shiftType'] = self.shift_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('period') is not None:
            self.period = m.get('period')
        if m.get('periodUnit') is not None:
            self.period_unit = m.get('periodUnit')
        self.scheduling_fine_shifts = []
        if m.get('schedulingFineShifts') is not None:
            for k in m.get('schedulingFineShifts'):
                temp_model = GetServiceGroupSchedulingResponseBodyDataFineSchedulingSchedulingFineShifts()
                self.scheduling_fine_shifts.append(temp_model.from_map(k))
        self.scheduling_template_fine_shifts = []
        if m.get('schedulingTemplateFineShifts') is not None:
            for k in m.get('schedulingTemplateFineShifts'):
                temp_model = GetServiceGroupSchedulingResponseBodyDataFineSchedulingSchedulingTemplateFineShifts()
                self.scheduling_template_fine_shifts.append(temp_model.from_map(k))
        if m.get('shiftType') is not None:
            self.shift_type = m.get('shiftType')
        return self


class GetServiceGroupSchedulingResponseBodyDataUsers(TeaModel):
    def __init__(
        self,
        user_id: int = None,
        user_name: str = None,
    ):
        self.user_id = user_id
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_name is not None:
            result['userName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userName') is not None:
            self.user_name = m.get('userName')
        return self


class GetServiceGroupSchedulingResponseBodyData(TeaModel):
    def __init__(
        self,
        fast_scheduling: GetServiceGroupSchedulingResponseBodyDataFastScheduling = None,
        fine_scheduling: GetServiceGroupSchedulingResponseBodyDataFineScheduling = None,
        scheduling_way: str = None,
        service_group_id: int = None,
        users: List[GetServiceGroupSchedulingResponseBodyDataUsers] = None,
    ):
        self.fast_scheduling = fast_scheduling
        self.fine_scheduling = fine_scheduling
        self.scheduling_way = scheduling_way
        self.service_group_id = service_group_id
        self.users = users

    def validate(self):
        if self.fast_scheduling:
            self.fast_scheduling.validate()
        if self.fine_scheduling:
            self.fine_scheduling.validate()
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.fast_scheduling is not None:
            result['fastScheduling'] = self.fast_scheduling.to_map()
        if self.fine_scheduling is not None:
            result['fineScheduling'] = self.fine_scheduling.to_map()
        if self.scheduling_way is not None:
            result['schedulingWay'] = self.scheduling_way
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        result['users'] = []
        if self.users is not None:
            for k in self.users:
                result['users'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fastScheduling') is not None:
            temp_model = GetServiceGroupSchedulingResponseBodyDataFastScheduling()
            self.fast_scheduling = temp_model.from_map(m['fastScheduling'])
        if m.get('fineScheduling') is not None:
            temp_model = GetServiceGroupSchedulingResponseBodyDataFineScheduling()
            self.fine_scheduling = temp_model.from_map(m['fineScheduling'])
        if m.get('schedulingWay') is not None:
            self.scheduling_way = m.get('schedulingWay')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        self.users = []
        if m.get('users') is not None:
            for k in m.get('users'):
                temp_model = GetServiceGroupSchedulingResponseBodyDataUsers()
                self.users.append(temp_model.from_map(k))
        return self


class GetServiceGroupSchedulingResponseBody(TeaModel):
    def __init__(
        self,
        data: GetServiceGroupSchedulingResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetServiceGroupSchedulingResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetServiceGroupSchedulingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetServiceGroupSchedulingResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetServiceGroupSchedulingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceGroupSchedulingPreviewRequestFastSchedulingSchedulingUsers(TeaModel):
    def __init__(
        self,
        scheduling_order: int = None,
        scheduling_user_id: int = None,
    ):
        self.scheduling_order = scheduling_order
        self.scheduling_user_id = scheduling_user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        return self


class GetServiceGroupSchedulingPreviewRequestFastScheduling(TeaModel):
    def __init__(
        self,
        duty_plan: str = None,
        scheduling_users: List[GetServiceGroupSchedulingPreviewRequestFastSchedulingSchedulingUsers] = None,
        single_duration: int = None,
        single_duration_unit: str = None,
    ):
        # FAST_CHOICE
        self.duty_plan = duty_plan
        self.scheduling_users = scheduling_users
        self.single_duration = single_duration
        # DAY
        self.single_duration_unit = single_duration_unit

    def validate(self):
        if self.scheduling_users:
            for k in self.scheduling_users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.duty_plan is not None:
            result['dutyPlan'] = self.duty_plan
        result['schedulingUsers'] = []
        if self.scheduling_users is not None:
            for k in self.scheduling_users:
                result['schedulingUsers'].append(k.to_map() if k else None)
        if self.single_duration is not None:
            result['singleDuration'] = self.single_duration
        if self.single_duration_unit is not None:
            result['singleDurationUnit'] = self.single_duration_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dutyPlan') is not None:
            self.duty_plan = m.get('dutyPlan')
        self.scheduling_users = []
        if m.get('schedulingUsers') is not None:
            for k in m.get('schedulingUsers'):
                temp_model = GetServiceGroupSchedulingPreviewRequestFastSchedulingSchedulingUsers()
                self.scheduling_users.append(temp_model.from_map(k))
        if m.get('singleDuration') is not None:
            self.single_duration = m.get('singleDuration')
        if m.get('singleDurationUnit') is not None:
            self.single_duration_unit = m.get('singleDurationUnit')
        return self


class GetServiceGroupSchedulingPreviewRequestFineSchedulingSchedulingFineShifts(TeaModel):
    def __init__(
        self,
        scheduling_end_time: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        shift_name: str = None,
    ):
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_order = scheduling_order
        self.scheduling_start_time = scheduling_start_time
        self.shift_name = shift_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.shift_name is not None:
            result['shiftName'] = self.shift_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('shiftName') is not None:
            self.shift_name = m.get('shiftName')
        return self


class GetServiceGroupSchedulingPreviewRequestFineScheduling(TeaModel):
    def __init__(
        self,
        period: int = None,
        period_unit: str = None,
        scheduling_fine_shifts: List[GetServiceGroupSchedulingPreviewRequestFineSchedulingSchedulingFineShifts] = None,
        shift_type: str = None,
    ):
        self.period = period
        self.period_unit = period_unit
        self.scheduling_fine_shifts = scheduling_fine_shifts
        self.shift_type = shift_type

    def validate(self):
        if self.scheduling_fine_shifts:
            for k in self.scheduling_fine_shifts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.period is not None:
            result['period'] = self.period
        if self.period_unit is not None:
            result['periodUnit'] = self.period_unit
        result['schedulingFineShifts'] = []
        if self.scheduling_fine_shifts is not None:
            for k in self.scheduling_fine_shifts:
                result['schedulingFineShifts'].append(k.to_map() if k else None)
        if self.shift_type is not None:
            result['shiftType'] = self.shift_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('period') is not None:
            self.period = m.get('period')
        if m.get('periodUnit') is not None:
            self.period_unit = m.get('periodUnit')
        self.scheduling_fine_shifts = []
        if m.get('schedulingFineShifts') is not None:
            for k in m.get('schedulingFineShifts'):
                temp_model = GetServiceGroupSchedulingPreviewRequestFineSchedulingSchedulingFineShifts()
                self.scheduling_fine_shifts.append(temp_model.from_map(k))
        if m.get('shiftType') is not None:
            self.shift_type = m.get('shiftType')
        return self


class GetServiceGroupSchedulingPreviewRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        end_time: str = None,
        fast_scheduling: GetServiceGroupSchedulingPreviewRequestFastScheduling = None,
        fine_scheduling: GetServiceGroupSchedulingPreviewRequestFineScheduling = None,
        scheduling_way: str = None,
        service_group_id: int = None,
        start_time: str = None,
    ):
        self.client_token = client_token
        self.end_time = end_time
        self.fast_scheduling = fast_scheduling
        self.fine_scheduling = fine_scheduling
        # This parameter is required.
        self.scheduling_way = scheduling_way
        # This parameter is required.
        self.service_group_id = service_group_id
        self.start_time = start_time

    def validate(self):
        if self.fast_scheduling:
            self.fast_scheduling.validate()
        if self.fine_scheduling:
            self.fine_scheduling.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.fast_scheduling is not None:
            result['fastScheduling'] = self.fast_scheduling.to_map()
        if self.fine_scheduling is not None:
            result['fineScheduling'] = self.fine_scheduling.to_map()
        if self.scheduling_way is not None:
            result['schedulingWay'] = self.scheduling_way
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.start_time is not None:
            result['startTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('fastScheduling') is not None:
            temp_model = GetServiceGroupSchedulingPreviewRequestFastScheduling()
            self.fast_scheduling = temp_model.from_map(m['fastScheduling'])
        if m.get('fineScheduling') is not None:
            temp_model = GetServiceGroupSchedulingPreviewRequestFineScheduling()
            self.fine_scheduling = temp_model.from_map(m['fineScheduling'])
        if m.get('schedulingWay') is not None:
            self.scheduling_way = m.get('schedulingWay')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        return self


class GetServiceGroupSchedulingPreviewResponseBody(TeaModel):
    def __init__(
        self,
        data: Dict[str, Any] = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetServiceGroupSchedulingPreviewResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetServiceGroupSchedulingPreviewResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetServiceGroupSchedulingPreviewResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetServiceGroupSpecialPersonSchedulingRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_group_id: int = None,
        user_id: int = None,
    ):
        self.client_token = client_token
        self.service_group_id = service_group_id
        # This parameter is required.
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class GetServiceGroupSpecialPersonSchedulingResponseBodyData(TeaModel):
    def __init__(
        self,
        scheduling_date: str = None,
        scheduling_end_time: str = None,
        scheduling_start_time: str = None,
        scheduling_user_id: int = None,
        service_group_id: int = None,
        service_group_name: str = None,
    ):
        self.scheduling_date = scheduling_date
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_start_time = scheduling_start_time
        self.scheduling_user_id = scheduling_user_id
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_date is not None:
            result['schedulingDate'] = self.scheduling_date
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingDate') is not None:
            self.scheduling_date = m.get('schedulingDate')
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        return self


class GetServiceGroupSpecialPersonSchedulingResponseBody(TeaModel):
    def __init__(
        self,
        data: List[GetServiceGroupSpecialPersonSchedulingResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = GetServiceGroupSpecialPersonSchedulingResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetServiceGroupSpecialPersonSchedulingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetServiceGroupSpecialPersonSchedulingResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetServiceGroupSpecialPersonSchedulingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSimilarIncidentStatisticsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        create_time: str = None,
        events: List[str] = None,
        incident_id: int = None,
        incident_title: str = None,
        related_service_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.create_time = create_time
        # This parameter is required.
        self.events = events
        # This parameter is required.
        self.incident_id = incident_id
        # This parameter is required.
        self.incident_title = incident_title
        # This parameter is required.
        self.related_service_id = related_service_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.events is not None:
            result['events'] = self.events
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('events') is not None:
            self.events = m.get('events')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        return self


class GetSimilarIncidentStatisticsResponseBodyDataDailySimilarIncidentsSimilarIncidents(TeaModel):
    def __init__(
        self,
        assign_user_id: int = None,
        assign_user_name: str = None,
        create_time: str = None,
        duration_time: int = None,
        finish_reason: int = None,
        finish_reason_description: str = None,
        finish_solution_description: str = None,
        incident_finish_solution: int = None,
        incident_id: int = None,
        incident_number: str = None,
        incident_title: str = None,
        related_route_rule_id: int = None,
        related_route_rule_name: str = None,
        similar_score: str = None,
    ):
        self.assign_user_id = assign_user_id
        self.assign_user_name = assign_user_name
        self.create_time = create_time
        self.duration_time = duration_time
        self.finish_reason = finish_reason
        self.finish_reason_description = finish_reason_description
        self.finish_solution_description = finish_solution_description
        self.incident_finish_solution = incident_finish_solution
        self.incident_id = incident_id
        self.incident_number = incident_number
        self.incident_title = incident_title
        self.related_route_rule_id = related_route_rule_id
        self.related_route_rule_name = related_route_rule_name
        self.similar_score = similar_score

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_user_id is not None:
            result['assignUserId'] = self.assign_user_id
        if self.assign_user_name is not None:
            result['assignUserName'] = self.assign_user_name
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.duration_time is not None:
            result['durationTime'] = self.duration_time
        if self.finish_reason is not None:
            result['finishReason'] = self.finish_reason
        if self.finish_reason_description is not None:
            result['finishReasonDescription'] = self.finish_reason_description
        if self.finish_solution_description is not None:
            result['finishSolutionDescription'] = self.finish_solution_description
        if self.incident_finish_solution is not None:
            result['incidentFinishSolution'] = self.incident_finish_solution
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_number is not None:
            result['incidentNumber'] = self.incident_number
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.related_route_rule_id is not None:
            result['relatedRouteRuleId'] = self.related_route_rule_id
        if self.related_route_rule_name is not None:
            result['relatedRouteRuleName'] = self.related_route_rule_name
        if self.similar_score is not None:
            result['similarScore'] = self.similar_score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignUserId') is not None:
            self.assign_user_id = m.get('assignUserId')
        if m.get('assignUserName') is not None:
            self.assign_user_name = m.get('assignUserName')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('durationTime') is not None:
            self.duration_time = m.get('durationTime')
        if m.get('finishReason') is not None:
            self.finish_reason = m.get('finishReason')
        if m.get('finishReasonDescription') is not None:
            self.finish_reason_description = m.get('finishReasonDescription')
        if m.get('finishSolutionDescription') is not None:
            self.finish_solution_description = m.get('finishSolutionDescription')
        if m.get('incidentFinishSolution') is not None:
            self.incident_finish_solution = m.get('incidentFinishSolution')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentNumber') is not None:
            self.incident_number = m.get('incidentNumber')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('relatedRouteRuleId') is not None:
            self.related_route_rule_id = m.get('relatedRouteRuleId')
        if m.get('relatedRouteRuleName') is not None:
            self.related_route_rule_name = m.get('relatedRouteRuleName')
        if m.get('similarScore') is not None:
            self.similar_score = m.get('similarScore')
        return self


class GetSimilarIncidentStatisticsResponseBodyDataDailySimilarIncidents(TeaModel):
    def __init__(
        self,
        commitment: int = None,
        date: str = None,
        day: int = None,
        month: int = None,
        similar_incidents: List[GetSimilarIncidentStatisticsResponseBodyDataDailySimilarIncidentsSimilarIncidents] = None,
        week: str = None,
    ):
        self.commitment = commitment
        self.date = date
        self.day = day
        self.month = month
        self.similar_incidents = similar_incidents
        self.week = week

    def validate(self):
        if self.similar_incidents:
            for k in self.similar_incidents:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.commitment is not None:
            result['commitment'] = self.commitment
        if self.date is not None:
            result['date'] = self.date
        if self.day is not None:
            result['day'] = self.day
        if self.month is not None:
            result['month'] = self.month
        result['similarIncidents'] = []
        if self.similar_incidents is not None:
            for k in self.similar_incidents:
                result['similarIncidents'].append(k.to_map() if k else None)
        if self.week is not None:
            result['week'] = self.week
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('commitment') is not None:
            self.commitment = m.get('commitment')
        if m.get('date') is not None:
            self.date = m.get('date')
        if m.get('day') is not None:
            self.day = m.get('day')
        if m.get('month') is not None:
            self.month = m.get('month')
        self.similar_incidents = []
        if m.get('similarIncidents') is not None:
            for k in m.get('similarIncidents'):
                temp_model = GetSimilarIncidentStatisticsResponseBodyDataDailySimilarIncidentsSimilarIncidents()
                self.similar_incidents.append(temp_model.from_map(k))
        if m.get('week') is not None:
            self.week = m.get('week')
        return self


class GetSimilarIncidentStatisticsResponseBodyDataTopFiveIncidents(TeaModel):
    def __init__(
        self,
        assign_user_id: str = None,
        assign_user_name: str = None,
        create_time: str = None,
        duration_time: int = None,
        finish_reason: int = None,
        finish_reason_description: str = None,
        finish_solution_description: str = None,
        incident_finish_solution: int = None,
        incident_id: int = None,
        incident_number: str = None,
        incident_title: str = None,
        related_route_rule_id: int = None,
        related_route_rule_name: str = None,
        similar_score: str = None,
    ):
        self.assign_user_id = assign_user_id
        self.assign_user_name = assign_user_name
        self.create_time = create_time
        self.duration_time = duration_time
        self.finish_reason = finish_reason
        self.finish_reason_description = finish_reason_description
        self.finish_solution_description = finish_solution_description
        self.incident_finish_solution = incident_finish_solution
        self.incident_id = incident_id
        self.incident_number = incident_number
        self.incident_title = incident_title
        self.related_route_rule_id = related_route_rule_id
        self.related_route_rule_name = related_route_rule_name
        self.similar_score = similar_score

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_user_id is not None:
            result['assignUserId'] = self.assign_user_id
        if self.assign_user_name is not None:
            result['assignUserName'] = self.assign_user_name
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.duration_time is not None:
            result['durationTime'] = self.duration_time
        if self.finish_reason is not None:
            result['finishReason'] = self.finish_reason
        if self.finish_reason_description is not None:
            result['finishReasonDescription'] = self.finish_reason_description
        if self.finish_solution_description is not None:
            result['finishSolutionDescription'] = self.finish_solution_description
        if self.incident_finish_solution is not None:
            result['incidentFinishSolution'] = self.incident_finish_solution
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_number is not None:
            result['incidentNumber'] = self.incident_number
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.related_route_rule_id is not None:
            result['relatedRouteRuleId'] = self.related_route_rule_id
        if self.related_route_rule_name is not None:
            result['relatedRouteRuleName'] = self.related_route_rule_name
        if self.similar_score is not None:
            result['similarScore'] = self.similar_score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignUserId') is not None:
            self.assign_user_id = m.get('assignUserId')
        if m.get('assignUserName') is not None:
            self.assign_user_name = m.get('assignUserName')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('durationTime') is not None:
            self.duration_time = m.get('durationTime')
        if m.get('finishReason') is not None:
            self.finish_reason = m.get('finishReason')
        if m.get('finishReasonDescription') is not None:
            self.finish_reason_description = m.get('finishReasonDescription')
        if m.get('finishSolutionDescription') is not None:
            self.finish_solution_description = m.get('finishSolutionDescription')
        if m.get('incidentFinishSolution') is not None:
            self.incident_finish_solution = m.get('incidentFinishSolution')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentNumber') is not None:
            self.incident_number = m.get('incidentNumber')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('relatedRouteRuleId') is not None:
            self.related_route_rule_id = m.get('relatedRouteRuleId')
        if m.get('relatedRouteRuleName') is not None:
            self.related_route_rule_name = m.get('relatedRouteRuleName')
        if m.get('similarScore') is not None:
            self.similar_score = m.get('similarScore')
        return self


class GetSimilarIncidentStatisticsResponseBodyData(TeaModel):
    def __init__(
        self,
        count_in_seven_days: int = None,
        count_in_six_months: int = None,
        daily_similar_incidents: List[GetSimilarIncidentStatisticsResponseBodyDataDailySimilarIncidents] = None,
        request_id: str = None,
        top_five_incidents: List[GetSimilarIncidentStatisticsResponseBodyDataTopFiveIncidents] = None,
    ):
        self.count_in_seven_days = count_in_seven_days
        self.count_in_six_months = count_in_six_months
        self.daily_similar_incidents = daily_similar_incidents
        # id of the request
        self.request_id = request_id
        # topFiveIncidents
        self.top_five_incidents = top_five_incidents

    def validate(self):
        if self.daily_similar_incidents:
            for k in self.daily_similar_incidents:
                if k:
                    k.validate()
        if self.top_five_incidents:
            for k in self.top_five_incidents:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.count_in_seven_days is not None:
            result['countInSevenDays'] = self.count_in_seven_days
        if self.count_in_six_months is not None:
            result['countInSixMonths'] = self.count_in_six_months
        result['dailySimilarIncidents'] = []
        if self.daily_similar_incidents is not None:
            for k in self.daily_similar_incidents:
                result['dailySimilarIncidents'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        result['topFiveIncidents'] = []
        if self.top_five_incidents is not None:
            for k in self.top_five_incidents:
                result['topFiveIncidents'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('countInSevenDays') is not None:
            self.count_in_seven_days = m.get('countInSevenDays')
        if m.get('countInSixMonths') is not None:
            self.count_in_six_months = m.get('countInSixMonths')
        self.daily_similar_incidents = []
        if m.get('dailySimilarIncidents') is not None:
            for k in m.get('dailySimilarIncidents'):
                temp_model = GetSimilarIncidentStatisticsResponseBodyDataDailySimilarIncidents()
                self.daily_similar_incidents.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        self.top_five_incidents = []
        if m.get('topFiveIncidents') is not None:
            for k in m.get('topFiveIncidents'):
                temp_model = GetSimilarIncidentStatisticsResponseBodyDataTopFiveIncidents()
                self.top_five_incidents.append(temp_model.from_map(k))
        return self


class GetSimilarIncidentStatisticsResponseBody(TeaModel):
    def __init__(
        self,
        data: GetSimilarIncidentStatisticsResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetSimilarIncidentStatisticsResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetSimilarIncidentStatisticsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetSimilarIncidentStatisticsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetSimilarIncidentStatisticsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetSubscriptionRequest(TeaModel):
    def __init__(
        self,
        not_filter_scope_object_deleted: bool = None,
        subscription_id: int = None,
    ):
        self.not_filter_scope_object_deleted = not_filter_scope_object_deleted
        self.subscription_id = subscription_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.not_filter_scope_object_deleted is not None:
            result['notFilterScopeObjectDeleted'] = self.not_filter_scope_object_deleted
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('notFilterScopeObjectDeleted') is not None:
            self.not_filter_scope_object_deleted = m.get('notFilterScopeObjectDeleted')
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        return self


class GetSubscriptionResponseBodyDataNotifyObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        name: str = None,
        notify_object_id: int = None,
        notify_object_type: int = None,
    ):
        self.id = id
        self.name = name
        self.notify_object_id = notify_object_id
        self.notify_object_type = notify_object_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        if self.notify_object_id is not None:
            result['notifyObjectId'] = self.notify_object_id
        if self.notify_object_type is not None:
            result['notifyObjectType'] = self.notify_object_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('notifyObjectId') is not None:
            self.notify_object_id = m.get('notifyObjectId')
        if m.get('notifyObjectType') is not None:
            self.notify_object_type = m.get('notifyObjectType')
        return self


class GetSubscriptionResponseBodyDataNotifyStrategyListStrategiesConditions(TeaModel):
    def __init__(
        self,
        action: str = None,
        effection: str = None,
        level: str = None,
        problem_notify_type: str = None,
    ):
        self.action = action
        self.effection = effection
        self.level = level
        self.problem_notify_type = problem_notify_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['action'] = self.action
        if self.effection is not None:
            result['effection'] = self.effection
        if self.level is not None:
            result['level'] = self.level
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('action') is not None:
            self.action = m.get('action')
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('level') is not None:
            self.level = m.get('level')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        return self


class GetSubscriptionResponseBodyDataNotifyStrategyListStrategiesPeriodChannel(TeaModel):
    def __init__(
        self,
        non_workday: str = None,
        workday: str = None,
    ):
        self.non_workday = non_workday
        self.workday = workday

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.non_workday is not None:
            result['nonWorkday'] = self.non_workday
        if self.workday is not None:
            result['workday'] = self.workday
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('nonWorkday') is not None:
            self.non_workday = m.get('nonWorkday')
        if m.get('workday') is not None:
            self.workday = m.get('workday')
        return self


class GetSubscriptionResponseBodyDataNotifyStrategyListStrategies(TeaModel):
    def __init__(
        self,
        channels: str = None,
        conditions: List[GetSubscriptionResponseBodyDataNotifyStrategyListStrategiesConditions] = None,
        id: int = None,
        period_channel: GetSubscriptionResponseBodyDataNotifyStrategyListStrategiesPeriodChannel = None,
    ):
        self.channels = channels
        self.conditions = conditions
        self.id = id
        self.period_channel = period_channel

    def validate(self):
        if self.conditions:
            for k in self.conditions:
                if k:
                    k.validate()
        if self.period_channel:
            self.period_channel.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channels is not None:
            result['channels'] = self.channels
        result['conditions'] = []
        if self.conditions is not None:
            for k in self.conditions:
                result['conditions'].append(k.to_map() if k else None)
        if self.id is not None:
            result['id'] = self.id
        if self.period_channel is not None:
            result['periodChannel'] = self.period_channel.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('channels') is not None:
            self.channels = m.get('channels')
        self.conditions = []
        if m.get('conditions') is not None:
            for k in m.get('conditions'):
                temp_model = GetSubscriptionResponseBodyDataNotifyStrategyListStrategiesConditions()
                self.conditions.append(temp_model.from_map(k))
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('periodChannel') is not None:
            temp_model = GetSubscriptionResponseBodyDataNotifyStrategyListStrategiesPeriodChannel()
            self.period_channel = temp_model.from_map(m['periodChannel'])
        return self


class GetSubscriptionResponseBodyDataNotifyStrategyList(TeaModel):
    def __init__(
        self,
        instance_type: int = None,
        strategies: List[GetSubscriptionResponseBodyDataNotifyStrategyListStrategies] = None,
    ):
        self.instance_type = instance_type
        self.strategies = strategies

    def validate(self):
        if self.strategies:
            for k in self.strategies:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        result['strategies'] = []
        if self.strategies is not None:
            for k in self.strategies:
                result['strategies'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        self.strategies = []
        if m.get('strategies') is not None:
            for k in m.get('strategies'):
                temp_model = GetSubscriptionResponseBodyDataNotifyStrategyListStrategies()
                self.strategies.append(temp_model.from_map(k))
        return self


class GetSubscriptionResponseBodyDataScopeObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        is_valid: int = None,
        scope: str = None,
        scope_object: str = None,
        scope_object_id: int = None,
    ):
        self.id = id
        self.is_valid = is_valid
        self.scope = scope
        self.scope_object = scope_object
        self.scope_object_id = scope_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.is_valid is not None:
            result['isValid'] = self.is_valid
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object is not None:
            result['scopeObject'] = self.scope_object
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('isValid') is not None:
            self.is_valid = m.get('isValid')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObject') is not None:
            self.scope_object = m.get('scopeObject')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        return self


class GetSubscriptionResponseBodyData(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        expired_type: str = None,
        notify_object_list: List[GetSubscriptionResponseBodyDataNotifyObjectList] = None,
        notify_object_type: str = None,
        notify_strategy_list: List[GetSubscriptionResponseBodyDataNotifyStrategyList] = None,
        period: str = None,
        scope: str = None,
        scope_object_list: List[GetSubscriptionResponseBodyDataScopeObjectList] = None,
        start_time: str = None,
        status: str = None,
        subscription_id: int = None,
        subscription_title: str = None,
    ):
        self.end_time = end_time
        self.expired_type = expired_type
        self.notify_object_list = notify_object_list
        self.notify_object_type = notify_object_type
        self.notify_strategy_list = notify_strategy_list
        self.period = period
        self.scope = scope
        # Array
        self.scope_object_list = scope_object_list
        self.start_time = start_time
        self.status = status
        self.subscription_id = subscription_id
        self.subscription_title = subscription_title

    def validate(self):
        if self.notify_object_list:
            for k in self.notify_object_list:
                if k:
                    k.validate()
        if self.notify_strategy_list:
            for k in self.notify_strategy_list:
                if k:
                    k.validate()
        if self.scope_object_list:
            for k in self.scope_object_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.expired_type is not None:
            result['expiredType'] = self.expired_type
        result['notifyObjectList'] = []
        if self.notify_object_list is not None:
            for k in self.notify_object_list:
                result['notifyObjectList'].append(k.to_map() if k else None)
        if self.notify_object_type is not None:
            result['notifyObjectType'] = self.notify_object_type
        result['notifyStrategyList'] = []
        if self.notify_strategy_list is not None:
            for k in self.notify_strategy_list:
                result['notifyStrategyList'].append(k.to_map() if k else None)
        if self.period is not None:
            result['period'] = self.period
        if self.scope is not None:
            result['scope'] = self.scope
        result['scopeObjectList'] = []
        if self.scope_object_list is not None:
            for k in self.scope_object_list:
                result['scopeObjectList'].append(k.to_map() if k else None)
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.status is not None:
            result['status'] = self.status
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        if self.subscription_title is not None:
            result['subscriptionTitle'] = self.subscription_title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('expiredType') is not None:
            self.expired_type = m.get('expiredType')
        self.notify_object_list = []
        if m.get('notifyObjectList') is not None:
            for k in m.get('notifyObjectList'):
                temp_model = GetSubscriptionResponseBodyDataNotifyObjectList()
                self.notify_object_list.append(temp_model.from_map(k))
        if m.get('notifyObjectType') is not None:
            self.notify_object_type = m.get('notifyObjectType')
        self.notify_strategy_list = []
        if m.get('notifyStrategyList') is not None:
            for k in m.get('notifyStrategyList'):
                temp_model = GetSubscriptionResponseBodyDataNotifyStrategyList()
                self.notify_strategy_list.append(temp_model.from_map(k))
        if m.get('period') is not None:
            self.period = m.get('period')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        self.scope_object_list = []
        if m.get('scopeObjectList') is not None:
            for k in m.get('scopeObjectList'):
                temp_model = GetSubscriptionResponseBodyDataScopeObjectList()
                self.scope_object_list.append(temp_model.from_map(k))
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        if m.get('subscriptionTitle') is not None:
            self.subscription_title = m.get('subscriptionTitle')
        return self


class GetSubscriptionResponseBody(TeaModel):
    def __init__(
        self,
        data: GetSubscriptionResponseBodyData = None,
        request_id: str = None,
    ):
        # Object
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetSubscriptionResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetSubscriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetSubscriptionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetSubscriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTenantApplicationRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        # This parameter is required.
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class GetTenantApplicationResponseBodyData(TeaModel):
    def __init__(
        self,
        biz_id: str = None,
        channel: str = None,
        corporation_id: str = None,
        original_corp_id: str = None,
        progress: str = None,
    ):
        self.biz_id = biz_id
        self.channel = channel
        self.corporation_id = corporation_id
        self.original_corp_id = original_corp_id
        self.progress = progress

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.biz_id is not None:
            result['bizId'] = self.biz_id
        if self.channel is not None:
            result['channel'] = self.channel
        if self.corporation_id is not None:
            result['corporationId'] = self.corporation_id
        if self.original_corp_id is not None:
            result['originalCorpId'] = self.original_corp_id
        if self.progress is not None:
            result['progress'] = self.progress
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('bizId') is not None:
            self.biz_id = m.get('bizId')
        if m.get('channel') is not None:
            self.channel = m.get('channel')
        if m.get('corporationId') is not None:
            self.corporation_id = m.get('corporationId')
        if m.get('originalCorpId') is not None:
            self.original_corp_id = m.get('originalCorpId')
        if m.get('progress') is not None:
            self.progress = m.get('progress')
        return self


class GetTenantApplicationResponseBody(TeaModel):
    def __init__(
        self,
        data: GetTenantApplicationResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetTenantApplicationResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetTenantApplicationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTenantApplicationResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetTenantApplicationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTenantStatusRequest(TeaModel):
    def __init__(
        self,
        tenant_ram_id: int = None,
    ):
        # This parameter is required.
        self.tenant_ram_id = tenant_ram_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.tenant_ram_id is not None:
            result['tenantRamId'] = self.tenant_ram_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('tenantRamId') is not None:
            self.tenant_ram_id = m.get('tenantRamId')
        return self


class GetTenantStatusResponseBodyData(TeaModel):
    def __init__(
        self,
        tenant_status: int = None,
    ):
        self.tenant_status = tenant_status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.tenant_status is not None:
            result['tenantStatus'] = self.tenant_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('tenantStatus') is not None:
            self.tenant_status = m.get('tenantStatus')
        return self


class GetTenantStatusResponseBody(TeaModel):
    def __init__(
        self,
        data: GetTenantStatusResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetTenantStatusResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetTenantStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTenantStatusResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetTenantStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetUserRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        user_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class GetUserResponseBodyDataServiceGroups(TeaModel):
    def __init__(
        self,
        name: str = None,
        service_group_id: int = None,
    ):
        self.name = name
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class GetUserResponseBodyData(TeaModel):
    def __init__(
        self,
        account_type: str = None,
        create_time: str = None,
        email: str = None,
        is_active: int = None,
        is_editable_user: bool = None,
        is_related: str = None,
        phone: str = None,
        ram_id: str = None,
        role_id_list: List[int] = None,
        role_name_list: List[str] = None,
        service_groups: List[GetUserResponseBodyDataServiceGroups] = None,
        user_id: int = None,
        username: str = None,
    ):
        self.account_type = account_type
        self.create_time = create_time
        # email
        self.email = email
        self.is_active = is_active
        self.is_editable_user = is_editable_user
        self.is_related = is_related
        self.phone = phone
        # ramId
        self.ram_id = ram_id
        self.role_id_list = role_id_list
        self.role_name_list = role_name_list
        self.service_groups = service_groups
        self.user_id = user_id
        self.username = username

    def validate(self):
        if self.service_groups:
            for k in self.service_groups:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_type is not None:
            result['accountType'] = self.account_type
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.email is not None:
            result['email'] = self.email
        if self.is_active is not None:
            result['isActive'] = self.is_active
        if self.is_editable_user is not None:
            result['isEditableUser'] = self.is_editable_user
        if self.is_related is not None:
            result['isRelated'] = self.is_related
        if self.phone is not None:
            result['phone'] = self.phone
        if self.ram_id is not None:
            result['ramId'] = self.ram_id
        if self.role_id_list is not None:
            result['roleIdList'] = self.role_id_list
        if self.role_name_list is not None:
            result['roleNameList'] = self.role_name_list
        result['serviceGroups'] = []
        if self.service_groups is not None:
            for k in self.service_groups:
                result['serviceGroups'].append(k.to_map() if k else None)
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accountType') is not None:
            self.account_type = m.get('accountType')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('email') is not None:
            self.email = m.get('email')
        if m.get('isActive') is not None:
            self.is_active = m.get('isActive')
        if m.get('isEditableUser') is not None:
            self.is_editable_user = m.get('isEditableUser')
        if m.get('isRelated') is not None:
            self.is_related = m.get('isRelated')
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('ramId') is not None:
            self.ram_id = m.get('ramId')
        if m.get('roleIdList') is not None:
            self.role_id_list = m.get('roleIdList')
        if m.get('roleNameList') is not None:
            self.role_name_list = m.get('roleNameList')
        self.service_groups = []
        if m.get('serviceGroups') is not None:
            for k in m.get('serviceGroups'):
                temp_model = GetUserResponseBodyDataServiceGroups()
                self.service_groups.append(temp_model.from_map(k))
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class GetUserResponseBody(TeaModel):
    def __init__(
        self,
        data: GetUserResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = GetUserResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetUserGuideStatusRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class GetUserGuideStatusResponseBody(TeaModel):
    def __init__(
        self,
        data: Dict[str, Any] = None,
        request_id: str = None,
    ):
        # map
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class GetUserGuideStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetUserGuideStatusResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetUserGuideStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAlertsRequest(TeaModel):
    def __init__(
        self,
        alert_level: str = None,
        alert_name: str = None,
        alert_source_name: str = None,
        end_time: str = None,
        monitor_source_id: str = None,
        page_number: int = None,
        page_size: int = None,
        related_service_id: int = None,
        rule_name: str = None,
        start_time: str = None,
    ):
        self.alert_level = alert_level
        self.alert_name = alert_name
        self.alert_source_name = alert_source_name
        # 2020-09-10 21:00:00
        self.end_time = end_time
        self.monitor_source_id = monitor_source_id
        self.page_number = page_number
        self.page_size = page_size
        self.related_service_id = related_service_id
        self.rule_name = rule_name
        # 2020-09-10 13:00:00
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alert_level is not None:
            result['alertLevel'] = self.alert_level
        if self.alert_name is not None:
            result['alertName'] = self.alert_name
        if self.alert_source_name is not None:
            result['alertSourceName'] = self.alert_source_name
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        if self.start_time is not None:
            result['startTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('alertLevel') is not None:
            self.alert_level = m.get('alertLevel')
        if m.get('alertName') is not None:
            self.alert_name = m.get('alertName')
        if m.get('alertSourceName') is not None:
            self.alert_source_name = m.get('alertSourceName')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        return self


class ListAlertsResponseBodyData(TeaModel):
    def __init__(
        self,
        alert_id: int = None,
        alert_level: str = None,
        alert_number: str = None,
        alert_source_name: str = None,
        create_time: str = None,
        first_event_time: str = None,
        monitor_source_name: str = None,
        rel_service_delete_type: int = None,
        related_service_name: str = None,
        route_rule_delete_type: int = None,
        route_rule_id: int = None,
        route_rule_name: str = None,
        source_event_count: int = None,
        title: str = None,
    ):
        self.alert_id = alert_id
        self.alert_level = alert_level
        self.alert_number = alert_number
        self.alert_source_name = alert_source_name
        self.create_time = create_time
        self.first_event_time = first_event_time
        self.monitor_source_name = monitor_source_name
        self.rel_service_delete_type = rel_service_delete_type
        self.related_service_name = related_service_name
        self.route_rule_delete_type = route_rule_delete_type
        self.route_rule_id = route_rule_id
        self.route_rule_name = route_rule_name
        self.source_event_count = source_event_count
        self.title = title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.alert_id is not None:
            result['alertId'] = self.alert_id
        if self.alert_level is not None:
            result['alertLevel'] = self.alert_level
        if self.alert_number is not None:
            result['alertNumber'] = self.alert_number
        if self.alert_source_name is not None:
            result['alertSourceName'] = self.alert_source_name
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.first_event_time is not None:
            result['firstEventTime'] = self.first_event_time
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.rel_service_delete_type is not None:
            result['relServiceDeleteType'] = self.rel_service_delete_type
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.route_rule_delete_type is not None:
            result['routeRuleDeleteType'] = self.route_rule_delete_type
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.route_rule_name is not None:
            result['routeRuleName'] = self.route_rule_name
        if self.source_event_count is not None:
            result['sourceEventCount'] = self.source_event_count
        if self.title is not None:
            result['title'] = self.title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('alertId') is not None:
            self.alert_id = m.get('alertId')
        if m.get('alertLevel') is not None:
            self.alert_level = m.get('alertLevel')
        if m.get('alertNumber') is not None:
            self.alert_number = m.get('alertNumber')
        if m.get('alertSourceName') is not None:
            self.alert_source_name = m.get('alertSourceName')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('firstEventTime') is not None:
            self.first_event_time = m.get('firstEventTime')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('relServiceDeleteType') is not None:
            self.rel_service_delete_type = m.get('relServiceDeleteType')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('routeRuleDeleteType') is not None:
            self.route_rule_delete_type = m.get('routeRuleDeleteType')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('routeRuleName') is not None:
            self.route_rule_name = m.get('routeRuleName')
        if m.get('sourceEventCount') is not None:
            self.source_event_count = m.get('sourceEventCount')
        if m.get('title') is not None:
            self.title = m.get('title')
        return self


class ListAlertsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListAlertsResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListAlertsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListAlertsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListAlertsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListAlertsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListByMonitorSourceIdRequest(TeaModel):
    def __init__(
        self,
        monitor_source_id: str = None,
    ):
        self.monitor_source_id = monitor_source_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        return self


class ListByMonitorSourceIdResponseBodyData(TeaModel):
    def __init__(
        self,
        id: int = None,
        rule_name: str = None,
    ):
        self.id = id
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        return self


class ListByMonitorSourceIdResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListByMonitorSourceIdResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListByMonitorSourceIdResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListByMonitorSourceIdResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListByMonitorSourceIdResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListByMonitorSourceIdResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListChartDataForServiceGroupRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        end_time: str = None,
        start_time: str = None,
    ):
        # clientToken
        self.client_token = client_token
        self.end_time = end_time
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.start_time is not None:
            result['startTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        return self


class ListChartDataForServiceGroupResponseBodyData(TeaModel):
    def __init__(
        self,
        effection_level: Dict[str, Any] = None,
        escalation_incident_count: int = None,
        incident_count: int = None,
        mean_time_to_acknowledge: int = None,
        mean_time_to_repair: int = None,
        time: str = None,
        total_mean_time_to_acknowledge: int = None,
        total_mean_time_to_repair: int = None,
        un_acknowledged_escalation_incident_count: int = None,
        un_finish_escalation_incident_count: int = None,
    ):
        self.effection_level = effection_level
        self.escalation_incident_count = escalation_incident_count
        self.incident_count = incident_count
        self.mean_time_to_acknowledge = mean_time_to_acknowledge
        self.mean_time_to_repair = mean_time_to_repair
        self.time = time
        self.total_mean_time_to_acknowledge = total_mean_time_to_acknowledge
        self.total_mean_time_to_repair = total_mean_time_to_repair
        self.un_acknowledged_escalation_incident_count = un_acknowledged_escalation_incident_count
        self.un_finish_escalation_incident_count = un_finish_escalation_incident_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.effection_level is not None:
            result['effectionLevel'] = self.effection_level
        if self.escalation_incident_count is not None:
            result['escalationIncidentCount'] = self.escalation_incident_count
        if self.incident_count is not None:
            result['incidentCount'] = self.incident_count
        if self.mean_time_to_acknowledge is not None:
            result['meanTimeToAcknowledge'] = self.mean_time_to_acknowledge
        if self.mean_time_to_repair is not None:
            result['meanTimeToRepair'] = self.mean_time_to_repair
        if self.time is not None:
            result['time'] = self.time
        if self.total_mean_time_to_acknowledge is not None:
            result['totalMeanTimeToAcknowledge'] = self.total_mean_time_to_acknowledge
        if self.total_mean_time_to_repair is not None:
            result['totalMeanTimeToRepair'] = self.total_mean_time_to_repair
        if self.un_acknowledged_escalation_incident_count is not None:
            result['unAcknowledgedEscalationIncidentCount'] = self.un_acknowledged_escalation_incident_count
        if self.un_finish_escalation_incident_count is not None:
            result['unFinishEscalationIncidentCount'] = self.un_finish_escalation_incident_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('effectionLevel') is not None:
            self.effection_level = m.get('effectionLevel')
        if m.get('escalationIncidentCount') is not None:
            self.escalation_incident_count = m.get('escalationIncidentCount')
        if m.get('incidentCount') is not None:
            self.incident_count = m.get('incidentCount')
        if m.get('meanTimeToAcknowledge') is not None:
            self.mean_time_to_acknowledge = m.get('meanTimeToAcknowledge')
        if m.get('meanTimeToRepair') is not None:
            self.mean_time_to_repair = m.get('meanTimeToRepair')
        if m.get('time') is not None:
            self.time = m.get('time')
        if m.get('totalMeanTimeToAcknowledge') is not None:
            self.total_mean_time_to_acknowledge = m.get('totalMeanTimeToAcknowledge')
        if m.get('totalMeanTimeToRepair') is not None:
            self.total_mean_time_to_repair = m.get('totalMeanTimeToRepair')
        if m.get('unAcknowledgedEscalationIncidentCount') is not None:
            self.un_acknowledged_escalation_incident_count = m.get('unAcknowledgedEscalationIncidentCount')
        if m.get('unFinishEscalationIncidentCount') is not None:
            self.un_finish_escalation_incident_count = m.get('unFinishEscalationIncidentCount')
        return self


class ListChartDataForServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListChartDataForServiceGroupResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListChartDataForServiceGroupResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListChartDataForServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListChartDataForServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListChartDataForServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListChartDataForUserRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        end_time: str = None,
        start_time: str = None,
    ):
        # clientToken
        self.client_token = client_token
        self.end_time = end_time
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.start_time is not None:
            result['startTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        return self


class ListChartDataForUserResponseBodyData(TeaModel):
    def __init__(
        self,
        effection_level: Dict[str, Any] = None,
        escalation_incident_count: int = None,
        incident_count: int = None,
        mean_time_to_acknowledge: int = None,
        mean_time_to_repair: int = None,
        time: str = None,
        total_mean_time_to_acknowledge: int = None,
        total_mean_time_to_repair: int = None,
        un_acknowledged_escalation_incident_count: int = None,
        un_finish_escalation_incident_count: int = None,
    ):
        self.effection_level = effection_level
        self.escalation_incident_count = escalation_incident_count
        self.incident_count = incident_count
        self.mean_time_to_acknowledge = mean_time_to_acknowledge
        self.mean_time_to_repair = mean_time_to_repair
        self.time = time
        self.total_mean_time_to_acknowledge = total_mean_time_to_acknowledge
        self.total_mean_time_to_repair = total_mean_time_to_repair
        self.un_acknowledged_escalation_incident_count = un_acknowledged_escalation_incident_count
        self.un_finish_escalation_incident_count = un_finish_escalation_incident_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.effection_level is not None:
            result['effectionLevel'] = self.effection_level
        if self.escalation_incident_count is not None:
            result['escalationIncidentCount'] = self.escalation_incident_count
        if self.incident_count is not None:
            result['incidentCount'] = self.incident_count
        if self.mean_time_to_acknowledge is not None:
            result['meanTimeToAcknowledge'] = self.mean_time_to_acknowledge
        if self.mean_time_to_repair is not None:
            result['meanTimeToRepair'] = self.mean_time_to_repair
        if self.time is not None:
            result['time'] = self.time
        if self.total_mean_time_to_acknowledge is not None:
            result['totalMeanTimeToAcknowledge'] = self.total_mean_time_to_acknowledge
        if self.total_mean_time_to_repair is not None:
            result['totalMeanTimeToRepair'] = self.total_mean_time_to_repair
        if self.un_acknowledged_escalation_incident_count is not None:
            result['unAcknowledgedEscalationIncidentCount'] = self.un_acknowledged_escalation_incident_count
        if self.un_finish_escalation_incident_count is not None:
            result['unFinishEscalationIncidentCount'] = self.un_finish_escalation_incident_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('effectionLevel') is not None:
            self.effection_level = m.get('effectionLevel')
        if m.get('escalationIncidentCount') is not None:
            self.escalation_incident_count = m.get('escalationIncidentCount')
        if m.get('incidentCount') is not None:
            self.incident_count = m.get('incidentCount')
        if m.get('meanTimeToAcknowledge') is not None:
            self.mean_time_to_acknowledge = m.get('meanTimeToAcknowledge')
        if m.get('meanTimeToRepair') is not None:
            self.mean_time_to_repair = m.get('meanTimeToRepair')
        if m.get('time') is not None:
            self.time = m.get('time')
        if m.get('totalMeanTimeToAcknowledge') is not None:
            self.total_mean_time_to_acknowledge = m.get('totalMeanTimeToAcknowledge')
        if m.get('totalMeanTimeToRepair') is not None:
            self.total_mean_time_to_repair = m.get('totalMeanTimeToRepair')
        if m.get('unAcknowledgedEscalationIncidentCount') is not None:
            self.un_acknowledged_escalation_incident_count = m.get('unAcknowledgedEscalationIncidentCount')
        if m.get('unFinishEscalationIncidentCount') is not None:
            self.un_finish_escalation_incident_count = m.get('unFinishEscalationIncidentCount')
        return self


class ListChartDataForUserResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListChartDataForUserResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListChartDataForUserResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListChartDataForUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListChartDataForUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListChartDataForUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListConfigsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class ListConfigsResponseBody(TeaModel):
    def __init__(
        self,
        data: Dict[str, List[DataValue]] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # requestId
        self.request_id = request_id

    def validate(self):
        if self.data:
            for v in self.data.values():
                for k1 in v:
                    if k1:
                        k1.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = {}
        if self.data is not None:
            for k, v in self.data.items():
                l1 = []
                for k1 in v:
                    l1.append(k1.to_map() if k1 else None)
                result['data'][k] = l1
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = {}
        if m.get('data') is not None:
            for k, v in m.get('data').items():
                l1 = []
                for k1 in v:
                    temp_model = DataValue()
                    l1.append(temp_model.from_map(k1))
                self.data['k'] = l1
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListConfigsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListConfigsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListConfigsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDataReportForServiceGroupRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        service_group_name: str = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.service_group_name = service_group_name
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        if self.start_time is not None:
            result['startTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        return self


class ListDataReportForServiceGroupResponseBodyData(TeaModel):
    def __init__(
        self,
        escalation_incident_count: int = None,
        finish_incident_count: int = None,
        finish_proportion: str = None,
        incident_count: int = None,
        mean_time_to_acknowledge: int = None,
        mean_time_to_repair: int = None,
        service_group_id: int = None,
        service_group_name: str = None,
        un_acknowledged_escalation_incident_count: int = None,
        un_finish_escalation_incident_count: int = None,
    ):
        self.escalation_incident_count = escalation_incident_count
        self.finish_incident_count = finish_incident_count
        self.finish_proportion = finish_proportion
        self.incident_count = incident_count
        # MRRA
        self.mean_time_to_acknowledge = mean_time_to_acknowledge
        # MTTR
        self.mean_time_to_repair = mean_time_to_repair
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name
        self.un_acknowledged_escalation_incident_count = un_acknowledged_escalation_incident_count
        self.un_finish_escalation_incident_count = un_finish_escalation_incident_count

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_incident_count is not None:
            result['escalationIncidentCount'] = self.escalation_incident_count
        if self.finish_incident_count is not None:
            result['finishIncidentCount'] = self.finish_incident_count
        if self.finish_proportion is not None:
            result['finishProportion'] = self.finish_proportion
        if self.incident_count is not None:
            result['incidentCount'] = self.incident_count
        if self.mean_time_to_acknowledge is not None:
            result['meanTimeToAcknowledge'] = self.mean_time_to_acknowledge
        if self.mean_time_to_repair is not None:
            result['meanTimeToRepair'] = self.mean_time_to_repair
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        if self.un_acknowledged_escalation_incident_count is not None:
            result['unAcknowledgedEscalationIncidentCount'] = self.un_acknowledged_escalation_incident_count
        if self.un_finish_escalation_incident_count is not None:
            result['unFinishEscalationIncidentCount'] = self.un_finish_escalation_incident_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationIncidentCount') is not None:
            self.escalation_incident_count = m.get('escalationIncidentCount')
        if m.get('finishIncidentCount') is not None:
            self.finish_incident_count = m.get('finishIncidentCount')
        if m.get('finishProportion') is not None:
            self.finish_proportion = m.get('finishProportion')
        if m.get('incidentCount') is not None:
            self.incident_count = m.get('incidentCount')
        if m.get('meanTimeToAcknowledge') is not None:
            self.mean_time_to_acknowledge = m.get('meanTimeToAcknowledge')
        if m.get('meanTimeToRepair') is not None:
            self.mean_time_to_repair = m.get('meanTimeToRepair')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        if m.get('unAcknowledgedEscalationIncidentCount') is not None:
            self.un_acknowledged_escalation_incident_count = m.get('unAcknowledgedEscalationIncidentCount')
        if m.get('unFinishEscalationIncidentCount') is not None:
            self.un_finish_escalation_incident_count = m.get('unFinishEscalationIncidentCount')
        return self


class ListDataReportForServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListDataReportForServiceGroupResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSIze'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListDataReportForServiceGroupResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSIze') is not None:
            self.page_size = m.get('pageSIze')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListDataReportForServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDataReportForServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDataReportForServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDataReportForUserRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        page_number: int = None,
        page_size: int = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.page_number = page_number
        self.page_size = page_size
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.start_time is not None:
            result['startTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        return self


class ListDataReportForUserResponseBodyData(TeaModel):
    def __init__(
        self,
        distribution_incident_count: int = None,
        escalation_incident_count: int = None,
        finish_incident_number: int = None,
        finish_proportion: str = None,
        mean_time_to_acknowledge: str = None,
        mean_time_to_repair: str = None,
        un_acknowledged_escalation_incident_count: int = None,
        un_distribution_incident_count: int = None,
        un_finish_escalation_incident_count: int = None,
        user_id: int = None,
        user_name: str = None,
    ):
        self.distribution_incident_count = distribution_incident_count
        self.escalation_incident_count = escalation_incident_count
        self.finish_incident_number = finish_incident_number
        self.finish_proportion = finish_proportion
        # MRRA
        self.mean_time_to_acknowledge = mean_time_to_acknowledge
        # MTTA
        self.mean_time_to_repair = mean_time_to_repair
        self.un_acknowledged_escalation_incident_count = un_acknowledged_escalation_incident_count
        self.un_distribution_incident_count = un_distribution_incident_count
        self.un_finish_escalation_incident_count = un_finish_escalation_incident_count
        self.user_id = user_id
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.distribution_incident_count is not None:
            result['distributionIncidentCount'] = self.distribution_incident_count
        if self.escalation_incident_count is not None:
            result['escalationIncidentCount'] = self.escalation_incident_count
        if self.finish_incident_number is not None:
            result['finishIncidentNumber'] = self.finish_incident_number
        if self.finish_proportion is not None:
            result['finishProportion'] = self.finish_proportion
        if self.mean_time_to_acknowledge is not None:
            result['meanTimeToAcknowledge'] = self.mean_time_to_acknowledge
        if self.mean_time_to_repair is not None:
            result['meanTimeToRepair'] = self.mean_time_to_repair
        if self.un_acknowledged_escalation_incident_count is not None:
            result['unAcknowledgedEscalationIncidentCount'] = self.un_acknowledged_escalation_incident_count
        if self.un_distribution_incident_count is not None:
            result['unDistributionIncidentCount'] = self.un_distribution_incident_count
        if self.un_finish_escalation_incident_count is not None:
            result['unFinishEscalationIncidentCount'] = self.un_finish_escalation_incident_count
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_name is not None:
            result['userName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('distributionIncidentCount') is not None:
            self.distribution_incident_count = m.get('distributionIncidentCount')
        if m.get('escalationIncidentCount') is not None:
            self.escalation_incident_count = m.get('escalationIncidentCount')
        if m.get('finishIncidentNumber') is not None:
            self.finish_incident_number = m.get('finishIncidentNumber')
        if m.get('finishProportion') is not None:
            self.finish_proportion = m.get('finishProportion')
        if m.get('meanTimeToAcknowledge') is not None:
            self.mean_time_to_acknowledge = m.get('meanTimeToAcknowledge')
        if m.get('meanTimeToRepair') is not None:
            self.mean_time_to_repair = m.get('meanTimeToRepair')
        if m.get('unAcknowledgedEscalationIncidentCount') is not None:
            self.un_acknowledged_escalation_incident_count = m.get('unAcknowledgedEscalationIncidentCount')
        if m.get('unDistributionIncidentCount') is not None:
            self.un_distribution_incident_count = m.get('unDistributionIncidentCount')
        if m.get('unFinishEscalationIncidentCount') is not None:
            self.un_finish_escalation_incident_count = m.get('unFinishEscalationIncidentCount')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userName') is not None:
            self.user_name = m.get('userName')
        return self


class ListDataReportForUserResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListDataReportForUserResponseBodyData] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListDataReportForUserResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListDataReportForUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDataReportForUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDataReportForUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListDictionariesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class ListDictionariesResponseBody(TeaModel):
    def __init__(
        self,
        data: Dict[str, List[DataValue]] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for v in self.data.values():
                for k1 in v:
                    if k1:
                        k1.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = {}
        if self.data is not None:
            for k, v in self.data.items():
                l1 = []
                for k1 in v:
                    l1.append(k1.to_map() if k1 else None)
                result['data'][k] = l1
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = {}
        if m.get('data') is not None:
            for k, v in m.get('data').items():
                l1 = []
                for k1 in v:
                    temp_model = DataValue()
                    l1.append(temp_model.from_map(k1))
                self.data['k'] = l1
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListDictionariesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListDictionariesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListDictionariesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListEscalationPlanServicesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        # clientToken
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class ListEscalationPlanServicesResponseBodyData(TeaModel):
    def __init__(
        self,
        scope: str = None,
        scope_object_id: int = None,
    ):
        self.scope = scope
        self.scope_object_id = scope_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        return self


class ListEscalationPlanServicesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListEscalationPlanServicesResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListEscalationPlanServicesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListEscalationPlanServicesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListEscalationPlanServicesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListEscalationPlanServicesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListEscalationPlansRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_name: str = None,
        is_global: bool = None,
        page_number: int = None,
        page_size: int = None,
        service_name: str = None,
        status: str = None,
    ):
        self.client_token = client_token
        self.escalation_plan_name = escalation_plan_name
        self.is_global = is_global
        self.page_number = page_number
        self.page_size = page_size
        self.service_name = service_name
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        if self.is_global is not None:
            result['isGlobal'] = self.is_global
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        if m.get('isGlobal') is not None:
            self.is_global = m.get('isGlobal')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListEscalationPlansResponseBodyDataEscalationPlanScopeObjects(TeaModel):
    def __init__(
        self,
        scope: str = None,
        scope_object_deleted_type: int = None,
        scope_object_id: int = None,
        scope_object_name: str = None,
    ):
        self.scope = scope
        self.scope_object_deleted_type = scope_object_deleted_type
        self.scope_object_id = scope_object_id
        self.scope_object_name = scope_object_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object_deleted_type is not None:
            result['scopeObjectDeletedType'] = self.scope_object_deleted_type
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        if self.scope_object_name is not None:
            result['scopeObjectName'] = self.scope_object_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObjectDeletedType') is not None:
            self.scope_object_deleted_type = m.get('scopeObjectDeletedType')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        if m.get('scopeObjectName') is not None:
            self.scope_object_name = m.get('scopeObjectName')
        return self


class ListEscalationPlansResponseBodyData(TeaModel):
    def __init__(
        self,
        escalation_plan_id: int = None,
        escalation_plan_name: str = None,
        escalation_plan_scope_objects: List[ListEscalationPlansResponseBodyDataEscalationPlanScopeObjects] = None,
        is_global: bool = None,
        modify_time: str = None,
        status: str = None,
    ):
        self.escalation_plan_id = escalation_plan_id
        self.escalation_plan_name = escalation_plan_name
        self.escalation_plan_scope_objects = escalation_plan_scope_objects
        self.is_global = is_global
        self.modify_time = modify_time
        self.status = status

    def validate(self):
        if self.escalation_plan_scope_objects:
            for k in self.escalation_plan_scope_objects:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        result['escalationPlanScopeObjects'] = []
        if self.escalation_plan_scope_objects is not None:
            for k in self.escalation_plan_scope_objects:
                result['escalationPlanScopeObjects'].append(k.to_map() if k else None)
        if self.is_global is not None:
            result['isGlobal'] = self.is_global
        if self.modify_time is not None:
            result['modifyTime'] = self.modify_time
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        self.escalation_plan_scope_objects = []
        if m.get('escalationPlanScopeObjects') is not None:
            for k in m.get('escalationPlanScopeObjects'):
                temp_model = ListEscalationPlansResponseBodyDataEscalationPlanScopeObjects()
                self.escalation_plan_scope_objects.append(temp_model.from_map(k))
        if m.get('isGlobal') is not None:
            self.is_global = m.get('isGlobal')
        if m.get('modifyTime') is not None:
            self.modify_time = m.get('modifyTime')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListEscalationPlansResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListEscalationPlansResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListEscalationPlansResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListEscalationPlansResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListEscalationPlansResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListEscalationPlansResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListEscalationPlansByNoticeObjectRequest(TeaModel):
    def __init__(
        self,
        notice_object_id: int = None,
        notice_object_type: int = None,
    ):
        self.notice_object_id = notice_object_id
        self.notice_object_type = notice_object_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.notice_object_id is not None:
            result['noticeObjectId'] = self.notice_object_id
        if self.notice_object_type is not None:
            result['noticeObjectType'] = self.notice_object_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('noticeObjectId') is not None:
            self.notice_object_id = m.get('noticeObjectId')
        if m.get('noticeObjectType') is not None:
            self.notice_object_type = m.get('noticeObjectType')
        return self


class ListEscalationPlansByNoticeObjectResponseBodyDataEscalationPlanScopeObjects(TeaModel):
    def __init__(
        self,
        scope: str = None,
        scope_object_deleted_type: int = None,
        scope_object_id: int = None,
        scope_object_name: str = None,
    ):
        self.scope = scope
        self.scope_object_deleted_type = scope_object_deleted_type
        self.scope_object_id = scope_object_id
        self.scope_object_name = scope_object_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object_deleted_type is not None:
            result['scopeObjectDeletedType'] = self.scope_object_deleted_type
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        if self.scope_object_name is not None:
            result['scopeObjectName'] = self.scope_object_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObjectDeletedType') is not None:
            self.scope_object_deleted_type = m.get('scopeObjectDeletedType')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        if m.get('scopeObjectName') is not None:
            self.scope_object_name = m.get('scopeObjectName')
        return self


class ListEscalationPlansByNoticeObjectResponseBodyData(TeaModel):
    def __init__(
        self,
        escalation_plan_id: int = None,
        escalation_plan_name: str = None,
        escalation_plan_scope_objects: List[ListEscalationPlansByNoticeObjectResponseBodyDataEscalationPlanScopeObjects] = None,
        modify_time: str = None,
        status: str = None,
    ):
        self.escalation_plan_id = escalation_plan_id
        self.escalation_plan_name = escalation_plan_name
        self.escalation_plan_scope_objects = escalation_plan_scope_objects
        self.modify_time = modify_time
        self.status = status

    def validate(self):
        if self.escalation_plan_scope_objects:
            for k in self.escalation_plan_scope_objects:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        result['escalationPlanScopeObjects'] = []
        if self.escalation_plan_scope_objects is not None:
            for k in self.escalation_plan_scope_objects:
                result['escalationPlanScopeObjects'].append(k.to_map() if k else None)
        if self.modify_time is not None:
            result['modifyTime'] = self.modify_time
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        self.escalation_plan_scope_objects = []
        if m.get('escalationPlanScopeObjects') is not None:
            for k in m.get('escalationPlanScopeObjects'):
                temp_model = ListEscalationPlansByNoticeObjectResponseBodyDataEscalationPlanScopeObjects()
                self.escalation_plan_scope_objects.append(temp_model.from_map(k))
        if m.get('modifyTime') is not None:
            self.modify_time = m.get('modifyTime')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListEscalationPlansByNoticeObjectResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListEscalationPlansByNoticeObjectResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListEscalationPlansByNoticeObjectResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListEscalationPlansByNoticeObjectResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListEscalationPlansByNoticeObjectResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListEscalationPlansByNoticeObjectResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIncidentDetailEscalationPlansRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_id: int = None,
    ):
        self.client_token = client_token
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlanNoticeObjectList(TeaModel):
    def __init__(
        self,
        notice_object_id: int = None,
        notice_object_name: str = None,
        notice_object_phone: str = None,
        role_name_list: List[str] = None,
    ):
        self.notice_object_id = notice_object_id
        self.notice_object_name = notice_object_name
        self.notice_object_phone = notice_object_phone
        self.role_name_list = role_name_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.notice_object_id is not None:
            result['noticeObjectId'] = self.notice_object_id
        if self.notice_object_name is not None:
            result['noticeObjectName'] = self.notice_object_name
        if self.notice_object_phone is not None:
            result['noticeObjectPhone'] = self.notice_object_phone
        if self.role_name_list is not None:
            result['roleNameList'] = self.role_name_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('noticeObjectId') is not None:
            self.notice_object_id = m.get('noticeObjectId')
        if m.get('noticeObjectName') is not None:
            self.notice_object_name = m.get('noticeObjectName')
        if m.get('noticeObjectPhone') is not None:
            self.notice_object_phone = m.get('noticeObjectPhone')
        if m.get('roleNameList') is not None:
            self.role_name_list = m.get('roleNameList')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlanServiceGroupList(TeaModel):
    def __init__(
        self,
        id: int = None,
        name: str = None,
    ):
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlan(TeaModel):
    def __init__(
        self,
        escalation_plan_type: str = None,
        notice_channels: List[str] = None,
        notice_object_list: List[ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlanNoticeObjectList] = None,
        notice_time: int = None,
        service_group_list: List[ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlanServiceGroupList] = None,
        start_time: int = None,
        status: str = None,
    ):
        self.escalation_plan_type = escalation_plan_type
        self.notice_channels = notice_channels
        self.notice_object_list = notice_object_list
        self.notice_time = notice_time
        self.service_group_list = service_group_list
        self.start_time = start_time
        self.status = status

    def validate(self):
        if self.notice_object_list:
            for k in self.notice_object_list:
                if k:
                    k.validate()
        if self.service_group_list:
            for k in self.service_group_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        if self.notice_channels is not None:
            result['noticeChannels'] = self.notice_channels
        result['noticeObjectList'] = []
        if self.notice_object_list is not None:
            for k in self.notice_object_list:
                result['noticeObjectList'].append(k.to_map() if k else None)
        if self.notice_time is not None:
            result['noticeTime'] = self.notice_time
        result['serviceGroupList'] = []
        if self.service_group_list is not None:
            for k in self.service_group_list:
                result['serviceGroupList'].append(k.to_map() if k else None)
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        if m.get('noticeChannels') is not None:
            self.notice_channels = m.get('noticeChannels')
        self.notice_object_list = []
        if m.get('noticeObjectList') is not None:
            for k in m.get('noticeObjectList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlanNoticeObjectList()
                self.notice_object_list.append(temp_model.from_map(k))
        if m.get('noticeTime') is not None:
            self.notice_time = m.get('noticeTime')
        self.service_group_list = []
        if m.get('serviceGroupList') is not None:
            for k in m.get('serviceGroupList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlanServiceGroupList()
                self.service_group_list.append(temp_model.from_map(k))
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanNoticeObjectList(TeaModel):
    def __init__(
        self,
        notice_object_id: int = None,
        notice_object_name: str = None,
        notice_object_phone: str = None,
        role_name_list: List[str] = None,
    ):
        self.notice_object_id = notice_object_id
        self.notice_object_name = notice_object_name
        self.notice_object_phone = notice_object_phone
        self.role_name_list = role_name_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.notice_object_id is not None:
            result['noticeObjectId'] = self.notice_object_id
        if self.notice_object_name is not None:
            result['noticeObjectName'] = self.notice_object_name
        if self.notice_object_phone is not None:
            result['noticeObjectPhone'] = self.notice_object_phone
        if self.role_name_list is not None:
            result['roleNameList'] = self.role_name_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('noticeObjectId') is not None:
            self.notice_object_id = m.get('noticeObjectId')
        if m.get('noticeObjectName') is not None:
            self.notice_object_name = m.get('noticeObjectName')
        if m.get('noticeObjectPhone') is not None:
            self.notice_object_phone = m.get('noticeObjectPhone')
        if m.get('roleNameList') is not None:
            self.role_name_list = m.get('roleNameList')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanNoticeRoleObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        name: str = None,
    ):
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanServiceGroupList(TeaModel):
    def __init__(
        self,
        id: int = None,
        name: str = None,
    ):
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlan(TeaModel):
    def __init__(
        self,
        escalation_plan_type: str = None,
        notice_channels: List[str] = None,
        notice_object_list: List[ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanNoticeObjectList] = None,
        notice_role_list: List[int] = None,
        notice_role_object_list: List[ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanNoticeRoleObjectList] = None,
        notice_time: int = None,
        service_group_list: List[ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanServiceGroupList] = None,
        start_time: int = None,
        status: str = None,
    ):
        self.escalation_plan_type = escalation_plan_type
        self.notice_channels = notice_channels
        self.notice_object_list = notice_object_list
        self.notice_role_list = notice_role_list
        self.notice_role_object_list = notice_role_object_list
        self.notice_time = notice_time
        self.service_group_list = service_group_list
        self.start_time = start_time
        self.status = status

    def validate(self):
        if self.notice_object_list:
            for k in self.notice_object_list:
                if k:
                    k.validate()
        if self.notice_role_object_list:
            for k in self.notice_role_object_list:
                if k:
                    k.validate()
        if self.service_group_list:
            for k in self.service_group_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        if self.notice_channels is not None:
            result['noticeChannels'] = self.notice_channels
        result['noticeObjectList'] = []
        if self.notice_object_list is not None:
            for k in self.notice_object_list:
                result['noticeObjectList'].append(k.to_map() if k else None)
        if self.notice_role_list is not None:
            result['noticeRoleList'] = self.notice_role_list
        result['noticeRoleObjectList'] = []
        if self.notice_role_object_list is not None:
            for k in self.notice_role_object_list:
                result['noticeRoleObjectList'].append(k.to_map() if k else None)
        if self.notice_time is not None:
            result['noticeTime'] = self.notice_time
        result['serviceGroupList'] = []
        if self.service_group_list is not None:
            for k in self.service_group_list:
                result['serviceGroupList'].append(k.to_map() if k else None)
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        if m.get('noticeChannels') is not None:
            self.notice_channels = m.get('noticeChannels')
        self.notice_object_list = []
        if m.get('noticeObjectList') is not None:
            for k in m.get('noticeObjectList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanNoticeObjectList()
                self.notice_object_list.append(temp_model.from_map(k))
        if m.get('noticeRoleList') is not None:
            self.notice_role_list = m.get('noticeRoleList')
        self.notice_role_object_list = []
        if m.get('noticeRoleObjectList') is not None:
            for k in m.get('noticeRoleObjectList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanNoticeRoleObjectList()
                self.notice_role_object_list.append(temp_model.from_map(k))
        if m.get('noticeTime') is not None:
            self.notice_time = m.get('noticeTime')
        self.service_group_list = []
        if m.get('serviceGroupList') is not None:
            for k in m.get('serviceGroupList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlanServiceGroupList()
                self.service_group_list.append(temp_model.from_map(k))
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanNoticeObjectList(TeaModel):
    def __init__(
        self,
        notice_object_id: int = None,
        notice_object_name: str = None,
        notice_object_phone: str = None,
        role_name_list: List[str] = None,
    ):
        self.notice_object_id = notice_object_id
        self.notice_object_name = notice_object_name
        self.notice_object_phone = notice_object_phone
        self.role_name_list = role_name_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.notice_object_id is not None:
            result['noticeObjectId'] = self.notice_object_id
        if self.notice_object_name is not None:
            result['noticeObjectName'] = self.notice_object_name
        if self.notice_object_phone is not None:
            result['noticeObjectPhone'] = self.notice_object_phone
        if self.role_name_list is not None:
            result['roleNameList'] = self.role_name_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('noticeObjectId') is not None:
            self.notice_object_id = m.get('noticeObjectId')
        if m.get('noticeObjectName') is not None:
            self.notice_object_name = m.get('noticeObjectName')
        if m.get('noticeObjectPhone') is not None:
            self.notice_object_phone = m.get('noticeObjectPhone')
        if m.get('roleNameList') is not None:
            self.role_name_list = m.get('roleNameList')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanNoticeRoleObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        name: str = None,
    ):
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanServiceGroupList(TeaModel):
    def __init__(
        self,
        id: int = None,
        name: str = None,
    ):
        self.id = id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('name') is not None:
            self.name = m.get('name')
        return self


class ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlan(TeaModel):
    def __init__(
        self,
        escalation_plan_type: str = None,
        notice_channels: List[str] = None,
        notice_object_list: List[ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanNoticeObjectList] = None,
        notice_role_list: List[int] = None,
        notice_role_object_list: List[ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanNoticeRoleObjectList] = None,
        notice_time: int = None,
        service_group_list: List[ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanServiceGroupList] = None,
        start_time: int = None,
        status: str = None,
    ):
        self.escalation_plan_type = escalation_plan_type
        self.notice_channels = notice_channels
        self.notice_object_list = notice_object_list
        self.notice_role_list = notice_role_list
        self.notice_role_object_list = notice_role_object_list
        self.notice_time = notice_time
        self.service_group_list = service_group_list
        self.start_time = start_time
        self.status = status

    def validate(self):
        if self.notice_object_list:
            for k in self.notice_object_list:
                if k:
                    k.validate()
        if self.notice_role_object_list:
            for k in self.notice_role_object_list:
                if k:
                    k.validate()
        if self.service_group_list:
            for k in self.service_group_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        if self.notice_channels is not None:
            result['noticeChannels'] = self.notice_channels
        result['noticeObjectList'] = []
        if self.notice_object_list is not None:
            for k in self.notice_object_list:
                result['noticeObjectList'].append(k.to_map() if k else None)
        if self.notice_role_list is not None:
            result['noticeRoleList'] = self.notice_role_list
        result['noticeRoleObjectList'] = []
        if self.notice_role_object_list is not None:
            for k in self.notice_role_object_list:
                result['noticeRoleObjectList'].append(k.to_map() if k else None)
        if self.notice_time is not None:
            result['noticeTime'] = self.notice_time
        result['serviceGroupList'] = []
        if self.service_group_list is not None:
            for k in self.service_group_list:
                result['serviceGroupList'].append(k.to_map() if k else None)
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        if m.get('noticeChannels') is not None:
            self.notice_channels = m.get('noticeChannels')
        self.notice_object_list = []
        if m.get('noticeObjectList') is not None:
            for k in m.get('noticeObjectList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanNoticeObjectList()
                self.notice_object_list.append(temp_model.from_map(k))
        if m.get('noticeRoleList') is not None:
            self.notice_role_list = m.get('noticeRoleList')
        self.notice_role_object_list = []
        if m.get('noticeRoleObjectList') is not None:
            for k in m.get('noticeRoleObjectList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanNoticeRoleObjectList()
                self.notice_role_object_list.append(temp_model.from_map(k))
        if m.get('noticeTime') is not None:
            self.notice_time = m.get('noticeTime')
        self.service_group_list = []
        if m.get('serviceGroupList') is not None:
            for k in m.get('serviceGroupList'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlanServiceGroupList()
                self.service_group_list.append(temp_model.from_map(k))
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListIncidentDetailEscalationPlansResponseBodyData(TeaModel):
    def __init__(
        self,
        convergence_escalation_plan: List[ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlan] = None,
        escalation_plan_id: int = None,
        escalation_plan_name: str = None,
        nu_acknowledge_escalation_plan: List[ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlan] = None,
        un_finish_escalation_plan: List[ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlan] = None,
    ):
        self.convergence_escalation_plan = convergence_escalation_plan
        self.escalation_plan_id = escalation_plan_id
        self.escalation_plan_name = escalation_plan_name
        self.nu_acknowledge_escalation_plan = nu_acknowledge_escalation_plan
        self.un_finish_escalation_plan = un_finish_escalation_plan

    def validate(self):
        if self.convergence_escalation_plan:
            for k in self.convergence_escalation_plan:
                if k:
                    k.validate()
        if self.nu_acknowledge_escalation_plan:
            for k in self.nu_acknowledge_escalation_plan:
                if k:
                    k.validate()
        if self.un_finish_escalation_plan:
            for k in self.un_finish_escalation_plan:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['convergenceEscalationPlan'] = []
        if self.convergence_escalation_plan is not None:
            for k in self.convergence_escalation_plan:
                result['convergenceEscalationPlan'].append(k.to_map() if k else None)
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        result['nuAcknowledgeEscalationPlan'] = []
        if self.nu_acknowledge_escalation_plan is not None:
            for k in self.nu_acknowledge_escalation_plan:
                result['nuAcknowledgeEscalationPlan'].append(k.to_map() if k else None)
        result['unFinishEscalationPlan'] = []
        if self.un_finish_escalation_plan is not None:
            for k in self.un_finish_escalation_plan:
                result['unFinishEscalationPlan'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.convergence_escalation_plan = []
        if m.get('convergenceEscalationPlan') is not None:
            for k in m.get('convergenceEscalationPlan'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataConvergenceEscalationPlan()
                self.convergence_escalation_plan.append(temp_model.from_map(k))
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        self.nu_acknowledge_escalation_plan = []
        if m.get('nuAcknowledgeEscalationPlan') is not None:
            for k in m.get('nuAcknowledgeEscalationPlan'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataNuAcknowledgeEscalationPlan()
                self.nu_acknowledge_escalation_plan.append(temp_model.from_map(k))
        self.un_finish_escalation_plan = []
        if m.get('unFinishEscalationPlan') is not None:
            for k in m.get('unFinishEscalationPlan'):
                temp_model = ListIncidentDetailEscalationPlansResponseBodyDataUnFinishEscalationPlan()
                self.un_finish_escalation_plan.append(temp_model.from_map(k))
        return self


class ListIncidentDetailEscalationPlansResponseBody(TeaModel):
    def __init__(
        self,
        data: ListIncidentDetailEscalationPlansResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = ListIncidentDetailEscalationPlansResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListIncidentDetailEscalationPlansResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIncidentDetailEscalationPlansResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIncidentDetailEscalationPlansResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIncidentDetailTimelinesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        id_sort: str = None,
        incident_id: int = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.client_token = client_token
        self.id_sort = id_sort
        self.incident_id = incident_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.id_sort is not None:
            result['idSort'] = self.id_sort
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('idSort') is not None:
            self.id_sort = m.get('idSort')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        return self


class ListIncidentDetailTimelinesResponseBodyData(TeaModel):
    def __init__(
        self,
        action: str = None,
        create_time: str = None,
        description: str = None,
        incident_id: int = None,
        rel_route_rule_delete_type: int = None,
        related_service_name: str = None,
        remark: str = None,
        snapshot_data: str = None,
        title: str = None,
    ):
        self.action = action
        self.create_time = create_time
        self.description = description
        self.incident_id = incident_id
        self.rel_route_rule_delete_type = rel_route_rule_delete_type
        self.related_service_name = related_service_name
        self.remark = remark
        self.snapshot_data = snapshot_data
        self.title = title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['action'] = self.action
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.rel_route_rule_delete_type is not None:
            result['relRouteRuleDeleteType'] = self.rel_route_rule_delete_type
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.remark is not None:
            result['remark'] = self.remark
        if self.snapshot_data is not None:
            result['snapshotData'] = self.snapshot_data
        if self.title is not None:
            result['title'] = self.title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('action') is not None:
            self.action = m.get('action')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('relRouteRuleDeleteType') is not None:
            self.rel_route_rule_delete_type = m.get('relRouteRuleDeleteType')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('remark') is not None:
            self.remark = m.get('remark')
        if m.get('snapshotData') is not None:
            self.snapshot_data = m.get('snapshotData')
        if m.get('title') is not None:
            self.title = m.get('title')
        return self


class ListIncidentDetailTimelinesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListIncidentDetailTimelinesResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListIncidentDetailTimelinesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListIncidentDetailTimelinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIncidentDetailTimelinesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIncidentDetailTimelinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIncidentSubtotalsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_id: int = None,
    ):
        self.client_token = client_token
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class ListIncidentSubtotalsResponseBodyData(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        create_user_id: int = None,
        create_user_name: str = None,
        create_user_phone: str = None,
        description: str = None,
    ):
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.create_user_name = create_user_name
        self.create_user_phone = create_user_phone
        self.description = description

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.create_user_id is not None:
            result['createUserId'] = self.create_user_id
        if self.create_user_name is not None:
            result['createUserName'] = self.create_user_name
        if self.create_user_phone is not None:
            result['createUserPhone'] = self.create_user_phone
        if self.description is not None:
            result['description'] = self.description
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('createUserId') is not None:
            self.create_user_id = m.get('createUserId')
        if m.get('createUserName') is not None:
            self.create_user_name = m.get('createUserName')
        if m.get('createUserPhone') is not None:
            self.create_user_phone = m.get('createUserPhone')
        if m.get('description') is not None:
            self.description = m.get('description')
        return self


class ListIncidentSubtotalsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListIncidentSubtotalsResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListIncidentSubtotalsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListIncidentSubtotalsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIncidentSubtotalsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIncidentSubtotalsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIncidentTimelinesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.client_token = client_token
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        return self


class ListIncidentTimelinesResponseBodyData(TeaModel):
    def __init__(
        self,
        action: str = None,
        create_time: str = None,
        description: int = None,
        incident_id: int = None,
        incident_number: str = None,
        incident_title: str = None,
        rel_route_rule_delete_type: int = None,
        related_service_name: str = None,
        remark: str = None,
        snapshot_data: str = None,
        title: str = None,
    ):
        self.action = action
        self.create_time = create_time
        self.description = description
        self.incident_id = incident_id
        self.incident_number = incident_number
        self.incident_title = incident_title
        self.rel_route_rule_delete_type = rel_route_rule_delete_type
        self.related_service_name = related_service_name
        self.remark = remark
        self.snapshot_data = snapshot_data
        self.title = title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['action'] = self.action
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_number is not None:
            result['incidentNumber'] = self.incident_number
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.rel_route_rule_delete_type is not None:
            result['relRouteRuleDeleteType'] = self.rel_route_rule_delete_type
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.remark is not None:
            result['remark'] = self.remark
        if self.snapshot_data is not None:
            result['snapshotData'] = self.snapshot_data
        if self.title is not None:
            result['title'] = self.title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('action') is not None:
            self.action = m.get('action')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentNumber') is not None:
            self.incident_number = m.get('incidentNumber')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('relRouteRuleDeleteType') is not None:
            self.rel_route_rule_delete_type = m.get('relRouteRuleDeleteType')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('remark') is not None:
            self.remark = m.get('remark')
        if m.get('snapshotData') is not None:
            self.snapshot_data = m.get('snapshotData')
        if m.get('title') is not None:
            self.title = m.get('title')
        return self


class ListIncidentTimelinesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListIncidentTimelinesResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # requestId
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListIncidentTimelinesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListIncidentTimelinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIncidentTimelinesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIncidentTimelinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIncidentsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        create_end_time: str = None,
        create_start_time: str = None,
        effect: str = None,
        incident_level: str = None,
        incident_status: str = None,
        me: int = None,
        page_number: int = None,
        page_size: int = None,
        relation_service_id: int = None,
        rule_name: str = None,
    ):
        self.client_token = client_token
        self.create_end_time = create_end_time
        self.create_start_time = create_start_time
        self.effect = effect
        self.incident_level = incident_level
        self.incident_status = incident_status
        self.me = me
        self.page_number = page_number
        self.page_size = page_size
        self.relation_service_id = relation_service_id
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.create_end_time is not None:
            result['createEndTime'] = self.create_end_time
        if self.create_start_time is not None:
            result['createStartTime'] = self.create_start_time
        if self.effect is not None:
            result['effect'] = self.effect
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.incident_status is not None:
            result['incidentStatus'] = self.incident_status
        if self.me is not None:
            result['me'] = self.me
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.relation_service_id is not None:
            result['relationServiceId'] = self.relation_service_id
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('createEndTime') is not None:
            self.create_end_time = m.get('createEndTime')
        if m.get('createStartTime') is not None:
            self.create_start_time = m.get('createStartTime')
        if m.get('effect') is not None:
            self.effect = m.get('effect')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('incidentStatus') is not None:
            self.incident_status = m.get('incidentStatus')
        if m.get('me') is not None:
            self.me = m.get('me')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('relationServiceId') is not None:
            self.relation_service_id = m.get('relationServiceId')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        return self


class ListIncidentsResponseBodyData(TeaModel):
    def __init__(
        self,
        assign_to_who_is_valid: int = None,
        assign_user_id: int = None,
        assign_user_name: str = None,
        assign_user_phone: str = None,
        create_time: str = None,
        effect: str = None,
        incident_id: int = None,
        incident_level: str = None,
        incident_number: str = None,
        incident_status: str = None,
        incident_title: str = None,
        is_manual: bool = None,
        rel_route_rule_delete_type: int = None,
        rel_service_delete_type: int = None,
        related_service_id: int = None,
        related_service_name: str = None,
        route_rule_id: int = None,
        route_rule_name: str = None,
    ):
        self.assign_to_who_is_valid = assign_to_who_is_valid
        # 代表创建时间的资源属性字段
        self.assign_user_id = assign_user_id
        # 代表资源一级ID的资源属性字段
        self.assign_user_name = assign_user_name
        self.assign_user_phone = assign_user_phone
        # 事件级别
        self.create_time = create_time
        # 时间指派人ID
        self.effect = effect
        # 修改时间
        self.incident_id = incident_id
        # 影响程度
        self.incident_level = incident_level
        self.incident_number = incident_number
        # 关联流转规则ID
        self.incident_status = incident_status
        # 事件内容
        self.incident_title = incident_title
        self.is_manual = is_manual
        self.rel_route_rule_delete_type = rel_route_rule_delete_type
        self.rel_service_delete_type = rel_service_delete_type
        # 事件状态
        self.related_service_id = related_service_id
        self.related_service_name = related_service_name
        # 关联的服务ID
        self.route_rule_id = route_rule_id
        self.route_rule_name = route_rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_to_who_is_valid is not None:
            result['assignToWhoIsValid'] = self.assign_to_who_is_valid
        if self.assign_user_id is not None:
            result['assignUserId'] = self.assign_user_id
        if self.assign_user_name is not None:
            result['assignUserName'] = self.assign_user_name
        if self.assign_user_phone is not None:
            result['assignUserPhone'] = self.assign_user_phone
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.effect is not None:
            result['effect'] = self.effect
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.incident_number is not None:
            result['incidentNumber'] = self.incident_number
        if self.incident_status is not None:
            result['incidentStatus'] = self.incident_status
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        if self.is_manual is not None:
            result['isManual'] = self.is_manual
        if self.rel_route_rule_delete_type is not None:
            result['relRouteRuleDeleteType'] = self.rel_route_rule_delete_type
        if self.rel_service_delete_type is not None:
            result['relServiceDeleteType'] = self.rel_service_delete_type
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.route_rule_name is not None:
            result['routeRuleName'] = self.route_rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignToWhoIsValid') is not None:
            self.assign_to_who_is_valid = m.get('assignToWhoIsValid')
        if m.get('assignUserId') is not None:
            self.assign_user_id = m.get('assignUserId')
        if m.get('assignUserName') is not None:
            self.assign_user_name = m.get('assignUserName')
        if m.get('assignUserPhone') is not None:
            self.assign_user_phone = m.get('assignUserPhone')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('effect') is not None:
            self.effect = m.get('effect')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('incidentNumber') is not None:
            self.incident_number = m.get('incidentNumber')
        if m.get('incidentStatus') is not None:
            self.incident_status = m.get('incidentStatus')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        if m.get('isManual') is not None:
            self.is_manual = m.get('isManual')
        if m.get('relRouteRuleDeleteType') is not None:
            self.rel_route_rule_delete_type = m.get('relRouteRuleDeleteType')
        if m.get('relServiceDeleteType') is not None:
            self.rel_service_delete_type = m.get('relServiceDeleteType')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('routeRuleName') is not None:
            self.route_rule_name = m.get('routeRuleName')
        return self


class ListIncidentsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListIncidentsResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # requestId
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListIncidentsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListIncidentsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIncidentsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIncidentsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIntegrationConfigTimelinesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        return self


class ListIntegrationConfigTimelinesResponseBodyData(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        description: str = None,
        title: str = None,
    ):
        self.create_time = create_time
        self.description = description
        self.title = title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.title is not None:
            result['title'] = self.title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('title') is not None:
            self.title = m.get('title')
        return self


class ListIntegrationConfigTimelinesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListIntegrationConfigTimelinesResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        # pageNumber
        self.page_number = page_number
        # pageSize
        self.page_size = page_size
        # requestId
        self.request_id = request_id
        # totalCount
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListIntegrationConfigTimelinesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListIntegrationConfigTimelinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIntegrationConfigTimelinesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIntegrationConfigTimelinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIntegrationConfigsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        monitor_source_name: str = None,
    ):
        self.client_token = client_token
        self.monitor_source_name = monitor_source_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        return self


class ListIntegrationConfigsResponseBodyData(TeaModel):
    def __init__(
        self,
        integration_config_id: int = None,
        is_received_event: bool = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
        monitor_source_short_name: str = None,
        monitor_source_type: int = None,
        status: str = None,
    ):
        self.integration_config_id = integration_config_id
        self.is_received_event = is_received_event
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name
        self.monitor_source_short_name = monitor_source_short_name
        self.monitor_source_type = monitor_source_type
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        if self.is_received_event is not None:
            result['isReceivedEvent'] = self.is_received_event
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.monitor_source_short_name is not None:
            result['monitorSourceShortName'] = self.monitor_source_short_name
        if self.monitor_source_type is not None:
            result['monitorSourceType'] = self.monitor_source_type
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        if m.get('isReceivedEvent') is not None:
            self.is_received_event = m.get('isReceivedEvent')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('monitorSourceShortName') is not None:
            self.monitor_source_short_name = m.get('monitorSourceShortName')
        if m.get('monitorSourceType') is not None:
            self.monitor_source_type = m.get('monitorSourceType')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class ListIntegrationConfigsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListIntegrationConfigsResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListIntegrationConfigsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListIntegrationConfigsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListIntegrationConfigsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListIntegrationConfigsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListMonitorSourcesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
    ):
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        return self


class ListMonitorSourcesResponseBodyData(TeaModel):
    def __init__(
        self,
        field_keys: List[str] = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
    ):
        self.field_keys = field_keys
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.field_keys is not None:
            result['fieldKeys'] = self.field_keys
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fieldKeys') is not None:
            self.field_keys = m.get('fieldKeys')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        return self


class ListMonitorSourcesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListMonitorSourcesResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListMonitorSourcesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListMonitorSourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListMonitorSourcesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListMonitorSourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListProblemDetailOperationsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        create_time_sort: str = None,
        page_number: int = None,
        page_size: int = None,
        problem_id: int = None,
    ):
        self.client_token = client_token
        self.create_time_sort = create_time_sort
        self.page_number = page_number
        self.page_size = page_size
        # This parameter is required.
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.create_time_sort is not None:
            result['createTimeSort'] = self.create_time_sort
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('createTimeSort') is not None:
            self.create_time_sort = m.get('createTimeSort')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class ListProblemDetailOperationsResponseBodyData(TeaModel):
    def __init__(
        self,
        action: str = None,
        create_time: str = None,
        description: str = None,
        related_service_name: str = None,
        remark: str = None,
        snapshot_data: str = None,
        title: str = None,
    ):
        self.action = action
        self.create_time = create_time
        self.description = description
        self.related_service_name = related_service_name
        self.remark = remark
        self.snapshot_data = snapshot_data
        self.title = title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['action'] = self.action
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.remark is not None:
            result['remark'] = self.remark
        if self.snapshot_data is not None:
            result['snapshotData'] = self.snapshot_data
        if self.title is not None:
            result['title'] = self.title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('action') is not None:
            self.action = m.get('action')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('remark') is not None:
            self.remark = m.get('remark')
        if m.get('snapshotData') is not None:
            self.snapshot_data = m.get('snapshotData')
        if m.get('title') is not None:
            self.title = m.get('title')
        return self


class ListProblemDetailOperationsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListProblemDetailOperationsResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # requestId
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListProblemDetailOperationsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListProblemDetailOperationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListProblemDetailOperationsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListProblemDetailOperationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListProblemOperationsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.client_token = client_token
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        return self


class ListProblemOperationsResponseBodyData(TeaModel):
    def __init__(
        self,
        action: str = None,
        create_time: str = None,
        description: str = None,
        problem_id: int = None,
        problem_name: str = None,
        problem_number: str = None,
        related_service_name: str = None,
        snapshot_data: str = None,
        title: str = None,
    ):
        self.action = action
        self.create_time = create_time
        self.description = description
        self.problem_id = problem_id
        self.problem_name = problem_name
        self.problem_number = problem_number
        self.related_service_name = related_service_name
        self.snapshot_data = snapshot_data
        self.title = title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['action'] = self.action
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.description is not None:
            result['description'] = self.description
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_name is not None:
            result['problemName'] = self.problem_name
        if self.problem_number is not None:
            result['problemNumber'] = self.problem_number
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.snapshot_data is not None:
            result['snapshotData'] = self.snapshot_data
        if self.title is not None:
            result['title'] = self.title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('action') is not None:
            self.action = m.get('action')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemName') is not None:
            self.problem_name = m.get('problemName')
        if m.get('problemNumber') is not None:
            self.problem_number = m.get('problemNumber')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('snapshotData') is not None:
            self.snapshot_data = m.get('snapshotData')
        if m.get('title') is not None:
            self.title = m.get('title')
        return self


class ListProblemOperationsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListProblemOperationsResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListProblemOperationsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListProblemOperationsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListProblemOperationsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListProblemOperationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListProblemSubtotalsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class ListProblemSubtotalsResponseBodyData(TeaModel):
    def __init__(
        self,
        create_ram_name: str = None,
        create_time: str = None,
        create_user_id: int = None,
        create_user_phone: str = None,
        description: str = None,
    ):
        self.create_ram_name = create_ram_name
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.create_user_phone = create_user_phone
        self.description = description

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_ram_name is not None:
            result['createRamName'] = self.create_ram_name
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.create_user_id is not None:
            result['createUserId'] = self.create_user_id
        if self.create_user_phone is not None:
            result['createUserPhone'] = self.create_user_phone
        if self.description is not None:
            result['description'] = self.description
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('createRamName') is not None:
            self.create_ram_name = m.get('createRamName')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('createUserId') is not None:
            self.create_user_id = m.get('createUserId')
        if m.get('createUserPhone') is not None:
            self.create_user_phone = m.get('createUserPhone')
        if m.get('description') is not None:
            self.description = m.get('description')
        return self


class ListProblemSubtotalsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListProblemSubtotalsResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListProblemSubtotalsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListProblemSubtotalsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListProblemSubtotalsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListProblemSubtotalsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListProblemTimeLinesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        return self


class ListProblemTimeLinesResponseBodyDataUsersInContent(TeaModel):
    def __init__(
        self,
        is_valid: int = None,
        user_id: int = None,
        username: str = None,
    ):
        self.is_valid = is_valid
        self.user_id = user_id
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_valid is not None:
            result['isValid'] = self.is_valid
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('isValid') is not None:
            self.is_valid = m.get('isValid')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class ListProblemTimeLinesResponseBodyData(TeaModel):
    def __init__(
        self,
        content: str = None,
        create_time: str = None,
        is_key: bool = None,
        key_node: str = None,
        problem_timeline_id: int = None,
        time: str = None,
        update_time: str = None,
        users_in_content: List[ListProblemTimeLinesResponseBodyDataUsersInContent] = None,
    ):
        self.content = content
        self.create_time = create_time
        self.is_key = is_key
        self.key_node = key_node
        self.problem_timeline_id = problem_timeline_id
        self.time = time
        self.update_time = update_time
        self.users_in_content = users_in_content

    def validate(self):
        if self.users_in_content:
            for k in self.users_in_content:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['content'] = self.content
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.is_key is not None:
            result['isKey'] = self.is_key
        if self.key_node is not None:
            result['keyNode'] = self.key_node
        if self.problem_timeline_id is not None:
            result['problemTimelineId'] = self.problem_timeline_id
        if self.time is not None:
            result['time'] = self.time
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        result['usersInContent'] = []
        if self.users_in_content is not None:
            for k in self.users_in_content:
                result['usersInContent'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('isKey') is not None:
            self.is_key = m.get('isKey')
        if m.get('keyNode') is not None:
            self.key_node = m.get('keyNode')
        if m.get('problemTimelineId') is not None:
            self.problem_timeline_id = m.get('problemTimelineId')
        if m.get('time') is not None:
            self.time = m.get('time')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        self.users_in_content = []
        if m.get('usersInContent') is not None:
            for k in m.get('usersInContent'):
                temp_model = ListProblemTimeLinesResponseBodyDataUsersInContent()
                self.users_in_content.append(temp_model.from_map(k))
        return self


class ListProblemTimeLinesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListProblemTimeLinesResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListProblemTimeLinesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListProblemTimeLinesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListProblemTimeLinesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListProblemTimeLinesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListProblemsRequest(TeaModel):
    def __init__(
        self,
        affect_service_id: int = None,
        client_token: str = None,
        discovery_end_time: str = None,
        discovery_start_time: str = None,
        main_handler_id: int = None,
        page_number: int = None,
        page_size: int = None,
        problem_level: str = None,
        problem_status: str = None,
        query_type: str = None,
        repeater_id: int = None,
        restore_end_time: str = None,
        restore_start_time: str = None,
        service_group_id: int = None,
    ):
        self.affect_service_id = affect_service_id
        self.client_token = client_token
        self.discovery_end_time = discovery_end_time
        self.discovery_start_time = discovery_start_time
        self.main_handler_id = main_handler_id
        self.page_number = page_number
        self.page_size = page_size
        self.problem_level = problem_level
        self.problem_status = problem_status
        self.query_type = query_type
        self.repeater_id = repeater_id
        self.restore_end_time = restore_end_time
        self.restore_start_time = restore_start_time
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.affect_service_id is not None:
            result['affectServiceId'] = self.affect_service_id
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.discovery_end_time is not None:
            result['discoveryEndTime'] = self.discovery_end_time
        if self.discovery_start_time is not None:
            result['discoveryStartTime'] = self.discovery_start_time
        if self.main_handler_id is not None:
            result['mainHandlerId'] = self.main_handler_id
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        if self.problem_status is not None:
            result['problemStatus'] = self.problem_status
        if self.query_type is not None:
            result['queryType'] = self.query_type
        if self.repeater_id is not None:
            result['repeaterId'] = self.repeater_id
        if self.restore_end_time is not None:
            result['restoreEndTime'] = self.restore_end_time
        if self.restore_start_time is not None:
            result['restoreStartTime'] = self.restore_start_time
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('affectServiceId') is not None:
            self.affect_service_id = m.get('affectServiceId')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('discoveryEndTime') is not None:
            self.discovery_end_time = m.get('discoveryEndTime')
        if m.get('discoveryStartTime') is not None:
            self.discovery_start_time = m.get('discoveryStartTime')
        if m.get('mainHandlerId') is not None:
            self.main_handler_id = m.get('mainHandlerId')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        if m.get('problemStatus') is not None:
            self.problem_status = m.get('problemStatus')
        if m.get('queryType') is not None:
            self.query_type = m.get('queryType')
        if m.get('repeaterId') is not None:
            self.repeater_id = m.get('repeaterId')
        if m.get('restoreEndTime') is not None:
            self.restore_end_time = m.get('restoreEndTime')
        if m.get('restoreStartTime') is not None:
            self.restore_start_time = m.get('restoreStartTime')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class ListProblemsResponseBodyDataAffectServices(TeaModel):
    def __init__(
        self,
        service_description: str = None,
        service_id: int = None,
        service_name: str = None,
        update_time: str = None,
    ):
        self.service_description = service_description
        self.service_id = service_id
        self.service_name = service_name
        self.update_time = update_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_description is not None:
            result['serviceDescription'] = self.service_description
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceDescription') is not None:
            self.service_description = m.get('serviceDescription')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class ListProblemsResponseBodyData(TeaModel):
    def __init__(
        self,
        affect_services: List[ListProblemsResponseBodyDataAffectServices] = None,
        cancel_time: str = None,
        create_time: str = None,
        discover_time: str = None,
        finish_time: str = None,
        incident_id: int = None,
        is_manual: bool = None,
        is_upgrade: bool = None,
        main_handler_id: int = None,
        main_handler_is_valid: int = None,
        main_handler_name: str = None,
        problem_id: int = None,
        problem_level: str = None,
        problem_name: str = None,
        problem_number: str = None,
        problem_status: str = None,
        recovery_time: str = None,
        related_service_id: str = None,
        replay_time: str = None,
        service_deleted_type: int = None,
        service_name: str = None,
        update_time: str = None,
    ):
        self.affect_services = affect_services
        self.cancel_time = cancel_time
        self.create_time = create_time
        self.discover_time = discover_time
        self.finish_time = finish_time
        self.incident_id = incident_id
        self.is_manual = is_manual
        self.is_upgrade = is_upgrade
        self.main_handler_id = main_handler_id
        self.main_handler_is_valid = main_handler_is_valid
        self.main_handler_name = main_handler_name
        self.problem_id = problem_id
        self.problem_level = problem_level
        self.problem_name = problem_name
        self.problem_number = problem_number
        self.problem_status = problem_status
        self.recovery_time = recovery_time
        self.related_service_id = related_service_id
        self.replay_time = replay_time
        self.service_deleted_type = service_deleted_type
        self.service_name = service_name
        self.update_time = update_time

    def validate(self):
        if self.affect_services:
            for k in self.affect_services:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['affectServices'] = []
        if self.affect_services is not None:
            for k in self.affect_services:
                result['affectServices'].append(k.to_map() if k else None)
        if self.cancel_time is not None:
            result['cancelTime'] = self.cancel_time
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.discover_time is not None:
            result['discoverTime'] = self.discover_time
        if self.finish_time is not None:
            result['finishTime'] = self.finish_time
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.is_manual is not None:
            result['isManual'] = self.is_manual
        if self.is_upgrade is not None:
            result['isUpgrade'] = self.is_upgrade
        if self.main_handler_id is not None:
            result['mainHandlerId'] = self.main_handler_id
        if self.main_handler_is_valid is not None:
            result['mainHandlerIsValid'] = self.main_handler_is_valid
        if self.main_handler_name is not None:
            result['mainHandlerName'] = self.main_handler_name
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        if self.problem_name is not None:
            result['problemName'] = self.problem_name
        if self.problem_number is not None:
            result['problemNumber'] = self.problem_number
        if self.problem_status is not None:
            result['problemStatus'] = self.problem_status
        if self.recovery_time is not None:
            result['recoveryTime'] = self.recovery_time
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.replay_time is not None:
            result['replayTime'] = self.replay_time
        if self.service_deleted_type is not None:
            result['serviceDeletedType'] = self.service_deleted_type
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.affect_services = []
        if m.get('affectServices') is not None:
            for k in m.get('affectServices'):
                temp_model = ListProblemsResponseBodyDataAffectServices()
                self.affect_services.append(temp_model.from_map(k))
        if m.get('cancelTime') is not None:
            self.cancel_time = m.get('cancelTime')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('discoverTime') is not None:
            self.discover_time = m.get('discoverTime')
        if m.get('finishTime') is not None:
            self.finish_time = m.get('finishTime')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('isManual') is not None:
            self.is_manual = m.get('isManual')
        if m.get('isUpgrade') is not None:
            self.is_upgrade = m.get('isUpgrade')
        if m.get('mainHandlerId') is not None:
            self.main_handler_id = m.get('mainHandlerId')
        if m.get('mainHandlerIsValid') is not None:
            self.main_handler_is_valid = m.get('mainHandlerIsValid')
        if m.get('mainHandlerName') is not None:
            self.main_handler_name = m.get('mainHandlerName')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        if m.get('problemName') is not None:
            self.problem_name = m.get('problemName')
        if m.get('problemNumber') is not None:
            self.problem_number = m.get('problemNumber')
        if m.get('problemStatus') is not None:
            self.problem_status = m.get('problemStatus')
        if m.get('recoveryTime') is not None:
            self.recovery_time = m.get('recoveryTime')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('replayTime') is not None:
            self.replay_time = m.get('replayTime')
        if m.get('serviceDeletedType') is not None:
            self.service_deleted_type = m.get('serviceDeletedType')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class ListProblemsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListProblemsResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListProblemsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListProblemsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListProblemsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListProblemsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListRouteRulesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        not_filter_route_rule_deleted: bool = None,
        page_number: int = None,
        page_size: int = None,
        route_type: int = None,
        rule_name: bytes = None,
        service_name: bytes = None,
    ):
        self.client_token = client_token
        self.not_filter_route_rule_deleted = not_filter_route_rule_deleted
        self.page_number = page_number
        self.page_size = page_size
        self.route_type = route_type
        self.rule_name = rule_name
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.not_filter_route_rule_deleted is not None:
            result['notFilterRouteRuleDeleted'] = self.not_filter_route_rule_deleted
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.route_type is not None:
            result['routeType'] = self.route_type
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('notFilterRouteRuleDeleted') is not None:
            self.not_filter_route_rule_deleted = m.get('notFilterRouteRuleDeleted')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('routeType') is not None:
            self.route_type = m.get('routeType')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class ListRouteRulesResponseBodyData(TeaModel):
    def __init__(
        self,
        assign_object_id: int = None,
        assign_object_type: str = None,
        create_time: str = None,
        effection: str = None,
        enable_status: str = None,
        incident_level: str = None,
        is_valid: int = None,
        match_count: int = None,
        monitor_source_names: str = None,
        rel_service_delete_type: int = None,
        related_service_id: int = None,
        related_service_name: str = None,
        route_rule_id: int = None,
        route_type: str = None,
        rule_name: str = None,
        tenant_ram_id: int = None,
        time_window: int = None,
        time_window_unit: int = None,
        update_time: str = None,
    ):
        self.assign_object_id = assign_object_id
        self.assign_object_type = assign_object_type
        self.create_time = create_time
        self.effection = effection
        self.enable_status = enable_status
        self.incident_level = incident_level
        self.is_valid = is_valid
        self.match_count = match_count
        self.monitor_source_names = monitor_source_names
        self.rel_service_delete_type = rel_service_delete_type
        self.related_service_id = related_service_id
        self.related_service_name = related_service_name
        self.route_rule_id = route_rule_id
        self.route_type = route_type
        self.rule_name = rule_name
        self.tenant_ram_id = tenant_ram_id
        self.time_window = time_window
        self.time_window_unit = time_window_unit
        self.update_time = update_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_object_id is not None:
            result['assignObjectId'] = self.assign_object_id
        if self.assign_object_type is not None:
            result['assignObjectType'] = self.assign_object_type
        if self.create_time is not None:
            result['createTime'] = self.create_time
        if self.effection is not None:
            result['effection'] = self.effection
        if self.enable_status is not None:
            result['enableStatus'] = self.enable_status
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.is_valid is not None:
            result['isValid'] = self.is_valid
        if self.match_count is not None:
            result['matchCount'] = self.match_count
        if self.monitor_source_names is not None:
            result['monitorSourceNames'] = self.monitor_source_names
        if self.rel_service_delete_type is not None:
            result['relServiceDeleteType'] = self.rel_service_delete_type
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.related_service_name is not None:
            result['relatedServiceName'] = self.related_service_name
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.route_type is not None:
            result['routeType'] = self.route_type
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        if self.tenant_ram_id is not None:
            result['tenantRamId'] = self.tenant_ram_id
        if self.time_window is not None:
            result['timeWindow'] = self.time_window
        if self.time_window_unit is not None:
            result['timeWindowUnit'] = self.time_window_unit
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignObjectId') is not None:
            self.assign_object_id = m.get('assignObjectId')
        if m.get('assignObjectType') is not None:
            self.assign_object_type = m.get('assignObjectType')
        if m.get('createTime') is not None:
            self.create_time = m.get('createTime')
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('enableStatus') is not None:
            self.enable_status = m.get('enableStatus')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('isValid') is not None:
            self.is_valid = m.get('isValid')
        if m.get('matchCount') is not None:
            self.match_count = m.get('matchCount')
        if m.get('monitorSourceNames') is not None:
            self.monitor_source_names = m.get('monitorSourceNames')
        if m.get('relServiceDeleteType') is not None:
            self.rel_service_delete_type = m.get('relServiceDeleteType')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('relatedServiceName') is not None:
            self.related_service_name = m.get('relatedServiceName')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('routeType') is not None:
            self.route_type = m.get('routeType')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        if m.get('tenantRamId') is not None:
            self.tenant_ram_id = m.get('tenantRamId')
        if m.get('timeWindow') is not None:
            self.time_window = m.get('timeWindow')
        if m.get('timeWindowUnit') is not None:
            self.time_window_unit = m.get('timeWindowUnit')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class ListRouteRulesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListRouteRulesResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListRouteRulesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListRouteRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListRouteRulesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListRouteRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListRouteRulesByAssignWhoIdRequest(TeaModel):
    def __init__(
        self,
        assign_who_id: int = None,
        assign_who_type: int = None,
    ):
        self.assign_who_id = assign_who_id
        self.assign_who_type = assign_who_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_who_id is not None:
            result['assignWhoId'] = self.assign_who_id
        if self.assign_who_type is not None:
            result['assignWhoType'] = self.assign_who_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignWhoId') is not None:
            self.assign_who_id = m.get('assignWhoId')
        if m.get('assignWhoType') is not None:
            self.assign_who_type = m.get('assignWhoType')
        return self


class ListRouteRulesByAssignWhoIdResponseBodyData(TeaModel):
    def __init__(
        self,
        id: int = None,
        rule_name: str = None,
        tenant_ram_id: int = None,
    ):
        self.id = id
        self.rule_name = rule_name
        self.tenant_ram_id = tenant_ram_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        if self.tenant_ram_id is not None:
            result['tenantRamId'] = self.tenant_ram_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        if m.get('tenantRamId') is not None:
            self.tenant_ram_id = m.get('tenantRamId')
        return self


class ListRouteRulesByAssignWhoIdResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListRouteRulesByAssignWhoIdResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListRouteRulesByAssignWhoIdResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListRouteRulesByAssignWhoIdResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListRouteRulesByAssignWhoIdResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListRouteRulesByAssignWhoIdResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListRouteRulesByServiceResponseBodyData(TeaModel):
    def __init__(
        self,
        id: int = None,
        rule_name: str = None,
    ):
        self.id = id
        self.rule_name = rule_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        return self


class ListRouteRulesByServiceResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListRouteRulesByServiceResponseBodyData] = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListRouteRulesByServiceResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListRouteRulesByServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListRouteRulesByServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListRouteRulesByServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListServiceGroupMonitorSourceTemplatesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        request_id: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.request_id = request_id
        self.service_group_id = service_group_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class ListServiceGroupMonitorSourceTemplatesResponseBodyData(TeaModel):
    def __init__(
        self,
        fields: List[str] = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
        template_content: str = None,
        template_id: int = None,
    ):
        self.fields = fields
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name
        self.template_content = template_content
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.fields is not None:
            result['fields'] = self.fields
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.template_content is not None:
            result['templateContent'] = self.template_content
        if self.template_id is not None:
            result['templateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('fields') is not None:
            self.fields = m.get('fields')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('templateContent') is not None:
            self.template_content = m.get('templateContent')
        if m.get('templateId') is not None:
            self.template_id = m.get('templateId')
        return self


class ListServiceGroupMonitorSourceTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListServiceGroupMonitorSourceTemplatesResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListServiceGroupMonitorSourceTemplatesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListServiceGroupMonitorSourceTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListServiceGroupMonitorSourceTemplatesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListServiceGroupMonitorSourceTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListServiceGroupsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        is_scheduled: bool = None,
        order_by_schedule_status: bool = None,
        page_number: int = None,
        page_size: int = None,
        query_name: str = None,
        query_type: str = None,
        service_id: int = None,
        user_id: int = None,
    ):
        self.client_token = client_token
        self.is_scheduled = is_scheduled
        self.order_by_schedule_status = order_by_schedule_status
        self.page_number = page_number
        self.page_size = page_size
        self.query_name = query_name
        self.query_type = query_type
        self.service_id = service_id
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.is_scheduled is not None:
            result['isScheduled'] = self.is_scheduled
        if self.order_by_schedule_status is not None:
            result['orderByScheduleStatus'] = self.order_by_schedule_status
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.query_name is not None:
            result['queryName'] = self.query_name
        if self.query_type is not None:
            result['queryType'] = self.query_type
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('isScheduled') is not None:
            self.is_scheduled = m.get('isScheduled')
        if m.get('orderByScheduleStatus') is not None:
            self.order_by_schedule_status = m.get('orderByScheduleStatus')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('queryName') is not None:
            self.query_name = m.get('queryName')
        if m.get('queryType') is not None:
            self.query_type = m.get('queryType')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class ListServiceGroupsResponseBodyDataUsers(TeaModel):
    def __init__(
        self,
        email: str = None,
        is_related: int = None,
        phone: str = None,
        service_group_id: int = None,
        user_id: int = None,
        user_name: str = None,
    ):
        self.email = email
        self.is_related = is_related
        self.phone = phone
        self.service_group_id = service_group_id
        self.user_id = user_id
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.email is not None:
            result['email'] = self.email
        if self.is_related is not None:
            result['isRelated'] = self.is_related
        if self.phone is not None:
            result['phone'] = self.phone
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.user_name is not None:
            result['userName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('email') is not None:
            self.email = m.get('email')
        if m.get('isRelated') is not None:
            self.is_related = m.get('isRelated')
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('userName') is not None:
            self.user_name = m.get('userName')
        return self


class ListServiceGroupsResponseBodyData(TeaModel):
    def __init__(
        self,
        enable_webhook: str = None,
        is_scheduled: bool = None,
        service_group_description: str = None,
        service_group_id: int = None,
        service_group_name: str = None,
        update_time: str = None,
        users: List[ListServiceGroupsResponseBodyDataUsers] = None,
        webhook_link: str = None,
        webhook_type: str = None,
    ):
        self.enable_webhook = enable_webhook
        self.is_scheduled = is_scheduled
        self.service_group_description = service_group_description
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name
        self.update_time = update_time
        self.users = users
        self.webhook_link = webhook_link
        self.webhook_type = webhook_type

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_webhook is not None:
            result['enableWebhook'] = self.enable_webhook
        if self.is_scheduled is not None:
            result['isScheduled'] = self.is_scheduled
        if self.service_group_description is not None:
            result['serviceGroupDescription'] = self.service_group_description
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        result['users'] = []
        if self.users is not None:
            for k in self.users:
                result['users'].append(k.to_map() if k else None)
        if self.webhook_link is not None:
            result['webhookLink'] = self.webhook_link
        if self.webhook_type is not None:
            result['webhookType'] = self.webhook_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('enableWebhook') is not None:
            self.enable_webhook = m.get('enableWebhook')
        if m.get('isScheduled') is not None:
            self.is_scheduled = m.get('isScheduled')
        if m.get('serviceGroupDescription') is not None:
            self.service_group_description = m.get('serviceGroupDescription')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        self.users = []
        if m.get('users') is not None:
            for k in m.get('users'):
                temp_model = ListServiceGroupsResponseBodyDataUsers()
                self.users.append(temp_model.from_map(k))
        if m.get('webhookLink') is not None:
            self.webhook_link = m.get('webhookLink')
        if m.get('webhookType') is not None:
            self.webhook_type = m.get('webhookType')
        return self


class ListServiceGroupsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListServiceGroupsResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListServiceGroupsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListServiceGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListServiceGroupsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListServiceGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListServiceGroupsByUserIdResponseBodyData(TeaModel):
    def __init__(
        self,
        is_scheduled: bool = None,
        service_group_id: int = None,
        service_group_name: str = None,
    ):
        self.is_scheduled = is_scheduled
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_scheduled is not None:
            result['isScheduled'] = self.is_scheduled
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('isScheduled') is not None:
            self.is_scheduled = m.get('isScheduled')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        return self


class ListServiceGroupsByUserIdResponseBody(TeaModel):
    def __init__(
        self,
        data: ListServiceGroupsByUserIdResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = ListServiceGroupsByUserIdResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListServiceGroupsByUserIdResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListServiceGroupsByUserIdResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListServiceGroupsByUserIdResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListServicesRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        page_number: int = None,
        page_size: int = None,
        service_name: str = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.page_number = page_number
        # This parameter is required.
        self.page_size = page_size
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class ListServicesResponseBodyData(TeaModel):
    def __init__(
        self,
        escalation_plan_id: int = None,
        escalation_plan_name: str = None,
        is_valid: int = None,
        service_description: str = None,
        service_group_id_list: List[int] = None,
        service_id: int = None,
        service_name: str = None,
        update_time: str = None,
    ):
        self.escalation_plan_id = escalation_plan_id
        self.escalation_plan_name = escalation_plan_name
        self.is_valid = is_valid
        self.service_description = service_description
        self.service_group_id_list = service_group_id_list
        self.service_id = service_id
        self.service_name = service_name
        self.update_time = update_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        if self.is_valid is not None:
            result['isValid'] = self.is_valid
        if self.service_description is not None:
            result['serviceDescription'] = self.service_description
        if self.service_group_id_list is not None:
            result['serviceGroupIdList'] = self.service_group_id_list
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        if self.update_time is not None:
            result['updateTime'] = self.update_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        if m.get('isValid') is not None:
            self.is_valid = m.get('isValid')
        if m.get('serviceDescription') is not None:
            self.service_description = m.get('serviceDescription')
        if m.get('serviceGroupIdList') is not None:
            self.service_group_id_list = m.get('serviceGroupIdList')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        if m.get('updateTime') is not None:
            self.update_time = m.get('updateTime')
        return self


class ListServicesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListServicesResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # Id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListServicesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListServicesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListServicesResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListServicesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSourceEventsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        end_time: str = None,
        instance_id: int = None,
        instance_type: str = None,
        page_number: int = None,
        page_size: int = None,
        start_row_key: str = None,
        start_time: str = None,
        stop_row_key: str = None,
    ):
        self.client_token = client_token
        # 2020-09-18 13:00:00
        self.end_time = end_time
        # This parameter is required.
        self.instance_id = instance_id
        # This parameter is required.
        self.instance_type = instance_type
        self.page_number = page_number
        self.page_size = page_size
        self.start_row_key = start_row_key
        # 2020-09-10 13:00:00
        self.start_time = start_time
        self.stop_row_key = stop_row_key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.start_row_key is not None:
            result['startRowKey'] = self.start_row_key
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.stop_row_key is not None:
            result['stopRowKey'] = self.stop_row_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('startRowKey') is not None:
            self.start_row_key = m.get('startRowKey')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('stopRowKey') is not None:
            self.stop_row_key = m.get('stopRowKey')
        return self


class ListSourceEventsResponseBodyData(TeaModel):
    def __init__(
        self,
        event_json: str = None,
        event_time: str = None,
        instance_id: int = None,
        instance_type: str = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
        route_rule_id: int = None,
        tenant_ram_id: int = None,
    ):
        self.event_json = event_json
        self.event_time = event_time
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name
        self.route_rule_id = route_rule_id
        self.tenant_ram_id = tenant_ram_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.event_json is not None:
            result['eventJson'] = self.event_json
        if self.event_time is not None:
            result['eventTime'] = self.event_time
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.tenant_ram_id is not None:
            result['tenantRamId'] = self.tenant_ram_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('eventJson') is not None:
            self.event_json = m.get('eventJson')
        if m.get('eventTime') is not None:
            self.event_time = m.get('eventTime')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('tenantRamId') is not None:
            self.tenant_ram_id = m.get('tenantRamId')
        return self


class ListSourceEventsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListSourceEventsResponseBodyData] = None,
        first_row_key: str = None,
        last_row_key: str = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        self.data = data
        # firstRowKey
        self.first_row_key = first_row_key
        # lastRowKey
        self.last_row_key = last_row_key
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.first_row_key is not None:
            result['firstRowKey'] = self.first_row_key
        if self.last_row_key is not None:
            result['lastRowKey'] = self.last_row_key
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListSourceEventsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('firstRowKey') is not None:
            self.first_row_key = m.get('firstRowKey')
        if m.get('lastRowKey') is not None:
            self.last_row_key = m.get('lastRowKey')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListSourceEventsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListSourceEventsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListSourceEventsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSourceEventsForMonitorSourceRequest(TeaModel):
    def __init__(
        self,
        monitor_source_id: int = None,
    ):
        self.monitor_source_id = monitor_source_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        return self


class ListSourceEventsForMonitorSourceResponseBodyData(TeaModel):
    def __init__(
        self,
        event_json: str = None,
        event_time: str = None,
        monitor_source_id: bool = None,
        monitor_source_name: str = None,
    ):
        self.event_json = event_json
        self.event_time = event_time
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.event_json is not None:
            result['eventJson'] = self.event_json
        if self.event_time is not None:
            result['eventTime'] = self.event_time
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('eventJson') is not None:
            self.event_json = m.get('eventJson')
        if m.get('eventTime') is not None:
            self.event_time = m.get('eventTime')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        return self


class ListSourceEventsForMonitorSourceResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListSourceEventsForMonitorSourceResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListSourceEventsForMonitorSourceResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListSourceEventsForMonitorSourceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListSourceEventsForMonitorSourceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListSourceEventsForMonitorSourceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSubscriptionServiceGroupsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        service_ids: List[int] = None,
    ):
        self.client_token = client_token
        self.service_ids = service_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.service_ids is not None:
            result['serviceIds'] = self.service_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('serviceIds') is not None:
            self.service_ids = m.get('serviceIds')
        return self


class ListSubscriptionServiceGroupsResponseBodyData(TeaModel):
    def __init__(
        self,
        service_group_description: str = None,
        service_id: int = None,
        service_name: str = None,
    ):
        self.service_group_description = service_group_description
        self.service_id = service_id
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_group_description is not None:
            result['serviceGroupDescription'] = self.service_group_description
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceGroupDescription') is not None:
            self.service_group_description = m.get('serviceGroupDescription')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class ListSubscriptionServiceGroupsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListSubscriptionServiceGroupsResponseBodyData] = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListSubscriptionServiceGroupsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListSubscriptionServiceGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListSubscriptionServiceGroupsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListSubscriptionServiceGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSubscriptionsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        not_filter_scope_object_deleted: bool = None,
        notify_object: str = None,
        notify_object_type: str = None,
        page_number: int = None,
        page_size: int = None,
        scope: str = None,
        scope_object: str = None,
        subscription_title: str = None,
    ):
        self.client_token = client_token
        self.not_filter_scope_object_deleted = not_filter_scope_object_deleted
        self.notify_object = notify_object
        self.notify_object_type = notify_object_type
        self.page_number = page_number
        self.page_size = page_size
        self.scope = scope
        self.scope_object = scope_object
        self.subscription_title = subscription_title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.not_filter_scope_object_deleted is not None:
            result['notFilterScopeObjectDeleted'] = self.not_filter_scope_object_deleted
        if self.notify_object is not None:
            result['notifyObject'] = self.notify_object
        if self.notify_object_type is not None:
            result['notifyObjectType'] = self.notify_object_type
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object is not None:
            result['scopeObject'] = self.scope_object
        if self.subscription_title is not None:
            result['subscriptionTitle'] = self.subscription_title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('notFilterScopeObjectDeleted') is not None:
            self.not_filter_scope_object_deleted = m.get('notFilterScopeObjectDeleted')
        if m.get('notifyObject') is not None:
            self.notify_object = m.get('notifyObject')
        if m.get('notifyObjectType') is not None:
            self.notify_object_type = m.get('notifyObjectType')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObject') is not None:
            self.scope_object = m.get('scopeObject')
        if m.get('subscriptionTitle') is not None:
            self.subscription_title = m.get('subscriptionTitle')
        return self


class ListSubscriptionsResponseBodyDataNotifyObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        is_valid: int = None,
        name: str = None,
        notify_object_id: int = None,
        notify_object_type: int = None,
    ):
        self.id = id
        self.is_valid = is_valid
        self.name = name
        self.notify_object_id = notify_object_id
        self.notify_object_type = notify_object_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.is_valid is not None:
            result['isValid'] = self.is_valid
        if self.name is not None:
            result['name'] = self.name
        if self.notify_object_id is not None:
            result['notifyObjectId'] = self.notify_object_id
        if self.notify_object_type is not None:
            result['notifyObjectType'] = self.notify_object_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('isValid') is not None:
            self.is_valid = m.get('isValid')
        if m.get('name') is not None:
            self.name = m.get('name')
        if m.get('notifyObjectId') is not None:
            self.notify_object_id = m.get('notifyObjectId')
        if m.get('notifyObjectType') is not None:
            self.notify_object_type = m.get('notifyObjectType')
        return self


class ListSubscriptionsResponseBodyDataScopeObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        is_valid: int = None,
        scope: int = None,
        scope_object: str = None,
        scope_object_id: int = None,
    ):
        self.id = id
        self.is_valid = is_valid
        self.scope = scope
        self.scope_object = scope_object
        self.scope_object_id = scope_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.is_valid is not None:
            result['isValid'] = self.is_valid
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object is not None:
            result['scopeObject'] = self.scope_object
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('isValid') is not None:
            self.is_valid = m.get('isValid')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObject') is not None:
            self.scope_object = m.get('scopeObject')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        return self


class ListSubscriptionsResponseBodyData(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        expired_type: str = None,
        notify_object_list: List[ListSubscriptionsResponseBodyDataNotifyObjectList] = None,
        notify_object_type: int = None,
        scope: int = None,
        scope_object_list: List[ListSubscriptionsResponseBodyDataScopeObjectList] = None,
        start_time: str = None,
        status: str = None,
        subscription_id: int = None,
        subscription_title: str = None,
    ):
        self.end_time = end_time
        self.expired_type = expired_type
        self.notify_object_list = notify_object_list
        self.notify_object_type = notify_object_type
        self.scope = scope
        self.scope_object_list = scope_object_list
        self.start_time = start_time
        self.status = status
        self.subscription_id = subscription_id
        self.subscription_title = subscription_title

    def validate(self):
        if self.notify_object_list:
            for k in self.notify_object_list:
                if k:
                    k.validate()
        if self.scope_object_list:
            for k in self.scope_object_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.expired_type is not None:
            result['expiredType'] = self.expired_type
        result['notifyObjectList'] = []
        if self.notify_object_list is not None:
            for k in self.notify_object_list:
                result['notifyObjectList'].append(k.to_map() if k else None)
        if self.notify_object_type is not None:
            result['notifyObjectType'] = self.notify_object_type
        if self.scope is not None:
            result['scope'] = self.scope
        result['scopeObjectList'] = []
        if self.scope_object_list is not None:
            for k in self.scope_object_list:
                result['scopeObjectList'].append(k.to_map() if k else None)
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.status is not None:
            result['status'] = self.status
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        if self.subscription_title is not None:
            result['subscriptionTitle'] = self.subscription_title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('expiredType') is not None:
            self.expired_type = m.get('expiredType')
        self.notify_object_list = []
        if m.get('notifyObjectList') is not None:
            for k in m.get('notifyObjectList'):
                temp_model = ListSubscriptionsResponseBodyDataNotifyObjectList()
                self.notify_object_list.append(temp_model.from_map(k))
        if m.get('notifyObjectType') is not None:
            self.notify_object_type = m.get('notifyObjectType')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        self.scope_object_list = []
        if m.get('scopeObjectList') is not None:
            for k in m.get('scopeObjectList'):
                temp_model = ListSubscriptionsResponseBodyDataScopeObjectList()
                self.scope_object_list.append(temp_model.from_map(k))
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        if m.get('subscriptionTitle') is not None:
            self.subscription_title = m.get('subscriptionTitle')
        return self


class ListSubscriptionsResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListSubscriptionsResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListSubscriptionsResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListSubscriptionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListSubscriptionsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListSubscriptionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTrendForSourceEventRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        instance_id: int = None,
        instance_type: str = None,
        request_id: str = None,
        start_time: str = None,
        time_unit: int = None,
    ):
        self.end_time = end_time
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.request_id = request_id
        self.start_time = start_time
        self.time_unit = time_unit

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.time_unit is not None:
            result['timeUnit'] = self.time_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('timeUnit') is not None:
            self.time_unit = m.get('timeUnit')
        return self


class ListTrendForSourceEventResponseBodyData(TeaModel):
    def __init__(
        self,
        convergence_rate: str = None,
        max_sustain_time: int = None,
        skip_day: bool = None,
        source_events_stat_map: Dict[str, Any] = None,
        unit: str = None,
    ):
        self.convergence_rate = convergence_rate
        self.max_sustain_time = max_sustain_time
        self.skip_day = skip_day
        self.source_events_stat_map = source_events_stat_map
        self.unit = unit

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.convergence_rate is not None:
            result['convergenceRate'] = self.convergence_rate
        if self.max_sustain_time is not None:
            result['maxSustainTime'] = self.max_sustain_time
        if self.skip_day is not None:
            result['skipDay'] = self.skip_day
        if self.source_events_stat_map is not None:
            result['sourceEventsStatMap'] = self.source_events_stat_map
        if self.unit is not None:
            result['unit'] = self.unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('convergenceRate') is not None:
            self.convergence_rate = m.get('convergenceRate')
        if m.get('maxSustainTime') is not None:
            self.max_sustain_time = m.get('maxSustainTime')
        if m.get('skipDay') is not None:
            self.skip_day = m.get('skipDay')
        if m.get('sourceEventsStatMap') is not None:
            self.source_events_stat_map = m.get('sourceEventsStatMap')
        if m.get('unit') is not None:
            self.unit = m.get('unit')
        return self


class ListTrendForSourceEventResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListTrendForSourceEventResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListTrendForSourceEventResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListTrendForSourceEventResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListTrendForSourceEventResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListTrendForSourceEventResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListUserSerivceGroupsRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        user_id: int = None,
    ):
        # clientToken
        self.client_token = client_token
        # This parameter is required.
        self.user_id = user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.user_id is not None:
            result['userId'] = self.user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        return self


class ListUserSerivceGroupsResponseBodyDataServiceGroups(TeaModel):
    def __init__(
        self,
        service_group_description: str = None,
        service_group_id: int = None,
        service_group_name: str = None,
    ):
        self.service_group_description = service_group_description
        self.service_group_id = service_group_id
        self.service_group_name = service_group_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.service_group_description is not None:
            result['serviceGroupDescription'] = self.service_group_description
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('serviceGroupDescription') is not None:
            self.service_group_description = m.get('serviceGroupDescription')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        return self


class ListUserSerivceGroupsResponseBodyData(TeaModel):
    def __init__(
        self,
        email: str = None,
        phone: str = None,
        ram_id: int = None,
        service_groups: List[ListUserSerivceGroupsResponseBodyDataServiceGroups] = None,
        user_id: int = None,
        username: str = None,
    ):
        self.email = email
        self.phone = phone
        self.ram_id = ram_id
        self.service_groups = service_groups
        self.user_id = user_id
        self.username = username

    def validate(self):
        if self.service_groups:
            for k in self.service_groups:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.email is not None:
            result['email'] = self.email
        if self.phone is not None:
            result['phone'] = self.phone
        if self.ram_id is not None:
            result['ramId'] = self.ram_id
        result['serviceGroups'] = []
        if self.service_groups is not None:
            for k in self.service_groups:
                result['serviceGroups'].append(k.to_map() if k else None)
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('email') is not None:
            self.email = m.get('email')
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('ramId') is not None:
            self.ram_id = m.get('ramId')
        self.service_groups = []
        if m.get('serviceGroups') is not None:
            for k in m.get('serviceGroups'):
                temp_model = ListUserSerivceGroupsResponseBodyDataServiceGroups()
                self.service_groups.append(temp_model.from_map(k))
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class ListUserSerivceGroupsResponseBody(TeaModel):
    def __init__(
        self,
        data: ListUserSerivceGroupsResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = ListUserSerivceGroupsResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ListUserSerivceGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListUserSerivceGroupsResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListUserSerivceGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListUsersRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        page_number: int = None,
        page_size: int = None,
        phone: str = None,
        ram_id: str = None,
        scene: int = None,
        synergy_channel: str = None,
        username: str = None,
    ):
        # clientToken
        self.client_token = client_token
        self.page_number = page_number
        self.page_size = page_size
        self.phone = phone
        self.ram_id = ram_id
        self.scene = scene
        self.synergy_channel = synergy_channel
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.phone is not None:
            result['phone'] = self.phone
        if self.ram_id is not None:
            result['ramId'] = self.ram_id
        if self.scene is not None:
            result['scene'] = self.scene
        if self.synergy_channel is not None:
            result['synergyChannel'] = self.synergy_channel
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('ramId') is not None:
            self.ram_id = m.get('ramId')
        if m.get('scene') is not None:
            self.scene = m.get('scene')
        if m.get('synergyChannel') is not None:
            self.synergy_channel = m.get('synergyChannel')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class ListUsersResponseBodyData(TeaModel):
    def __init__(
        self,
        account_type: int = None,
        app_account: str = None,
        email: str = None,
        gmt_active: str = None,
        gmt_create: str = None,
        is_active: int = None,
        is_editable_user: int = None,
        is_operation: int = None,
        is_ram: int = None,
        is_related: str = None,
        phone: str = None,
        ram_id: int = None,
        role_id_list: List[int] = None,
        role_name_list: List[str] = None,
        synergy_channel: str = None,
        user_id: int = None,
        username: str = None,
    ):
        self.account_type = account_type
        self.app_account = app_account
        self.email = email
        self.gmt_active = gmt_active
        self.gmt_create = gmt_create
        self.is_active = is_active
        self.is_editable_user = is_editable_user
        self.is_operation = is_operation
        self.is_ram = is_ram
        self.is_related = is_related
        self.phone = phone
        self.ram_id = ram_id
        self.role_id_list = role_id_list
        self.role_name_list = role_name_list
        self.synergy_channel = synergy_channel
        self.user_id = user_id
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_type is not None:
            result['accountType'] = self.account_type
        if self.app_account is not None:
            result['appAccount'] = self.app_account
        if self.email is not None:
            result['email'] = self.email
        if self.gmt_active is not None:
            result['gmtActive'] = self.gmt_active
        if self.gmt_create is not None:
            result['gmtCreate'] = self.gmt_create
        if self.is_active is not None:
            result['isActive'] = self.is_active
        if self.is_editable_user is not None:
            result['isEditableUser'] = self.is_editable_user
        if self.is_operation is not None:
            result['isOperation'] = self.is_operation
        if self.is_ram is not None:
            result['isRam'] = self.is_ram
        if self.is_related is not None:
            result['isRelated'] = self.is_related
        if self.phone is not None:
            result['phone'] = self.phone
        if self.ram_id is not None:
            result['ramId'] = self.ram_id
        if self.role_id_list is not None:
            result['roleIdList'] = self.role_id_list
        if self.role_name_list is not None:
            result['roleNameList'] = self.role_name_list
        if self.synergy_channel is not None:
            result['synergyChannel'] = self.synergy_channel
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accountType') is not None:
            self.account_type = m.get('accountType')
        if m.get('appAccount') is not None:
            self.app_account = m.get('appAccount')
        if m.get('email') is not None:
            self.email = m.get('email')
        if m.get('gmtActive') is not None:
            self.gmt_active = m.get('gmtActive')
        if m.get('gmtCreate') is not None:
            self.gmt_create = m.get('gmtCreate')
        if m.get('isActive') is not None:
            self.is_active = m.get('isActive')
        if m.get('isEditableUser') is not None:
            self.is_editable_user = m.get('isEditableUser')
        if m.get('isOperation') is not None:
            self.is_operation = m.get('isOperation')
        if m.get('isRam') is not None:
            self.is_ram = m.get('isRam')
        if m.get('isRelated') is not None:
            self.is_related = m.get('isRelated')
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('ramId') is not None:
            self.ram_id = m.get('ramId')
        if m.get('roleIdList') is not None:
            self.role_id_list = m.get('roleIdList')
        if m.get('roleNameList') is not None:
            self.role_name_list = m.get('roleNameList')
        if m.get('synergyChannel') is not None:
            self.synergy_channel = m.get('synergyChannel')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class ListUsersResponseBody(TeaModel):
    def __init__(
        self,
        data: List[ListUsersResponseBodyData] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total_count: int = None,
    ):
        # data
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        # id of the request
        self.request_id = request_id
        self.total_count = total_count

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['pageNumber'] = self.page_number
        if self.page_size is not None:
            result['pageSize'] = self.page_size
        if self.request_id is not None:
            result['requestId'] = self.request_id
        if self.total_count is not None:
            result['totalCount'] = self.total_count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = ListUsersResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('pageNumber') is not None:
            self.page_number = m.get('pageNumber')
        if m.get('pageSize') is not None:
            self.page_size = m.get('pageSize')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        if m.get('totalCount') is not None:
            self.total_count = m.get('totalCount')
        return self


class ListUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ListUsersResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PushMonitorRequest(TeaModel):
    def __init__(
        self,
        body: str = None,
    ):
        self.body = body

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body is not None:
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class PushMonitorResponseBody(TeaModel):
    def __init__(
        self,
        data: Any = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class PushMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PushMonitorResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PushMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RecoverProblemRequest(TeaModel):
    def __init__(
        self,
        problem_id: int = None,
        problem_notify_type: str = None,
        recovery_time: str = None,
    ):
        self.problem_id = problem_id
        self.problem_notify_type = problem_notify_type
        self.recovery_time = recovery_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        if self.recovery_time is not None:
            result['recoveryTime'] = self.recovery_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        if m.get('recoveryTime') is not None:
            self.recovery_time = m.get('recoveryTime')
        return self


class RecoverProblemResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class RecoverProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RecoverProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RecoverProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RefreshIntegrationConfigKeyRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class RefreshIntegrationConfigKeyResponseBodyData(TeaModel):
    def __init__(
        self,
        key: str = None,
    ):
        self.key = key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        return self


class RefreshIntegrationConfigKeyResponseBody(TeaModel):
    def __init__(
        self,
        data: RefreshIntegrationConfigKeyResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = RefreshIntegrationConfigKeyResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class RefreshIntegrationConfigKeyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RefreshIntegrationConfigKeyResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RefreshIntegrationConfigKeyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class RemoveIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class RemoveIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RemoveIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RemoveIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveProblemServiceGroupRequest(TeaModel):
    def __init__(
        self,
        problem_id: int = None,
        service_group_ids: List[int] = None,
    ):
        self.problem_id = problem_id
        self.service_group_ids = service_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.service_group_ids is not None:
            result['serviceGroupIds'] = self.service_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('serviceGroupIds') is not None:
            self.service_group_ids = m.get('serviceGroupIds')
        return self


class RemoveProblemServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class RemoveProblemServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RemoveProblemServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RemoveProblemServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ReplayProblemRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
        replay_duty_user_id: int = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id
        self.replay_duty_user_id = replay_duty_user_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.replay_duty_user_id is not None:
            result['replayDutyUserId'] = self.replay_duty_user_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('replayDutyUserId') is not None:
            self.replay_duty_user_id = m.get('replayDutyUserId')
        return self


class ReplayProblemResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class ReplayProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ReplayProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ReplayProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RespondIncidentRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        incident_ids: List[int] = None,
    ):
        self.client_token = client_token
        # 影响程度
        self.incident_ids = incident_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.incident_ids is not None:
            result['incidentIds'] = self.incident_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('incidentIds') is not None:
            self.incident_ids = m.get('incidentIds')
        return self


class RespondIncidentResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class RespondIncidentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RespondIncidentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RespondIncidentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RevokeProblemRecoveryRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
        problem_notify_type: str = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id
        self.problem_notify_type = problem_notify_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        return self


class RevokeProblemRecoveryResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class RevokeProblemRecoveryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RevokeProblemRecoveryResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RevokeProblemRecoveryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UnbindUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UnbindUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UnbindUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UnbindUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateEscalationPlanRequestEscalationPlanRulesEscalationPlanConditions(TeaModel):
    def __init__(
        self,
        effection: str = None,
        level: str = None,
    ):
        # LOW HIGH
        self.effection = effection
        # P1 P2 P3 P4
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.effection is not None:
            result['effection'] = self.effection
        if self.level is not None:
            result['level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('level') is not None:
            self.level = m.get('level')
        return self


class UpdateEscalationPlanRequestEscalationPlanRulesEscalationPlanStrategies(TeaModel):
    def __init__(
        self,
        enable_webhook: bool = None,
        escalation_plan_type: str = None,
        notice_channels: List[str] = None,
        notice_objects: List[int] = None,
        notice_role_list: List[int] = None,
        notice_time: int = None,
        service_group_ids: List[int] = None,
    ):
        self.enable_webhook = enable_webhook
        self.escalation_plan_type = escalation_plan_type
        self.notice_channels = notice_channels
        self.notice_objects = notice_objects
        self.notice_role_list = notice_role_list
        self.notice_time = notice_time
        self.service_group_ids = service_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.enable_webhook is not None:
            result['enableWebhook'] = self.enable_webhook
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        if self.notice_channels is not None:
            result['noticeChannels'] = self.notice_channels
        if self.notice_objects is not None:
            result['noticeObjects'] = self.notice_objects
        if self.notice_role_list is not None:
            result['noticeRoleList'] = self.notice_role_list
        if self.notice_time is not None:
            result['noticeTime'] = self.notice_time
        if self.service_group_ids is not None:
            result['serviceGroupIds'] = self.service_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('enableWebhook') is not None:
            self.enable_webhook = m.get('enableWebhook')
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        if m.get('noticeChannels') is not None:
            self.notice_channels = m.get('noticeChannels')
        if m.get('noticeObjects') is not None:
            self.notice_objects = m.get('noticeObjects')
        if m.get('noticeRoleList') is not None:
            self.notice_role_list = m.get('noticeRoleList')
        if m.get('noticeTime') is not None:
            self.notice_time = m.get('noticeTime')
        if m.get('serviceGroupIds') is not None:
            self.service_group_ids = m.get('serviceGroupIds')
        return self


class UpdateEscalationPlanRequestEscalationPlanRules(TeaModel):
    def __init__(
        self,
        escalation_plan_conditions: List[UpdateEscalationPlanRequestEscalationPlanRulesEscalationPlanConditions] = None,
        escalation_plan_strategies: List[UpdateEscalationPlanRequestEscalationPlanRulesEscalationPlanStrategies] = None,
        escalation_plan_type: str = None,
        id: int = None,
    ):
        self.escalation_plan_conditions = escalation_plan_conditions
        self.escalation_plan_strategies = escalation_plan_strategies
        self.escalation_plan_type = escalation_plan_type
        self.id = id

    def validate(self):
        if self.escalation_plan_conditions:
            for k in self.escalation_plan_conditions:
                if k:
                    k.validate()
        if self.escalation_plan_strategies:
            for k in self.escalation_plan_strategies:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['escalationPlanConditions'] = []
        if self.escalation_plan_conditions is not None:
            for k in self.escalation_plan_conditions:
                result['escalationPlanConditions'].append(k.to_map() if k else None)
        result['escalationPlanStrategies'] = []
        if self.escalation_plan_strategies is not None:
            for k in self.escalation_plan_strategies:
                result['escalationPlanStrategies'].append(k.to_map() if k else None)
        if self.escalation_plan_type is not None:
            result['escalationPlanType'] = self.escalation_plan_type
        if self.id is not None:
            result['id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.escalation_plan_conditions = []
        if m.get('escalationPlanConditions') is not None:
            for k in m.get('escalationPlanConditions'):
                temp_model = UpdateEscalationPlanRequestEscalationPlanRulesEscalationPlanConditions()
                self.escalation_plan_conditions.append(temp_model.from_map(k))
        self.escalation_plan_strategies = []
        if m.get('escalationPlanStrategies') is not None:
            for k in m.get('escalationPlanStrategies'):
                temp_model = UpdateEscalationPlanRequestEscalationPlanRulesEscalationPlanStrategies()
                self.escalation_plan_strategies.append(temp_model.from_map(k))
        if m.get('escalationPlanType') is not None:
            self.escalation_plan_type = m.get('escalationPlanType')
        if m.get('id') is not None:
            self.id = m.get('id')
        return self


class UpdateEscalationPlanRequestEscalationPlanScopeObjects(TeaModel):
    def __init__(
        self,
        id: int = None,
        scope: str = None,
        scope_object_id: int = None,
    ):
        # This parameter is required.
        self.id = id
        self.scope = scope
        # This parameter is required.
        self.scope_object_id = scope_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.scope is not None:
            result['scope'] = self.scope
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        return self


class UpdateEscalationPlanRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_description: str = None,
        escalation_plan_id: int = None,
        escalation_plan_name: str = None,
        escalation_plan_rules: List[UpdateEscalationPlanRequestEscalationPlanRules] = None,
        escalation_plan_scope_objects: List[UpdateEscalationPlanRequestEscalationPlanScopeObjects] = None,
        is_global: bool = None,
    ):
        # clientToken
        self.client_token = client_token
        self.escalation_plan_description = escalation_plan_description
        # This parameter is required.
        self.escalation_plan_id = escalation_plan_id
        self.escalation_plan_name = escalation_plan_name
        self.escalation_plan_rules = escalation_plan_rules
        self.escalation_plan_scope_objects = escalation_plan_scope_objects
        self.is_global = is_global

    def validate(self):
        if self.escalation_plan_rules:
            for k in self.escalation_plan_rules:
                if k:
                    k.validate()
        if self.escalation_plan_scope_objects:
            for k in self.escalation_plan_scope_objects:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_description is not None:
            result['escalationPlanDescription'] = self.escalation_plan_description
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        result['escalationPlanRules'] = []
        if self.escalation_plan_rules is not None:
            for k in self.escalation_plan_rules:
                result['escalationPlanRules'].append(k.to_map() if k else None)
        result['escalationPlanScopeObjects'] = []
        if self.escalation_plan_scope_objects is not None:
            for k in self.escalation_plan_scope_objects:
                result['escalationPlanScopeObjects'].append(k.to_map() if k else None)
        if self.is_global is not None:
            result['isGlobal'] = self.is_global
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanDescription') is not None:
            self.escalation_plan_description = m.get('escalationPlanDescription')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        self.escalation_plan_rules = []
        if m.get('escalationPlanRules') is not None:
            for k in m.get('escalationPlanRules'):
                temp_model = UpdateEscalationPlanRequestEscalationPlanRules()
                self.escalation_plan_rules.append(temp_model.from_map(k))
        self.escalation_plan_scope_objects = []
        if m.get('escalationPlanScopeObjects') is not None:
            for k in m.get('escalationPlanScopeObjects'):
                temp_model = UpdateEscalationPlanRequestEscalationPlanScopeObjects()
                self.escalation_plan_scope_objects.append(temp_model.from_map(k))
        if m.get('isGlobal') is not None:
            self.is_global = m.get('isGlobal')
        return self


class UpdateEscalationPlanResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateEscalationPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateEscalationPlanResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateEscalationPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateIncidentRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        effect: str = None,
        incident_id: int = None,
        incident_level: str = None,
        incident_title: str = None,
    ):
        self.client_token = client_token
        self.effect = effect
        # This parameter is required.
        self.incident_id = incident_id
        self.incident_level = incident_level
        self.incident_title = incident_title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.effect is not None:
            result['effect'] = self.effect
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.incident_title is not None:
            result['incidentTitle'] = self.incident_title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('effect') is not None:
            self.effect = m.get('effect')
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('incidentTitle') is not None:
            self.incident_title = m.get('incidentTitle')
        return self


class UpdateIncidentResponseBodyData(TeaModel):
    def __init__(
        self,
        incident_id: int = None,
    ):
        self.incident_id = incident_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.incident_id is not None:
            result['incidentId'] = self.incident_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('incidentId') is not None:
            self.incident_id = m.get('incidentId')
        return self


class UpdateIncidentResponseBody(TeaModel):
    def __init__(
        self,
        data: UpdateIncidentResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = UpdateIncidentResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateIncidentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateIncidentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateIncidentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateIntegrationConfigRequest(TeaModel):
    def __init__(
        self,
        access_key: str = None,
        client_token: str = None,
        integration_config_id: int = None,
    ):
        # accessKey
        self.access_key = access_key
        self.client_token = client_token
        self.integration_config_id = integration_config_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key is not None:
            result['accessKey'] = self.access_key
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.integration_config_id is not None:
            result['integrationConfigId'] = self.integration_config_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKey') is not None:
            self.access_key = m.get('accessKey')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('integrationConfigId') is not None:
            self.integration_config_id = m.get('integrationConfigId')
        return self


class UpdateIntegrationConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateIntegrationConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateIntegrationConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateIntegrationConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateProblemRequest(TeaModel):
    def __init__(
        self,
        feedback: str = None,
        level: str = None,
        main_handler_id: int = None,
        preliminary_reason: str = None,
        problem_id: int = None,
        problem_name: str = None,
        progress_summary: str = None,
        progress_summary_rich_text_id: int = None,
        related_service_id: int = None,
        service_group_ids: List[int] = None,
    ):
        self.feedback = feedback
        self.level = level
        self.main_handler_id = main_handler_id
        self.preliminary_reason = preliminary_reason
        self.problem_id = problem_id
        self.problem_name = problem_name
        self.progress_summary = progress_summary
        self.progress_summary_rich_text_id = progress_summary_rich_text_id
        self.related_service_id = related_service_id
        self.service_group_ids = service_group_ids

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.feedback is not None:
            result['feedback'] = self.feedback
        if self.level is not None:
            result['level'] = self.level
        if self.main_handler_id is not None:
            result['mainHandlerId'] = self.main_handler_id
        if self.preliminary_reason is not None:
            result['preliminaryReason'] = self.preliminary_reason
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_name is not None:
            result['problemName'] = self.problem_name
        if self.progress_summary is not None:
            result['progressSummary'] = self.progress_summary
        if self.progress_summary_rich_text_id is not None:
            result['progressSummaryRichTextId'] = self.progress_summary_rich_text_id
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        if self.service_group_ids is not None:
            result['serviceGroupIds'] = self.service_group_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('feedback') is not None:
            self.feedback = m.get('feedback')
        if m.get('level') is not None:
            self.level = m.get('level')
        if m.get('mainHandlerId') is not None:
            self.main_handler_id = m.get('mainHandlerId')
        if m.get('preliminaryReason') is not None:
            self.preliminary_reason = m.get('preliminaryReason')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemName') is not None:
            self.problem_name = m.get('problemName')
        if m.get('progressSummary') is not None:
            self.progress_summary = m.get('progressSummary')
        if m.get('progressSummaryRichTextId') is not None:
            self.progress_summary_rich_text_id = m.get('progressSummaryRichTextId')
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        if m.get('serviceGroupIds') is not None:
            self.service_group_ids = m.get('serviceGroupIds')
        return self


class UpdateProblemResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateProblemResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateProblemResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateProblemResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateProblemEffectionServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        description: str = None,
        effection_service_id: int = None,
        level: str = None,
        pic_url: List[str] = None,
        problem_id: int = None,
        service_id: int = None,
        status: str = None,
    ):
        # clientToken
        self.client_token = client_token
        self.description = description
        self.effection_service_id = effection_service_id
        self.level = level
        self.pic_url = pic_url
        self.problem_id = problem_id
        self.service_id = service_id
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.description is not None:
            result['description'] = self.description
        if self.effection_service_id is not None:
            result['effectionServiceId'] = self.effection_service_id
        if self.level is not None:
            result['level'] = self.level
        if self.pic_url is not None:
            result['picUrl'] = self.pic_url
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.status is not None:
            result['status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('description') is not None:
            self.description = m.get('description')
        if m.get('effectionServiceId') is not None:
            self.effection_service_id = m.get('effectionServiceId')
        if m.get('level') is not None:
            self.level = m.get('level')
        if m.get('picUrl') is not None:
            self.pic_url = m.get('picUrl')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('status') is not None:
            self.status = m.get('status')
        return self


class UpdateProblemEffectionServiceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # requestId
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateProblemEffectionServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateProblemEffectionServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateProblemEffectionServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateProblemImprovementRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        custom_problem_reason: str = None,
        discover_source: int = None,
        duty_department_id: int = None,
        duty_department_name: str = None,
        duty_user_id: int = None,
        injection_mode: str = None,
        monitor_source_name: str = None,
        problem_id: int = None,
        problem_reason: str = None,
        recent_activity: str = None,
        recovery_mode: str = None,
        relation_changes: str = None,
        remark: str = None,
        replay_duty_user_id: int = None,
        user_report: int = None,
    ):
        self.client_token = client_token
        self.custom_problem_reason = custom_problem_reason
        self.discover_source = discover_source
        self.duty_department_id = duty_department_id
        self.duty_department_name = duty_department_name
        self.duty_user_id = duty_user_id
        self.injection_mode = injection_mode
        self.monitor_source_name = monitor_source_name
        self.problem_id = problem_id
        self.problem_reason = problem_reason
        self.recent_activity = recent_activity
        self.recovery_mode = recovery_mode
        self.relation_changes = relation_changes
        self.remark = remark
        self.replay_duty_user_id = replay_duty_user_id
        self.user_report = user_report

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.custom_problem_reason is not None:
            result['customProblemReason'] = self.custom_problem_reason
        if self.discover_source is not None:
            result['discoverSource'] = self.discover_source
        if self.duty_department_id is not None:
            result['dutyDepartmentId'] = self.duty_department_id
        if self.duty_department_name is not None:
            result['dutyDepartmentName'] = self.duty_department_name
        if self.duty_user_id is not None:
            result['dutyUserId'] = self.duty_user_id
        if self.injection_mode is not None:
            result['injectionMode'] = self.injection_mode
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_reason is not None:
            result['problemReason'] = self.problem_reason
        if self.recent_activity is not None:
            result['recentActivity'] = self.recent_activity
        if self.recovery_mode is not None:
            result['recoveryMode'] = self.recovery_mode
        if self.relation_changes is not None:
            result['relationChanges'] = self.relation_changes
        if self.remark is not None:
            result['remark'] = self.remark
        if self.replay_duty_user_id is not None:
            result['replayDutyUserId'] = self.replay_duty_user_id
        if self.user_report is not None:
            result['userReport'] = self.user_report
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('customProblemReason') is not None:
            self.custom_problem_reason = m.get('customProblemReason')
        if m.get('discoverSource') is not None:
            self.discover_source = m.get('discoverSource')
        if m.get('dutyDepartmentId') is not None:
            self.duty_department_id = m.get('dutyDepartmentId')
        if m.get('dutyDepartmentName') is not None:
            self.duty_department_name = m.get('dutyDepartmentName')
        if m.get('dutyUserId') is not None:
            self.duty_user_id = m.get('dutyUserId')
        if m.get('injectionMode') is not None:
            self.injection_mode = m.get('injectionMode')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemReason') is not None:
            self.problem_reason = m.get('problemReason')
        if m.get('recentActivity') is not None:
            self.recent_activity = m.get('recentActivity')
        if m.get('recoveryMode') is not None:
            self.recovery_mode = m.get('recoveryMode')
        if m.get('relationChanges') is not None:
            self.relation_changes = m.get('relationChanges')
        if m.get('remark') is not None:
            self.remark = m.get('remark')
        if m.get('replayDutyUserId') is not None:
            self.replay_duty_user_id = m.get('replayDutyUserId')
        if m.get('userReport') is not None:
            self.user_report = m.get('userReport')
        return self


class UpdateProblemImprovementResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateProblemImprovementResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateProblemImprovementResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateProblemImprovementResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateProblemMeasureRequest(TeaModel):
    def __init__(
        self,
        check_standard: str = None,
        check_user_id: int = None,
        client_token: str = None,
        content: str = None,
        director_id: int = None,
        measure_id: int = None,
        plan_finish_time: str = None,
        problem_id: int = None,
        stalker_id: int = None,
        status: str = None,
        type: int = None,
    ):
        self.check_standard = check_standard
        self.check_user_id = check_user_id
        self.client_token = client_token
        self.content = content
        self.director_id = director_id
        self.measure_id = measure_id
        self.plan_finish_time = plan_finish_time
        self.problem_id = problem_id
        self.stalker_id = stalker_id
        self.status = status
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.check_standard is not None:
            result['checkStandard'] = self.check_standard
        if self.check_user_id is not None:
            result['checkUserId'] = self.check_user_id
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.content is not None:
            result['content'] = self.content
        if self.director_id is not None:
            result['directorId'] = self.director_id
        if self.measure_id is not None:
            result['measureId'] = self.measure_id
        if self.plan_finish_time is not None:
            result['planFinishTime'] = self.plan_finish_time
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.stalker_id is not None:
            result['stalkerId'] = self.stalker_id
        if self.status is not None:
            result['status'] = self.status
        if self.type is not None:
            result['type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('checkStandard') is not None:
            self.check_standard = m.get('checkStandard')
        if m.get('checkUserId') is not None:
            self.check_user_id = m.get('checkUserId')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('directorId') is not None:
            self.director_id = m.get('directorId')
        if m.get('measureId') is not None:
            self.measure_id = m.get('measureId')
        if m.get('planFinishTime') is not None:
            self.plan_finish_time = m.get('planFinishTime')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('stalkerId') is not None:
            self.stalker_id = m.get('stalkerId')
        if m.get('status') is not None:
            self.status = m.get('status')
        if m.get('type') is not None:
            self.type = m.get('type')
        return self


class UpdateProblemMeasureResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateProblemMeasureResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateProblemMeasureResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateProblemMeasureResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateProblemNoticeRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        problem_id: int = None,
        problem_notify_type: str = None,
    ):
        self.client_token = client_token
        self.problem_id = problem_id
        self.problem_notify_type = problem_notify_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        return self


class UpdateProblemNoticeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateProblemNoticeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateProblemNoticeResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateProblemNoticeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateProblemTimelineRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        content: str = None,
        key_node: str = None,
        problem_id: int = None,
        problem_timeline_id: int = None,
        time: str = None,
    ):
        self.client_token = client_token
        self.content = content
        self.key_node = key_node
        self.problem_id = problem_id
        self.problem_timeline_id = problem_timeline_id
        self.time = time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.content is not None:
            result['content'] = self.content
        if self.key_node is not None:
            result['keyNode'] = self.key_node
        if self.problem_id is not None:
            result['problemId'] = self.problem_id
        if self.problem_timeline_id is not None:
            result['problemTimelineId'] = self.problem_timeline_id
        if self.time is not None:
            result['time'] = self.time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('content') is not None:
            self.content = m.get('content')
        if m.get('keyNode') is not None:
            self.key_node = m.get('keyNode')
        if m.get('problemId') is not None:
            self.problem_id = m.get('problemId')
        if m.get('problemTimelineId') is not None:
            self.problem_timeline_id = m.get('problemTimelineId')
        if m.get('time') is not None:
            self.time = m.get('time')
        return self


class UpdateProblemTimelineResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateProblemTimelineResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateProblemTimelineResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateProblemTimelineResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateRichTextRequest(TeaModel):
    def __init__(
        self,
        instance_id: int = None,
        instance_type: str = None,
        rich_text: str = None,
        rich_text_id: int = None,
    ):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.rich_text = rich_text
        self.rich_text_id = rich_text_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_id is not None:
            result['instanceId'] = self.instance_id
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        if self.rich_text is not None:
            result['richText'] = self.rich_text
        if self.rich_text_id is not None:
            result['richTextId'] = self.rich_text_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceId') is not None:
            self.instance_id = m.get('instanceId')
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        if m.get('richText') is not None:
            self.rich_text = m.get('richText')
        if m.get('richTextId') is not None:
            self.rich_text_id = m.get('richTextId')
        return self


class UpdateRichTextResponseBodyData(TeaModel):
    def __init__(
        self,
        id: int = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        return self


class UpdateRichTextResponseBody(TeaModel):
    def __init__(
        self,
        data: UpdateRichTextResponseBodyData = None,
        request_id: str = None,
    ):
        # data
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = UpdateRichTextResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateRichTextResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateRichTextResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateRichTextResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateRouteRuleRequestRouteChildRulesConditions(TeaModel):
    def __init__(
        self,
        key: str = None,
        operation_symbol: str = None,
        value: str = None,
    ):
        # This parameter is required.
        self.key = key
        # This parameter is required.
        self.operation_symbol = operation_symbol
        # This parameter is required.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['key'] = self.key
        if self.operation_symbol is not None:
            result['operationSymbol'] = self.operation_symbol
        if self.value is not None:
            result['value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('key') is not None:
            self.key = m.get('key')
        if m.get('operationSymbol') is not None:
            self.operation_symbol = m.get('operationSymbol')
        if m.get('value') is not None:
            self.value = m.get('value')
        return self


class UpdateRouteRuleRequestRouteChildRules(TeaModel):
    def __init__(
        self,
        child_condition_relation: int = None,
        child_route_rule_id: int = None,
        conditions: List[UpdateRouteRuleRequestRouteChildRulesConditions] = None,
        is_valid_child_rule: bool = None,
        monitor_source_id: int = None,
        problem_level: str = None,
    ):
        self.child_condition_relation = child_condition_relation
        # This parameter is required.
        self.child_route_rule_id = child_route_rule_id
        # This parameter is required.
        self.conditions = conditions
        # This parameter is required.
        self.is_valid_child_rule = is_valid_child_rule
        # This parameter is required.
        self.monitor_source_id = monitor_source_id
        self.problem_level = problem_level

    def validate(self):
        if self.conditions:
            for k in self.conditions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.child_condition_relation is not None:
            result['childConditionRelation'] = self.child_condition_relation
        if self.child_route_rule_id is not None:
            result['childRouteRuleId'] = self.child_route_rule_id
        result['conditions'] = []
        if self.conditions is not None:
            for k in self.conditions:
                result['conditions'].append(k.to_map() if k else None)
        if self.is_valid_child_rule is not None:
            result['isValidChildRule'] = self.is_valid_child_rule
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.problem_level is not None:
            result['problemLevel'] = self.problem_level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('childConditionRelation') is not None:
            self.child_condition_relation = m.get('childConditionRelation')
        if m.get('childRouteRuleId') is not None:
            self.child_route_rule_id = m.get('childRouteRuleId')
        self.conditions = []
        if m.get('conditions') is not None:
            for k in m.get('conditions'):
                temp_model = UpdateRouteRuleRequestRouteChildRulesConditions()
                self.conditions.append(temp_model.from_map(k))
        if m.get('isValidChildRule') is not None:
            self.is_valid_child_rule = m.get('isValidChildRule')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('problemLevel') is not None:
            self.problem_level = m.get('problemLevel')
        return self


class UpdateRouteRuleRequest(TeaModel):
    def __init__(
        self,
        assign_object_id: int = None,
        assign_object_type: str = None,
        child_rule_relation: str = None,
        client_token: str = None,
        convergence_fields: List[str] = None,
        convergence_type: int = None,
        coverage_problem_levels: List[str] = None,
        effection: str = None,
        incident_level: str = None,
        match_count: int = None,
        notify_channels: List[str] = None,
        problem_effection_services: List[int] = None,
        problem_level_group: Dict[str, ProblemLevelGroupValue] = None,
        related_service_id: int = None,
        route_child_rules: List[UpdateRouteRuleRequestRouteChildRules] = None,
        route_rule_id: int = None,
        route_type: str = None,
        rule_name: str = None,
        time_window: int = None,
        time_window_unit: str = None,
    ):
        # This parameter is required.
        self.assign_object_id = assign_object_id
        # This parameter is required.
        self.assign_object_type = assign_object_type
        self.child_rule_relation = child_rule_relation
        self.client_token = client_token
        self.convergence_fields = convergence_fields
        self.convergence_type = convergence_type
        self.coverage_problem_levels = coverage_problem_levels
        # This parameter is required.
        self.effection = effection
        # This parameter is required.
        self.incident_level = incident_level
        # This parameter is required.
        self.match_count = match_count
        # This parameter is required.
        self.notify_channels = notify_channels
        self.problem_effection_services = problem_effection_services
        self.problem_level_group = problem_level_group
        # This parameter is required.
        self.related_service_id = related_service_id
        # This parameter is required.
        self.route_child_rules = route_child_rules
        # This parameter is required.
        self.route_rule_id = route_rule_id
        # This parameter is required.
        self.route_type = route_type
        # This parameter is required.
        self.rule_name = rule_name
        # This parameter is required.
        self.time_window = time_window
        # This parameter is required.
        self.time_window_unit = time_window_unit

    def validate(self):
        if self.problem_level_group:
            for v in self.problem_level_group.values():
                if v:
                    v.validate()
        if self.route_child_rules:
            for k in self.route_child_rules:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.assign_object_id is not None:
            result['assignObjectId'] = self.assign_object_id
        if self.assign_object_type is not None:
            result['assignObjectType'] = self.assign_object_type
        if self.child_rule_relation is not None:
            result['childRuleRelation'] = self.child_rule_relation
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.convergence_fields is not None:
            result['convergenceFields'] = self.convergence_fields
        if self.convergence_type is not None:
            result['convergenceType'] = self.convergence_type
        if self.coverage_problem_levels is not None:
            result['coverageProblemLevels'] = self.coverage_problem_levels
        if self.effection is not None:
            result['effection'] = self.effection
        if self.incident_level is not None:
            result['incidentLevel'] = self.incident_level
        if self.match_count is not None:
            result['matchCount'] = self.match_count
        if self.notify_channels is not None:
            result['notifyChannels'] = self.notify_channels
        if self.problem_effection_services is not None:
            result['problemEffectionServices'] = self.problem_effection_services
        result['problemLevelGroup'] = {}
        if self.problem_level_group is not None:
            for k, v in self.problem_level_group.items():
                result['problemLevelGroup'][k] = v.to_map()
        if self.related_service_id is not None:
            result['relatedServiceId'] = self.related_service_id
        result['routeChildRules'] = []
        if self.route_child_rules is not None:
            for k in self.route_child_rules:
                result['routeChildRules'].append(k.to_map() if k else None)
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        if self.route_type is not None:
            result['routeType'] = self.route_type
        if self.rule_name is not None:
            result['ruleName'] = self.rule_name
        if self.time_window is not None:
            result['timeWindow'] = self.time_window
        if self.time_window_unit is not None:
            result['timeWindowUnit'] = self.time_window_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('assignObjectId') is not None:
            self.assign_object_id = m.get('assignObjectId')
        if m.get('assignObjectType') is not None:
            self.assign_object_type = m.get('assignObjectType')
        if m.get('childRuleRelation') is not None:
            self.child_rule_relation = m.get('childRuleRelation')
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('convergenceFields') is not None:
            self.convergence_fields = m.get('convergenceFields')
        if m.get('convergenceType') is not None:
            self.convergence_type = m.get('convergenceType')
        if m.get('coverageProblemLevels') is not None:
            self.coverage_problem_levels = m.get('coverageProblemLevels')
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('incidentLevel') is not None:
            self.incident_level = m.get('incidentLevel')
        if m.get('matchCount') is not None:
            self.match_count = m.get('matchCount')
        if m.get('notifyChannels') is not None:
            self.notify_channels = m.get('notifyChannels')
        if m.get('problemEffectionServices') is not None:
            self.problem_effection_services = m.get('problemEffectionServices')
        self.problem_level_group = {}
        if m.get('problemLevelGroup') is not None:
            for k, v in m.get('problemLevelGroup').items():
                temp_model = ProblemLevelGroupValue()
                self.problem_level_group[k] = temp_model.from_map(v)
        if m.get('relatedServiceId') is not None:
            self.related_service_id = m.get('relatedServiceId')
        self.route_child_rules = []
        if m.get('routeChildRules') is not None:
            for k in m.get('routeChildRules'):
                temp_model = UpdateRouteRuleRequestRouteChildRules()
                self.route_child_rules.append(temp_model.from_map(k))
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        if m.get('routeType') is not None:
            self.route_type = m.get('routeType')
        if m.get('ruleName') is not None:
            self.rule_name = m.get('ruleName')
        if m.get('timeWindow') is not None:
            self.time_window = m.get('timeWindow')
        if m.get('timeWindowUnit') is not None:
            self.time_window_unit = m.get('timeWindowUnit')
        return self


class UpdateRouteRuleResponseBody(TeaModel):
    def __init__(
        self,
        data: int = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateRouteRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateRouteRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateRouteRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateServiceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        escalation_plan_id: int = None,
        service_description: str = None,
        service_group_id_list: List[int] = None,
        service_id: int = None,
        service_name: str = None,
    ):
        self.client_token = client_token
        self.escalation_plan_id = escalation_plan_id
        self.service_description = service_description
        self.service_group_id_list = service_group_id_list
        self.service_id = service_id
        self.service_name = service_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.service_description is not None:
            result['serviceDescription'] = self.service_description
        if self.service_group_id_list is not None:
            result['serviceGroupIdList'] = self.service_group_id_list
        if self.service_id is not None:
            result['serviceId'] = self.service_id
        if self.service_name is not None:
            result['serviceName'] = self.service_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('serviceDescription') is not None:
            self.service_description = m.get('serviceDescription')
        if m.get('serviceGroupIdList') is not None:
            self.service_group_id_list = m.get('serviceGroupIdList')
        if m.get('serviceId') is not None:
            self.service_id = m.get('serviceId')
        if m.get('serviceName') is not None:
            self.service_name = m.get('serviceName')
        return self


class UpdateServiceResponseBody(TeaModel):
    def __init__(
        self,
        data: int = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateServiceResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateServiceGroupRequestMonitorSourceTemplates(TeaModel):
    def __init__(
        self,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
        template_content: str = None,
        template_id: int = None,
    ):
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name
        self.template_content = template_content
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        if self.template_content is not None:
            result['templateContent'] = self.template_content
        if self.template_id is not None:
            result['templateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        if m.get('templateContent') is not None:
            self.template_content = m.get('templateContent')
        if m.get('templateId') is not None:
            self.template_id = m.get('templateId')
        return self


class UpdateServiceGroupRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        enable_webhook: str = None,
        monitor_source_templates: List[UpdateServiceGroupRequestMonitorSourceTemplates] = None,
        service_group_description: str = None,
        service_group_id: int = None,
        service_group_name: str = None,
        user_ids: List[int] = None,
        webhook_link: str = None,
        webhook_type: str = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.enable_webhook = enable_webhook
        self.monitor_source_templates = monitor_source_templates
        self.service_group_description = service_group_description
        # This parameter is required.
        self.service_group_id = service_group_id
        # This parameter is required.
        self.service_group_name = service_group_name
        # This parameter is required.
        self.user_ids = user_ids
        # This parameter is required.
        self.webhook_link = webhook_link
        # This parameter is required.
        self.webhook_type = webhook_type

    def validate(self):
        if self.monitor_source_templates:
            for k in self.monitor_source_templates:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.enable_webhook is not None:
            result['enableWebhook'] = self.enable_webhook
        result['monitorSourceTemplates'] = []
        if self.monitor_source_templates is not None:
            for k in self.monitor_source_templates:
                result['monitorSourceTemplates'].append(k.to_map() if k else None)
        if self.service_group_description is not None:
            result['serviceGroupDescription'] = self.service_group_description
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        if self.service_group_name is not None:
            result['serviceGroupName'] = self.service_group_name
        if self.user_ids is not None:
            result['userIds'] = self.user_ids
        if self.webhook_link is not None:
            result['webhookLink'] = self.webhook_link
        if self.webhook_type is not None:
            result['webhookType'] = self.webhook_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('enableWebhook') is not None:
            self.enable_webhook = m.get('enableWebhook')
        self.monitor_source_templates = []
        if m.get('monitorSourceTemplates') is not None:
            for k in m.get('monitorSourceTemplates'):
                temp_model = UpdateServiceGroupRequestMonitorSourceTemplates()
                self.monitor_source_templates.append(temp_model.from_map(k))
        if m.get('serviceGroupDescription') is not None:
            self.service_group_description = m.get('serviceGroupDescription')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        if m.get('serviceGroupName') is not None:
            self.service_group_name = m.get('serviceGroupName')
        if m.get('userIds') is not None:
            self.user_ids = m.get('userIds')
        if m.get('webhookLink') is not None:
            self.webhook_link = m.get('webhookLink')
        if m.get('webhookType') is not None:
            self.webhook_type = m.get('webhookType')
        return self


class UpdateServiceGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateServiceGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateServiceGroupResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateServiceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateServiceGroupSchedulingRequestFastSchedulingSchedulingUsers(TeaModel):
    def __init__(
        self,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
    ):
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        return self


class UpdateServiceGroupSchedulingRequestFastScheduling(TeaModel):
    def __init__(
        self,
        duty_plan: str = None,
        id: int = None,
        scheduling_users: List[UpdateServiceGroupSchedulingRequestFastSchedulingSchedulingUsers] = None,
        single_duration: int = None,
        single_duration_unit: str = None,
    ):
        self.duty_plan = duty_plan
        self.id = id
        self.scheduling_users = scheduling_users
        self.single_duration = single_duration
        self.single_duration_unit = single_duration_unit

    def validate(self):
        if self.scheduling_users:
            for k in self.scheduling_users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.duty_plan is not None:
            result['dutyPlan'] = self.duty_plan
        if self.id is not None:
            result['id'] = self.id
        result['schedulingUsers'] = []
        if self.scheduling_users is not None:
            for k in self.scheduling_users:
                result['schedulingUsers'].append(k.to_map() if k else None)
        if self.single_duration is not None:
            result['singleDuration'] = self.single_duration
        if self.single_duration_unit is not None:
            result['singleDurationUnit'] = self.single_duration_unit
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dutyPlan') is not None:
            self.duty_plan = m.get('dutyPlan')
        if m.get('id') is not None:
            self.id = m.get('id')
        self.scheduling_users = []
        if m.get('schedulingUsers') is not None:
            for k in m.get('schedulingUsers'):
                temp_model = UpdateServiceGroupSchedulingRequestFastSchedulingSchedulingUsers()
                self.scheduling_users.append(temp_model.from_map(k))
        if m.get('singleDuration') is not None:
            self.single_duration = m.get('singleDuration')
        if m.get('singleDurationUnit') is not None:
            self.single_duration_unit = m.get('singleDurationUnit')
        return self


class UpdateServiceGroupSchedulingRequestFineSchedulingSchedulingFineShifts(TeaModel):
    def __init__(
        self,
        cycle_order: int = None,
        scheduling_end_time: str = None,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
        shift_name: str = None,
        skip_one_day: bool = None,
    ):
        self.cycle_order = cycle_order
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_start_time = scheduling_start_time
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list
        self.shift_name = shift_name
        self.skip_one_day = skip_one_day

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cycle_order is not None:
            result['cycleOrder'] = self.cycle_order
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        if self.shift_name is not None:
            result['shiftName'] = self.shift_name
        if self.skip_one_day is not None:
            result['skipOneDay'] = self.skip_one_day
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('cycleOrder') is not None:
            self.cycle_order = m.get('cycleOrder')
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        if m.get('shiftName') is not None:
            self.shift_name = m.get('shiftName')
        if m.get('skipOneDay') is not None:
            self.skip_one_day = m.get('skipOneDay')
        return self


class UpdateServiceGroupSchedulingRequestFineSchedulingSchedulingTemplateFineShifts(TeaModel):
    def __init__(
        self,
        scheduling_end_time: str = None,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
        shift_name: str = None,
        skip_one_day: bool = None,
    ):
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        self.scheduling_start_time = scheduling_start_time
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list
        self.shift_name = shift_name
        self.skip_one_day = skip_one_day

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        if self.shift_name is not None:
            result['shiftName'] = self.shift_name
        if self.skip_one_day is not None:
            result['skipOneDay'] = self.skip_one_day
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        if m.get('shiftName') is not None:
            self.shift_name = m.get('shiftName')
        if m.get('skipOneDay') is not None:
            self.skip_one_day = m.get('skipOneDay')
        return self


class UpdateServiceGroupSchedulingRequestFineScheduling(TeaModel):
    def __init__(
        self,
        id: int = None,
        period: int = None,
        period_unit: str = None,
        scheduling_fine_shifts: List[UpdateServiceGroupSchedulingRequestFineSchedulingSchedulingFineShifts] = None,
        scheduling_template_fine_shifts: List[UpdateServiceGroupSchedulingRequestFineSchedulingSchedulingTemplateFineShifts] = None,
        shift_type: str = None,
    ):
        self.id = id
        self.period = period
        self.period_unit = period_unit
        self.scheduling_fine_shifts = scheduling_fine_shifts
        self.scheduling_template_fine_shifts = scheduling_template_fine_shifts
        self.shift_type = shift_type

    def validate(self):
        if self.scheduling_fine_shifts:
            for k in self.scheduling_fine_shifts:
                if k:
                    k.validate()
        if self.scheduling_template_fine_shifts:
            for k in self.scheduling_template_fine_shifts:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.period is not None:
            result['period'] = self.period
        if self.period_unit is not None:
            result['periodUnit'] = self.period_unit
        result['schedulingFineShifts'] = []
        if self.scheduling_fine_shifts is not None:
            for k in self.scheduling_fine_shifts:
                result['schedulingFineShifts'].append(k.to_map() if k else None)
        result['schedulingTemplateFineShifts'] = []
        if self.scheduling_template_fine_shifts is not None:
            for k in self.scheduling_template_fine_shifts:
                result['schedulingTemplateFineShifts'].append(k.to_map() if k else None)
        if self.shift_type is not None:
            result['shiftType'] = self.shift_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('period') is not None:
            self.period = m.get('period')
        if m.get('periodUnit') is not None:
            self.period_unit = m.get('periodUnit')
        self.scheduling_fine_shifts = []
        if m.get('schedulingFineShifts') is not None:
            for k in m.get('schedulingFineShifts'):
                temp_model = UpdateServiceGroupSchedulingRequestFineSchedulingSchedulingFineShifts()
                self.scheduling_fine_shifts.append(temp_model.from_map(k))
        self.scheduling_template_fine_shifts = []
        if m.get('schedulingTemplateFineShifts') is not None:
            for k in m.get('schedulingTemplateFineShifts'):
                temp_model = UpdateServiceGroupSchedulingRequestFineSchedulingSchedulingTemplateFineShifts()
                self.scheduling_template_fine_shifts.append(temp_model.from_map(k))
        if m.get('shiftType') is not None:
            self.shift_type = m.get('shiftType')
        return self


class UpdateServiceGroupSchedulingRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        fast_scheduling: UpdateServiceGroupSchedulingRequestFastScheduling = None,
        fine_scheduling: UpdateServiceGroupSchedulingRequestFineScheduling = None,
        scheduling_way: str = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        self.fast_scheduling = fast_scheduling
        self.fine_scheduling = fine_scheduling
        # This parameter is required.
        self.scheduling_way = scheduling_way
        # This parameter is required.
        self.service_group_id = service_group_id

    def validate(self):
        if self.fast_scheduling:
            self.fast_scheduling.validate()
        if self.fine_scheduling:
            self.fine_scheduling.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.fast_scheduling is not None:
            result['fastScheduling'] = self.fast_scheduling.to_map()
        if self.fine_scheduling is not None:
            result['fineScheduling'] = self.fine_scheduling.to_map()
        if self.scheduling_way is not None:
            result['schedulingWay'] = self.scheduling_way
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('fastScheduling') is not None:
            temp_model = UpdateServiceGroupSchedulingRequestFastScheduling()
            self.fast_scheduling = temp_model.from_map(m['fastScheduling'])
        if m.get('fineScheduling') is not None:
            temp_model = UpdateServiceGroupSchedulingRequestFineScheduling()
            self.fine_scheduling = temp_model.from_map(m['fineScheduling'])
        if m.get('schedulingWay') is not None:
            self.scheduling_way = m.get('schedulingWay')
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class UpdateServiceGroupSchedulingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateServiceGroupSchedulingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateServiceGroupSchedulingResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateServiceGroupSchedulingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateServiceGroupSpecialDaySchedulingRequestSchedulingSpecialDays(TeaModel):
    def __init__(
        self,
        scheduling_end_time: str = None,
        scheduling_object_type: str = None,
        scheduling_order: int = None,
        scheduling_start_time: str = None,
        scheduling_user_id: int = None,
        scheduling_user_id_list: List[int] = None,
    ):
        # This parameter is required.
        self.scheduling_end_time = scheduling_end_time
        self.scheduling_object_type = scheduling_object_type
        self.scheduling_order = scheduling_order
        # This parameter is required.
        self.scheduling_start_time = scheduling_start_time
        # This parameter is required.
        self.scheduling_user_id = scheduling_user_id
        self.scheduling_user_id_list = scheduling_user_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.scheduling_end_time is not None:
            result['schedulingEndTime'] = self.scheduling_end_time
        if self.scheduling_object_type is not None:
            result['schedulingObjectType'] = self.scheduling_object_type
        if self.scheduling_order is not None:
            result['schedulingOrder'] = self.scheduling_order
        if self.scheduling_start_time is not None:
            result['schedulingStartTime'] = self.scheduling_start_time
        if self.scheduling_user_id is not None:
            result['schedulingUserId'] = self.scheduling_user_id
        if self.scheduling_user_id_list is not None:
            result['schedulingUserIdList'] = self.scheduling_user_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('schedulingEndTime') is not None:
            self.scheduling_end_time = m.get('schedulingEndTime')
        if m.get('schedulingObjectType') is not None:
            self.scheduling_object_type = m.get('schedulingObjectType')
        if m.get('schedulingOrder') is not None:
            self.scheduling_order = m.get('schedulingOrder')
        if m.get('schedulingStartTime') is not None:
            self.scheduling_start_time = m.get('schedulingStartTime')
        if m.get('schedulingUserId') is not None:
            self.scheduling_user_id = m.get('schedulingUserId')
        if m.get('schedulingUserIdList') is not None:
            self.scheduling_user_id_list = m.get('schedulingUserIdList')
        return self


class UpdateServiceGroupSpecialDaySchedulingRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        scheduling_date: str = None,
        scheduling_special_days: List[UpdateServiceGroupSpecialDaySchedulingRequestSchedulingSpecialDays] = None,
        service_group_id: int = None,
    ):
        self.client_token = client_token
        # This parameter is required.
        self.scheduling_date = scheduling_date
        # This parameter is required.
        self.scheduling_special_days = scheduling_special_days
        # This parameter is required.
        self.service_group_id = service_group_id

    def validate(self):
        if self.scheduling_special_days:
            for k in self.scheduling_special_days:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.scheduling_date is not None:
            result['schedulingDate'] = self.scheduling_date
        result['schedulingSpecialDays'] = []
        if self.scheduling_special_days is not None:
            for k in self.scheduling_special_days:
                result['schedulingSpecialDays'].append(k.to_map() if k else None)
        if self.service_group_id is not None:
            result['serviceGroupId'] = self.service_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('schedulingDate') is not None:
            self.scheduling_date = m.get('schedulingDate')
        self.scheduling_special_days = []
        if m.get('schedulingSpecialDays') is not None:
            for k in m.get('schedulingSpecialDays'):
                temp_model = UpdateServiceGroupSpecialDaySchedulingRequestSchedulingSpecialDays()
                self.scheduling_special_days.append(temp_model.from_map(k))
        if m.get('serviceGroupId') is not None:
            self.service_group_id = m.get('serviceGroupId')
        return self


class UpdateServiceGroupSpecialDaySchedulingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateServiceGroupSpecialDaySchedulingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateServiceGroupSpecialDaySchedulingResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateServiceGroupSpecialDaySchedulingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateSubscriptionRequestNotifyObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        notify_object_id: int = None,
    ):
        self.id = id
        # This parameter is required.
        self.notify_object_id = notify_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.notify_object_id is not None:
            result['notifyObjectId'] = self.notify_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('notifyObjectId') is not None:
            self.notify_object_id = m.get('notifyObjectId')
        return self


class UpdateSubscriptionRequestNotifyStrategyListStrategiesConditions(TeaModel):
    def __init__(
        self,
        action: str = None,
        effection: str = None,
        level: str = None,
        problem_notify_type: str = None,
    ):
        self.action = action
        self.effection = effection
        self.level = level
        self.problem_notify_type = problem_notify_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['action'] = self.action
        if self.effection is not None:
            result['effection'] = self.effection
        if self.level is not None:
            result['level'] = self.level
        if self.problem_notify_type is not None:
            result['problemNotifyType'] = self.problem_notify_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('action') is not None:
            self.action = m.get('action')
        if m.get('effection') is not None:
            self.effection = m.get('effection')
        if m.get('level') is not None:
            self.level = m.get('level')
        if m.get('problemNotifyType') is not None:
            self.problem_notify_type = m.get('problemNotifyType')
        return self


class UpdateSubscriptionRequestNotifyStrategyListStrategiesPeriodChannel(TeaModel):
    def __init__(
        self,
        non_workday: str = None,
        workday: str = None,
    ):
        self.non_workday = non_workday
        self.workday = workday

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.non_workday is not None:
            result['nonWorkday'] = self.non_workday
        if self.workday is not None:
            result['workday'] = self.workday
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('nonWorkday') is not None:
            self.non_workday = m.get('nonWorkday')
        if m.get('workday') is not None:
            self.workday = m.get('workday')
        return self


class UpdateSubscriptionRequestNotifyStrategyListStrategies(TeaModel):
    def __init__(
        self,
        channels: str = None,
        conditions: List[UpdateSubscriptionRequestNotifyStrategyListStrategiesConditions] = None,
        id: str = None,
        period_channel: UpdateSubscriptionRequestNotifyStrategyListStrategiesPeriodChannel = None,
    ):
        self.channels = channels
        self.conditions = conditions
        self.id = id
        self.period_channel = period_channel

    def validate(self):
        if self.conditions:
            for k in self.conditions:
                if k:
                    k.validate()
        if self.period_channel:
            self.period_channel.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.channels is not None:
            result['channels'] = self.channels
        result['conditions'] = []
        if self.conditions is not None:
            for k in self.conditions:
                result['conditions'].append(k.to_map() if k else None)
        if self.id is not None:
            result['id'] = self.id
        if self.period_channel is not None:
            result['periodChannel'] = self.period_channel.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('channels') is not None:
            self.channels = m.get('channels')
        self.conditions = []
        if m.get('conditions') is not None:
            for k in m.get('conditions'):
                temp_model = UpdateSubscriptionRequestNotifyStrategyListStrategiesConditions()
                self.conditions.append(temp_model.from_map(k))
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('periodChannel') is not None:
            temp_model = UpdateSubscriptionRequestNotifyStrategyListStrategiesPeriodChannel()
            self.period_channel = temp_model.from_map(m['periodChannel'])
        return self


class UpdateSubscriptionRequestNotifyStrategyList(TeaModel):
    def __init__(
        self,
        instance_type: int = None,
        strategies: List[UpdateSubscriptionRequestNotifyStrategyListStrategies] = None,
    ):
        # This parameter is required.
        self.instance_type = instance_type
        # This parameter is required.
        self.strategies = strategies

    def validate(self):
        if self.strategies:
            for k in self.strategies:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_type is not None:
            result['instanceType'] = self.instance_type
        result['strategies'] = []
        if self.strategies is not None:
            for k in self.strategies:
                result['strategies'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceType') is not None:
            self.instance_type = m.get('instanceType')
        self.strategies = []
        if m.get('strategies') is not None:
            for k in m.get('strategies'):
                temp_model = UpdateSubscriptionRequestNotifyStrategyListStrategies()
                self.strategies.append(temp_model.from_map(k))
        return self


class UpdateSubscriptionRequestScopeObjectList(TeaModel):
    def __init__(
        self,
        id: int = None,
        scope_object_id: int = None,
    ):
        self.id = id
        # This parameter is required.
        self.scope_object_id = scope_object_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.id is not None:
            result['id'] = self.id
        if self.scope_object_id is not None:
            result['scopeObjectId'] = self.scope_object_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('id') is not None:
            self.id = m.get('id')
        if m.get('scopeObjectId') is not None:
            self.scope_object_id = m.get('scopeObjectId')
        return self


class UpdateSubscriptionRequest(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        expired_type: str = None,
        notify_object_list: List[UpdateSubscriptionRequestNotifyObjectList] = None,
        notify_object_type: str = None,
        notify_strategy_list: List[UpdateSubscriptionRequestNotifyStrategyList] = None,
        period: str = None,
        scope: str = None,
        scope_object_list: List[UpdateSubscriptionRequestScopeObjectList] = None,
        start_time: str = None,
        subscription_id: int = None,
        subscription_title: str = None,
    ):
        self.end_time = end_time
        # This parameter is required.
        self.expired_type = expired_type
        # This parameter is required.
        self.notify_object_list = notify_object_list
        # This parameter is required.
        self.notify_object_type = notify_object_type
        # This parameter is required.
        self.notify_strategy_list = notify_strategy_list
        self.period = period
        # This parameter is required.
        self.scope = scope
        # This parameter is required.
        self.scope_object_list = scope_object_list
        self.start_time = start_time
        # This parameter is required.
        self.subscription_id = subscription_id
        # This parameter is required.
        self.subscription_title = subscription_title

    def validate(self):
        if self.notify_object_list:
            for k in self.notify_object_list:
                if k:
                    k.validate()
        if self.notify_strategy_list:
            for k in self.notify_strategy_list:
                if k:
                    k.validate()
        if self.scope_object_list:
            for k in self.scope_object_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['endTime'] = self.end_time
        if self.expired_type is not None:
            result['expiredType'] = self.expired_type
        result['notifyObjectList'] = []
        if self.notify_object_list is not None:
            for k in self.notify_object_list:
                result['notifyObjectList'].append(k.to_map() if k else None)
        if self.notify_object_type is not None:
            result['notifyObjectType'] = self.notify_object_type
        result['notifyStrategyList'] = []
        if self.notify_strategy_list is not None:
            for k in self.notify_strategy_list:
                result['notifyStrategyList'].append(k.to_map() if k else None)
        if self.period is not None:
            result['period'] = self.period
        if self.scope is not None:
            result['scope'] = self.scope
        result['scopeObjectList'] = []
        if self.scope_object_list is not None:
            for k in self.scope_object_list:
                result['scopeObjectList'].append(k.to_map() if k else None)
        if self.start_time is not None:
            result['startTime'] = self.start_time
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        if self.subscription_title is not None:
            result['subscriptionTitle'] = self.subscription_title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('endTime') is not None:
            self.end_time = m.get('endTime')
        if m.get('expiredType') is not None:
            self.expired_type = m.get('expiredType')
        self.notify_object_list = []
        if m.get('notifyObjectList') is not None:
            for k in m.get('notifyObjectList'):
                temp_model = UpdateSubscriptionRequestNotifyObjectList()
                self.notify_object_list.append(temp_model.from_map(k))
        if m.get('notifyObjectType') is not None:
            self.notify_object_type = m.get('notifyObjectType')
        self.notify_strategy_list = []
        if m.get('notifyStrategyList') is not None:
            for k in m.get('notifyStrategyList'):
                temp_model = UpdateSubscriptionRequestNotifyStrategyList()
                self.notify_strategy_list.append(temp_model.from_map(k))
        if m.get('period') is not None:
            self.period = m.get('period')
        if m.get('scope') is not None:
            self.scope = m.get('scope')
        self.scope_object_list = []
        if m.get('scopeObjectList') is not None:
            for k in m.get('scopeObjectList'):
                temp_model = UpdateSubscriptionRequestScopeObjectList()
                self.scope_object_list.append(temp_model.from_map(k))
        if m.get('startTime') is not None:
            self.start_time = m.get('startTime')
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        if m.get('subscriptionTitle') is not None:
            self.subscription_title = m.get('subscriptionTitle')
        return self


class UpdateSubscriptionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateSubscriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateSubscriptionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateSubscriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateUserRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        email: str = None,
        phone: str = None,
        ram_id: int = None,
        role_id_list: List[int] = None,
        user_id: int = None,
        username: str = None,
    ):
        self.client_token = client_token
        self.email = email
        self.phone = phone
        self.ram_id = ram_id
        self.role_id_list = role_id_list
        # This parameter is required.
        self.user_id = user_id
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.email is not None:
            result['email'] = self.email
        if self.phone is not None:
            result['phone'] = self.phone
        if self.ram_id is not None:
            result['ramId'] = self.ram_id
        if self.role_id_list is not None:
            result['roleIdList'] = self.role_id_list
        if self.user_id is not None:
            result['userId'] = self.user_id
        if self.username is not None:
            result['username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('email') is not None:
            self.email = m.get('email')
        if m.get('phone') is not None:
            self.phone = m.get('phone')
        if m.get('ramId') is not None:
            self.ram_id = m.get('ramId')
        if m.get('roleIdList') is not None:
            self.role_id_list = m.get('roleIdList')
        if m.get('userId') is not None:
            self.user_id = m.get('userId')
        if m.get('username') is not None:
            self.username = m.get('username')
        return self


class UpdateUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateUserResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateUserGuideStatusRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        guide_action: str = None,
    ):
        self.client_token = client_token
        self.guide_action = guide_action

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['clientToken'] = self.client_token
        if self.guide_action is not None:
            result['guideAction'] = self.guide_action
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('clientToken') is not None:
            self.client_token = m.get('clientToken')
        if m.get('guideAction') is not None:
            self.guide_action = m.get('guideAction')
        return self


class UpdateUserGuideStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        # Id of the request
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class UpdateUserGuideStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateUserGuideStatusResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateUserGuideStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class VerifyRouteRuleRequestTestSourceEvents(TeaModel):
    def __init__(
        self,
        event_json: str = None,
        event_time: str = None,
        monitor_source_id: int = None,
        monitor_source_name: str = None,
    ):
        self.event_json = event_json
        self.event_time = event_time
        self.monitor_source_id = monitor_source_id
        self.monitor_source_name = monitor_source_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.event_json is not None:
            result['eventJson'] = self.event_json
        if self.event_time is not None:
            result['eventTime'] = self.event_time
        if self.monitor_source_id is not None:
            result['monitorSourceId'] = self.monitor_source_id
        if self.monitor_source_name is not None:
            result['monitorSourceName'] = self.monitor_source_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('eventJson') is not None:
            self.event_json = m.get('eventJson')
        if m.get('eventTime') is not None:
            self.event_time = m.get('eventTime')
        if m.get('monitorSourceId') is not None:
            self.monitor_source_id = m.get('monitorSourceId')
        if m.get('monitorSourceName') is not None:
            self.monitor_source_name = m.get('monitorSourceName')
        return self


class VerifyRouteRuleRequest(TeaModel):
    def __init__(
        self,
        route_rule_id: int = None,
        test_source_events: List[VerifyRouteRuleRequestTestSourceEvents] = None,
    ):
        self.route_rule_id = route_rule_id
        self.test_source_events = test_source_events

    def validate(self):
        if self.test_source_events:
            for k in self.test_source_events:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.route_rule_id is not None:
            result['routeRuleId'] = self.route_rule_id
        result['testSourceEvents'] = []
        if self.test_source_events is not None:
            for k in self.test_source_events:
                result['testSourceEvents'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('routeRuleId') is not None:
            self.route_rule_id = m.get('routeRuleId')
        self.test_source_events = []
        if m.get('testSourceEvents') is not None:
            for k in m.get('testSourceEvents'):
                temp_model = VerifyRouteRuleRequestTestSourceEvents()
                self.test_source_events.append(temp_model.from_map(k))
        return self


class VerifyRouteRuleResponseBodyDataEscalationPlans(TeaModel):
    def __init__(
        self,
        escalation_plan_id: int = None,
        escalation_plan_name: str = None,
    ):
        self.escalation_plan_id = escalation_plan_id
        self.escalation_plan_name = escalation_plan_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.escalation_plan_id is not None:
            result['escalationPlanId'] = self.escalation_plan_id
        if self.escalation_plan_name is not None:
            result['escalationPlanName'] = self.escalation_plan_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('escalationPlanId') is not None:
            self.escalation_plan_id = m.get('escalationPlanId')
        if m.get('escalationPlanName') is not None:
            self.escalation_plan_name = m.get('escalationPlanName')
        return self


class VerifyRouteRuleResponseBodyDataNotifySubscriptionNames(TeaModel):
    def __init__(
        self,
        subscription_id: int = None,
        title: str = None,
    ):
        self.subscription_id = subscription_id
        self.title = title

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.subscription_id is not None:
            result['subscriptionId'] = self.subscription_id
        if self.title is not None:
            result['title'] = self.title
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('subscriptionId') is not None:
            self.subscription_id = m.get('subscriptionId')
        if m.get('title') is not None:
            self.title = m.get('title')
        return self


class VerifyRouteRuleResponseBodyData(TeaModel):
    def __init__(
        self,
        escalation_plans: List[VerifyRouteRuleResponseBodyDataEscalationPlans] = None,
        is_valid_rule: bool = None,
        monitor_source_ids: List[int] = None,
        notify_subscription_names: List[VerifyRouteRuleResponseBodyDataNotifySubscriptionNames] = None,
        route_rule_fail_reason: List[str] = None,
        route_type: str = None,
    ):
        self.escalation_plans = escalation_plans
        self.is_valid_rule = is_valid_rule
        self.monitor_source_ids = monitor_source_ids
        self.notify_subscription_names = notify_subscription_names
        self.route_rule_fail_reason = route_rule_fail_reason
        self.route_type = route_type

    def validate(self):
        if self.escalation_plans:
            for k in self.escalation_plans:
                if k:
                    k.validate()
        if self.notify_subscription_names:
            for k in self.notify_subscription_names:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['escalationPlans'] = []
        if self.escalation_plans is not None:
            for k in self.escalation_plans:
                result['escalationPlans'].append(k.to_map() if k else None)
        if self.is_valid_rule is not None:
            result['isValidRule'] = self.is_valid_rule
        if self.monitor_source_ids is not None:
            result['monitorSourceIds'] = self.monitor_source_ids
        result['notifySubscriptionNames'] = []
        if self.notify_subscription_names is not None:
            for k in self.notify_subscription_names:
                result['notifySubscriptionNames'].append(k.to_map() if k else None)
        if self.route_rule_fail_reason is not None:
            result['routeRuleFailReason'] = self.route_rule_fail_reason
        if self.route_type is not None:
            result['routeType'] = self.route_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.escalation_plans = []
        if m.get('escalationPlans') is not None:
            for k in m.get('escalationPlans'):
                temp_model = VerifyRouteRuleResponseBodyDataEscalationPlans()
                self.escalation_plans.append(temp_model.from_map(k))
        if m.get('isValidRule') is not None:
            self.is_valid_rule = m.get('isValidRule')
        if m.get('monitorSourceIds') is not None:
            self.monitor_source_ids = m.get('monitorSourceIds')
        self.notify_subscription_names = []
        if m.get('notifySubscriptionNames') is not None:
            for k in m.get('notifySubscriptionNames'):
                temp_model = VerifyRouteRuleResponseBodyDataNotifySubscriptionNames()
                self.notify_subscription_names.append(temp_model.from_map(k))
        if m.get('routeRuleFailReason') is not None:
            self.route_rule_fail_reason = m.get('routeRuleFailReason')
        if m.get('routeType') is not None:
            self.route_type = m.get('routeType')
        return self


class VerifyRouteRuleResponseBody(TeaModel):
    def __init__(
        self,
        data: VerifyRouteRuleResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        # Id of the request
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data.to_map()
        if self.request_id is not None:
            result['requestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            temp_model = VerifyRouteRuleResponseBodyData()
            self.data = temp_model.from_map(m['data'])
        if m.get('requestId') is not None:
            self.request_id = m.get('requestId')
        return self


class VerifyRouteRuleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: VerifyRouteRuleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = VerifyRouteRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


