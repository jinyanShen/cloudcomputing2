from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class MRErrorCount(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, _, line):
        line = line.lstrip('\ufeff').strip()
        if not line or line.startswith('timestamp'):
            return
        fields = line.split(',')
        if len(fields) >= 7:
            try:
                status = int(fields[6].strip())
                if status >= 500:
                    service = fields[3].strip()
                    if service:
                        yield service, 1
            except ValueError:
                return

    def reducer(self, service, counts):
        yield None, f"{service}\t{sum(counts)}"

if __name__ == '__main__':
    MRErrorCount.run()
