# Modules

## file_content

This module create file with delivered content or read content from existed file on host.

Available options:

- **path** [str] - Path to file. Required
- **content** [str] - Content of the file. Optional. Empty string is default

Returned values:

- **path** - Path to file
- **content** - Content of the file. Can be readed from file or written to.
- **status** [str] - Operation status. Can be one of the follewing:
  - **created**: the file was created and content were saved to file
  - **modified**: the file existed and its contents overwritten (content option is not empty)
  - **readed**: the file existed and its content read (content option is omitted)
  - **resisted**: the file existed and its contents are equal to transferred
  - **denied**: module could not access the file - error
- **uid** - File owner user id
- **gid** - File owner group id
- **owner** - File owner name
- **group** - File owner group name
- **mode** - File access rights
- **state** - File state: file or directory
- **size** - File size
