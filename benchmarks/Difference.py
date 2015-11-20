import json
import os


class Difference(object):
    def __init__(self, mutant, rand, total, add):
        self.tag = "[Difference]\t"
        self.mutant_results = mutant
        self.random = rand
        self.total = total
        self.additional = add

        # this maintains the raw data for fault exposure
        self.intermediary_results = {}
        # this maintains the actual number of faults/prioritization
        self.results = {'random': {'branches': 0, 'statements': 0, 'total': 0},
                        'total': {'branches': 0, 'statements': 0, 'total': 0},
                        'additional': {'branches': 0, 'statements': 0, 'total': 0}}

        self.find_differences(self.random)
        self.find_differences(self.total)
        self.find_differences(self.additional)
        print self.tag, "json: ", json.dumps(self.intermediary_results)
        print self.tag, self.intermediary_results
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
            self.intermediary_results[coverage] = {}
            # iterate all the mutants in that coverage form is
            # {id: {index: {...test-data}}}
            for mutant in self.mutant_results[coverage]:
                self.intermediary_results[coverage][mutant] = {}
                if coverage == "random":
                    self.iterate_diff(self.random, coverage, mutant)
                elif coverage == "total":
                    self.iterate_diff(self.total, coverage, mutant)
                elif coverage == "additional":
                    self.iterate_diff(self.additional, coverage, mutant)
        print self.tag, "========="

        return None

    def iterate_diff(self, iterate, coverage, mutant):
        # iterate the branch/statement of the actual results
        output = {'branches': {}, 'statements': {}}
        for types in iterate:
            # iterate all the tests in the actual result
            for test in iterate[types]:
                # iterate the index of the
                for t in self.mutant_results[coverage][mutant][test['id']]:
                    """
                    if types == "statements":
                        self.results[coverage][mutant][types].append(
                            self.diff_statement(test, self.mutant_results[coverage][mutant][test['id']][t][types]))
                    elif types == "branches":
                        self.results[coverage][mutant][types].append(
                            self.diff_branch(test, self.mutant_results[coverage][mutant][test['id']][t][types]))
                    """
                    if test['output'] != self.mutant_results[coverage][mutant][test['id']][t][types]['output']:
                        output[types][test['id']] = self.mutant_results[coverage][mutant][test['id']][t][types]['output']
                        print self.results[coverage][types]
                        self.results[coverage][types] += 1

            self.results[coverage]['total'] = self.results[coverage]['branches'] + self.results[coverage]['statements']
        if len(output['branches']) > 0 and len(output['statements']) > 0:
            self.intermediary_results[coverage][mutant] = output

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
        return difference

    def diff_statement(self, a, b):
        diff = b['covered'] - a['covered']
        if len(diff) > 0:
            return diff
        return set()

    def print_diff(self):
        pass