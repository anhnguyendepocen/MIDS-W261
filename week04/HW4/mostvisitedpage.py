from mrjob.job import MRJob 
from mrjob.step import MRStep
import heapq

class MRMostVisitedPage(MRJob):
    def mapper_get_visits(self, _, record):
        self.increment_counter('Execution Counts', 'mapper calls', 1)
        # yield each visit in the line
        tokens = record.split(',')
        if tokens[0] == 'V':
            yield (tokens[1], 1)

    def combiner_count_visits(self, page, counts): 
        self.increment_counter('Execution Counts', 'combiner calls', 1)
        # sum the page visits we've seen so far
        yield (page, sum(counts))
        
    def reducer_count_visits(self, page, counts):
        self.increment_counter('Execution Counts', 'reducer_count calls', 1)
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function. yield None, (sum(counts), page)
        # discard the key; it is just None
        yield None, (sum(counts), page)
        
    def reducer_find_top5_visits(self, _, page_count_pairs):
        self.increment_counter('Execution Counts', 'reducer_find_max calls', 1)
        # each item of page_count_pairs is (count, page),
        # so yielding one results in key=counts, value=page yield max(page_count_pairs)
        return heapq.nlargest(5, page_count_pairs)

        
    def steps(self): return [
            MRStep(mapper=self.mapper_get_visits,
                   combiner=self.combiner_count_visits,
                   reducer=self.reducer_count_visits),
            MRStep(reducer=self.reducer_find_top5_visits)
        ]
    
if __name__ == '__main__': 
    MRMostVisitedPage.run()