from jira.model.issue_base import IssueBase
from datetime import datetime

import pytz

tz = pytz.timezone('America/Lima')


class Feature(IssueBase):
    def __init__(self):
        super().__init__()
        # self.project_jira_name = ''
        self.team_backlog_id = ''
        self.pi_result = ''
        # self.team_backlog_name = ''
        self.label_ttv_name = ''
        self.label_one_name = ''
        self.label_portfolio_id = ''
        self.label_sda_tool_id = ''
        #
        self.sprint_estimate = ''
        self.acceptance_criteria = ''
        self.business_value = ''
        self.project_sda_name = ''
        self.project_sda_tool_id = ''
        self.deliverable = ''
        self.type_of_delivery_name = ''
        self.time_in_status_blocked = ''

    def convert_json_to_feature(self, json_feature):

        # variables de JiraBase
        self.id = json_feature.get('id')
        self.key = json_feature.get('key')
        fields = json_feature.get('fields')
        changelog = json_feature.get('changelog')
        histories = changelog.get('histories')
        self.title = fields.get('customfield_10006')
        self.issue_type_id = fields.get('issuetype').get('id')
        self.issue_type_name = fields.get('issuetype').get('name')
        self.jira_project_id = fields.get('project').get('id')
        self.jira_project_key = fields.get('project').get('key')
        self.jira_project_name = fields.get('project').get('name')
        self.description = fields.get('description')
        if fields.get('assignee') is not None:
            self.assignee_name = fields.get('assignee').get('name')
            self.assignee_email = fields.get('assignee').get('emailAddress')
        self.creator_name = fields.get('creator').get('name')
        self.creator_email = fields.get('creator').get('emailAddress')
        if fields.get("status") is not None:
            self.status_id = fields.get("status").get("id")
            self.status_name = fields.get("status").get("name")
        created_date = datetime.strptime(fields.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
        created_date = created_date.astimezone(tz)
        created_date = created_date.strftime("%Y-%m-%d %H:%M:%S")
        self.create_date = created_date
        update_date = datetime.strptime(fields.get('updated'), '%Y-%m-%dT%H:%M:%S.%f%z')
        update_date = update_date.astimezone(tz)
        update_date = update_date.strftime("%Y-%m-%d %H:%M:%S")
        self.update_date = update_date
        self._convert_histories_to_status(histories)
        labels = fields["labels"]

        for label in labels:
            label_without_sharp = label.replace("#", "")
            if label_without_sharp[0:3] == 'DE_':
                self.label_one_name = label_without_sharp
            if label_without_sharp[0:3] == 'TTV':
                self.label_ttv_name = label_without_sharp[4:len(label)]
            if label_without_sharp[0:7] == 'SDATOOL':
                self.label_sda_tool_id = label_without_sharp

        self.labels = ', '.join(fields.get('labels'))
        # variables solo de Feature

        # self.team_backlog_id = fields.get('customfield_13300')
        self.team_backlog_id = ', '.join(fields.get('customfield_13300'))
        self.pi_result = ', '.join(fields.get('customfield_10264'))
        if fields.get('customfield_10272') is not None:
            self.sprint_estimate = fields.get('customfield_10272').get('value')
        self.acceptance_criteria = fields.get('customfield_10260')
        self.business_value = fields.get('customfield_10003')

        issuelinks = fields.get('issuelinks')
        for issue in issuelinks:
            if issue.get('outwardIssue') is not None:
                if issue.get('outwardIssue').get('fields') is not None:
                    sda = issue.get('outwardIssue').get('fields').get('summary')
                    self.project_sda_name = sda[0:-7].strip()
                    self.project_sda_tool_id = 'SDATOOL-' + sda[-6:-1]

        if fields.get('customfield_12900') is not None:
            self.deliverable = ', '.join(fields.get('customfield_12900'))
        if fields.get('customfield_19001') is not None:
            self.type_of_delivery_name = fields.get('customfield_19001').get('value')
        self.time_in_status_blocked = fields.get('customfield_10400')
