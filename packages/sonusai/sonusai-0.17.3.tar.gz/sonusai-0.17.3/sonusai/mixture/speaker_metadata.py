from functools import cached_property
from pathlib import Path

from praatio import textgrid
from praatio.data_classes.textgrid_tier import TextgridTier
from praatio.utilities.constants import Interval

from sonusai.mixture.datatypes import TargetFiles
from sonusai.mixture.tokenized_shell_vars import tokenized_expand


class SpeakerMetadata:
    def __init__(self, target_files: TargetFiles) -> None:
        self.data: dict[str, dict[str, TextgridTier]] = {}
        for file in target_files:
            self.data[file.name] = {}
            file_name, _ = tokenized_expand(file.name)
            tg_file = Path(file_name).with_suffix('.TextGrid')
            if tg_file.exists():
                tg = textgrid.openTextgrid(str(tg_file), includeEmptyIntervals=False)
                for tier in tg.tierNames:
                    self.data[file.name][tier] = tg.getTier(tier)

    @cached_property
    def tiers(self) -> list[str]:
        return sorted(list(set([key for value in self.data.values() for key in value.keys()])))

    def all(self, tier: str, label_only: bool = False) -> list[Interval]:
        results = [value[tier].entries for value in self.data.values()]
        if label_only:
            return sorted(set([r.label for result in results for r in result]))
        return results

    def mixids_for(self, tier: str, value: str) -> list[int]:
        pass
