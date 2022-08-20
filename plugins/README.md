# Modules

## file_content

This module create file with delivered content or read content from existed file on host.

### Available options:

- **path** [str] - Path to file. Required
- **content** [str] - Content of the file. Optional. Empty string is default

### Returned values:

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

## yc_vpc

This module allow control Yandex Virtual Private Cloud resources through Yandex Cloud CLI.

### Available options:

- **net** [str] - Name of the network. Required
- **subnet** [str] - Name of the subnet. Required
- **ip_range** [str] - IP address space allocated to subnet in CIDR notation. Optional. Default `10.2.0.0/16`
- **state** [str] - State of subnet/net. Must be `exists` or `absent`. Optional. Default value is `exists`

### Returned values:

- **version** [str] - Yandex.Cloud CLI version. Returned always.
- **net_config** [str] - Network configuration from Yandex Cloud. Return if net exists or created
- **subnet_config** [str] - Subnet configuration of network from Yandex Cloud. Return if subnet exists or created

## yc_cmp

This module allow control Yandex Compute Cloud resources through Yandex Cloud CLI.

### Available options:

- **machine** [str] - Name of the instance. Required
- **config** [dict] - Instance configuration with Yandex Cloud CLI parameters. Required.
- **state** [str] - State of the instance. Must be `exists` or `absent`. Optional. Default value is `exists`

### Returned values:

- **machine** [str] - Name of the instance. Required
- **config** [dict] - Instance configuration from Yandex.Cloud CLI. Return if instance is exists or created.
- **ip** [str] - External IP address of the YC instance. Return if instance is exists or created.
