import json
import os
import csv


class Difference(object):

    __results_file = "suite_size.csv"
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
        pass

    """
    Do it for single
    """
    def find_differences_single(self):
        # iterate the random/total/additional coverages
        for coverage in self.mutant_results:
            self.raw_results[coverage] = {}
            # iterate all the mutants in that coverage form is
            # {id: {index: {...test-data}}}
            for mutant in self.mutant_results[coverage]:
                self.raw_results[coverage][mutant] = {}
                if coverage == "random":
                    self.iterate_diff_single(self.random, coverage, mutant)
                elif coverage == "total":
                    self.iterate_diff_single(self.total, coverage, mutant)
                elif coverage == "additional":
                    self.iterate_diff_single(self.additional, coverage, mutant)

        # print self.tag, "results: ", self.results
        # print self.tag, "raw_results:", self.raw_results
        # print self.tag, "coverage_diff:", self.coverage_diff

    """
    Do it for union
    """
    def find_differences_union(self):
        # iterate the random/total/additional coverages
        for coverage in self.mutant_results:
            self.raw_results[coverage] = {}
            # iterate all the mutants in that coverage form is
            # {id: {index: {...test-data}}}
            for mutant in self.mutant_results[coverage]:
                self.raw_results[coverage][mutant] = {}
                if coverage == "random" and len(self.mutant_results[coverage][mutant]) > 0:
                    self.iterate_diff_union(self.random, coverage, mutant)
                elif coverage == "total" and len(self.mutant_results[coverage][mutant]) > 0:
                    self.iterate_diff_union(self.total, coverage, mutant)
                elif coverage == "additional" and len(mutant) > 0:
                    self.iterate_diff_union(self.additional, coverage, mutant)

    """
    Do it for union
    """
    def iterate_diff_union(self, iterate, coverage, mutant):
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

                if test['output'][0] != self.mutant_results[coverage][mutant][test['id']][types]['output'][0] or \
                   test['output'][1] != self.mutant_results[coverage][mutant][test['id']][types]['output'][1]:
                    output[types][test['id']] = self.mutant_results[coverage][mutant][test['id']][types]['output']
                    self.results[coverage][types] += 1

                self.coverage_diff[coverage][mutant][test['id']] = {'branches': branch, 'statements': statement}
            self.results[coverage]['total'] = self.results[coverage]['branches'] + self.results[coverage]['statements']
        if len(output['branches']) > 0 or len(output['statements']) > 0:
            self.raw_results[coverage][mutant] = output

    """
    Do it for single
    """
    def iterate_diff_single(self, iterate, coverage, mutant):
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
                    print test
                    statement[test['id']] = self.diff_statement(test, self.mutant_results[coverage][mutant][test['id']][types])
                elif types == "branches":
                    branch[test['id']] = self.diff_branch(test, self.mutant_results[coverage][mutant][test['id']][types])
                if test['output'][0] != self.mutant_results[coverage][mutant][test['id']][types]['output'][0] or \
                   test['output'][1] != self.mutant_results[coverage][mutant][test['id']][types]['output'][1]:
                    output[types][test['id']] = self.mutant_results[coverage][mutant][test['id']][types]['output']
                    self.results[coverage][types] += 1

                self.coverage_diff[coverage][mutant][test['id']] = {'branches': branch, 'statements': statement}
            self.results[coverage]['total'] = self.results[coverage]['branches'] + self.results[coverage]['statements']
        if len(output['branches']) > 0 or len(output['statements']) > 0:
            self.raw_results[coverage][mutant] = output

    """
    This checks the difference between the
    implementation and the mutant.  The mutant
    is "b" and the implementation is "a"
    """

    def diff_branch(self, a, b):
        difference = {}
        if a['type'] == 'branch' and b['type'] == 'branch':
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
        if a['type'] == 'statement' and b['type'] == 'statement':
            diff = b['covered'] - a['covered']
            if len(diff) > 0:
                return diff
        return set()

    def diff_between_branch_statement(self, a, b):
        pass

    def write_results(self, path=None):
        if path is not None:
            with open(path + "_" + Difference.__results_file, 'a') as output_file:
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
            #print self.tag, self.coverage_diff
            pass

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
