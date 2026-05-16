from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol
import heapq

class MRSlowEndpoints(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol

    def steps(self):
        return [
            MRStep(mapper=self.mapper_count,
                   reducer=self.reducer_count),
            MRStep(reducer=self.reducer_top10)
        ]

    def mapper_count(self, _, line):
        line = line.lstrip('\ufeff').strip()
        if not line or line.startswith('timestamp'):
            return
        fields = line.split(',')
        if len(fields) >= 8:
            try:
                rt = int(fields[7].strip())
                if rt > 800:
                    service = fields[3].strip()
                    endpoint = fields[4].strip()
                    if service and endpoint:
                        yield f"{service},{endpoint}", 1
            except ValueError:
                return

    def reducer_count(self, key, values):
        yield None, (sum(values), key)

    def reducer_top10(self, _, value_pairs):
        top10 = heapq.nlargest(10, value_pairs)
        for count, key in top10:
            yield None, f"{key}\t{count}"

if __name__ == '__main__':
    MRSlowEndpoints.run()