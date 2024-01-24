from typing import Optional

from .utils import is_hetero
from ..base import BaseUserInfo, SearchResults
from ..easy import EasySearcher
from ..utils import parse_specification_type
from ...logger import get_module_logger

logger = get_module_logger("hetero_searcher")


class HeteroSearcher(EasySearcher):
    def __call__(
        self,
        user_info: BaseUserInfo,
        check_status: Optional[int] = None,
        max_search_num: int = 5,
        search_method: str = "greedy",
    ) -> SearchResults:
        """Search learnwares based on user_info from learnwares with check_status.
           Employs heterogeneous learnware search if specific requirements are met, otherwise resorts to homogeneous search methods.

        Parameters
        ----------
        user_info : BaseUserInfo
            user_info contains semantic_spec and stat_info
        max_search_num : int
            The maximum number of the returned learnwares
        check_status : int, optional
            - None: search from all learnwares
            - Others: search from learnwares with check_status

        Returns
        -------
        Tuple[List[float], List[Learnware], float, List[Learnware]]
            the first is the sorted list of rkme dist
            the second is the sorted list of Learnware (single) by the rkme dist
            the third is the score of Learnware (mixture)
            the fourth is the list of Learnware (mixture), the size is search_num
        """
        learnware_list = self.learnware_organizer.get_learnwares(check_status=check_status)
        semantic_search_result = self.semantic_searcher(learnware_list, user_info)

        learnware_list = [search_item.learnware for search_item in semantic_search_result.get_single_results()]
        if len(learnware_list) == 0:
            return SearchResults()

        if parse_specification_type(stat_specs=user_info.stat_info) is not None:
            if is_hetero(stat_specs=user_info.stat_info, semantic_spec=user_info.semantic_spec):
                user_hetero_spec = self.learnware_organizer.generate_hetero_map_spec(user_info)
                user_info.update_stat_info(user_hetero_spec.type, user_hetero_spec)
            return self.stat_searcher(learnware_list, user_info, max_search_num, search_method)
        else:
            return semantic_search_result
