import os
import json
class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self.title, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def __str__(self):
        return self.title

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    @classmethod
    def from_json(cls, value: dict):
        entry = cls(value["title"])
        for item in value.get("entries", []):
            child = cls.from_json(item)
            entry.add_entry(child)
        return entry

    def save(self, path):
        filename = f'{self.title}.json'
        filepath = os.path.join(path, filename)
        with open(filepath, 'w') as file:
            file.write(json.dumps(self.json()))

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            content = file.read()
            data = json.loads(content)
            return cls.from_json(data)


def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


def entry_from_json(value: dict):
    entry = Entry(value["title"])
    for item in value.get("entries", []):
        child = entry_from_json(item)
        entry.add_entry(child)
    return entry


from resources import Entry
import os


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        files = os.listdir(self.data_path)
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(self.data_path, file)
                entry = Entry.load(filepath)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)





