# Lighthouse-role

Configure **SystemD** operation systems to use **VK Lighthouse** with **nginx**

## Variables

- **lighthouse_path** - Lighthouse data file path

- **lighthouse_port** - Lighthouse port. Use number after 1024. Default 8088

- **clickhouse_host**: - Clickhouse host where metrics are collected

- **clickhosue_port**: - Clickhouse port where metrics are collected

- **clickhosue_user**: - Clickhouse user to view metrics

- **clickhosue_password**: - Clickhouse user password

## Example

```yaml
- name: Install and configure Lighthouse
  hosts: lighthouse
  become: true
  vars:
    lighthouse_path: "/home/user/lighthouse"
    clickhouse_host: hostvars['clickhouse']['ansible_host']
  roles:
    - lighthouse_role
```
