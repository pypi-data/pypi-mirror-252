import setuptools

PACKAGE_NAME = "whatsapp-message-vonage-local"
# Since all PACAKGE_NAMEs are with an underscore, we don't need this. Why do we need it?
package_dir = "whatsapp_message_vonage_local"

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.13',  # https://pypi.org/project/whatsapp-message-vonage-local
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles whatsapp-message-vonage-local",
    long_description="This is a package for sharing common whatsapp function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles-zone/whatsapp-message-vonage-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'vonage>=3.11.0',
        'message-local>=0.0.3',
        'logger-local>=0.0.71',
        'database-mysql-local>=0.0.121',
        'api-management-local'
    ]
)
