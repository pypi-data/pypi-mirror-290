class Module:
    def __init__(self):
        self.name = "module"

    def get_name(self):
        return self.name

    def get_version(self):
        return "0.1"

    def get_classifiers(self):
        return [
            'Development Status :: 1 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'TOPIC :: Internet :: WWW/HTTP :: Indexing/Search',
        ]

    def get_description(self):
        return "This is a sample module"

    def get_author(self):
        return "PLI"