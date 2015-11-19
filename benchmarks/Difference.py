class Difference(object):
    def __init__(self, mutant, rand, total, add):
        self.tag = "[Difference]\t"
        self.mutant_results = mutant
        self.random = rand
        self.total = total
        self.additional = add

        self.results = {}

        self.find_differences(self.random)
        self.find_differences(self.total)
        print self.tag, self.results
        pass

    """
    this cycles both lists in order
    to 'align' them so that we can
    discern what the difference
    actually is between the
    mutant and implementation
    """

    def find_differences(self, input):
        # iterate the random/total/additional coverages
        for coverage in self.mutant_results:
            self.results[coverage] = {}
            # iterate all the mutants in that coverage form is
            # {id: {index: {...test-data}}}
            for mutant in self.mutant_results[coverage]:
                self.results[coverage][mutant] = {}
                if coverage == "random":
                    self.iterate_diff(self.random, coverage, mutant)
                elif coverage == "total":
                    self.iterate_diff(self.total, coverage, mutant)
                elif coverage == "additional":
                    self.iterate_diff(self.additional, coverage, mutant)

        return None

    def iterate_diff(self, iterate, coverage, mutant):
        # iterate the branch/statement of the actual results
        for types in iterate:
            self.results[coverage][mutant][types] = []
            self.results[coverage][mutant]['output'] = []
            # iterate all the tests in the actual result
            for test in iterate[types]:
                # iterate the index of the
                for t in self.mutant_results[coverage][mutant][test['id']]:
                    if types == "statements":
                        self.results[coverage][mutant][types].append(self.diff_statement(test, self.mutant_results[coverage][mutant][test['id']][t][types]))
                    elif types == "branches":
                        self.results[coverage][mutant][types].append(self.diff_branch(test, self.mutant_results[coverage][mutant][test['id']][t][types]))
                    if test['output'] != self.mutant_results[coverage][mutant][test['id']][t][types]['output']:
                        self.results[coverage][mutant]['output'].append(self.mutant_results[coverage][mutant][test['id']][t][types]['output'])

    """
    This checks the difference between the
    implementation and the mutant.  The mutant
    is "b" and the implementation is "a"
    """
    def diff_branch(self, a, b):
        difference = {}
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

    def diff_statement(self, a, b):
        diff = b['covered'] - a['covered']
        if len(diff) > 0:
            return diff
        return set()

    def print_diff(self):
        pass
