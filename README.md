# Ansible Collection - artem_shtepa.utils

## Plugins

- **file_content** [module] - Write content to file or read from.

- **yc_vpc** [module] - Manage Yandex Virtual Private Cloud resources.

- **yc_cmp** [module] - Manage Yandex Compute Cloud resources.

[Details about plugins...](plugins/)

## Roles

- **file_content** - Role to test module **file_content**. [Details...](roles/file_content/)

- **vector_role** - Demo role: install and configure vector. [Details...](roles/vector_role/)

- **lighthouse_role** - Demo role: install and configure lighthouse and nginx. [Details...](roles/lighthouse_role/)

## Playbooks

- **test_file_content** - Single task playbook for test role file_content

- **demo_site** - Demonstration of collection, including the use of Yandex.Cloud modules for infrastructure deployment and roles for service deployment

- **demo_site_remove** - Destruction of the demonstration infrastructure

> Demo playbooks require **AlexeySetevoi**`s [Clickhouse role](https://github.com/AlexeySetevoi/ansible-clickhouse)

## License (MIT)

Copyright (c) 2022 Artem Shtepa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

Artem Shtepa