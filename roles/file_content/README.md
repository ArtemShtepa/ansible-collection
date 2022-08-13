# File_Content Role

Role to test file_content module.

By default role write **test_content** string to file **test_file** on host.
You can change file name and file content by variables.
If content is omitted role will try to read file content from existed file on host.

# Variables

- **test_file** [str] - Path to file. Optional
- **test_content** [str] - Content of the file. Optional

# Output

- **path** - Path to file
- **content** - Content of the file. Can be readed from file or written to.
- **status** - Operation status. Can be one of the following:
  - **created** - the file was created and content were saved to file
  - **modified** - the file existed and its contents overwritten (content option is not empty)
  - **readed** - the file existed and its content read (content option is omitted)
  - **resisted** - the file existed and its contents are equal to transferred
  - **denied** - module could not access the file - error
- **uid** - File owner user id
- **gid** - File owner group id
- **owner** - File owner name
- **group** - File owner group name
- **mode** - File access rights
- **state** - File state: file or directory
- **size** - File size

# Examples

```yaml
---
- hosts: all
  roles:
    - file_content
      path: 'test'
      content: 'write some bytes'
...
```
