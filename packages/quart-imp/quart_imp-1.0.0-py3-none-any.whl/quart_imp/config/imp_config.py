import typing as t


class ImpConfig:
    IMP_INIT_SESSION: t.Optional[t.Dict[str, t.Any]]

    def __init__(
        self,
        init_session: t.Optional[t.Dict[str, t.Any]] = None,
    ):
        if not init_session:
            self.IMP_INIT_SESSION = {}
        else:
            self.IMP_INIT_SESSION = init_session
