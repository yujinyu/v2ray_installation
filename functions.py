import os
import urllib.request
import json
import platform

work_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])


def download_and_install_v2ray(installation_dir):
    global browser_download_url, release_filename, version_name
    git_account = "v2ray"
    git_repo = "v2ray-core"
    url = "https://api.github.com/repos/{0}/{1}/releases/latest".format(git_account, git_repo)

    res = urllib.request.urlopen(url)
    html = json.loads(res.read().decode('utf-8'))
    assets = html.get('assets')
    if platform.system() == "Linux":
        version_name = "v2ray-linux-64"
    else:
        version_name = "v2ray-linux-64"

    for release in assets:
        if release.get('name').startswith(version_name):
            release_filename = release.get('name')
            browser_download_url = release.get('browser_download_url')
            break
    if not os.path.exists(os.path.join(work_dir, version_name)):
        os.system("mkdir -p {0}".format(os.path.join(work_dir, version_name)))
    else:
        os.system("rm -rf {0}/*".format(os.path.join(work_dir, version_name)))
    os.system("cd {0} && wget {1} && mv {3} {2} "
              "&& cd {2} && unzip {3} && rm -f {3} *.json *.sig "
              "&& rm -rf doc system*".format(work_dir, browser_download_url, version_name, release_filename))
    if not os.path.exists(os.path.join(installation_dir, "v2ray")):
        os.system("mkdir -p {0}".format(os.path.join(installation_dir, "v2ray")))
    os.system(
        "mv {0}/* {1} && rm -rf {0}".format(os.path.join(work_dir, version_name),
                                            os.path.join(installation_dir, "v2ray")))


def config_v2ray(installation_dir, config_dir):
    if not os.path.exists(os.path.join(config_dir, "v2ray")):
        os.system("mkdir -p {0}".format(os.path.join(config_dir, "v2ray")))
    os.system("cp -f {0} {1}".format(
        os.path.join(work_dir, "config", "config.json"), os.path.join(config_dir, "v2ray")))
    os.system(
        "cp -f {0} {1} && systemctl daemon-reload".format(
            os.path.join(work_dir, "config", "v2ray.service"), "/usr/lib/systemd/system/"))
    fp = open("/usr/lib/systemd/system/v2ray.service", "r")
    lines = fp.readlines()
    fp.close()
    fp = open("/usr/lib/systemd/system/v2ray.service", "w")
    for line in lines:
        if line.startswith("ExecStart="):
            line = "ExecStart={0}/v2ray -config {1}/config.json\n".format(os.path.join(installation_dir, "v2ray"),
                                                                          os.path.join(config_dir, "v2ray"))
        fp.write(line)
    fp.close()


def install_and_create_crt(config_dir, domain_name):
    if not os.path.exists(os.path.join(config_dir, "v2ray")):
        os.system("mkdir -p {0}".format(os.path.join(config_dir, "v2ray")))
    os.system("curl https://get.acme.sh | sh")

    os.system("export CF_Key=\"aa930e7b3927e7183f2428cc8da2e7e8d0938\" "
              "&& export CF_Email=\"yu_jinyu@yeah.net\" "
              "&& acme.sh --issue --dns dns_cf -d {0} "
              "&& acme.sh --install-cert -d {0} --key-file {1}/v2ray.key --fullchain-file {1}/v2ray.crt "
              "&& acme.sh --upgrade --auto-upgrade".format(domain_name, os.path.join(config_dir, "v2ray")))


def restart_v2ray():
    os.system("systemctl enable v2ray.service && systemctl restart v2ray.service")
