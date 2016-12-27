"""APK Asset Changer"""
import argparse
import sys
import os
import zipfile
import tempfile
import shutil
import shlex
import subprocess

def unpack_apk(apk_path, unpack_path):
    """"Unpacks APK"""
    zipf = zipfile.ZipFile(apk_path, 'r')
    zipf.extractall(unpack_path)
    zipf.close()

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("APK_FILE")
    PARSER.add_argument("Asset_FILE")
    PARSER.add_argument("ASSET_NAME")
    PARSER.add_argument("KEYSTORE")
    PARSER.add_argument("KEYPASS")
    PARSER.parse_args()

    AND_BT = os.getenv("ANDROID_HOME_BT")
    AND_BT = AND_BT[1:-1]

    if AND_BT is None:
        print "set ANDROID_HOME_BT Environment Variable to [SDK PATH]\build-tools\\{ver}"
        print "Also make sure to use the build tools >= 24.0.3"
        exit(1)

    T_ALIGN = os.path.join(AND_BT, "zipalign.exe")
    T_SIGN = os.path.join(AND_BT, "apksigner.bat")

    ALIGN = '"{0}" -v -p 4 {1} AL-{1}'
    SIGN = '"{0}" sign -v --ks "{1}" --ks-pass pass:{2} --out signed-{3} AL-{3}'

    APK_PATH = os.path.abspath(sys.argv[1])
    ASSET_PATH = os.path.abspath(sys.argv[2])
    ASSET = sys.argv[3]
    KEYSTORE = os.path.abspath(sys.argv[4])
    KEYPASS = sys.argv[5]

    print "APK PATH: %s" % APK_PATH
    print "NEW ASSET PATH: %s" % ASSET_PATH
    print "NAME OF ASSET TO BE REPLACED: %s" % ASSET
    print "KEYSTORE PATH: %s" % KEYSTORE
    print "KEYSTORE PASSWORD: %s" % KEYPASS

    APK_NAME = os.path.basename(APK_PATH)
    ASSET_NAME = os.path.basename(ASSET_PATH)

    print "APK NAME: %s" % APK_NAME
    print "ASSET NAME %s" % ASSET_NAME

    TEMP_PATH = os.path.join(tempfile.gettempdir(), ASSET_NAME + '_' +APK_NAME)
    TEMP_APK = os.path.join(TEMP_PATH, APK_NAME)
    ASSET_FOLDER = os.path.join(TEMP_PATH, "Assets")
    ASSET_FILE = os.path.join(ASSET_FOLDER, ASSET)

    print "TEMP FOLDER PATH TO BE USED: %s" % TEMP_PATH
    print "TEMP APK PATH TO BE USED: %s" % TEMP_APK
    print "PATH TO ASSETS Folder: %s" % ASSET_FOLDER
    print "PATH TO ASSET FILE TO BE REPLACED %s" % ASSET_FILE

    if not os.path.exists(APK_PATH):
        print "Unable to find the APK file"
    elif not os.path.exists(ASSET_PATH):
        print "Unable to find the asset file"
    elif not os.path.exists(KEYSTORE):
        print "Unable to find the KEYSTORE"
    else:
        if os.path.exists(TEMP_PATH):
            print "TEMP PATH ALREADY EXISTS."
            print "DELETEING TEMP FOLDER..."
            shutil.rmtree(TEMP_PATH)

        print "CREATING TEMP DIRECTORY..."
        os.mkdir(TEMP_PATH)

        print "COPYING APK FILE TO TEMP FOLDER..."
        shutil.copy(APK_PATH, TEMP_PATH)

        print "UNPACKING APK..."
        unpack_apk(TEMP_APK, TEMP_PATH)

        print "DELETING TEMP APK..."
        os.remove(TEMP_APK)

        if not os.path.exists(ASSET_FOLDER):
            print "INVALID APK."
            print "NO ASSETS FOLDER FOUND"
            exit(1)

        if not os.path.exists(ASSET_FILE):
            print "INVALID ASSET NAME."
            print "USE NAME OF AN EXISTING ASSET"
            exit(1)

        print "DELETING OLD ASSET..."
        os.remove(ASSET_FILE)

        print "COPYING NEW ASSET..."
        shutil.copy(ASSET_PATH, ASSET_FILE)

        print "PACKING APK FILE..."
        shutil.make_archive(APK_NAME, 'zip', TEMP_PATH)
        os.rename(APK_NAME + ".zip", APK_NAME)

        print "REMOVING TEMP DIRECTORY..."
        shutil.rmtree(TEMP_PATH)

        print "ALIGNING APK..."
        #os.system('"' + T_ALIGN + '"'+ " 4 " + APK_NAME + " AL-" + APK_NAME)
        subprocess.Popen(shlex.split(str.format(ALIGN, T_ALIGN, APK_NAME))).wait()
        print "REMOVING UNALIGNED APK..."
        os.remove(APK_NAME)
        print "SIGNING APK..."
        subprocess.Popen(shlex.split(str.format(SIGN, T_SIGN, KEYSTORE, KEYPASS, APK_NAME))).wait()
