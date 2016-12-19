# APK-Asset-Changer
WIP together APK Asset Changer

`My Python kung-fu is weak as fuck`

## Note
In order to use this script you have to set an enviroment variabale `ANDROID_HOME_BT` to point to your `build-tools\{version}` in android SDK folder. You also need to have `build-tools >= 24.0.3` because the `apksigner` utility this script uses to sign the apk is only included in `build-tools >= 24.0.3`.
In order to use this script with an older version of the `build-tools` you have to edit this script to use `jarsigner` from `JDK\bin`.
I might include it later down the road but for now its better to install `build-tools >= 24.0.3` using the `SDK Manager`
