

class Difference(object):

    def __init__(self, mutant, rand, total, add):
        self.tag = "[Difference]\t"
        self.mutant_results = mutant
        self.random = rand
        self.total = total
        self.additional = add

        self.results = {}

        self.find_differences()
        print self.tag, self.results
        pass

    """
    this cycles both lists in order
    to 'align' them so that we can
    discern what the difference
    actually is between the
    mutant and implementation
    """
    def find_differences(self):
        # iterate the branch/statement of the actual results
        for types in self.random:
            # iterate all the tests in the actual result
            for test in self.random[types]:
                # iterate the random/total/additional coverages
                for coverage in self.mutant_results:
                    # iterate all the mutants in that coverage form is
                    # {id: {index: {...test-data}}}
                    for mutant in self.mutant_results[coverage]:
                        # iterate the index of the
                        for t in self.mutant_results[coverage][mutant][test['id']]:
                            self.results[mutant] = \
                                self.where_they_differ(test,
                                                       self.mutant_results[coverage][mutant][test['id']][t][types])

    """
    This checks the difference between the
    implementation and the mutant.  The mutant
    is "b" and the implementation is "a"
    """
    def where_they_differ(self, a, b):
        difference = {}
        if isinstance(a['not'], set):
            diff = b['covered'] - a['covered']
            if len(diff) > 0:
                difference['line'] = diff
        else:
            for key in a['covered']:
                if key in b['covered']:
                    diff = b['covered'][key] - a['covered'][key]
                    if len(diff) > 0:
                        difference[key] = diff
                else:
                    if len(a['covered'][key]) > 0:
                        difference[key] = a['covered'][key]
        if a['output'] != b['output']:
            difference['output'] = b['output']
        return difference
