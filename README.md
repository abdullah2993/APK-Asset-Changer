# APK-Asset-Changer
WIP together APK Asset Changer

## Usage
```
usage: Change an existing asset in an APK file and sign it.
       [-h] [-q] APK_FILE ASSET_FILE ASSET_NAME KEYSTORE KEYPASS

positional arguments:
  APK_FILE     Path to APK file
  ASSET_FILE   Path to new Asset file
  ASSET_NAME   Name of the Asset to be replaced
  KEYSTORE     Path to Keystore
  KEYPASS      Password of Keystore

optional arguments:
  -h, --help   show this help message and exit
  -q, --quite
 ```

## Note
In order to use this script you have to set an enviroment variabale `ANDROID_HOME_BT` to point to your `build-tools\{version}` in android SDK folder. You also need to have `build-tools >= 24.0.3` because the `apksigner` utility this script uses to sign the apk is only included in `build-tools >= 24.0.3`.
In order to use this script with an older version of the `build-tools` you have to edit this script to use `jarsigner` from `JDK\bin`.
I might include it later down the road but for now its better to install `build-tools >= 24.0.3` using the `SDK Manager`
