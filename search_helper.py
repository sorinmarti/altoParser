import re


class SearchHelper:
    LIST_BF_PATTERN = 0
    PATTERN_BF_LIST = 1
    EXIT_AFTER_MATCH = False

    def __init__(self, name):
        self.name = name
        self.search_list = []
        self.pattern_list = []
        self.result = {}

    def set_search_list(self, search_list):
        self.search_list = search_list

    def set_pattern_list(self, pattern_list):
        self.pattern_list = pattern_list

    def search(self, text, priority=LIST_BF_PATTERN, exit_after_match=EXIT_AFTER_MATCH):
        if priority == self.LIST_BF_PATTERN:
            self.search_in_list(text)
            if exit_after_match:
                if self.name + "_found" not in self.result:
                    self.search_in_pattern(text)
            else:
                self.search_in_pattern(text)
        else:
            self.search_in_pattern(text)
            if exit_after_match:
                if self.name + "_found" not in self.result:
                    self.search_in_list(text)
            else:
                self.search_in_list(text)


        # All searches have been done, check if there are multiple matches and return the best one
        # The best match is the one with the longest string



        return self.result

    def search_in_list(self, text):
        for item in self.search_list:
            if item in text:
                self.result[self.name + "_list_match"] = True
                self.result[self.name + "_list_item"] = item
                self.result[self.name + "_list_result"] = item
                break
        return self.result

    def search_in_pattern(self, text):
        for pattern in self.pattern_list:
            match = re.search(pattern, text)
            if match:
                self.result[self.name + "pattern_match"] = True
                self.result[self.name + "_pattern_item"] = pattern
                self.result[self.name + "_pattern_result"] = match.group(0)
                break
        return self.result
