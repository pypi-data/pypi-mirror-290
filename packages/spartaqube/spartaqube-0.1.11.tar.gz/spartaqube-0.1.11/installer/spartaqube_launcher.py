import os, site, subprocess

def get_spartaqube_path():
    '''
    Get spartaqube path within site-packages
    '''
    site_packages_dir = site.getsitepackages()
    site_packages_path = [elem for elem in site_packages_dir if 'site-packages' in elem][0]
    return os.path.join(site_packages_path, 'spartaqube')

if __name__ == '__main__':
    base_path = get_spartaqube_path()
    api_folder = os.path.join(base_path, 'api')
    process = subprocess.Popen("python spartaqube_install.py", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=api_folder, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())