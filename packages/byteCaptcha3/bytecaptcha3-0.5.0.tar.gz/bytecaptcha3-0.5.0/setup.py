import setuptools
with open(r'C:\Users\minia\Downloads\Проекты\byteCaptcha3\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='byteCaptcha3',
	version='0.5.0',
	author='h3xcolor',
	author_email='oktk0728@gmail.com',
	description='A powerful captcha generation library for Python',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/sjskUw/ByteCaptcha3',
	packages=['byteCaptcha3'],
	install_requires=["Pillow"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)