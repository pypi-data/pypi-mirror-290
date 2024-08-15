# OakVar Dual License
# 
# Copyright (c) 2023 Oak Bioinformatics, LLC
# 
# This program is dual licensed under the Affero GPL-3.0 or later for 
# non-commercial and open source use, and under a commercial license, 
# which is available for purchase, for closed-source or commercial use.
# 
# For the commercial use, please contact Oak Bioinformatics, LLC 
# for obtaining such a license. OakVar commercial license does not impose 
# the Affero GPL open-source licensing terms, conditions, and limitations. 
# To obtain a commercial-use license of OakVar, please visit our website at
# https://oakbioinformatics.com or contact us at info@oakbioinformatics.com 
# for more information.

from oakvar import BaseReporter
from typing import Union
from typing import Any
from typing import Dict
from typing import List


class Reporter(BaseReporter):
    """Reporter module template."""

    def write_preface(self, level: str):
        """Method to set up output files and write "preface".
        Preface means content before the headers for output columns.
        Opening an output file and saving the file handler should be done
        in this method.

        Args:
            level (str): Level of reporting. For example, "variant" or "gene".
        """
        _ = level
        pass

    def write_header(self, level: str):
        """Method to write column headers.
        This method is supposed to write column headers.
        The file handler saved in write_preface method is supposed to be
        used here to write column headers.

        Args:
            level (str): Level of reporting. For example, "variant" or "gene".
        """
        _ = level
        pass

    def write_table_row(self, row: Union[Dict[str, Any], List[Any]]):
        """Method to write annotation results.

        The file handler saved in write_preface method is supposed to be
        used here to write column headers.

        Variants are sent to this method one by one as `row`. It is either
        a dictionary or a list. If `self.dictrow` is `True`, a dict will be
        passed to this method. If not, a list will. The dict's keys will be
        output column names. If a list is passed, `self.columns` will have
        the column information in the same order as in the list.

        Args:
            row (Union[Dict[str, Any], List[Any]]): annotation result for a variant.
        """
        _ = row
        pass
