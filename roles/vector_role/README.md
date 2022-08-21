# Vector-role

Configure **SystemD** operation systems to use **Vector** for logging changes of LOG files and send collected metrics to **Clickhouse**

## Variables

- **vector_version** - Version of **Vector**. Default **0.23.0**

- **vector_test_dir** - Directory of LOG files

- **clickhouse_host**: - **Clickhouse** host where metrics will be transferred

- **clickhosue_port**: - **Clickhouse** port where metrics will be transferred

- **clickhosue_user**: - **Clickhouse** user with write access

- **clickhosue_password**: - Password for **Clickhouse** user

## Example

```yaml
- name: Install and configure Vector
  hosts: vector
  become: true
  vars:
    vector_test_dir: "/home/centos/test"
    clickhouse_host: hostvars['clickhouse']['ansible_host']
  roles:
    - vector_role
```
