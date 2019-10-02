Requirements:
- Python version 3
- Packages (at least runs successfully with these versions):
  - EQL v0.7
  - PyYAML v5.1.2

When run successfully, it should produce the following output:
```
Query:  process where pid == 424
Result: 1 event(s) ↓

[{'command_line': 'wininit.exe',
  'event_type': 'process',
  'md5': '94355c28c1970635a31b3fe52eb7ceba',
  'pid': 424,
  'ppid': 364,
  'process_name': 'wininit.exe',
  'process_path': 'C:\\Windows\\System32\\wininit.exe',
  'subtype': 'create',
  'timestamp': 131485996510000000,
  'user': 'NT AUTHORITY\\SYSTEM',
  'user_domain': 'NT AUTHORITY',
  'user_name': 'SYSTEM'}]

--------------------------------------------------------------------------------

Query:  data_sources where date_connected >= "2019-01-01"
Result: 2 event(s) ↓

[{'available_for_data_analytics': True,
  'comment': '',
  'data_quality': {'consistency': 5,
                   'data_field_completeness': 5,
                   'device_completeness': 5,
                   'retention': 5,
                   'timeliness': 5},
  'data_source_name': 'Process use of network',
  'date_connected': '2019-07-25',
  'date_registered': '2019-07-25',
  'products': ['Sysmon']},
 {'available_for_data_analytics': False,
  'comment': '',
  'data_quality': {'consistency': 5,
                   'data_field_completeness': 5,
                   'device_completeness': 5,
                   'retention': 0,
                   'timeliness': 1},
  'data_source_name': 'Disk forensics',
  'date_connected': '2019-01-01',
  'date_registered': '2019-01-10',
  'products': ['Manual', 'Commercial tool']}]
```
