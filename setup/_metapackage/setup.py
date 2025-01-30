import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-akretion-sale-import",
    description="Meta package for akretion-sale-import Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-queue_job_chunk>=16.0dev,<16.1dev',
        'odoo-addon-sale_channel>=16.0dev,<16.1dev',
        'odoo-addon-sale_channel_partner>=16.0dev,<16.1dev',
        'odoo-addon-sale_channel_white_label>=16.0dev,<16.1dev',
        'odoo-addon-sale_import_base>=16.0dev,<16.1dev',
        'odoo-addon-sale_import_rest>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
