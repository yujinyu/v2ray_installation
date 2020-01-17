from functions import *

if __name__ == "__main__":
    installation_dir = "/usr/bin/"
    config_dir = "/etc/"
    create_crt(config_dir, "wnlo.tk")
    restart_v2ray()