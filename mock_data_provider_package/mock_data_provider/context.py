from pydantic import BaseModel

_context = None


class MockDataProviderContext(BaseModel):
    dataset_name: str
    number_of_partitions: int
    data_tag: str

    def model_post_init(self, _) -> None:
        global _context
        _context = self


def get_context() -> MockDataProviderContext:
    return _context
