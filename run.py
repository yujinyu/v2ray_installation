from functions import *

if __name__ == "__main__":
    installation_dir = "/usr/bin/"
    config_dir = "/etc/"
    download_and_install_v2ray(installation_dir)
    install_and_create_crt(config_dir, "wnlo.tk")
    config_v2ray(installation_dir, config_dir)
    restart_v2ray()
