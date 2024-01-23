import setuptools
with open(r'C:\Users\anp50\OneDrive\Рабочий стол\capcha\capcha\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='capcha',
	version='2.0',
	author='BornTheHell',
	author_email='anp50158@gmail.com',
	description='',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['capcha'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)