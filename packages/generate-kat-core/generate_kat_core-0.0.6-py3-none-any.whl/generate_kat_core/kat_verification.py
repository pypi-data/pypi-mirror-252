import importlib
from typing import Any, List, Optional

from generate_kat_core.general_parsing import ParsingType
from generate_kat_core.utils import KATParseError


class KATVerifier:
    """
    Class used to parse and check or generate and write KAT files.
    """

    def __init__(self, considered_algs: list[str], arguments: list[str]) -> None:
        self.considered_algs = considered_algs
        self.testcases: dict[str, List[ParsingType]] = dict()
        self.arguments = arguments

    def _test_kat(self, algorithm: str, test_case: dict[str, Any]) -> None:
        self._get_factory(algorithm).parse(test_case)

    def parse(self, filelist: list[str]) -> None:
        # reset test cases
        for algorithm in self.considered_algs:
            self.testcases[algorithm.upper()] = []

        for file in filelist:
            for algorithm in self.considered_algs:
                results = self._get_factory(algorithm).try_to_parse(file)
                if results is None:
                    raise KATParseError('KAT parsing result is empty')

                for result in results:
                    self.testcases[algorithm.upper()].append(result)

        for algorithm in self.considered_algs:
            if len(self.testcases[algorithm.upper()]) == 0:
                raise KATParseError('Test cases list is not complete')

    def test_kat(self, algs: Optional[list[str]] = None) -> dict[str, list[ParsingType]]:
        """Verify correctness for all previously parsed testcases

        Parameters:
        algs (list): list of algorithms to consider
        """
        if algs is None:
            algs = self.considered_algs
        for alg in algs:
            print('Testing ', alg)
            self.validate_algorithm_name(alg)

            for test_case in self.testcases[alg]:
                self._test_kat(alg, test_case)
            print('\t---> OK')

        return self.testcases

    def validate_algorithm_name(self, alg: str) -> None:
        if alg not in self.testcases:
            raise KATParseError(alg, ' not in ', self.testcases)
        if self.testcases[alg] is None or len(self.testcases[alg]) == 0:
            raise KATParseError('No valid test case found for ' +
                                'requested algorithm ', alg)

    def _get_factory(self, algorithm: str) -> Any:
        algorithm_ = f'src.{algorithm}'
        my_module = importlib.import_module(algorithm_, package=None)
        cryptography_generator = getattr(my_module, 'Factory').new(arguments=self.arguments)
        return cryptography_generator
