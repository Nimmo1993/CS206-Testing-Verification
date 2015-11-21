import json
import os
import csv


class Difference(object):

    __results_file = "results.csv"
    __diff_file = "diff.csv"
    __raw_file = "_raw.csv"

    def __init__(self, mutant, rand, total, add):
        self.tag = "[Difference]\t"
        self.mutant_results = mutant
        self.random = rand
        self.total = total
        self.additional = add

        self.mutant_faults = {}

        self.coverage_diff = {}
        # this maintains the raw data for fault exposure
        self.raw_results = {}
        # this maintains the actual number of faults/prioritization
        self.results = {'random': {'branches': 0, 'statements': 0, 'total': 0},
                        'total': {'branches': 0, 'statements': 0, 'total': 0},
                        'additional': {'branches': 0, 'statements': 0, 'total': 0}}

        self.find_differences(self.random)
        self.find_differences(self.total)
        self.find_differences(self.additional)
        print self.tag, "results: ", self.results
        print self.tag, "raw_results:", self.raw_results
        print self.tag, "coverage_diff:", self.coverage_diff
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
            self.raw_results[coverage] = {}
            # iterate all the mutants in that coverage form is
            # {id: {index: {...test-data}}}
            for mutant in self.mutant_results[coverage]:
                self.raw_results[coverage][mutant] = {}
                if coverage == "random":
                    self.iterate_diff(self.random, coverage, mutant)
                elif coverage == "total":
                    self.iterate_diff(self.total, coverage, mutant)
                elif coverage == "additional":
                    self.iterate_diff(self.additional, coverage, mutant)

        return None

    def iterate_diff(self, iterate, coverage, mutant):
        # iterate the branch/statement of the actual results
        output = {'branches': {}, 'statements': {}}
        branch = {}
        statement = {}
        self.coverage_diff[coverage] = {mutant: {}}
        # print self.tag, self.mutant_results[coverage][mutant]
        for types in iterate:
            # iterate all the tests in the actual result
            for test in iterate[types]:
                if types == "statements":
                    statement[test['id']] = self.diff_statement(test, self.mutant_results[coverage][mutant][test['id']][types])
                elif types == "branches":
                    branch[test['id']] = self.diff_branch(test, self.mutant_results[coverage][mutant][test['id']][types])
                if test['output'] != self.mutant_results[coverage][mutant][test['id']][types]['output']:
                    output[types][test['id']] = self.mutant_results[coverage][mutant][test['id']][types]['output']
                    self.results[coverage][types] += 1

            self.results[coverage]['total'] = self.results[coverage]['branches'] + self.results[coverage]['statements']
        if len(output['branches']) > 0 or len(output['statements']) > 0:
            self.raw_results[coverage][mutant] = output
        self.coverage_diff[coverage][mutant] = {'branches': branch, 'statements': statement}
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

    def write_results(self, path=None):
        if path is not None:
            with open(path + Difference.__results_file, 'a') as output_file:
                keys = self.results['total'].keys()
                writer = csv.DictWriter(output_file, keys)
                writer.writeheader()
                for key, value in self.results.items():
                    d = {}
                    for priority in keys:
                        d[priority] = key
                    writer.writerow(d)
                    writer.writerow(value)
        else:
            print self.tag, self.results

    def write_coverage_diff(self, path=None):
        if path is not None:
            pass
            #with open(path + "/" + Difference.__diff_file, 'a') as output_file:
        else:
            print self.tag, self.coverage_diff

    def write_raw_results(self, path=None):
        if path is not None:
            for priority, test in self.raw_results.items():
                with open(path + "_"+ priority + Difference.__raw_file, 'a') as output_file:
                    output_file.write("mutant, statement, branch\n")
                    for mutant, value in test.items():
                        # coverage { test_id: output}
                        branch = ""
                        statement = ""
                        for coverage, v in value.items():
                            for tid, out in v.items():
                                if coverage == 'branches':
                                    branch = tid
                                elif coverage == 'statements':
                                    statement = tid
                        # we don't care about mutants that we didn't identify faults in
                        if len(value) > 0:
                            output_file.write("{0}, {1}, {2}\n".format(mutant, statement, branch))

        else:
            print self.tag, self.raw_results
