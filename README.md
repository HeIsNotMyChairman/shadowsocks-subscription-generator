# shadowsocks-config-generator
A simple script to generate multiple shadowsocks configs

## Usage:
Open [android.py](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py) and modify the following variables:
- **servercfgs**: Use for customizing settings for servers which are different from **default_config** variable
- **default_config**: Default settings for all servers
- **android_list**: apps that needs proxy on android, welcome PR to add more

[Here is the example output file](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.json)

## Priority:
If key collisions, the values are overwritten in the following order:

**default_config**

**servercfgs**

**servercfgs['subconfigs']**
