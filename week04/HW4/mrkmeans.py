from mrjob.job import MRJob 
from mrjob.step import MRStep 

class MRKMeans(MRJob):
    def configure_options(self):
        super(MRKMeans, self).configure_options()
        self.SORT_VALUES = True
        
    # generate a dictionary of pages and URLs for them
    def mapper_init(self):
        self.types = {}

        with open('/Users/rcordell/Documents/MIDS/W261/week04/HW4/topUsers_Apr-Jul_2014_1000-words_summaries.txt',
                  'rU') as summaries:
            for line in summaries:
                tokens = line.split(",")
                if tokens[0].strip('"') == 'ID':
                    self.types['words'] = [ s.strip('"') for s in tokens[3:] ]
                elif tokens[0].strip() == 'ALL_CODES':
                    self.types['total'] = int(tokens[2])
                    self.types['totals'] = [ int(x) for x in tokens[3:]]
                elif tokens[0].strip() == 'CODE':
                    self.types[tokens[1]] = {'total' : [int(tokens[2])]}
                    self.types[tokens[1]] = {'vector' : [ int(x) for x in tokens[3:]] }

    def mapper(self, _, record):
        self.increment_counter('Execution Counts', 'mapper calls', 1)
          
    def steps(self): return [
            MRStep(mapper_init=self.mapper_init,
                    mapper=self.mapper)
#                   combiner=self.combiner_count_visits,
#                   reducer_init=self.reducer_count_visits_init,
#                   reducer=self.reducer_count_visits),
#            MRStep(reducer_init=self.reducer_find_max_visits_init,
#                    reducer=self.reducer_find_max_visits)
        ]
    
if __name__ == '__main__': 
    MRKMeans.run()