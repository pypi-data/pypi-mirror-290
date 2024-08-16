from dataclasses import dataclass, field
from loguru import logger
from ahocorasick_rs import AhoCorasick, MatchKind

from .database import EntityModel
from .primitives import MaterialsEntity, Language, Span


logger = logger.bind(name=__name__)


@dataclass
class EntityMatchResult:
    entity: EntityModel = field(repr=False)
    span: Span
    lang: Language

    def __post_init__(self):
        if self.lang == Language.ZH:
            self.matched_display_name = self.entity.display_name_cn
        elif self.lang == Language.EN:
            self.matched_display_name = self.entity.display_name_en


class EntityMatcher:
    """A simple matcher based on the names in the entity list."""

    def __init__(
        self,
        entity_collection: list[EntityModel],
        lang: Language = Language.ZH,
        selected_subset: list[EntityModel] = [],
        skip_aliases: list[str] = [],
    ):
        self.lang = lang
        if len(selected_subset) != 0:
            # replace the property collection with the selected properties
            entity_collection = selected_subset
        if self.lang == Language.ZH:
            self.mention2norm = {
                alias: one
                for one in entity_collection
                for alias in one.alias_list_cn
            }
            self.mention2norm.update(
                {
                    one.display_name_cn: one
                    for one in entity_collection
                }
            )
        elif self.lang == Language.EN:
            self.mention2norm = {
                alias: one
                for one in entity_collection
                for alias in one.alias_list_en
            }
            self.mention2norm.update(
                {
                    one.display_name_en: one
                    for one in entity_collection
                }
            )

        self.all_mentions = list(self.mention2norm.keys())
        # remove skip aliases
        self.all_mentions = [
            one for one in self.all_mentions if one not in skip_aliases
        ]
        # remove duplicates
        self.all_mentions = list(set(self.all_mentions))
        # remove empty mentions
        self.all_mentions = [one for one in self.all_mentions if one]
        self.ac = AhoCorasick(self.all_mentions, matchkind=MatchKind.LeftmostLongest)

    def normalize(self, alias: str) -> EntityModel:
        return self.mention2norm[alias]

    def get_all_mentions(self, document: str) -> list[str]:
        found = self.ac.find_matches_as_strings(document)
        return found

    def is_match(self, document: str) -> bool:
        return len(self.get_all_mentions(document)) > 0

    def match(self, document: str) -> list[EntityMatchResult]:
        res = []
        matches = self.ac.find_matches_as_indexes(document)
        for idx, one in enumerate(matches):
            mention = self.all_mentions[one[0]]
            matched = document[one[1] : one[2]]
            assert mention == matched
            prop = self.mention2norm[mention]
            entry = EntityMatchResult(
                prop,
                Span(str(idx), one[1], one[2], mention, MaterialsEntity.AUT),
                self.lang,
            )
            res.append(entry)
        return res
