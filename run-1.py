from functions import *

if __name__ == "__main__":
    installation_dir = "/usr/bin/"
    config_dir = "/etc/"
    download_and_install_v2ray(installation_dir)
    config_v2ray(installation_dir, config_dir)
    install_crt()
