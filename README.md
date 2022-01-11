# shadowsocks-subscription-generator
A simple script to generate subscription with multiple shadowsocks servers

## Usage:
Open [android.py](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py) and modify the following variables:
- [**servercfgs**](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py#L4-L20): Use for customizing settings for servers which are different from [**default_config**](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py#L22-L32) variable
- [**default_config**](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py#L22-L32): Default settings for all servers
- [**android_list**](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py#L34-L82): apps that needs proxy on android, welcome PR to add more

Here is the example output file

[android.json for shadowsocks android](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.json)

[SIP002 subscription](https://github.com/HeIsNotMyChairman/shadowsocks-subscription-generator/blob/main/subscription)

## Priority:
If key collisions, the values are overwritten in the following order:

[**default_config**](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py#L22-L32)

[**servercfgs**](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py#L4-L20)

[**servercfgs['subconfigs']**](https://github.com/HeIsNotMyChairman/shadowsocks-config-generator/blob/main/android.py#L7)
