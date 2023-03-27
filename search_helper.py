import re


class SearchHelper:
    LIST_BF_PATTERN = 0
    PATTERN_BF_LIST = 1
    EXIT_AFTER_MATCH = False

    MATCHING_STRATEGY_LONGEST = "longest_match"
    MATCHING_STRATEGY_SHORTEST = "shortest_match"

    def __init__(self, name):
        self.name = name
        self.search_list = []
        self.pattern_list = []
        self.result = {}

    def set_search_list(self, search_list):
        self.search_list = search_list

    def set_pattern_list(self, pattern_list):
        self.pattern_list = pattern_list

    def search(self, text, priority=LIST_BF_PATTERN, exit_after_match=EXIT_AFTER_MATCH,
               matching_strategy=MATCHING_STRATEGY_LONGEST):
        self.result = {}

        if priority == self.LIST_BF_PATTERN:
            self.search_in_list(text, clear_data=False)
            if exit_after_match:
                if self.name + "_found" not in self.result:
                    self.search_in_pattern(text, clear_data=False)
            else:
                self.search_in_pattern(text, clear_data=False)
        else:
            self.search_in_pattern(text, clear_data=False)
            if exit_after_match:
                if self.name + "_found" not in self.result:
                    self.search_in_list(text, clear_data=False)
            else:
                self.search_in_list(text, clear_data=False)

        # All searches have been done, check if there are multiple matches and return the best one
        if self.name + "_list_match" in self.result and self.name + "_pattern_match" in self.result:
            # Both search types found results: decide which is best
            if matching_strategy == self.MATCHING_STRATEGY_LONGEST:
                # Check which one is longer and set it as best match
                if len(self.result[self.name + "_pattern_result"]) > len(self.result[self.name + "_list_result"]):
                    self.result[self.name + "_best_match"] = self.result[self.name + "_pattern_result"]
                    self.result[self.name + "_best_match_type"] = "pattern"
                else:
                    self.result[self.name + "_best_match"] = self.result[self.name + "_list_result"]
                    self.result[self.name + "_best_match_type"] = "list"
                self.result[self.name + "_best_match_strategy"] = self.MATCHING_STRATEGY_LONGEST

            elif matching_strategy == self.MATCHING_STRATEGY_SHORTEST:
                # Check which one is shorter and set it as best match
                if len(self.result[self.name + "_pattern_result"]) < len(self.result[self.name + "_list_result"]):
                    self.result[self.name + "_best_match"] = self.result[self.name + "_pattern_result"]
                    self.result[self.name + "_best_match_type"] = "pattern"
                else:
                    self.result[self.name + "_best_match"] = self.result[self.name + "_list_result"]
                    self.result[self.name + "_best_match_type"] = "list"
                self.result[self.name + "_best_match_strategy"] = self.MATCHING_STRATEGY_SHORTEST
        return self.result

    def search_in_list(self, text, clear_data=True):
        if clear_data:
            self.result = {}

        for item in self.search_list:
            if item in text:
                self.result[self.name + "_list_match"] = True
                self.result[self.name + "_list_item"] = item
                self.result[self.name + "_list_result"] = item
                break
        return self.result

    def search_in_pattern(self, text, clear_data=True):
        if clear_data:
            self.result = {}

        for pattern in self.pattern_list:
            match = re.search(pattern, text)
            if match:
                self.result[self.name + "_pattern_match"] = True
                self.result[self.name + "_pattern_item"] = pattern
                self.result[self.name + "_pattern_result"] = match.group(0)
                break
        return self.result
