try:
    import requests
except ImportError as err:
    pip_cmd = 'pip' if os.name == 'nt' else 'pip3'
    installation_cmd = f'{pip_cmd} install {err.name}'
    installation_result = subprocess.run(installation_cmd, shell=True)

    if installation_result.returncode == 0:
        import requests
    else:
        print(f"Failed to install {err.name}. Please install it manually.")

from setuptools import setup, find_packages


def get_readme_content(owner, repo, branch='main'):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(url)

    if response.status_code == 200:
        contents = response.json()
        readme_content = None

        for content in contents:
            if content['name'].lower() == 'readme.md':
                readme_url = content['download_url']
                readme_response = requests.get(readme_url)

                if readme_response.status_code == 200:
                    readme_content = readme_response.text
                    break

        return readme_content

    else:
        return None


setup(
    name='luminance',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    author='Artem Reslaid',
    description='Luminance is a library for working with user output and console input',
    license='MIT',
    long_description=get_readme_content('reslaid', 'luminance'),
    long_description_content_type='text/markdown',
    url='https://github.com/reslaid/luminance',
    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
