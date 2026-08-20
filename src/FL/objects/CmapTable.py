from vfbLib.typing import CustomCmap


class CmapTable:
    __slots__ = ["pid", "eid", "lid", "format", "type", "pagename", "parent"]

    def __init__(
        self,
        cmap_table_or_pid: "CmapTable | int | None" = None,
        eid: int | None = None,
        lid: int | None = None,
        format: int | None = None,
        type: int | None = None,
        pagename: str | None = None,
    ) -> None:
        """
        A custom CMAP definition

        Args:
            cmap_table_or_pid (CmapTable | int | None, optional): A CmapTable to copy
                from, or the Platform ID. Defaults to None.
            eid (int | None, optional): The Platform Encoding ID. Defaults to None.
            lid (int | None, optional): The Language ID. Defaults to None.
            format (int | None, optional): The CMAP format. Defaults to None.
            type (int | None, optional): Undocumented. Defaults to None.
            pagename (str | None, optional): The page name. Defaults to None.
        """
        self.pid: int = 3
        self.eid: int = 1
        self.lid: int = 1033
        self.format: int = 4
        self.type: int = 0
        self.pagename: str = ""
        self.parent = None
        if cmap_table_or_pid is not None:
            # TODO: If the expected number of arguments is not passed, raise_init_num()
            if isinstance(cmap_table_or_pid, CmapTable):
                self.pid = cmap_table_or_pid.pid
                self.eid = cmap_table_or_pid.eid
                self.lid = cmap_table_or_pid.lid
                self.format = cmap_table_or_pid.format
                self.type = cmap_table_or_pid.type
                self.pagename = cmap_table_or_pid.pagename
            elif isinstance(cmap_table_or_pid, int):
                if (
                    not isinstance(eid, int)
                    or not isinstance(lid, int)
                    or not isinstance(format, int)
                    or not isinstance(type, int)
                    or not isinstance(pagename, str)
                ):
                    self.raise_init_type()
                self.pid = cmap_table_or_pid
                self.eid = eid
                self.lid = lid
                self.format = format
                self.type = type
                self.pagename = pagename
            else:
                self.raise_init_type()

    def raise_init_type(self) -> None:
        raise RuntimeError(
            "RuntimeError: Incorrect type of arguments:\n"
            " CmapRecord((Pid, Eid, Lid, Format, Type, string PageName))"
        )

    def raise_init_num(self) -> None:
        raise RuntimeError("RuntimeError: Incorrect # of args to:\n CmapRecord()")

    def fake_deserialize(self, cmap_dict: CustomCmap) -> None:
        self.pid = cmap_dict["platform_id"]
        self.eid = cmap_dict["encoding_id"]
        self.lid = cmap_dict["language_id"]
        self.format = cmap_dict["format"]
        self.type = cmap_dict["option"]
        self.pagename = cmap_dict["page_name"]
        self.parent = None

    def fake_serialize(self) -> CustomCmap:
        return CustomCmap(
            language_id=self.lid,
            platform_id=self.pid,
            encoding_id=self.eid,
            format=self.format,
            option=self.type,
            page_name=self.pagename,
        )
