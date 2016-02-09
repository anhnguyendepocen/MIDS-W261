from mrjob.job import MRJob 
from mrjob.step import MRStep 

class MRMostFrequentVisitors(MRJob):
    def configure_options(self):
        super(MRMostFrequentVisitors, self).configure_options()
        self.SORT_VALUES = True
        
    def mapper_get_visits_init(self):
        # create a dictionary to use for the page URLs and ids
        self.pages = {}
        
    def mapper_get_visits(self, _, record):
        self.increment_counter('Execution Counts', 'mapper calls', 1)
        tokens = record.split(',')
        
        # the page definitions come first in the file so create a dictionary from them.
        if tokens[0] == 'A':
            self.pages[tokens[1]] = tokens[4].strip('"')
            
        # emit a key = (page_id, client_id, url) and value = 1
        elif tokens[0] == 'V':
            yield ((tokens[1], tokens[4], self.pages[tokens[1]]), 1)
        else:
            pass

    def combiner_count_visits(self, key, counts): 
        self.increment_counter('Execution Counts', 'combiner count visits', 1)
        # sum the keys we've seen so far.
        # the key is (page_id, cust_id, page_url) so we're counting page views by client
        yield (key, sum(counts))
        
    def reducer_count_visits_init(self):
        self.current_page = None
        self.max_count = 0
        
    def reducer_count_visits(self, key, counts):
        self.increment_counter('Execution Counts', 'reducer_count visits', 1)
        # make sure we have sums of all keys 
        s = sum(counts)
        if self.current_page == key[0]:
            if self.max_count < s:
                self.max_count = s
        else:
            if self.current_page:
                p = self.current_page
                t = self.max_count
                yield((self.current_page,'*',key[2]), t)
                
            self.current_page = key[0]
            self.max_count = s

        yield (key, s)
        
    def reducer_find_max_visits_init(self):
        self.page = None
        self.page_max = 0
        
    def reducer_find_max_visits(self, key, counts):
        self.increment_counter('Execution Counts', 'reducer_find_max visits', 1)
        if key[1] == '*':
            self.page_max = sum(counts)
        else:
            p = sum(counts)
            if p == self.page_max:
                yield key, p
        
          
    def steps(self): return [
            MRStep(mapper_init=self.mapper_get_visits_init,
                    mapper=self.mapper_get_visits,
                   combiner=self.combiner_count_visits,
                   reducer_init=self.reducer_count_visits_init,
                   reducer=self.reducer_count_visits),
            MRStep(reducer_init=self.reducer_find_max_visits_init,
                    reducer=self.reducer_find_max_visits)
        ]
    
if __name__ == '__main__': 
    MRMostFrequentVisitors.run()