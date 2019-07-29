# Set PagerDuty Base Notification Rules

This script allows you to set a base notification rules for a team in [PagerDuty](https://www.pagerduty.com/). It is based on the default team rules used by [7-Eleven, Inc](https://www.7-eleven.com/).

## Prerequisites

* PagerDuty Account
* PagerDuty v2 API Key (write access)
* Python 3.x
* The following Python modules: os, json, requests, sys

## Installation

1.  Download project or just 'pd-setBaseNotificationPolicy.py'.
2.	Ensure 'pd-setBaseNotificationPolicy.py' has execution rights. `chmod +x pd-setBaseNotificationPolicy.py`

## Example Usage

`./pd-setBaseNotificationPolicy.py -k <PagerDuty v2 API Key>`

`./pd-setBaseNotificationPolicy.py -key <PagerDuty v2 API Key>`
