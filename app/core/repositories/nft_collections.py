from app.core.dependnecies import ChCursor


class NftCollectionsRepository:
    def __init__(self, ch_cursor: ChCursor) -> None:
        self._ch_cursor = ch_cursor
