import subprocess
import os
import numpy as np
import sys
import re, sys


files_processed = list()
header = list()
header.append('file_name')
header.append('file_length')
header.append('import statements')
header.append('pep checker score')

files_processed.append(header)

root_path = '/home/david/big_data_git_downloads/'



def main():
    file_list = open('/home/david/big_data_git_downloads/file_list.txt', mode='r')
    print('file name, number of lines, pep violations, imports')
    for file in file_list:
        analyze_file(file)


def analyze_file(file):
    print(file[2:].replace('\n', ''), end=', ')
    try:
        print(file_length(file), '', end=', ')
        print(run_pep(file), end=', ')
        imports = read_imports(file)
        for imp in imports:
            print(imp.replace('\n', '').replace(',', ''), end=' ')
    except UnicodeDecodeError as e:
        print('error decoding file, ' + str(e).replace('\n', '\\n'))
    print()


def run_pep(file):
    output = subprocess.Popen(["/home/david/anaconda3/bin/pep8", root_path +
                               file[2:-1]], stdout=subprocess.PIPE).communicate()[0]
    output = output.decode("utf-8")
    # Use a regular expression to find all line ends in pep8 output
    pep_violations = output.split('\n')
    pep_violations_filtered = list()
    for line in pep_violations:
        if line.count('E501') == 0 and len(line) > 2:  # to remove blank lines
            pep_violations_filtered.append(line)

    n_errors = len(pep_violations_filtered)
    return n_errors


def read_imports(file):
    current_file = open(root_path + file[2:-1], mode='r')
    packages = list()

    for line in current_file:
        line_components = line.split(' ')

        if len(line_components) < 2:
            pass
        elif line_components[0] == 'import':
            if line_components[-2] != 'as':
                for package in line_components[1:]:
                    package = package.replace('(', '').replace(')', '')
                    package = package.replace(',', '').replace('\n', '')
                    packages.append(package)
            else:
                for package in line_components[1:-2]:
                    package = package.replace('(', '').replace(')', '')
                    package = package.replace(',', '').replace('\n', '')
                    packages.append(package)
        elif line_components[0] == 'from':
            if line_components[-2] != 'as':
                parent_package = line_components[1]
                for package in line_components[3:]:
                    package = package.replace('(', '').replace(')', '')
                    package = package.replace(',', '').replace('\n', '')
                    packages.append(parent_package + '.' + package)
            else:
                parent_package = line_components[1]
                for package in line_components[3:-2]:
                    package = package.replace('(', '').replace(')', '')
                    package = package.replace(',', '').replace('\n', '')
                    packages.append(parent_package + '.' + package)

    return packages


def file_length(file):
    current_file = open(root_path + file[2:-1], mode='r')
    count = 0
    for line in current_file:
        count += 1
    return count


    # # list of repositories to download. These are the first n most forked repositories with a few exceptions.\
    # repository_urls = ('https://github.com/odoo/odoo.git',
    #                    'https://github.com/django/django.git',
    #                    'https://github.com/scikit-learn/scikit-learn.git',
    #                    'https://github.com/mitsuhiko/flask.git',
    #                    'https://github.com/ansible/ansible.git',
    #                    'https://github.com/scrapy/scrapy.git',
    #                    'https://github.com/vinta/awesome-python.git',
    #                    'https://github.com/tornadoweb/tornado.git',
    #                    'https://github.com/kennethreitz/requests.git',
    #                    'https://github.com/rg3/youtube-dl.git',
    #                    'https://github.com/saltstack/salt.git',
    #                    'https://github.com/wbond/package_control_channel.git',
    #                    'https://github.com/udacity/fullstack-nanodegree-vm.git',
    #                    'https://github.com/ipython/ipython.git',
    #                    'https://github.com/josephmisiti/awesome-machine-learning.git',
    #                    'https://github.com/pydata/pandas.git',
    #                    'https://github.com/reddit/reddit.git',
    #                    'https://github.com/XX-net/XX-Net.git',
    #                    'https://github.com/midgetspy/Sick-Beard.git')
    #
    #
    # def download_repo(url):
    #     os.chdir('git_files')
    #     print('starting')
    #     print(subprocess.Popen("git clone " + url, shell=True, stdout=subprocess.PIPE).stdout.read())
    #     print('done')
    #
    #
    # try:
    #     os.mkdir('git_files')
    # except:
    #     pass
    #     # the directory already exists, nothing to do
    # os.chdir('git_files')
    #
    # # print bash command to download all repos
    # for url in repository_urls:
    #     print('git clone --depth 1 ' + url + ' && ', end='')
    # print('all done')

if __name__ == '__main__':
    main()

