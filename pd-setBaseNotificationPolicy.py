#!/usr/bin/python3

# Modules Used
import os
import json
import requests
import sys

# PagerDuty REST API Details as Global Variables (change as needed)
SET_LIMIT = 1000
SET_OFFSET = 0

# Help Message
message = """
Example usage:
    ./pd-setBaseNotificationPolicy.py -k <PagerDuty v2 API Key>
    ./pd-setBaseNotificationPolicy.py -key <PagerDuty v2 API Key>
    
Get a PagerDuty v2 API Key at https://(your-subdomain).pagerduty.com/api_keys
"""

# Passing arguments. Either help (-h) or the PagerDuty v2 API Key (-k)
if len(sys.argv) == 1:
    print(message)
    sys.exit(2)
elif sys.argv[1] not in ('-h', '--help', '-k', '--key'):
    print(message)
    sys.exit(2)

elif sys.argv[1] in ('-h', '--help'):
    print(message)
    sys.exit(2)

elif sys.argv[1] in ('-k', '--key') and len(sys.argv) == 3:
    api_key = sys.argv[2]
else:
    print(message)
    sys.exit(2)

teamId = str(input(
    "\nEnter the PagerDuty ID for the team you want to apply the base notification rules (e.g. PTJ9Z73): "))


def get_users_request():

    endpoint_headers = {'Authorization': 'Token token=' + api_key,
                        'Accept': 'application/vnd.pagerduty+json;version=2'}
    api_ref = '?include%5B%5D=contact_methods&include%5B%5D=notification_rules&team_ids%5B%5D='
    endpoint_url = 'https://api.pagerduty.com/users' + api_ref + \
        teamId + '&limit=' + str(SET_LIMIT) + '&offset=' + str(SET_OFFSET)
    response = requests.get(endpoint_url, headers=endpoint_headers)

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        teams = data['users'][0]['teams']

        for team in teams:
            if team['id'] == teamId:
                print("\nApplying base PagerDuty notification rules to the '" +
                      team['summary'].strip() + "' team...\n")

        return(data)
    elif response.status_code == 429:
        print(
            '[!] Too many PagerDuty API requests have been made, the rate limit has been reached.')
        sys.exit(2)
    else:
        print('[!] PagerDuty REST API Connection Failure on Getting User Information & Notification Rules')
        sys.exit(2)


def delete_notification_rules_request(user_id, notify_id):

    endpoint_headers = {'Authorization': 'Token token=' + api_key,
                        'Accept': 'application/vnd.pagerduty+json;version=2'}
    endpoint_url = 'https://api.pagerduty.com/users/' + \
        user_id + '/notification_rules/' + notify_id
    response = requests.delete(endpoint_url, headers=endpoint_headers)

    if response.status_code == 204:
        pass  # do nothing
    elif response.status_code == 429:
        print(
            '[!] Too many PagerDuty API requests have been made, the rate limit has been reached.')
        sys.exit(2)
    else:
        print('[!] PagerDuty REST API Connection Failure on Deleting Notification Rules')


def post_notification_rules_request(notify_type, user_id, notify_method_id):

    endpoint_headers = {'Authorization': 'Token token=' + api_key,
                        'Accept': 'application/vnd.pagerduty+json;version=2', 'Content-Type': 'application/json'}
    endpoint_url = 'https://api.pagerduty.com/users/' + user_id + '/notification_rules'

    if notify_type == 'push':
        payload = {
            'notification_rule': {
                'start_delay_in_minutes': 0,
                'contact_method': {
                    'id': notify_method_id,
                    'type': 'push_notification_contact_method'
                },
                'type': 'assignment_notification_rule',
                'urgency': 'high'
            }
        }

    elif notify_type == 'email':
        payload = {
            'notification_rule': {
                'start_delay_in_minutes': 0,
                'contact_method': {
                    'id': notify_method_id,
                    'type': 'email_contact_method'
                },
                'type': 'assignment_notification_rule',
                'urgency': 'high'
            }
        }

    elif notify_type == 'sms':
        payload = {
            'notification_rule': {
                'type': 'assignment_notification_rule',
                'start_delay_in_minutes': 5,
                'contact_method': {
                    'id': notify_method_id,
                    'type': 'sms_contact_method'
                },
                'urgency': 'high'
            }
        }

    elif notify_type == 'phone':
        payload = {
            'notification_rule': {
                'type': 'assignment_notification_rule',
                'start_delay_in_minutes': 7,
                'contact_method': {
                    'id': notify_method_id,
                    'type': 'phone_contact_method'
                },
                'urgency': 'high'
            }
        }

    else:
        print(
            '[!] Not A Valid PagerDuty REST API Function on Posting Notification Rules')
        sys.exit(2)

    response = requests.post(
        endpoint_url, headers=endpoint_headers, data=json.dumps(payload))

    if response.status_code == 201:
        pass  # do nothing
    elif response.status_code == 429:
        print(
            '[!] Too many PagerDuty API requests have been made, the rate limit has been reached.')
        sys.exit(2)
    else:
        print('[!] PagerDuty REST API Connection Failure')


def get_oncall_handoff_request(user_id):

    endpoint_headers = {'Authorization': 'Token token=' + api_key,
                        'Accept': 'application/vnd.pagerduty+json;version=2'}
    api_ref = '/oncall_handoff_notification_rules?limit=' + \
        str(SET_LIMIT) + '&offset=' + str(SET_OFFSET)
    endpoint_url = 'https://api.pagerduty.com/users/' + user_id + api_ref
    response = requests.get(endpoint_url, headers=endpoint_headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    elif response.status_code == 429:
        print(
            '[!] Too many PagerDuty API requests have been made, the rate limit has been reached.')
        sys.exit(2)
    else:
        print(
            '[!] PagerDuty REST API Connection Failure on Getting On-Call Handoff Rules')


def delete_oncall_handoff_request(user_id, notify_id):

    endpoint_headers = {'Authorization': 'Token token=' + api_key,
                        'Accept': 'application/vnd.pagerduty+json;version=2'}
    endpoint_url = 'https://api.pagerduty.com/users/' + \
        user_id + '/oncall_handoff_notification_rules/' + notify_id
    response = requests.delete(endpoint_url, headers=endpoint_headers)

    if response.status_code == 204:
        pass  # do nothing
    elif response.status_code == 429:
        print(
            '[!] Too many PagerDuty API requests have been made, the rate limit has been reached.')
        sys.exit(2)
    else:
        print(
            '[!] PagerDuty REST API Connection Failure on Deleting On-Call Handoff Rules')


def post_oncall_handoff_request(notify_type, user_id, notify_method_id):

    endpoint_headers = {'Authorization': 'Token token=' + api_key,
                        'Accept': 'application/vnd.pagerduty+json;version=2', 'Content-Type': 'application/json'}
    endpoint_url = 'https://api.pagerduty.com/users/' + \
        user_id + '/oncall_handoff_notification_rules'

    if notify_type == 'push':
        payload = {
            'oncall_handoff_notification_rule': {
                'handoff_type': 'both',
                'notify_advance_in_minutes': 0,
                'contact_method': {
                    'id': notify_method_id,
                    'type': 'push_notification_contact_method'
                }
            }
        }

    elif notify_type == 'email':
        payload = {
            'oncall_handoff_notification_rule': {
                'handoff_type': 'both',
                'notify_advance_in_minutes': 0,
                'contact_method': {
                    'id': notify_method_id,
                    'type': 'email_contact_method'
                }
            }
        }

    response = requests.post(
        endpoint_url, headers=endpoint_headers, data=json.dumps(payload))

    if response.status_code == 201:
        pass
    elif response.status_code == 429:
        print(
            '[!] Too many PagerDuty API requests have been made, the rate limit has been reached.')
        sys.exit(2)
    else:
        print(
            '[!] PagerDuty REST API Connection Failure on Posting On-Call Handoff Rules')


def get_users_info():

    data = get_users_request()

    user_detail = {}
    i = 0
    for user in data['users']:

        email = phone = app = sms = 'not active'
        for contact_method in user['contact_methods']:
            if contact_method['type'] == 'email_contact_method':
                email = str(contact_method['id'])
            elif contact_method['type'] == 'phone_contact_method':
                phone = str(contact_method['id'])
            elif contact_method['type'] == 'sms_contact_method':
                sms = str(contact_method['id'])
            elif contact_method['type'] == 'push_notification_contact_method':
                app = str(contact_method['id'])

        user_detail[i] = {'name': str(user['name']),
                          'id': str(user['id']),
                          'role': str(user['role']),
                          'email_pg_id': email,
                          'phone_pg_id': phone,
                          'sms_pg_id': sms,
                          'app_pg_id': app,
                          'note_rule_ids': {},
                          'handoff_rule_ids': {}
                          }
        j = 0
        for notification_rule in user['notification_rules']:
            user_detail[i]['note_rule_ids'].update(
                {j: str(notification_rule['id'])})
            j += 1

        handoff_rules = get_oncall_handoff_request(str(user['id']))

        h = 0
        for handoff_rule in handoff_rules['oncall_handoff_notification_rules']:
            user_detail[i]['handoff_rule_ids'].update(
                {h: str(handoff_rule['id'])})
            h += 1

        i += 1

    return(user_detail)


def delete_current_notification_rules(users):

    i = 0
    while i < len(users):
        j = 0
        while j < len(users[i]['note_rule_ids']):
            delete_notification_rules_request(
                users[i]['id'], users[i]['note_rule_ids'][j])
            j += 1

        i += 1


def create_notification_rules(users):

    i = 0
    while i < len(users):
        if users[i]['app_pg_id'] != 'not active':
            post_notification_rules_request(
                'push', users[i]['id'], users[i]['app_pg_id'])

        # if users[i]['email_pg_id'] != 'not active':
        #     post_notification_rules_request(
        #         'email', users[i]['id'], users[i]['email_pg_id'])

        if users[i]['sms_pg_id'] != 'not active':
            post_notification_rules_request(
                'sms', users[i]['id'], users[i]['sms_pg_id'])

        if users[i]['phone_pg_id'] != 'not active':
            post_notification_rules_request(
                'phone', users[i]['id'], users[i]['phone_pg_id'])

        i += 1


def delete_oncall_handoff_rules(users):

    i = 0
    while i < len(users):
        j = 0
        while j < len(users[i]['handoff_rule_ids']):
            delete_oncall_handoff_request(
                users[i]['id'], users[i]['handoff_rule_ids'][j])
            j += 1

        i += 1


def create_oncall_handoff_rules(users):

    i = 0
    while i < len(users):
        if users[i]['app_pg_id'] != 'not active':
            post_oncall_handoff_request(
                'push', users[i]['id'], users[i]['app_pg_id'])

        if users[i]['email_pg_id'] != 'not active':
            post_oncall_handoff_request(
                'email', users[i]['id'], users[i]['email_pg_id'])

        print("[✓] Updated notification rules for findings for " +
              users[i]['name'] + ".")
        i += 1
    print("\n")


user_data = get_users_info()

delete_current_notification_rules(user_data)

create_notification_rules(user_data)

delete_oncall_handoff_rules(user_data)

create_oncall_handoff_rules(user_data)
