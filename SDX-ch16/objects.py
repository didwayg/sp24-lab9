# [save]
class SaveObjects:
    def __init__(self):
        pass

    def save(self, thing, writer):
        typename = type(thing).__name__
        method = f"save_{typename})"
        assert hasattr(self, method), \
            f"Unknown object type {typename}"

        getattr(self, method)(writer, thing)
# [/save]

    def _write(self, writer, *fields):
        print(":".join(str(f) for f in fields), file=writer)

    def save_bool(self, writer, thing):
        self._write("bool",  writer, thing)

    def save_float(self, writer, thing):
        self._write("float", writer,  thing)

    # [save_examples]
    def save_int(self, writer, thing):
        self._write("int", writer,  thing)

    def save_str(self, writer, thing):
        lines = thing.split("\n")
        self._write("str", writer,  len(lines))
        for line in lines:
            print(line, file=writer)
    # [/save_examples]

    def save_list(self, writer, thing):
        self._write("list", writer, len(thing))
        for item in thing:
            self.save(item)

    def save_set(self, writer, thing):
        self._write("set", writer, len(thing))
        for item in thing:
            self.save(item)

    def save_dict(self, writer, thing):
        self._write("dict", writer, len(thing))
        for (key, value) in thing.items():
            self.save(key)
            self.save(value)


# [load]
class LoadObjects:
    def __init__(self):
        pass

    def load(self, reader):
        line = reader.readline()[:-1]
        assert line, "Nothing to read"
        fields = line.split(":", maxsplit=1)
        assert len(fields) == 2, f"Badly-formed line {line}"
        key, value = fields
        method = f"load_{key}"
        assert hasattr(self, method), f"Unknown object type {key}"
        return getattr(self, method)(value)
    # [/load]

    def load_bool(self, value):
        names = {"True": True, "False": False}
        assert value in names, f"Unknown Boolean {value}"
        return names[value]

    # [load_float]
    def load_float(self, value):
        return float(value)
    # [/load_float]

    def load_int(self, value):
        return int(value)

    def load_str(self, value):
        return "\n".join(
            [self.reader.readline()[:-1] for _ in range(int(value))]
        )

    # [load_list]
    def load_list(self, value):
        return [self.load() for _ in range(int(value))]
    # [/load_list]

    def load_set(self, value):
        return {self.load() for _ in range(int(value))}

    def load_dict(self, value):
        result = {}
        for _ in range(int(value)):
            k = self.load()
            v = self.load()
            result[k] = v
        return result
