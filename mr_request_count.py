from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class MRRequestCount(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol  # Output plain text

    def mapper(self, _, line):
        line = line.lstrip('\ufeff').strip()
        if not line or line.startswith('timestamp'):
            return
        fields = line.split(',')
        if len(fields) >= 4:
            service_name = fields[3].strip()
            if service_name:
                yield service_name, 1

    def reducer(self, service, counts):
        # Output None key + formatted string
        yield None, f"{service}\t{sum(counts)}"

if __name__ == '__main__':
    MRRequestCount.run()
