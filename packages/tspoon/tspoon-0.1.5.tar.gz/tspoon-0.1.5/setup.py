from setuptools import setup, find_packages

with open('README.md', 'r') as f:
	description = f.read()

setup(
	name='tspoon',
	version='0.1.5',
	packages=find_packages(),
	install_requires=[
		# 'os',
		# 'time',
		# 'sys',
		# 'pickle',
		# 'pandas',
		# 'numpy',
		# 'regex',
		# 'datetime',
		# 'matplotlib',
		# 'statsmodels',
		# 'copy'
	],
	description='Time-series pre-processing, period conversion, normalization, visualization, and more.',
	long_description=description,
	long_description_content_type='text/markdown',
)