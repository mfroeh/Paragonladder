import io
from pathlib import Path
from diablo_api import Region
from typing import List, Tuple
from extractor import AccountInfo
import datetime as dt
from database import Database
from constants import regions
from itertools import chain

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
            region_infos = db.get_account_infos()

            infos += [(region, info) for info in region_infos]

        md = f"# Season {season} (ALL)\n\n---\n"
        md += f"Table created at {dt.datetime.now()}\n\n"
        md += table_from_mixed_account_infos(season, infos)

        save_path = f"../docs/{season}/all.md"
        Path(f"../docs/{season}").mkdir(parents=True, exist_ok=True)

        f = io.open(save_path, "w+", encoding="utf-8")
        f.write(md)

        toc += f"* [ALL]({season}/all.md)\n"

        # Tables for individual regions
        for region in regions:
            db = Database(season, region)
            infos = db.get_account_infos()

            md = f"# Season {season} ({str.upper(region.value)})\n\n---\n"
            md += f"Table created at {dt.datetime.now()}\n\n"
            md += table_from_account_infos(season, region, infos)

            save_path = f"../docs/{season}/{region.value}.md"
            Path(f"../docs/{season}").mkdir(parents=True, exist_ok=True)

            f = io.open(save_path, "w+", encoding="utf-8")
            f.write(md)

            toc += f"* [{str.upper(region.value)}]({season}/{region.value}.md)\n"

    f = io.open("../docs/index.md", "w+")
    f.write(toc)


def table_from_mixed_account_infos(
    season: int, infos: List[Tuple[Region, AccountInfo]]
) -> str:
    headings = [
        "#",
        "Region",
        "BattleTag",
        "Paragon Season",
        "Most played",
        "Paragon NonSeason",
        "Last update",
    ]
    print(infos)
    _sorted = sorted(infos, key=lambda a: a[1].paragon_season, reverse=True)

    data = [
        (
            i + 1,
            str.upper(a[0].value),
            f"[{a[1].battletag}](https://{a[0].value}.diablo3.com/en-us/profile/{a[1].battletag.replace('#', '-')}/)",
            a[1].paragon_season,
            class_names[a[1].most_played_class],
            a[1].paragon_nonseason,
            dt.datetime.fromtimestamp(a[1].last_update),
        )
        for i, a in enumerate(_sorted)
        if a[1].last_update
    ]
    fields = [0, 1, 2, 3, 4, 5, 6]
    align = [
        ("^", "<"),
        ("^", "^"),
        ("^", "<"),
        ("^", "^"),
        ("^", "^"),
        ("^", "^"),
        ("^", "<"),
    ]

    return table(data, fields, headings, align)


def table_from_account_infos(
    season: int, region: Region, infos: List[AccountInfo]
) -> str:
    """
    Generates a doxygen-flavored markdown table from the account information.
    """
    headings = [
        "#",
        "BattleTag",
        "Paragon Season",
        "Most played",
        "Paragon NonSeason",
        "Last update",
    ]
    _sorted = sorted(infos, key=lambda a: a.paragon_season, reverse=True)

    data = [
        (
            i + 1,
            f"[{a.battletag}](https://{region.value}.diablo3.com/en-us/profile/{a.battletag.replace('#', '-')}/)",
            a.paragon_season,
            class_names[a.most_played_class],
            a.paragon_nonseason,
            dt.datetime.fromtimestamp(a.last_update),
        )
        for i, a in enumerate(_sorted)
        if a.last_update
    ]
    fields = [0, 1, 2, 3, 4, 5]
    align = [("^", "<"), ("^", "<"), ("^", "^"), ("^", "^"), ("^", "^"), ("^", "<")]

    return table(data, fields, headings, align)


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


def table(records, fields, headings, alignment=None) -> str:
    """
    Generate a Doxygen-flavor Markdown table from records.

    records -- Iterable.  Rows will be generated from this.
    fields -- List of fields for each row.  Each entry may be an integer,
        string or a function.  If the entry is an integer, it is assumed to be
        an index of each record.  If the entry is a string, it is assumed to be
        a field of each record.  If the entry is a function, it is called with
        the record and its return value is taken as the value of the field.
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

    num_columns = len(fields)
    assert len(headings) == num_columns

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
