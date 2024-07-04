class OVPN:
    def __init__(self, file_path):
        self.file_path = file_path

        with open(self.file_path, "r") as read_file:
            self.file_lines = read_file.readlines()

        self.ports = []
        self.ip_addresses = []

        self.parse()

    def parse(self):

        for line in self.file_lines:
            line = line.strip()

            if not line.strip():
                # empty line
                continue

            if line.startswith("remote "):
                params = line.split(" ")
                self.ip_addresses.append(params[1])
                continue
            elif line.startswith("client"):
                continue
            elif line.startswith("proto"):
                continue
