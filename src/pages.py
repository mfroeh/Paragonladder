import io
from pathlib import Path
from analyzer import AccountInfo
from typing import List, Tuple
import datetime as dt
from database import Database
from constants import Region, regions
from util import nice_number

left_rule = {"<": ":", "^": ":", ">": "-"}
right_rule = {"<": "-", "^": ":", ">": ":"}

class_names = {
    "demon-hunter": "DH",
    "barbarian": "Barbarian",
    "witch-doctor": "WD",
    "necromancer": "Necro",
    "wizard": "Wizard",
    "monk": "Monk",
    "crusader": "Crusader",
    None: "-",
}


def make_site():
    toc = "# Diablo3 Paragonladder\n\n---\n"

    # Generate files and toc
    for season_dir in Path("../database").glob("*"):
        season = int(season_dir.name)
        toc += f"# Season {season} \n"

        # Mixed table
        infos = []
        for region in regions:
            db = Database(season, region)
            region_infos = db.get_tracked()

            infos += [(region, info) for info in region_infos]

        md = f"# Season {season} (ALL)\n\n---\n"
        md += f"Table created at {dt.datetime.now()}\n\n"
        md += table_for_all(infos)

        save_path = f"../docs/{season}/all.md"
        Path(f"../docs/{season}").mkdir(parents=True, exist_ok=True)

        f = io.open(save_path, "w+", encoding="utf-8")
        f.write(md)

        toc += f"* [ALL]({season}/all.md)\n"

        # Tables for individual regions
        for region in regions:
            db = Database(season, region)
            infos = db.get_tracked()

            md = f"# Season {season} ({str.upper(region)})\n\n---\n"
            md += f"Table created at {dt.datetime.now()}\n\n"
            md += table_for_region(region, infos)

            f = io.open(f"../docs/{season}/{region}.md", "w+", encoding="utf-8")
            f.write(md)

            toc += f"* [{str.upper(region)}]({season}/{region}.md)\n"

    toc += "\n\n"

    f = io.open("../docs/index.md", "w+")
    f.write(toc)


def table_for_all(infos: List[Tuple[str, AccountInfo]]) -> str:
    """
    Generates a doxygen-flavored markdown table from the given account information.
    """
    headings = [
        "#",
        "Region",
        "BattleTag",
        "Paragon Season",
        "Experience gained",
        "Most played",
        "Last update",
    ]

    _sorted = sorted(infos, key=lambda tuple: tuple[1].paragon_season, reverse=True)

    data = [
        (
            i + 1,
            str.upper(tuple[0]),
            f"[{tuple[1].battletag}](https://{tuple[0]}.diablo3.com/profile/{tuple[1].battletag.replace('#', '-')}/)"
            if tuple[0] != Region.CN
            else f"[{tuple[1].battletag}](https://d3.blizzard.cn/profile/{tuple[1].battletag.replace('#', '-')}/)",
            tuple[1].paragon_season,
            nice_number(tuple[1].xp_gained),
            class_names[tuple[1].most_played_class],
            dt.datetime.fromtimestamp(tuple[1].last_update),
        )
        for i, tuple in enumerate(_sorted)
        if tuple[1].last_update
    ]
    align = [
        ("^", "<"),
        ("^", "^"),
        ("^", "<"),
        ("^", "^"),
        ("^", "<"),
        ("^", "^"),
        ("^", "<"),
    ]

    return table(data, headings, align)


def table_for_region(region: str, infos: List[AccountInfo]) -> str:
    """
    Generates a doxygen-flavored markdown table from the given account information.
    """
    headings = [
        "#",
        "BattleTag",
        "Paragon Season",
        "Experience gained",
        "Most played",
        "Last update",
    ]
    _sorted = sorted(infos, key=lambda info: info.paragon_season, reverse=True)

    data = [
        (
            i + 1,
            f"[{info.battletag}](https://{region}.diablo3.com/profile/{info.battletag.replace('#', '-')}/)"
            if region != Region.CN
            else f"[{info.battletag}](https://d3.blizzard.cn/profile/{info.battletag.replace('#', '-')}/)",
            info.paragon_season,
            nice_number(info.xp_gained),
            class_names[info.most_played_class],
            dt.datetime.fromtimestamp(info.last_update),
        )
        for i, info in enumerate(_sorted)
        if info.last_update
    ]

    align = [
        ("^", "<"),
        ("^", "<"),
        ("^", "^"),
        ("^", "<"),
        ("^", "^"),
        ("^", "<"),
    ]
    return table(data, headings, align)


def evalute_field(record, field_spec) -> str:
    """
    Evalute a field of a record using the type of the field_spec as a guide.
    """
    if type(field_spec) is int:
        return str(record[field_spec])
    elif type(field_spec) is str:
        return str(getattr(record, field_spec))
    else:
        return str(field_spec(record))


def table(records, headings, alignment=None) -> str:
    """
    Generate a Doxygen-flavor Markdown table from records.

    records -- Iterable.  Rows will be generated from this.
    headings -- List of column headings.
    alignment - List of pairs alignment characters.  The first of the pair
        specifies the alignment of the header, (Doxygen won't respect this, but
        it might look good, the second specifies the alignment of the cells in
        the column.

        Possible alignment characters are:
            '<' = Left align (default for cells)
            '>' = Right align
            '^' = Center (default for column headings)
    """

    num_columns = len(headings)
    fields = range(num_columns)

    # Compute the table cell data
    columns = [[] for i in range(num_columns)]
    for record in records:
        for i, field in enumerate(fields):
            columns[i].append(evalute_field(record, field))

    # Fill out any missing alignment characters.
    extended_align = alignment if alignment != None else []
    if len(extended_align) > num_columns:
        extended_align = extended_align[0:num_columns]
    elif len(extended_align) < num_columns:
        extended_align += [("^", "<") for i in range[num_columns - len(extended_align)]]

    heading_align, cell_align = [x for x in zip(*extended_align)]

    field_widths = [
        len(max(column, key=len)) if len(column) > 0 else 0 for column in columns
    ]
    heading_widths = [max(len(head), 2) for head in headings]
    column_widths = [max(x) for x in zip(field_widths, heading_widths)]

    _ = " | ".join(
        ["{:" + a + str(w) + "}" for a, w in zip(heading_align, column_widths)]
    )
    heading_template = "| " + _ + " |"
    _ = " | ".join(["{:" + a + str(w) + "}" for a, w in zip(cell_align, column_widths)])
    row_template = "| " + _ + " |"

    _ = " | ".join(
        [
            left_rule[a] + "-" * (w - 2) + right_rule[a]
            for a, w in zip(cell_align, column_widths)
        ]
    )
    ruling = "| " + _ + " |"

    table = heading_template.format(*headings).rstrip() + "\n"
    table += ruling.rstrip() + "\n"
    for row in zip(*columns):
        table += row_template.format(*row).rstrip() + "\n"

    return table
